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

import pytest

from .common import HideezTest
from ..support import ckd_public as bip32
from hideezlib import messages as proto

from hideezlib.tools import parse_path


class TestMsgGetaddress(HideezTest):

    def test_btc(self):
        self.setup_mnemonic_nopin_nopassphrase()
        assert self.client.get_address('Bitcoin', []) == '18yLC4JMMNWLpwhR2AZJDzQciNpNJsdWMP'
        assert self.client.get_address('Bitcoin', [1]) == '1P7omjnoyYXGFRm9hXjM72a8KdmsAcSziA'
        assert self.client.get_address('Bitcoin', [0, -1]) == '13t8VMeMpVTqT93KMAHVoP7MXjR7nWgz1z'
        assert self.client.get_address('Bitcoin', [-9, 0]) == '1LtwvhsgeW9WY6Y3osimiAw5xteUuubZVy'
        assert self.client.get_address('Bitcoin', [0, 9999999]) == '1HVjzFwwDXauJANsLv2QvFcK5x1wZEPnjF'

    def test_ltc(self):
        self.setup_mnemonic_nopin_nopassphrase()
        assert self.client.get_address('Litecoin', []) == 'LTCHTGcBS2kQ5kPaCJYbW1UNvbBeNt48iG'
        assert self.client.get_address('Litecoin', [1]) == 'LhLm2x6e4CmKWETJsfieP3dtXr99EHAqig'
        assert self.client.get_address('Litecoin', [0, -1]) == 'LN75kZxBu9hthwjUXJGo5QB7jwnPpoWWH6'
        assert self.client.get_address('Litecoin', [-9, 0]) == 'Lf7uBvBWjAPZnuECz1i4zBzrB71m1APJCs'
        assert self.client.get_address('Litecoin', [0, 9999999]) == 'LbihFUFmJBpxYy52X41iCGg5JAPDed3ShD'

    def test_tbtc(self):
        self.setup_mnemonic_nopin_nopassphrase()
        assert self.client.get_address('Testnet', [111, 42]) == 'mo2pgiTkGXnHnF3i6bcceikHTjy21iRoed'

    def test_bch(self):
        self.setup_mnemonic_allallall()
        assert self.client.get_address('Bcash', parse_path("44'/145'/0'/0/0")) == 'bitcoincash:qp68396zpxkvcnqjtesk5fsa2kuw6ltresw9cjdlx0'
        assert self.client.get_address('Bcash', parse_path("44'/145'/0'/0/1")) == 'bitcoincash:qpzk3hufhgl5tj3cgzefppjpe832mfv6tsrtlhdpae'
        assert self.client.get_address('Bcash', parse_path("44'/145'/0'/1/0")) == 'bitcoincash:qpknzn0ltugd0475z3z6pscuazldvgtyqvurcqwxs6'

    def test_bch_multisig(self):
        self.setup_mnemonic_allallall()
        xpubs = []
        for n in map(lambda index: self.client.get_public_node(parse_path("44'/145'/" + str(index) + "'")), range(1, 4)):
            xpubs.append(n.xpub)

        def getmultisig(chain, nr, signatures=[b'', b'', b''], xpubs=xpubs):
            return proto.MultisigRedeemScriptType(
                pubkeys=list(map(lambda xpub: proto.HDNodePathType(node=bip32.deserialize(xpub), address_n=[chain, nr]), xpubs)),
                signatures=signatures,
                m=2,
            )
        for nr in range(1, 4):
            assert self.client.get_address('Bcash', parse_path("44'/145'/" + str(nr) + "'/0/0"), show_display=(nr == 1), multisig=getmultisig(0, 0)) == 'bitcoincash:ppvepa7y0ek8p2f2gm4pmeatvxev9u2vmsfvj2ktxg'
            assert self.client.get_address('Bcash', parse_path("44'/145'/" + str(nr) + "'/1/0"), show_display=(nr == 1), multisig=getmultisig(1, 0)) == 'bitcoincash:pr8hvff8m8hwrlg389mr4c40qjhf8zw6vulhlj3emm'

    def test_public_ckd(self):
        self.setup_mnemonic_nopin_nopassphrase()

        node = self.client.get_public_node([]).node
        node_sub1 = self.client.get_public_node([1]).node
        node_sub2 = bip32.public_ckd(node, [1])

        assert node_sub1.chain_code == node_sub2.chain_code
        assert node_sub1.public_key == node_sub2.public_key

        address1 = self.client.get_address('Bitcoin', [1])
        address2 = bip32.get_address(node_sub2, 0)

        assert address2 == '1P7omjnoyYXGFRm9hXjM72a8KdmsAcSziA'
        assert address1 == address2
