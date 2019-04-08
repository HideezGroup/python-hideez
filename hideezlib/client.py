# This file is part of the Trezor project.
#
# Copyright (C) 2012-2018 SatoshiLabs and contributors
# Copyright (C) 2019      Drynode
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import functools
import logging
import os
import sys
import binascii
import unicodedata
import getpass
import warnings

from mnemonic import Mnemonic

from . import messages as proto
from . import tools
from . import mapping


if sys.version_info.major < 3:
    raise Exception("hideezlib does not support Python 2.")


LOG = logging.getLogger(__name__)

# make a getch function
try:
    import termios
    import tty
    # POSIX system. Create and return a getch that manipulates the tty.
    # On Windows, termios will fail to import.

    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

except ImportError:
    # Windows system.
    # Use msvcrt's getch function.
    import msvcrt

    def getch():
        while True:
            key = msvcrt.getch()
            if key in (0x00, 0xe0):
                # skip special keys: read the scancode and repeat
                msvcrt.getch()
                continue
            return key.decode('latin1')


class CallException(Exception):
    pass


class PinException(CallException):
    pass


class field:
    # Decorator extracts single value from
    # protobuf object. If the field is not
    # present, raises an exception.
    def __init__(self, field):
        self.field = field

    def __call__(self, f):
        @functools.wraps(f)
        def wrapped_f(*args, **kwargs):
            ret = f(*args, **kwargs)
            return getattr(ret, self.field)
        return wrapped_f


class expect:
    # Decorator checks if the method
    # returned one of expected protobuf messages
    # or raises an exception
    def __init__(self, *expected):
        self.expected = expected

    def __call__(self, f):
        @functools.wraps(f)
        def wrapped_f(*args, **kwargs):
            ret = f(*args, **kwargs)
            if not isinstance(ret, self.expected):
                raise RuntimeError("Got %s, expected %s" %
                                   (ret.__class__, self.expected))
            return ret
        return wrapped_f


def session(f):
    # Decorator wraps a BaseClient method
    # with session activation / deactivation
    @functools.wraps(f)
    def wrapped_f(*args, **kwargs):
        # pytest traceback hiding, this function won't appear in tracebacks
        __tracebackhide__ = True
        client = args[0]
        client.transport.session_begin()
        try:
            return f(*args, **kwargs)
        finally:
            client.transport.session_end()
    return wrapped_f


def normalize_nfc(txt):
    '''
    Normalize message to NFC and return bytes suitable for protobuf.
    This seems to be bitcoin-qt standard of doing things.
    '''
    if isinstance(txt, bytes):
        txt = txt.decode('utf-8')
    return unicodedata.normalize('NFC', txt).encode('utf-8')


class BaseClient(object):
    # Implements very basic layer of sending raw protobuf
    # messages to device and getting its response back.
    def __init__(self, transport, **kwargs):
        LOG.info("creating client instance for device: "
                 "{}".format(transport.get_path()))
        self.transport = transport
        super(BaseClient, self).__init__()  # *args, **kwargs)

    def close(self):
        pass

    def cancel(self):
        self.transport.write(proto.Cancel())

    @session
    def call_raw(self, msg):
        # pytest traceback hiding - this function won't appear in tracebacks
        __tracebackhide__ = True
        self.transport.write(msg)
        return self.transport.read()

    @session
    def call(self, msg):
        resp = self.call_raw(msg)
        handler_name = "callback_%s" % resp.__class__.__name__
        handler = getattr(self, handler_name, None)

        if handler is not None:
            msg = handler(resp)
            if msg is None:
                raise ValueError("Callback %s must return protobuf message, "
                                 "not None" % handler)
            resp = self.call(msg)

        return resp

    def callback_Failure(self, msg):
        if msg.code in (proto.FailureType.PinInvalid,
                        proto.FailureType.PinCancelled,
                        proto.FailureType.PinExpected):
            raise PinException(msg.code, msg.message)

        raise CallException(msg.code, msg.message)

    def register_message(self, msg):
        '''Allow application to register custom protobuf message type'''
        mapping.register_message(msg)


class TextUIMixin(object):
    # This class demonstrates easy test-based UI
    # integration between the device and wallet.
    # You can implement similar functionality
    # by implementing your own GuiMixin with
    # graphical widgets for every type of these callbacks.

    def __init__(self, *args, **kwargs):
        super(TextUIMixin, self).__init__(*args, **kwargs)

    @staticmethod
    def print(text):
        print(text, file=sys.stderr)

    def callback_ButtonRequest(self, msg):
        return proto.ButtonAck()


