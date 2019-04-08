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

from .common import HideezTest
from ..support import ckd_public as bip32
from hideezlib import messages as proto
from hideezlib.tools import parse_path


class TestMsgGetaddressSegwitNative(HideezTest):

    def test_show_segwit(self):
        self.setup_mnemonic_allallall()
        assert self.client.get_address("Testnet", parse_path("49'/1'/0'/0/0"), True, None, script_type=proto.InputScriptType.SPENDWITNESS) == 'tb1qnkeww24u2z6q92n7exrn2zwsy8q3yhtw5v5gfn'
        assert self.client.get_address("Testnet", parse_path("49'/1'/0'/1/0"), False, None, script_type=proto.InputScriptType.SPENDWITNESS) == 'tb1qsf8mzqm4226t62acf4l383dz4f9j4vxjmefmck'
        assert self.client.get_address("Testnet", parse_path("44'/1'/0'/0/0"), False, None, script_type=proto.InputScriptType.SPENDWITNESS) == 'tb1qa699g92dtfpwwmtcjq44rkcrm3dshhfrxyx97z'
        assert self.client.get_address("Testnet", parse_path("44'/1'/0'/0/0"), False, None, script_type=proto.InputScriptType.SPENDADDRESS) == 'n3GEpwQbivawYe9Hb6rfNsAdgn76qUJnuM'

    def test_show_multisig_3(self):
        self.setup_mnemonic_allallall()
        nodes = [self.client.get_public_node(parse_path("999'/1'/%d'" % index)) for index in range(1, 4)]
        multisig1 = proto.MultisigRedeemScriptType(
            pubkeys=list(map(lambda n: proto.HDNodePathType(node=bip32.deserialize(n.xpub), address_n=[2, 0]), nodes)),
            signatures=[b'', b'', b''],
            m=2,
        )
        multisig2 = proto.MultisigRedeemScriptType(
            pubkeys=list(map(lambda n: proto.HDNodePathType(node=bip32.deserialize(n.xpub), address_n=[2, 1]), nodes)),
            signatures=[b'', b'', b''],
            m=2,
        )
        for i in [1, 2, 3]:
            assert self.client.get_address("Testnet", parse_path("999'/1'/%d'/2/1" % i), False, multisig2, script_type=proto.InputScriptType.SPENDWITNESS) == 'tb1qr60gl0vt6nrduwrhl32jqcefce8zw0ewfr8y6n4h0mqe9xwa4z0svt3rk7'
            assert self.client.get_address("Testnet", parse_path("999'/1'/%d'/2/0" % i), False, multisig1, script_type=proto.InputScriptType.SPENDWITNESS) == 'tb1qsvhqde0wme09er327gdn806af22nh908g47qxnctc8acq2xvtwdstc34v7'
