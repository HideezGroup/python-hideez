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
import pytest

from .common import HideezTest
from hideezlib.client import CallException


class TestMsgGetpublickeyCurve(HideezTest):

    def test_default_curve(self):
        self.setup_mnemonic_nopin_nopassphrase()
        assert hexlify(self.client.get_public_node([0x80000000 | 111, 42]).node.public_key).decode() == '02ab724de40a3b4080ef5fab04f69b09b7dc9c2758d68ba9f1032acefe52110f8a'
        assert hexlify(self.client.get_public_node([0x80000000 | 111, 0x80000000 | 42]).node.public_key).decode() == '02cd1e6901bfda3cef191bd5a3839573e9785b2ecdf8f1dc94401f0e51d0346aa8'

    def test_secp256k1_curve(self):
        self.setup_mnemonic_nopin_nopassphrase()
        assert hexlify(self.client.get_public_node([0x80000000 | 111, 42], ecdsa_curve_name='secp256k1').node.public_key).decode() == '02ab724de40a3b4080ef5fab04f69b09b7dc9c2758d68ba9f1032acefe52110f8a'
        assert hexlify(self.client.get_public_node([0x80000000 | 111, 0x80000000 | 42], ecdsa_curve_name='secp256k1').node.public_key).decode() == '02cd1e6901bfda3cef191bd5a3839573e9785b2ecdf8f1dc94401f0e51d0346aa8'