class DebugLinkMixin(object):
    # This class implements automatic responses
    # and other functionality for unit tests
    # for various callbacks, created in order
    # to automatically pass unit tests.
    #
    # This mixing should be used only for purposes
    # of unit testing, because it will fail to work
    # without special DebugLink interface provided
    # by the device.
    DEBUG = LOG.getChild('debug_link').debug

    def __init__(self, *args, **kwargs):
        super(DebugLinkMixin, self).__init__(*args, **kwargs)
        self.debug = True
        self.in_with_statement = 0
        self.button_wait = 0
        self.screenshot_id = 0

        # Always press Yes and provide correct pin
        self.setup_debuglink(True, True)

        # Do not expect any specific response from device
        self.expected_responses = None

    def close(self):
        super(DebugLinkMixin, self).close()

    def set_buttonwait(self, secs):
        self.button_wait = secs

    def __enter__(self):
        # For usage in with/expected_responses
        self.in_with_statement += 1
        return self

    def __exit__(self, _type, value, traceback):
        self.in_with_statement -= 1

        if _type is not None:
            # Another exception raised
            return False

        # return isinstance(value, TypeError)
        # Evaluate missed responses in 'with' statement
        if (self.expected_responses is not None
                and len(self.expected_responses)):
            raise RuntimeError("Some of expected responses didn't come "
                               "from device: %s" %
                               [repr(x) for x in self.expected_responses])

        # Cleanup
        self.expected_responses = None
        return False

    def set_expected_responses(self, expected):
        if not self.in_with_statement:
            raise RuntimeError("Must be called inside 'with' statement")
        self.expected_responses = expected

    def setup_debuglink(self, button, pin_correct):
        self.button = button  # True -> YES button, False -> NO button
        self.pin_correct = pin_correct

    def call_raw(self, msg):
        # pytest traceback hiding - this function won't appear in tracebacks
        __tracebackhide__ = True

        resp = super(DebugLinkMixin, self).call_raw(msg)
        self._check_request(resp)
        return resp

    def _check_request(self, msg):
        # pytest traceback hiding - this function won't appear in tracebacks
        __tracebackhide__ = True

        if self.expected_responses is not None:
            try:
                expected = self.expected_responses.pop(0)
            except IndexError:
                raise AssertionError(proto.FailureType.UnexpectedMessage,
                                     "Got %s, but no message has been "
                                     "expected" % repr(msg))

            if msg.__class__ != expected.__class__:
                raise AssertionError(proto.FailureType.UnexpectedMessage,
                                     "Expected %s, got %s" %
                                     (repr(expected), repr(msg)))

            for field, value in expected.__dict__.items():
                if value is None or value == []:
                    continue
                if getattr(msg, field) != value:
                    raise AssertionError(proto.FailureType.UnexpectedMessage,
                                         "Expected %s, got %s" %
                                         (repr(expected), repr(msg)))

    @session
    def debug_wipe(self):
        self.transport.debug_wipe()
        self.init_device()

    @session
    def debug_load(self, **kwargs):
        mnemonic = kwargs.pop('mnemonic', None)
        self.transport.debug_load(mnemonic)


