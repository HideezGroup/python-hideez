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

from binascii import hexlify, unhexlify

from .common import HideezTest
from ..support import ckd_public as bip32
from hideezlib import messages as proto
from hideezlib.coins import tx_api
from hideezlib.tools import parse_path


class TestMultisigChange(HideezTest):

    def setup_method(self, method):
        super(TestMultisigChange, self).setup_method(method)
        self.client.set_tx_api(tx_api['Testnet'])

    node_ext1 = bip32.deserialize('tpubDADHV9u9Y6gkggintTdMjJE3be58zKNLhpxBQyuEM6Pwx3sN9JVLmMCMN4DNVwL9AKec27z5TaWcWuHzMXiGAtcra5DjwWbvppGX4gaEGVN')
    # m/1 => 02c0d0c5fee952620757c6128dbf327c996cd72ed3358d15d6518a1186099bc15e
    # m/2 => 0375b9dfaad928ce1a7eed88df7c084e67d99e9ab74332419458a9a45779706801

    node_ext2 = bip32.deserialize('tpubDADHV9u9Y6gkhWXBmDJ6TUhZajLWjvKukRe2w9FfhdbQpUux8Z8jnPHNAZqFRgHPg9sR7YR93xThM32M7NfRu8S5WyDtext7S62sqxeJNkd')
    # m/1 => 0388460dc439f4c8f5bcfc268c36e11b4375cad5c3535c336cfdf8c32c3afad5c1
    # m/2 => 03a04f945d5a3685729dde697d574076de4bdf38e904f813b22a851548e1110fc0

    node_ext3 = bip32.deserialize('tpubDADHV9u9Y6gkmM5ohWRGTswrc6fr7soH7e2D2ic5a86PDUaHc5Ln9EbER69cEr5bDZPa7EXguJ1MhWVzPZpZWVdG5fvoF3hfirXvRbpCCBg')
    # m/1 => 02e0c21e2a7cf00b94c5421725acff97f9826598b91f2340c5ddda730caca7d648
    # m/2 => 03928301ffb8c0d7a364b794914c716ba3107cc78a6fe581028b0d8638b22e8573

    # m/45'/0
    node_int = bip32.deserialize('tpubDAr57pLnvN3Z6VjGJvqULNdJig1QKVh87QnNuDymu11WfGSTMbcDtrTU66GAqF9yAdLgiYFSfPdp6LXPWQC6S3iFBRaYNzXPfKy1jvS8NSm')
    # m/1 => 03f91460d79e4e463d7d90cb75254bcd62b515a99a950574c721efdc5f711dff35
    # m/2 => 038caebd6f753bbbd2bb1f3346a43cd32140648583673a31d62f2dfb56ad0ab9e3

    # ext1 + ext2 + int
    #   redeemscript (2 of 3): 522102c0d0c5fee952620757c6128dbf327c996cd72ed3358d15d6518a1186099bc15e210388460dc439f4c8f5bcfc268c36e11b4375cad5c3535c336cfdf8c32c3afad5c1210338d78612e990f2eea0c426b5e48a8db70b9d7ed66282b3b26511e0b1c75515a653ae
    #   multisig address: 3Gj7y1FdTppx2JEDqYqAEZFnKCA4GRysKF
    #   tx: d1d08ea63255af4ad16b098e9885a252632086fa6be53301521d05253ce8a73d
    #   input 0: 0.001 BTC

    # ext1 + int + ext2
    #   redeemscript (2 of 3): 522102c0d0c5fee952620757c6128dbf327c996cd72ed3358d15d6518a1186099bc15e210338d78612e990f2eea0c426b5e48a8db70b9d7ed66282b3b26511e0b1c75515a6210388460dc439f4c8f5bcfc268c36e11b4375cad5c3535c336cfdf8c32c3afad5c153ae
    #   multisig address: 3QsvfB6d1LzYcpm8xyhS1N1HBRrzHTgLHB
    #   tx: a6e2829d089cee47e481b1a753a53081b40738cc87e38f1d9b23ab57d9ad4396
    #   input 0: 0.001 BTC

    # ext1 + ext3 + int
    #   redeemscript (2 of 3): 522102c0d0c5fee952620757c6128dbf327c996cd72ed3358d15d6518a1186099bc15e2102e0c21e2a7cf00b94c5421725acff97f9826598b91f2340c5ddda730caca7d648210338d78612e990f2eea0c426b5e48a8db70b9d7ed66282b3b26511e0b1c75515a653ae
    #   multisig address: 37LvC1Q5CyKbMbKMncEJdXxqGhHxrBEgPE
    #   tx: e4bc1ae5e5007a08f2b3926fe11c66612e8f73c6b00c69c7027213b84d259be3
    #   input 1: 0.001 BTC

    multisig_in1 = proto.MultisigRedeemScriptType(
        pubkeys=[
            proto.HDNodePathType(node=node_ext2, address_n=[0, 0]),
            proto.HDNodePathType(node=node_ext1, address_n=[0, 0]),
            proto.HDNodePathType(node=node_int, address_n=[0, 0])
        ],
        signatures=[b'', b'', b''],
        m=2,
    )

    multisig_in2 = proto.MultisigRedeemScriptType(
        pubkeys=[
            proto.HDNodePathType(node=node_ext1, address_n=[0, 1]),
            proto.HDNodePathType(node=node_ext2, address_n=[0, 1]),
            proto.HDNodePathType(node=node_int, address_n=[0, 1]),
        ],
        signatures=[b'', b'', b''],
        m=2,
    )

    multisig_in3 = proto.MultisigRedeemScriptType(
        pubkeys=[
            proto.HDNodePathType(node=node_ext1, address_n=[0, 1]),
            proto.HDNodePathType(node=node_ext3, address_n=[0, 1]),
            proto.HDNodePathType(node=node_int, address_n=[0, 1])
        ],
        signatures=[b'', b'', b''],
        m=2,
    )

    # 2N9W4z9AhAPaHghtqVQPbaTAGHdbrhKeBQw
    inp1 = proto.TxInputType(
        address_n=[45 | 0x80000000, 0, 0, 0],
        prev_hash=unhexlify('16c6c8471b8db7a628f2b2bb86bfeefae1766463ce8692438c7fd3fce3f43ce5'),
        prev_index=1,
        script_type=proto.InputScriptType.SPENDMULTISIG,
        multisig=multisig_in1,
    )

    # 2NDBG6QXQLtnQ3jRGkrqo53BiCeXfQXLdj4
    inp2 = proto.TxInputType(
        address_n=[45 | 0x80000000, 0, 0, 1],
        prev_hash=unhexlify('d80c34ee14143a8bf61125102b7ef594118a3796cad670fa8ee15080ae155318'),
        prev_index=0,
        script_type=proto.InputScriptType.SPENDMULTISIG,
        multisig=multisig_in2,
    )

    # 2MvwPWfp2XPU3S1cMwgEMKBPUw38VP5SBE4
    inp3 = proto.TxInputType(
        address_n=[45 | 0x80000000, 0, 0, 1],
        prev_hash=unhexlify('b0946dc27ba308a749b11afecc2018980af18f79e89ad6b080b58220d856f739'),
        prev_index=0,
        script_type=proto.InputScriptType.SPENDMULTISIG,
        multisig=multisig_in3,
    )

    def _responses(self, inp1, inp2, change=0):
        resp = [
            proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
            proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=inp1.prev_hash)),
            proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=inp1.prev_hash)),
            proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=inp1.prev_hash)),
            proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=inp1.prev_hash)),
            proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=1)),
            proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=inp2.prev_hash)),
            proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=inp2.prev_hash)),
            proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=inp2.prev_hash)),
            proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=inp2.prev_hash)),
            proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
        ]
        resp.append(
            proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1))
        )
        resp += [
            proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
            proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=1)),
            proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
            proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
            proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
            proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=1)),
            proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
            proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
            proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
            proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
            proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
        ]
        return resp

    # both outputs are external
    def test_external_external(self):
        self.setup_mnemonic_nopin_nopassphrase()

        out1 = proto.TxOutputType(
            address='muevUcG1Bb8eM2nGUGhqmeujHRX7YXjSEu',
            amount=40000000,
            script_type=proto.OutputScriptType.PAYTOADDRESS
        )

        out2 = proto.TxOutputType(
            address='mwdrpMVSJxxsM8f8xbnCHn9ERaRT1NG1UX',
            amount=44000000,
            script_type=proto.OutputScriptType.PAYTOADDRESS
        )

        with self.client:
            self.client.set_expected_responses(self._responses(self.inp1, self.inp2))
            (_, serialized_tx) = self.client.sign_tx('Testnet', [self.inp1, self.inp2, ], [out1, out2, ])

        assert hexlify(serialized_tx) == b'0100000002e53cf4e3fcd37f8c439286ce636476e1faeebf86bbb2f228a6b78d1b47c8c61601000000b500483045022100b83f55b5909d5d368ad53f016586b49cf6d64189089efc1eeba2f1f316541e7f02201d41be646e08de2af07db9b4880a5ddc9f460c32d75dd3c4666dc602bae2dfb1014c69522103dc07026aacb5918dac4e09f9da8290d0ae22161699636c22cace78082116a7792103e70db185fad69c2971f0107a42930e5d82a9ed3a11b922a96fdfc4124b63e54c21038c124bfafc58ba5de8f3e2200ad904e11b66a1ffafd0ceb2ea26da187d68e02853aeffffffff185315ae8050e18efa70d6ca96378a1194f57e2b102511f68b3a1414ee340cd800000000b40047304402207d9a207b6139ea1fcc7c10d02db2b6d671f39d46ef3644f75ba9e45b728076fa02202d1cab6cb8303e89fd79dbc646cb819dc63e315a6ab7a1daa9d14369107824fe014c6952210297ad8a5df42f9e362ef37d9a4ddced89d8f7a143690649aa0d0ff049c7daca842103ed1fd93989595d7ad4b488efd05a22c0239482c9a20923f2f214a38e54f6c41a21025b464f5a3068dce6dbdbd30c099e9e9e213967db0e0add273d386ba1d767bbe753aeffffffff02005a6202000000001976a9149b139230e4fe91c05a37ec334dc8378f3dbe377088ac00639f02000000001976a914b0d05a10926a7925508febdbab9a5bd4cda8c8f688ac00000000'

    # first external, second internal
    def test_external_internal(self):
        self.setup_mnemonic_nopin_nopassphrase()

        out1 = proto.TxOutputType(
            address='muevUcG1Bb8eM2nGUGhqmeujHRX7YXjSEu',
            amount=40000000,
            script_type=proto.OutputScriptType.PAYTOADDRESS
        )

        out2 = proto.TxOutputType(
            address_n=parse_path("45'/0/1/1"),
            amount=44000000,
            script_type=proto.OutputScriptType.PAYTOADDRESS
        )

        with self.client:
            self.client.set_expected_responses(self._responses(self.inp1, self.inp2, change=2))
            (_, serialized_tx) = self.client.sign_tx('Testnet', [self.inp1, self.inp2, ], [out1, out2, ])

        assert hexlify(serialized_tx) == b'0100000002e53cf4e3fcd37f8c439286ce636476e1faeebf86bbb2f228a6b78d1b47c8c61601000000b40047304402200c4fa6e53961b88ce8319924dc07b23feb931923b8e8d0625028ee408d6f6a970220360b7bd8e585a331a2b2c87f9c1f36197f351f9fc4949068cf3359a7f2b6d73f014c69522103dc07026aacb5918dac4e09f9da8290d0ae22161699636c22cace78082116a7792103e70db185fad69c2971f0107a42930e5d82a9ed3a11b922a96fdfc4124b63e54c21038c124bfafc58ba5de8f3e2200ad904e11b66a1ffafd0ceb2ea26da187d68e02853aeffffffff185315ae8050e18efa70d6ca96378a1194f57e2b102511f68b3a1414ee340cd800000000b40047304402206c612fe0e17cf37f7e035be7faa5c5df721e7463de621bb953f099ac3f3a828902206b86dad2bb4377f4a2d77a248e3d5d5c69abdcb544f40bd261e12b7cd67f9456014c6952210297ad8a5df42f9e362ef37d9a4ddced89d8f7a143690649aa0d0ff049c7daca842103ed1fd93989595d7ad4b488efd05a22c0239482c9a20923f2f214a38e54f6c41a21025b464f5a3068dce6dbdbd30c099e9e9e213967db0e0add273d386ba1d767bbe753aeffffffff02005a6202000000001976a9149b139230e4fe91c05a37ec334dc8378f3dbe377088ac00639f02000000001976a914794659b1482d713ae4facfc09cf45466eed7dd3e88ac00000000'

    # first internal, second external
    def test_internal_external(self):
        self.setup_mnemonic_nopin_nopassphrase()

        out1 = proto.TxOutputType(
            address_n=parse_path("45'/0/1/0"),
            amount=40000000,
            script_type=proto.OutputScriptType.PAYTOADDRESS
        )

        out2 = proto.TxOutputType(
            address='mwdrpMVSJxxsM8f8xbnCHn9ERaRT1NG1UX',
            amount=44000000,
            script_type=proto.OutputScriptType.PAYTOADDRESS
        )

        with self.client:
            self.client.set_expected_responses(self._responses(self.inp1, self.inp2, change=1))
            (_, serialized_tx) = self.client.sign_tx('Testnet', [self.inp1, self.inp2, ], [out1, out2, ])

        assert hexlify(serialized_tx) == b'0100000002e53cf4e3fcd37f8c439286ce636476e1faeebf86bbb2f228a6b78d1b47c8c61601000000b500483045022100aa0a1b8e97e62d63b02cb7a714c3dbb816cd7b56304c36ca91e4b59e48627b650220527b412cb1f71ac208cf1f4c25c3174fe13297cd0299a1071170d58bbea387ba014c69522103dc07026aacb5918dac4e09f9da8290d0ae22161699636c22cace78082116a7792103e70db185fad69c2971f0107a42930e5d82a9ed3a11b922a96fdfc4124b63e54c21038c124bfafc58ba5de8f3e2200ad904e11b66a1ffafd0ceb2ea26da187d68e02853aeffffffff185315ae8050e18efa70d6ca96378a1194f57e2b102511f68b3a1414ee340cd800000000b5004830450221009036e6bbb0a7af02f5993525b9e4e63ddfadd17a645f40fc46fb4d517d38f99402206f13e81596b10eab8e0c81a59830ae4ad3a82c43c177dc6d5c40a757e42254fd014c6952210297ad8a5df42f9e362ef37d9a4ddced89d8f7a143690649aa0d0ff049c7daca842103ed1fd93989595d7ad4b488efd05a22c0239482c9a20923f2f214a38e54f6c41a21025b464f5a3068dce6dbdbd30c099e9e9e213967db0e0add273d386ba1d767bbe753aeffffffff02005a6202000000001976a914c5d93a7fc535d6a9f6668830b33fa68b14b250ae88ac00639f02000000001976a914b0d05a10926a7925508febdbab9a5bd4cda8c8f688ac00000000'

    # both outputs are external
    def test_multisig_external_external(self):
        self.setup_mnemonic_nopin_nopassphrase()

        out1 = proto.TxOutputType(
            address='2N2aFoogGntQFFwdUVPfRmutXD22ThcNTsR',
            amount=40000000,
            script_type=proto.OutputScriptType.PAYTOADDRESS
        )

        out2 = proto.TxOutputType(
            address='2NFJjQcU8mw4Z3ywpbek8HL1VoJ27GDrkHw',
            amount=44000000,
            script_type=proto.OutputScriptType.PAYTOADDRESS
        )

        with self.client:
            self.client.set_expected_responses(self._responses(self.inp1, self.inp2))
            (_, serialized_tx) = self.client.sign_tx('Testnet', [self.inp1, self.inp2, ], [out1, out2, ])

        assert hexlify(serialized_tx) == b'0100000002e53cf4e3fcd37f8c439286ce636476e1faeebf86bbb2f228a6b78d1b47c8c61601000000b40047304402204248374f704cee8ac074577a107f7445d49a4ec0f4f323b74a49e1939a88484602203e5024b1e8c57a8146281f87bef81b8b860db6b3bef95df1aac0760ace0ab62e014c69522103dc07026aacb5918dac4e09f9da8290d0ae22161699636c22cace78082116a7792103e70db185fad69c2971f0107a42930e5d82a9ed3a11b922a96fdfc4124b63e54c21038c124bfafc58ba5de8f3e2200ad904e11b66a1ffafd0ceb2ea26da187d68e02853aeffffffff185315ae8050e18efa70d6ca96378a1194f57e2b102511f68b3a1414ee340cd800000000b40047304402205818d7f6be68dbd75e2e14a5264c5de00b4259483912d77fd549b8721c9b2a360220214ea606137980f12dd14a69f8a62533f380da9422021b9cdde662be4694e82e014c6952210297ad8a5df42f9e362ef37d9a4ddced89d8f7a143690649aa0d0ff049c7daca842103ed1fd93989595d7ad4b488efd05a22c0239482c9a20923f2f214a38e54f6c41a21025b464f5a3068dce6dbdbd30c099e9e9e213967db0e0add273d386ba1d767bbe753aeffffffff02005a62020000000017a91466528dd543f94d162c8111d2ec248d25ba9b90948700639f020000000017a914f1fc92c0aed1712911c70a2e09ac15ff0922652f8700000000'

    # inputs match, change matches (first is change)
    def test_multisig_change_match_first(self):
        self.setup_mnemonic_nopin_nopassphrase()

        multisig_out1 = proto.MultisigRedeemScriptType(
            pubkeys=[
                proto.HDNodePathType(node=self.node_ext2, address_n=[1, 0]),
                proto.HDNodePathType(node=self.node_ext1, address_n=[1, 0]),
                proto.HDNodePathType(node=self.node_int, address_n=[1, 0])
            ],
            signatures=[b'', b'', b''],
            m=2,
        )

        out1 = proto.TxOutputType(
            address_n=[0x80000000 | 45, 0, 1, 0],
            multisig=multisig_out1,
            amount=40000000,
            script_type=proto.OutputScriptType.PAYTOMULTISIG
        )

        out2 = proto.TxOutputType(
            address='2NFJjQcU8mw4Z3ywpbek8HL1VoJ27GDrkHw',
            amount=44000000,
            script_type=proto.OutputScriptType.PAYTOADDRESS
        )

        with self.client:
            self.client.set_expected_responses(self._responses(self.inp1, self.inp2, change=1))
            (_, serialized_tx) = self.client.sign_tx('Testnet', [self.inp1, self.inp2, ], [out1, out2, ])

        assert hexlify(serialized_tx) == b'0100000002e53cf4e3fcd37f8c439286ce636476e1faeebf86bbb2f228a6b78d1b47c8c61601000000b500483045022100a0c9c923a27f9852ced3064ec8183ba2f7d9897b1a416357f1e8bf242f194c1d02202cebe99b428d2ff539fad2ba428e821de9a6a1891eaf941b921ad98534513626014c69522103dc07026aacb5918dac4e09f9da8290d0ae22161699636c22cace78082116a7792103e70db185fad69c2971f0107a42930e5d82a9ed3a11b922a96fdfc4124b63e54c21038c124bfafc58ba5de8f3e2200ad904e11b66a1ffafd0ceb2ea26da187d68e02853aeffffffff185315ae8050e18efa70d6ca96378a1194f57e2b102511f68b3a1414ee340cd800000000b500483045022100c5c59484926e1b2560d964f28c6fd62a44fb01fb895cad23978f5940b53b2509022072338a2621f6e5a078994a57095a28397348812f0ea46e1a5ded117afb89a0a3014c6952210297ad8a5df42f9e362ef37d9a4ddced89d8f7a143690649aa0d0ff049c7daca842103ed1fd93989595d7ad4b488efd05a22c0239482c9a20923f2f214a38e54f6c41a21025b464f5a3068dce6dbdbd30c099e9e9e213967db0e0add273d386ba1d767bbe753aeffffffff02005a62020000000017a914705d4f1d91c05ee5bde07e8e81fe878c2a2d48a68700639f020000000017a914f1fc92c0aed1712911c70a2e09ac15ff0922652f8700000000'

    # inputs match, change matches (second is change)
    def test_multisig_change_match_second(self):
        self.setup_mnemonic_nopin_nopassphrase()

        multisig_out2 = proto.MultisigRedeemScriptType(
            pubkeys=[
                proto.HDNodePathType(node=self.node_ext1, address_n=[1, 1]),
                proto.HDNodePathType(node=self.node_ext2, address_n=[1, 1]),
                proto.HDNodePathType(node=self.node_int, address_n=[1, 1])
            ],
            signatures=[b'', b'', b''],
            m=2,
        )

        out1 = proto.TxOutputType(
            address='2N2aFoogGntQFFwdUVPfRmutXD22ThcNTsR',
            amount=40000000,
            script_type=proto.OutputScriptType.PAYTOADDRESS
        )

        out2 = proto.TxOutputType(
            address_n=[0x80000000 | 45, 0, 1, 1],
            multisig=multisig_out2,
            amount=44000000,
            script_type=proto.OutputScriptType.PAYTOMULTISIG
        )

        with self.client:
            self.client.set_expected_responses(self._responses(self.inp1, self.inp2, change=2))
            (_, serialized_tx) = self.client.sign_tx('Testnet', [self.inp1, self.inp2, ], [out1, out2, ])

        assert hexlify(serialized_tx) == b'0100000002e53cf4e3fcd37f8c439286ce636476e1faeebf86bbb2f228a6b78d1b47c8c61601000000b400473044022027cd3f397e006922a45978dffde57ad87fca656372526c1c494726c9dd216d7502206674ad0281f4210d32b37da1651921750f8c66c1e6d2b69c8909b701f602901a014c69522103dc07026aacb5918dac4e09f9da8290d0ae22161699636c22cace78082116a7792103e70db185fad69c2971f0107a42930e5d82a9ed3a11b922a96fdfc4124b63e54c21038c124bfafc58ba5de8f3e2200ad904e11b66a1ffafd0ceb2ea26da187d68e02853aeffffffff185315ae8050e18efa70d6ca96378a1194f57e2b102511f68b3a1414ee340cd800000000b500483045022100b24ca91c00574e1ed3d7370a4cdc52f004040ea308d18977450bc428477eb62002203e1be7e1a990a29c019202a5f9631dd7a94d603f8ca77834740b3be814718172014c6952210297ad8a5df42f9e362ef37d9a4ddced89d8f7a143690649aa0d0ff049c7daca842103ed1fd93989595d7ad4b488efd05a22c0239482c9a20923f2f214a38e54f6c41a21025b464f5a3068dce6dbdbd30c099e9e9e213967db0e0add273d386ba1d767bbe753aeffffffff02005a62020000000017a91466528dd543f94d162c8111d2ec248d25ba9b90948700639f020000000017a914a13fc6db7be0606fb301567d90c9f89d05cd3a1b8700000000'

    # inputs match, change mismatches (second tries to be change but isn't)
    def test_multisig_mismatch_change(self):
        self.setup_mnemonic_nopin_nopassphrase()

        multisig_out2 = proto.MultisigRedeemScriptType(
            pubkeys=[
                proto.HDNodePathType(node=self.node_ext1, address_n=[1, 0]),
                proto.HDNodePathType(node=self.node_int, address_n=[1, 0]),
                proto.HDNodePathType(node=self.node_ext3, address_n=[1, 0])
            ],
            signatures=[b'', b'', b''],
            m=2,
        )

        out1 = proto.TxOutputType(
            address='2N2aFoogGntQFFwdUVPfRmutXD22ThcNTsR',
            amount=40000000,
            script_type=proto.OutputScriptType.PAYTOADDRESS
        )

        out2 = proto.TxOutputType(
            address_n=[0x80000000 | 45, 0, 1, 0],
            multisig=multisig_out2,
            amount=44000000,
            script_type=proto.OutputScriptType.PAYTOMULTISIG
        )

        with self.client:
            self.client.set_expected_responses(self._responses(self.inp1, self.inp2))
            (_, serialized_tx) = self.client.sign_tx('Testnet', [self.inp1, self.inp2, ], [out1, out2, ])

        assert hexlify(serialized_tx) == b'0100000002e53cf4e3fcd37f8c439286ce636476e1faeebf86bbb2f228a6b78d1b47c8c61601000000b40047304402205a647596f2ba4746a07dbcb8c3efed1ccbe3b29212ffe6493a8763c0e7227ff302205c7897deaa1183fea95a6b6b97c00c7460aa0219413c7329fc624b98d366ef21014c69522103dc07026aacb5918dac4e09f9da8290d0ae22161699636c22cace78082116a7792103e70db185fad69c2971f0107a42930e5d82a9ed3a11b922a96fdfc4124b63e54c21038c124bfafc58ba5de8f3e2200ad904e11b66a1ffafd0ceb2ea26da187d68e02853aeffffffff185315ae8050e18efa70d6ca96378a1194f57e2b102511f68b3a1414ee340cd800000000b500483045022100fcc5b14240541914824c79c1f1d760cf9b61d2802c99ee1c4d3b449fa7b2fca502206e368c03813ef0a4b2ac32a6e5ea6ac52b0f6deb9dbf0c45198f1d3abcafc7f0014c6952210297ad8a5df42f9e362ef37d9a4ddced89d8f7a143690649aa0d0ff049c7daca842103ed1fd93989595d7ad4b488efd05a22c0239482c9a20923f2f214a38e54f6c41a21025b464f5a3068dce6dbdbd30c099e9e9e213967db0e0add273d386ba1d767bbe753aeffffffff02005a62020000000017a91466528dd543f94d162c8111d2ec248d25ba9b90948700639f020000000017a9146169c87e30105747aafd636bfd35bc9e3a5e13ea8700000000'

    # inputs mismatch, change matches with first input
    def test_multisig_mismatch_inputs(self):
        self.setup_mnemonic_nopin_nopassphrase()

        multisig_out1 = proto.MultisigRedeemScriptType(
            pubkeys=[
                proto.HDNodePathType(node=self.node_ext2, address_n=[1, 0]),
                proto.HDNodePathType(node=self.node_ext1, address_n=[1, 0]),
                proto.HDNodePathType(node=self.node_int, address_n=[1, 0])
            ],
            signatures=[b'', b'', b''],
            m=2,
        )

        out1 = proto.TxOutputType(
            address_n=[0x80000000 | 45, 0, 1, 0],
            multisig=multisig_out1,
            amount=40000000,
            script_type=proto.OutputScriptType.PAYTOMULTISIG
        )

        out2 = proto.TxOutputType(
            address='2NFJjQcU8mw4Z3ywpbek8HL1VoJ27GDrkHw',
            amount=65000000,
            script_type=proto.OutputScriptType.PAYTOADDRESS
        )

        with self.client:
            self.client.set_expected_responses(self._responses(self.inp1, self.inp3))
            (_, serialized_tx) = self.client.sign_tx('Testnet', [self.inp1, self.inp3, ], [out1, out2, ])

        assert hexlify(serialized_tx) == b'0100000002e53cf4e3fcd37f8c439286ce636476e1faeebf86bbb2f228a6b78d1b47c8c61601000000b500483045022100b7f49a255464bc69a5ea576bc5512084561d527d6cb2cd056cfa6350c51c21a8022017bb0b4eeb4dfd28646c234b3c7c49e535378675caa60b83bbdc629baeb94d28014c69522103dc07026aacb5918dac4e09f9da8290d0ae22161699636c22cace78082116a7792103e70db185fad69c2971f0107a42930e5d82a9ed3a11b922a96fdfc4124b63e54c21038c124bfafc58ba5de8f3e2200ad904e11b66a1ffafd0ceb2ea26da187d68e02853aeffffffff39f756d82082b580b0d69ae8798ff10a981820ccfe1ab149a708a37bc26d94b000000000b500483045022100a9ca27e9943ba7bfbf5b654f38982d62cf2cb82c0b99156ab739b472e31cd580022074b564cf50ad8078bbae89b86af8e31a098eddc61b1a91697ea9b8c52acece7d014c6952210297ad8a5df42f9e362ef37d9a4ddced89d8f7a143690649aa0d0ff049c7daca842103b6321a1194e5cc47b6b7edc3f67a096e6f71ccb72440f84f390b6e98df0ea8ec21025b464f5a3068dce6dbdbd30c099e9e9e213967db0e0add273d386ba1d767bbe753aeffffffff02005a62020000000017a914705d4f1d91c05ee5bde07e8e81fe878c2a2d48a68740d2df030000000017a914f1fc92c0aed1712911c70a2e09ac15ff0922652f8700000000'
