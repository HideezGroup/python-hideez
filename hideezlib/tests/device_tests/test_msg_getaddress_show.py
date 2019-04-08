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


class TestMsgGetaddressShow(HideezTest):

    def test_show(self):
        self.setup_mnemonic_nopin_nopassphrase()
        assert self.client.get_address('Bitcoin', [1], show_display=True) == '1P7omjnoyYXGFRm9hXjM72a8KdmsAcSziA'
        assert self.client.get_address('Bitcoin', [2], show_display=True) == '18qMjThHFrMSsep5ivs48ecTw3NVMY3b1C'
        assert self.client.get_address('Bitcoin', [3], show_display=True) == '1CRKkvKo9VV27FajEjWj1ztYhJvvtfDuxS'

    def test_show_multisig_3(self):
        self.setup_mnemonic_nopin_nopassphrase()

        node = bip32.deserialize('xpub661MyMwAqRbcFW3NvPPCXr3RKSnks2UPNj543xvx3zKaWMTDH7rifpbTxgRbeavHFgke9vrfGZSb16ePwqWpguRYquYo8QtNRKcnVnPdmMp')
        multisig = proto.MultisigRedeemScriptType(
            pubkeys=[
                proto.HDNodePathType(node=node, address_n=[1]),
                proto.HDNodePathType(node=node, address_n=[2]),
                proto.HDNodePathType(node=node, address_n=[3])
            ],
            signatures=[b'', b'', b''],
            m=2,
        )

        for i in [1, 2, 3]:
            assert self.client.get_address('Bitcoin', [i], show_display=True, multisig=multisig) == '33JHGqGsPuAgfYyNK5rw9tyzB7D7gjM9VZ'

    def test_show_multisig_15(self):
        self.setup_mnemonic_nopin_nopassphrase()

        node = bip32.deserialize('xpub661MyMwAqRbcFW3NvPPCXr3RKSnks2UPNj543xvx3zKaWMTDH7rifpbTxgRbeavHFgke9vrfGZSb16ePwqWpguRYquYo8QtNRKcnVnPdmMp')

        pubs = []
        for x in range(15):
            pubs.append(proto.HDNodePathType(node=node, address_n=[x]))

        multisig = proto.MultisigRedeemScriptType(
            pubkeys=pubs,
            signatures=[b''] * 15,
            m=15,
        )

        for i in range(15):
            assert self.client.get_address('Bitcoin', [i], show_display=True, multisig=multisig) == '3DTbMcL2LFgDwGY3M2YLVev1Kvata3x1Ws'