class ProtocolMixin(object):
    VENDORS = ('hideez.com', 'bitcointrezor.com')

    def __init__(self, state=None, *args, **kwargs):
        super(ProtocolMixin, self).__init__(*args, **kwargs)
        self.state = state
        self.init_device()
        self.tx_api = None

    def set_tx_api(self, tx_api):
        self.tx_api = tx_api

    def init_device(self):
        init_msg = proto.Initialize()
        if self.state is not None:
            init_msg.state = self.state
        self.features = expect(proto.Features)(self.call)(init_msg)
        if str(self.features.vendor) not in self.VENDORS:
            raise RuntimeError("Unsupported device")

    def _get_local_entropy(self):
        return os.urandom(32)

    @staticmethod
    def _convert_prime(n: tools.Address) -> tools.Address:
        # Convert minus signs to uint32 with flag
        return [tools.H_(int(abs(x))) if x < 0 else x for x in n]

    @staticmethod
    def expand_path(n):
        warnings.warn('expand_path is deprecated, use tools.parse_path',
                      DeprecationWarning)
        return tools.parse_path(n)

    @expect(proto.PublicKey)
    def get_public_node(self, n, ecdsa_curve_name=None, show_display=False,
                        coin_name=None):
        n = self._convert_prime(n)
        return self.call(proto.GetPublicKey(address_n=n,
                                            ecdsa_curve_name=ecdsa_curve_name,
                                            show_display=show_display,
                                            coin_name=coin_name))

    @field('address')
    @expect(proto.Address)
    def get_address(self, coin_name, n, show_display=False, multisig=None,
                    script_type=proto.InputScriptType.SPENDADDRESS):
        n = self._convert_prime(n)
        if multisig:
            return self.call(proto.GetAddress(address_n=n, coin_name=coin_name,
                                              show_display=show_display,
                                              multisig=multisig,
                                              script_type=script_type))
        else:
            return self.call(proto.GetAddress(address_n=n, coin_name=coin_name,
                                              show_display=show_display,
                                              script_type=script_type))

    @field('message')
    @expect(proto.Success)
    def ping(self, msg, button_protection=False, pin_protection=False,
             passphrase_protection=False):
        msg = proto.Ping(message=msg,
                         button_protection=button_protection,
                         pin_protection=pin_protection,
                         passphrase_protection=passphrase_protection)
        return self.call(msg)

    def get_device_id(self):
        return self.features.device_id

    @field('message')
    @expect(proto.Success)
    def clear_session(self):
        return self.call(proto.ClearSession())

    @expect(proto.MessageSignature)
    def sign_message(self, coin_name, n, message,
                     script_type=proto.InputScriptType.SPENDADDRESS):
        n = self._convert_prime(n)
        message = normalize_nfc(message)
        return self.call(proto.SignMessage(coin_name=coin_name, address_n=n,
                         message=message, script_type=script_type))

    @expect(proto.SignedIdentity)
    def sign_identity(self, identity, challenge_hidden, challenge_visual,
                      ecdsa_curve_name=None):
        return self.call(proto.SignIdentity(identity=identity,
                         challenge_hidden=challenge_hidden,
                         challenge_visual=challenge_visual,
                         ecdsa_curve_name=ecdsa_curve_name))

    @expect(proto.ECDHSessionKey)
    def get_ecdh_session_key(self, identity, peer_public_key,
                             ecdsa_curve_name=None):
        return self.call(proto.GetECDHSessionKey(identity=identity,
                         peer_public_key=peer_public_key,
                         ecdsa_curve_name=ecdsa_curve_name))

    @expect(proto.CosiCommitment)
    def cosi_commit(self, n, data):
        n = self._convert_prime(n)
        return self.call(proto.CosiCommit(address_n=n, data=data))

    @expect(proto.CosiSignature)
    def cosi_sign(self, n, data, global_commitment, global_pubkey):
        n = self._convert_prime(n)
        return self.call(proto.CosiSign(address_n=n, data=data,
                         global_commitment=global_commitment,
                         global_pubkey=global_pubkey))

    def verify_message(self, coin_name, address, signature, message):
        message = normalize_nfc(message)
        try:
            resp = self.call(proto.VerifyMessage(address=address,
                                                 signature=signature,
                                                 message=message,
                                                 coin_name=coin_name))
        except CallException as e:
            resp = e
        if isinstance(resp, proto.Success):
            return True
        return False

    @expect(proto.EncryptedMessage)
    def encrypt_message(self, pubkey, message, display_only, coin_name, n):
        if coin_name and n:
            n = self._convert_prime(n)
            return self.call(proto.EncryptMessage(pubkey=pubkey,
                                                  message=message,
                                                  display_only=display_only,
                                                  coin_name=coin_name,
                                                  address_n=n))
        else:
            return self.call(proto.EncryptMessage(pubkey=pubkey,
                                                  message=message,
                                                  display_only=display_only))

    @expect(proto.DecryptedMessage)
    def decrypt_message(self, n, nonce, message, msg_hmac):
        n = self._convert_prime(n)
        return self.call(proto.DecryptMessage(address_n=n, nonce=nonce,
                                              message=message, hmac=msg_hmac))

    @field('value')
    @expect(proto.CipheredKeyValue)
    def encrypt_keyvalue(self, n, key, value, ask_on_encrypt=True,
                         ask_on_decrypt=True, iv=b''):
        n = self._convert_prime(n)
        return self.call(proto.CipherKeyValue(address_n=n,
                                              key=key,
                                              value=value,
                                              encrypt=True,
                                              ask_on_encrypt=ask_on_encrypt,
                                              ask_on_decrypt=ask_on_decrypt,
                                              iv=iv))

    @field('value')
    @expect(proto.CipheredKeyValue)
    def decrypt_keyvalue(self, n, key, value, ask_on_encrypt=True,
                         ask_on_decrypt=True, iv=b''):
        n = self._convert_prime(n)
        return self.call(proto.CipherKeyValue(address_n=n,
                                              key=key,
                                              value=value,
                                              encrypt=False,
                                              ask_on_encrypt=ask_on_encrypt,
                                              ask_on_decrypt=ask_on_decrypt,
                                              iv=iv))

    def _prepare_sign_tx(self, inputs, outputs):
        tx = proto.TransactionType()
        tx.inputs = inputs
        tx.outputs = outputs

        txes = {None: tx}

        for inp in inputs:
            if inp.prev_hash in txes:
                continue

            if inp.script_type in (proto.InputScriptType.SPENDP2SHWITNESS,
                                   proto.InputScriptType.SPENDWITNESS):
                continue

            if not self.tx_api:
                raise RuntimeError('TX_API not defined')

            prev_hash = binascii.hexlify(inp.prev_hash).decode('utf-8')
            prev_tx = self.tx_api.get_tx(prev_hash)
            txes[inp.prev_hash] = prev_tx

        return txes

    @session
    def sign_tx(self, coin_name, inputs, outputs, version=None, lock_time=None,
                expiry=None, overwintered=None, debug_processor=None):

        txes = self._prepare_sign_tx(inputs, outputs)

        # Prepare and send initial message
        tx = proto.SignTx()
        tx.inputs_count = len(inputs)
        tx.outputs_count = len(outputs)
        tx.coin_name = coin_name
        if version is not None:
            tx.version = version
        if lock_time is not None:
            tx.lock_time = lock_time
        if expiry is not None:
            tx.expiry = expiry
        if overwintered is not None:
            tx.overwintered = overwintered
        res = self.call(tx)

        # Prepare structure for signatures
        signatures = [None] * len(inputs)
        serialized_tx = b''

        counter = 0
        while True:
            counter += 1

            if isinstance(res, proto.Failure):
                raise CallException("Signing failed")

            if not isinstance(res, proto.TxRequest):
                raise CallException("Unexpected message")

            # If there's some part of signed transaction, let's add it
            if res.serialized and res.serialized.serialized_tx:
                serialized_tx += res.serialized.serialized_tx

            if res.serialized and res.serialized.signature_index is not None:
                if signatures[res.serialized.signature_index] is not None:
                    raise ValueError("Signature for index %d already filled" %
                                     res.serialized.signature_index)
                sig = res.serialized.signature
                signatures[res.serialized.signature_index] = sig

            if res.request_type == proto.RequestType.TXFINISHED:
                # Device didn't ask for more information, finish workflow
                break

            # Device asked for one more information, let's process it.
            if not res.details.tx_hash:
                current_tx = txes[None]
            else:
                current_tx = txes[bytes(res.details.tx_hash)]

            if res.request_type == proto.RequestType.TXMETA:
                msg = proto.TransactionType()
                msg.version = current_tx.version
                msg.lock_time = current_tx.lock_time
                msg.inputs_cnt = len(current_tx.inputs)
                if res.details.tx_hash:
                    msg.outputs_cnt = len(current_tx.bin_outputs)
                else:
                    msg.outputs_cnt = len(current_tx.outputs)
                if current_tx.extra_data:
                    msg.extra_data_len = len(current_tx.extra_data)
                else:
                    msg.extra_data_len = 0
                res = self.call(proto.TxAck(tx=msg))
                continue

            elif res.request_type == proto.RequestType.TXINPUT:
                msg = proto.TransactionType()
                msg.inputs = [current_tx.inputs[res.details.request_index]]
                if debug_processor is not None:
                    # msg needs to be deep copied so when it's modified
                    # the other messages stay intact
                    from copy import deepcopy
                    msg = deepcopy(msg)
                    # If debug_processor function is provided,
                    # pass thru it the request and prepared response.
                    # This is useful for tests, see test_msg_signtx
                    msg = debug_processor(res, msg)

                res = self.call(proto.TxAck(tx=msg))
                continue

            elif res.request_type == proto.RequestType.TXOUTPUT:
                msg = proto.TransactionType()
                if res.details.tx_hash:
                    msg.bin_outputs = [
                        current_tx.bin_outputs[res.details.request_index]
                    ]
                else:
                    msg.outputs = [
                        current_tx.outputs[res.details.request_index]
                    ]

                if debug_processor is not None:
                    # msg needs to be deep copied so when it's modified
                    # the other messages stay intact
                    from copy import deepcopy
                    msg = deepcopy(msg)
                    # If debug_processor function is provided,
                    # pass thru it the request and prepared response.
                    # This is useful for tests, see test_msg_signtx
                    msg = debug_processor(res, msg)

                res = self.call(proto.TxAck(tx=msg))
                continue

            elif res.request_type == proto.RequestType.TXEXTRADATA:
                exd_o, exd_l = (res.details.extra_data_offset,
                                res.details.extra_data_len)
                msg = proto.TransactionType()
                msg.extra_data = current_tx.extra_data[exd_o:exd_o+exd_l]
                res = self.call(proto.TxAck(tx=msg))
                continue

        if None in signatures:
            raise RuntimeError("Some signatures are missing!")

        return (signatures, serialized_tx)


class HideezClient(ProtocolMixin, TextUIMixin, BaseClient):
    def __init__(self, transport, *args, **kwargs):
        super().__init__(transport=transport, *args, **kwargs)


class DebugHideezClient(ProtocolMixin, DebugLinkMixin, BaseClient):
    def __init__(self, transport, *args, **kwargs):
        super().__init__(transport=transport, *args, **kwargs)
