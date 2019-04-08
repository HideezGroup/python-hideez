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

from binascii import unhexlify, hexlify

from .common import HideezTest
from hideezlib import messages as proto


class TestMsgGetECDHSessionKey(HideezTest):

    def test_ecdh(self):
        self.setup_mnemonic_nopin_nopassphrase()

        # URI  : gpg://Satoshi Nakamoto <satoshi@bitcoin.org>
        identity = proto.IdentityType(proto='gpg', user='', host='Satoshi Nakamoto <satoshi@bitcoin.org>', port='', path='', index=0)

        peer_public_key = unhexlify('0407f2c6e5becf3213c1d07df0cfbe8e39f70a8c643df7575e5c56859ec52c45ca950499c019719dae0fda04248d851e52cf9d66eeb211d89a77be40de22b6c89d')
        result = self.client.get_ecdh_session_key(identity=identity, peer_public_key=peer_public_key, ecdsa_curve_name='secp256k1')
        assert result.session_key == unhexlify('043846892d9014619384be914d0f660310ad0d4e950eb80d451dcbc8384f3d5c7b490e9258409db1599ab380ab721914c4ccff26085e3fe85578267c3730f36e4b')

        peer_public_key = unhexlify('04811a6c2bd2a547d0dd84747297fec47719e7c3f9b0024f027c2b237be99aac39a9230acbd163d0cb1524a0f5ea4bfed6058cec6f18368f72a12aa0c4d083ff64')
        result = self.client.get_ecdh_session_key(identity=identity, peer_public_key=peer_public_key, ecdsa_curve_name='nist256p1')
        assert result.session_key == unhexlify('04b57a25379cf32801fff3111a373caadadbe91fee72bd7b9ea833d596e48c449e858c42097ba8a825a8395fb58ebbbb92247803c32332cd5bf56649d0188db624')

        peer_public_key = unhexlify('40a8cf4b6a64c4314e80f15a8ea55812bd735fbb365936a48b2d78807b575fa17a')
        result = self.client.get_ecdh_session_key(identity=identity, peer_public_key=peer_public_key, ecdsa_curve_name='curve25519')
        assert result.session_key == unhexlify('046042056bf095f1c04a5f6a3ff33386d7df1b38d7f21c329641bf8b43d546d948')
