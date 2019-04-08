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

import struct
from binascii import hexlify, unhexlify

from .common import HideezTest

from hideezlib import messages as proto


def check_path(identity):
    from hashlib import sha256
    m = sha256()
    m.update(struct.pack("<I", identity.index))
    uri = ''
    if identity.proto:
        uri += identity.proto + '://'
    if identity.user:
        uri += identity.user + '@'
    if identity.host:
        uri += identity.host
    if identity.port:
        uri += ':' + identity.port
    if identity.path:
        uri += identity.path
    m.update(uri)
    print('hash:', m.hexdigest())
    (a, b, c, d, _, _, _, _) = struct.unpack('<8I', m.digest())
    address_n = [0x80000000 | 13, 0x80000000 | a, 0x80000000 | b, 0x80000000 | c, 0x80000000 | d]
    print('path:', 'm/' + '/'.join([str(x) for x in address_n]))


class TestMsgSignidentity(HideezTest):

    def test_sign(self):
        self.setup_mnemonic_nopin_nopassphrase()

        hidden = unhexlify('cd8552569d6e4509266ef137584d1e62c7579b5b8ed69bbafa4b864c6521e7c2')
        visual = '2015-03-23 17:39:22'

        # URI  : https://satoshi@bitcoin.org/login
        # hash : d0e2389d4c8394a9f3e32de01104bf6e8db2d9e2bb0905d60fffa5a18fd696db
        # path : m/2147483661/2637750992/2845082444/3761103859/4005495825
        identity = proto.IdentityType(proto='https', user='satoshi', host='bitcoin.org', port='', path='/login', index=0)
        sig = self.client.sign_identity(identity, hidden, visual)
        assert sig.address == '1993MxgvySRDqwaBxwKL29UcSopDEYtjQY'
        assert hexlify(sig.public_key) == b'03049a4e90f1ee845f20cea6264325aaaa2dd6eb9d22f087f7f30b8d537608defb'
        assert hexlify(sig.signature) == b'1f8ee9f58ceccffa26a32d36fa38fccd7adf1887ba6431e5f4f24c342479b8577b329a7aed838bb06a386d0e1390baa8c64eecea1754ded27a399c58d23d64dab4'

        # URI  : ftp://satoshi@bitcoin.org:2323/pub
        # hash : 79a6b53831c6ff224fb283587adc4ebae8fb0d734734a46c876838f52dff53f3
        # path : m/2147483661/3098912377/2734671409/3632509519/3125730426
        identity = proto.IdentityType(proto='ftp', user='satoshi', host='bitcoin.org', port='2323', path='/pub', index=3)
        sig = self.client.sign_identity(identity, hidden, visual)
        assert sig.address == '1MCmX3eQiAyuDKZpryTUE1L1q3CgUiQo4Q'
        assert hexlify(sig.public_key) == b'02fd2e2f310f4890cea85abbcfbb3100ea50489bb298f9eaceb862ed4f56cb68d6'
        assert hexlify(sig.signature) == b'1f463aafa26910f5b116868a993349fc2f85a608f9136c1efc5329afef5a07ee793643d949e2a316a845a0726a2bdd31fc48f28a263112d059f8d344359622404b'

        # URI  : ssh://satoshi@bitcoin.org
        # hash : 5fa612f558a1a3b1fb7f010b2ea0a25cb02520a0ffa202ce74a92fc6145da5f3
        # path : m/2147483661/4111640159/2980290904/2332131323/3701645358
        identity = proto.IdentityType(proto='ssh', user='satoshi', host='bitcoin.org', port='', path='', index=47)
        sig = self.client.sign_identity(identity, hidden, visual, ecdsa_curve_name='nist256p1')
        assert sig.address is None
        assert hexlify(sig.public_key) == b'033397dca80e47b404ef318a7e35220b89cbbf8fc583f305eb98c88ac8f60d3213'
        assert hexlify(sig.signature) == b'00e5de7032de95978e78f5e5cd3dfaa3e7a0c079da42ae3b1de18a04538145d6f038a43355d1f4215f3b68c23401e4013bbad26d262529b633a531789e6f9899c9'

        # URI  : ssh://satoshi@bitcoin.org
        # hash : 5fa612f558a1a3b1fb7f010b2ea0a25cb02520a0ffa202ce74a92fc6145da5f3
        # path : m/2147483661/4111640159/2980290904/2332131323/3701645358
        identity = proto.IdentityType(proto='ssh', user='satoshi', host='bitcoin.org', port='', path='', index=47)
        sig = self.client.sign_identity(identity, hidden, visual, ecdsa_curve_name='ed25519')
        assert sig.address is None
        assert hexlify(sig.public_key) == b'00c26eb30e8a4c176785c9bdf1156290523d2bf6ac1f4d935d7d0b164297d3a2e8'
        assert hexlify(sig.signature) == b'0086d9adaf8b94aeeb65ebf1e4203ff5d5d251ab2f844182421b960c1e01c625a3a6e7f3252f863a2b8db118e844b9c7c776b96d6c94db61e63e023673cfc4e508'
