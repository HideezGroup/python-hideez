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

from binascii import hexlify

from .common import HideezTest
from hideezlib import messages as proto


class TestMsgSignmessageSegwit(HideezTest):

    def test_sign(self):
        self.setup_mnemonic_nopin_nopassphrase()
        sig = self.client.sign_message('Bitcoin', [0], "This is an example of a signed message.", script_type=proto.InputScriptType.SPENDP2SHWITNESS)
        assert sig.address == '3JCM56MUX7eFSsKcb1jvDbyY6P7xdAnTxW'
        assert hexlify(sig.signature) == b'23571fe4a1b88a3dc014ab9ff7f9b0e13eba24af3bec45cf2b650f0bcc7c09ff7e1b8b8efd55b42b29b47fd332f950d9e53730f5fc7a6e2df48371b304d4b69651'

    def test_sign_testnet(self):
        self.setup_mnemonic_nopin_nopassphrase()
        sig = self.client.sign_message('Testnet', [0], "This is an example of a signed message.", script_type=proto.InputScriptType.SPENDP2SHWITNESS)
        assert sig.address == '2N9kZ8qHW8a9beexAG9MnqYxoJjL8SM1reD'
        assert hexlify(sig.signature) == b'23571fe4a1b88a3dc014ab9ff7f9b0e13eba24af3bec45cf2b650f0bcc7c09ff7e1b8b8efd55b42b29b47fd332f950d9e53730f5fc7a6e2df48371b304d4b69651'

    def test_sign_long(self):
        self.setup_mnemonic_nopin_nopassphrase()
        sig = self.client.sign_message('Bitcoin', [0], "VeryLongMessage!" * 64, script_type=proto.InputScriptType.SPENDP2SHWITNESS)
        assert sig.address == '3JCM56MUX7eFSsKcb1jvDbyY6P7xdAnTxW'
        assert hexlify(sig.signature) == b'2350347cfd6a62c137cd4c5b004f04305de634cc5da4d0ef93ee7c8f416a76259621b95ab8363f4371287932e3fa35abf00c61d88b94aab9b849f355e440466b38'

    def test_sign_utf(self):
        self.setup_mnemonic_nopin_nopassphrase()

        words_nfkd = u'Pr\u030ci\u0301s\u030cerne\u030c z\u030clut\u030couc\u030cky\u0301 ku\u030an\u030c u\u0301pe\u030cl d\u030ca\u0301belske\u0301 o\u0301dy za\u0301ker\u030cny\u0301 uc\u030cen\u030c be\u030cz\u030ci\u0301 pode\u0301l zo\u0301ny u\u0301lu\u030a'
        words_nfc = u'P\u0159\xed\u0161ern\u011b \u017elu\u0165ou\u010dk\xfd k\u016f\u0148 \xfap\u011bl \u010f\xe1belsk\xe9 \xf3dy z\xe1ke\u0159n\xfd u\u010de\u0148 b\u011b\u017e\xed pod\xe9l z\xf3ny \xfal\u016f'

        sig_nfkd = self.client.sign_message('Bitcoin', [0], words_nfkd, script_type=proto.InputScriptType.SPENDP2SHWITNESS)
        assert sig_nfkd.address == '3JCM56MUX7eFSsKcb1jvDbyY6P7xdAnTxW'
        assert hexlify(sig_nfkd.signature) == b'236e61e828e94dc5fcc53fcfcbfaceaa4b2eb0e516f32b68f43d359e8d0676c76834969eca024f548fcf8695ec765186aa8919dc510b423f2ece1939fe2402dec4'

        sig_nfc = self.client.sign_message('Bitcoin', [0], words_nfc, script_type=proto.InputScriptType.SPENDP2SHWITNESS)
        assert sig_nfc.address == '3JCM56MUX7eFSsKcb1jvDbyY6P7xdAnTxW'
        assert hexlify(sig_nfc.signature) == b'236e61e828e94dc5fcc53fcfcbfaceaa4b2eb0e516f32b68f43d359e8d0676c76834969eca024f548fcf8695ec765186aa8919dc510b423f2ece1939fe2402dec4'
