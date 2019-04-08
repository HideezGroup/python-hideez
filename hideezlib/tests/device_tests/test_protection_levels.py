# This file is part of the Trezor project.
#
# Copyright (C) 2012-2018 SatoshiLabs and contributors
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

from binascii import unhexlify
import pytest

from .common import HideezTest
from hideezlib import messages as proto


TXHASH_d5f65e = unhexlify('d5f65ee80147b4bcc70b75e4bbf2d7382021b871bd8867ef8fa525ef50864882')


@pytest.mark.skip
class TestProtectionLevels(HideezTest):

    def test_initialize(self):
        with self.client:
            self.setup_mnemonic_nopin_passphrase()
            self.client.set_expected_responses([proto.Features()])
            self.client.init_device()

    def test_apply_settings(self):
        with self.client:
            self.setup_mnemonic_nopin_passphrase()
            self.client.set_expected_responses([
                proto.Success(),
                proto.Features()
            ])  # HideezClient reinitializes device
            self.client.apply_settings(label='nazdar')

    def test_ping(self):
        with self.client:
            self.setup_mnemonic_nopin_passphrase()
            self.client.set_expected_responses([
                proto.PassphraseRequest(),
                proto.PassphraseStateRequest(),
                proto.Success()
            ])
            self.client.ping('msg', True, True, True)

    def test_get_entropy(self):
        with self.client:
            self.setup_mnemonic_nopin_passphrase()
            self.client.set_expected_responses([
                proto.Entropy()
            ])
            self.client.get_entropy(10)

    def test_get_public_key(self):
        with self.client:
            self.setup_mnemonic_nopin_passphrase()
            self.client.set_expected_responses([
                proto.PassphraseRequest(),
                proto.PassphraseStateRequest(),
                proto.PublicKey()
            ])
            self.client.get_public_node([])

    def test_get_address(self):
        with self.client:
            self.setup_mnemonic_nopin_passphrase()
            self.client.set_expected_responses([
                proto.PassphraseRequest(),
                proto.PassphraseStateRequest(),
                proto.Address()
            ])
            self.client.get_address('Bitcoin', [])

    def test_wipe_device(self):
        with self.client:
            self.setup_mnemonic_nopin_passphrase()
            self.client.set_expected_responses([
                proto.Success(),
                proto.Features()
            ])
            self.client.wipe_device()

    def test_load_device(self):
        with self.client:
            self.client.set_expected_responses([proto.Success(),
                                                proto.Features()])
            self.client.load_device_by_mnemonic('this is mnemonic', '1234', True, 'label', 'english', skip_checksum=True)

        # This must fail, because device is already initialized
        with pytest.raises(Exception):
            self.client.load_device_by_mnemonic('this is mnemonic', '1234', True, 'label', 'english', skip_checksum=True)

    def test_sign_message(self):
        with self.client:
            self.setup_mnemonic_nopin_passphrase()
            self.client.set_expected_responses([
                proto.PassphraseRequest(),
                proto.PassphraseStateRequest(),
                proto.MessageSignature()
            ])
            self.client.sign_message('Bitcoin', [], 'testing message')

    def test_verify_message(self):
        with self.client:
            self.setup_mnemonic_nopin_passphrase()
            self.client.set_expected_responses([proto.Success()])
            self.client.verify_message(
                'Bitcoin',
                '14LmW5k4ssUrtbAB4255zdqv3b4w1TuX9e',
                unhexlify('209e23edf0e4e47ff1dec27f32cd78c50e74ef018ee8a6adf35ae17c7a9b0dd96f48b493fd7dbab03efb6f439c6383c9523b3bbc5f1a7d158a6af90ab154e9be80'),
                'This is an example of a signed message.')

    def test_signtx(self):
        self.setup_mnemonic_nopin_passphrase()

        inp1 = proto.TxInputType(
            address_n=[0],  # 14LmW5k4ssUrtbAB4255zdqv3b4w1TuX9e
            prev_hash=TXHASH_d5f65e,
            prev_index=0,
        )

        out1 = proto.TxOutputType(
            address='1MJ2tj2ThBE62zXbBYA5ZaN3fdve5CPAz1',
            amount=390000 - 10000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        with self.client:

            self.client.set_expected_responses([
                proto.PassphraseRequest(),
                proto.PassphraseStateRequest(),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=TXHASH_d5f65e)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_d5f65e)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_d5f65e)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_d5f65e)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            self.client.sign_tx('Bitcoin', [inp1, ], [out1, ])
