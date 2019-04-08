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
import pytest

from .common import HideezTest
from ..support import ckd_public as bip32
from hideezlib import messages as proto
from hideezlib.client import CallException

TXHASH_c6091a = unhexlify('c6091adf4c0c23982a35899a6e58ae11e703eacd7954f588ed4b9cdefc4dba52')


# Multisig howto:
#
# https://sx.dyne.org/multisig.html
#


class TestMultisig(HideezTest):

    def test_2_of_3(self):
        self.setup_mnemonic_nopin_nopassphrase()

        # key1 = self.client.get_public_node([1])
        # key2 = self.client.get_public_node([2])
        # key3 = self.client.get_public_node([3])

        # xpub:
        # print(bip32.serialize(self.client.get_public_node([]).node))
        # xpub661MyMwAqRbcF1zGijBb2K6x9YiJPh58xpcCeLvTxMX6spkY3PcpJ4ABcCyWfskq5DDxM3e6Ez5ePCqG5bnPUXR4wL8TZWyoDaUdiWW7bKy

        # pubkeys:
        #    xpub/1: 0338d78612e990f2eea0c426b5e48a8db70b9d7ed66282b3b26511e0b1c75515a6
        #    xpub/2: 038caebd6f753bbbd2bb1f3346a43cd32140648583673a31d62f2dfb56ad0ab9e3
        #    xpub/3: 03477b9f0f34ae85434ce795f0c5e1e90c9420e5b5fad084d7cce9a487b94a7902

        # redeem script:
        # 52210338d78612e990f2eea0c426b5e48a8db70b9d7ed66282b3b26511e0b1c75515a621038caebd6f753bbbd2bb1f3346a43cd32140648583673a31d62f2dfb56ad0ab9e32103477b9f0f34ae85434ce795f0c5e1e90c9420e5b5fad084d7cce9a487b94a790253ae

        # multisig address: 3E7GDtuHqnqPmDgwH59pVC7AvySiSkbibz

        # tx: c6091adf4c0c23982a35899a6e58ae11e703eacd7954f588ed4b9cdefc4dba52
        # input 1: 0.001 BTC

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

        # Let's go to sign with key 1
        inp1 = proto.TxInputType(
            address_n=[1],
            prev_hash=TXHASH_c6091a,
            prev_index=1,
            script_type=proto.InputScriptType.SPENDMULTISIG,
            multisig=multisig,
        )

        out1 = proto.TxOutputType(
            address='12iyMbUb4R2K3gre4dHSrbu5azG5KaqVss',
            amount=100000,
            script_type=proto.OutputScriptType.PAYTOADDRESS
        )

        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=TXHASH_c6091a)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_c6091a)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_c6091a)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_c6091a)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])

            # Now we have first signature
            (signatures1, _) = self.client.sign_tx('Bitcoin', [inp1, ], [out1, ])

        assert hexlify(signatures1[0]) == b'30440220650a2b065231511223a200afbd39dbe31e217de71443f3e1bf6f16184ffb454102207363a9991104273be3bacb51d77e53055f32a6c324e296567705d53ad1266f04'

        # ---------------------------------------
        # Let's do second signature using 3rd key

        multisig = proto.MultisigRedeemScriptType(
            pubkeys=[
                proto.HDNodePathType(node=node, address_n=[1]),
                proto.HDNodePathType(node=node, address_n=[2]),
                proto.HDNodePathType(node=node, address_n=[3])
            ],
            signatures=[signatures1[0], b'', b''],  # Fill signature from previous signing process
            m=2,
        )

        # Let's do a second signature with key 3
        inp3 = proto.TxInputType(
            address_n=[3],
            prev_hash=TXHASH_c6091a,
            prev_index=1,
            script_type=proto.InputScriptType.SPENDMULTISIG,
            multisig=multisig,
        )

        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=TXHASH_c6091a)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_c6091a)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_c6091a)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_c6091a)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures2, serialized_tx) = self.client.sign_tx('Bitcoin', [inp3, ], [out1, ])

        assert hexlify(signatures2[0]) == b'30450221009181106fe1ac79dd86b84e349cdc46d6c842018bbad4a0d0464590d380f9466c02207dc0c6678dbd2df7d8560239dfe9db6dda35483870f8db3f3ff2534e15b4da6d'

        # Accepted by network: tx 8382a2b2e3ec8788800c1d46d285dfa9dd4051edddd75982fad166b9273e5ac6
        assert hexlify(serialized_tx) == b'010000000152ba4dfcde9c4bed88f55479cdea03e711ae586e9a89352a98230c4cdf1a09c601000000fdfd00004730440220650a2b065231511223a200afbd39dbe31e217de71443f3e1bf6f16184ffb454102207363a9991104273be3bacb51d77e53055f32a6c324e296567705d53ad1266f04014830450221009181106fe1ac79dd86b84e349cdc46d6c842018bbad4a0d0464590d380f9466c02207dc0c6678dbd2df7d8560239dfe9db6dda35483870f8db3f3ff2534e15b4da6d014c69522103912a8f07b60de8f0b2800f1088f9b016059219cc63beeb4bf26e1bd5e7da5319210309b80e44b9ee837a2ef8e839cce1d6bb7c1408646143fb9b59569f39669e3049210262f6426d6942332874d20899b44c136b0b56c66b876de9658a97182ad1cafc7953aeffffffff01a0860100000000001976a91412e8391ad256dcdc023365978418d658dfecba1c88ac00000000'

    def test_15_of_15(self):
        self.setup_mnemonic_nopin_nopassphrase()

        """
        pubs = []
        for x in range(15):
            pubs.append(hexlify(self.client.get_public_node([x]).node.public_key))
        """

        # xpub:
        # print(bip32.serialize(self.client.get_public_node([]).node))
        # xpub661MyMwAqRbcF1zGijBb2K6x9YiJPh58xpcCeLvTxMX6spkY3PcpJ4ABcCyWfskq5DDxM3e6Ez5ePCqG5bnPUXR4wL8TZWyoDaUdiWW7bKy
        node = bip32.deserialize('xpub661MyMwAqRbcFW3NvPPCXr3RKSnks2UPNj543xvx3zKaWMTDH7rifpbTxgRbeavHFgke9vrfGZSb16ePwqWpguRYquYo8QtNRKcnVnPdmMp')

        pubs = []
        for x in range(15):
            pubs.append(proto.HDNodePathType(node=node, address_n=[x]))

        # redeeemscript
        # 5f21023230848585885f63803a0a8aecdd6538792d5c539215c91698e315bf0253b43d210338d78612e990f2eea0c426b5e48a8db70b9d7ed66282b3b26511e0b1c75515a621038caebd6f753bbbd2bb1f3346a43cd32140648583673a31d62f2dfb56ad0ab9e32103477b9f0f34ae85434ce795f0c5e1e90c9420e5b5fad084d7cce9a487b94a79022103fe91eca10602d7dad4c9dab2b2a0858f71e25a219a6940749ce7a48118480dae210234716c01c2dd03fa7ee302705e2b8fbd1311895d94b1dca15e62eedea9b0968f210341fb2ead334952cf60f4481ba435c4693d0be649be01d2cfe9b02018e483e7bd2102dad8b2bce360a705c16e74a50a36459b4f8f4b78f9cd67def29d54ef6f7c7cf9210222dbe3f5f197a34a1d50e2cbe2a1085cac2d605c9e176f9a240e0fd0c669330d2103fb41afab56c9cdb013fda63d777d4938ddc3cb2ad939712da688e3ed333f95982102435f177646bdc717cb3211bf46656ca7e8d642726144778c9ce816b8b8c36ccf2102158d8e20095364031d923c7e9f7f08a14b1be1ddee21fe1a5431168e31345e5521026259794892428ca0818c8fb61d2d459ddfe20e57f50803c7295e6f4e2f5586652102815f910a8689151db627e6e262e0a2075ad5ec2993a6bc1b876a9d420923d681210318f54647f645ff01bd49fedc0219343a6a22d3ea3180a3c3d3097e4b888a8db45fae

        # multisig address
        # 3QaKF8zobqcqY8aS6nxCD5ZYdiRfL3RCmU

        signatures = [b''] * 15

        out1 = proto.TxOutputType(
            address='17kTB7qSk3MupQxWdiv5ZU3zcrZc2Azes1',
            amount=10000,
            script_type=proto.OutputScriptType.PAYTOADDRESS
        )

        for x in range(15):
            multisig = proto.MultisigRedeemScriptType(
                pubkeys=pubs,
                signatures=signatures,
                m=15,
            )

            inp1 = proto.TxInputType(
                address_n=[x],
                prev_hash=unhexlify('6189e3febb5a21cee8b725aa1ef04ffce7e609448446d3a8d6f483c634ef5315'),
                prev_index=1,
                script_type=proto.InputScriptType.SPENDMULTISIG,
                multisig=multisig,
            )

            with self.client:
                (sig, serialized_tx) = self.client.sign_tx('Bitcoin', [inp1, ], [out1, ])
                signatures[x] = sig[0]

        # Accepted as tx id dd320786d1f58c095be0509dc56b277b6de8f2fb5517f519c6e6708414e3300b
        assert hexlify(serialized_tx) == b'01000000011553ef34c683f4d6a8d346844409e6e7fc4ff01eaa25b7e8ce215abbfee3896101000000fd440600473044022069759a1f82ba3eb3577e13e36b199aa54939a097accb085766b8e3796b98afaa022024bb93a30fa66d90930f5b3b5f37411a850e4a84d3c9b0d6522014ea37d3a66301473044022017de2986c48dc9f3227d95c93d04b75061f038076459af9ae0f61ba46fa8f6a6022061ec4d4a2a99e67934946ea76619e14ecad90631089daabca5b8c0eab17b168b014830450221008ea5fb5e6555ac745988baaf1beccad1f21957ce4b8769424c0d9856ee6b2ed902204c2ce90bae9a478a7e3d9b2d9c22b6136026fc653d677a74e6c6600696af3a96014730440220567ee5c2027841e21c5597b648eea192b4a12eed7182f940b896770cffa87ed30220607023fafed86a1373ccd4c8de6b223cd226a3c0bdf669b06fa66c905afdd24b01483045022100cd664977973c0f51384b6feb2eb651cca52377c7c91ec96b4838d1a96084b03102205cf95ea28b4f4dfb6abceb02ee517ff8e03ddce9fe40434b0d70896f24c2e234014730440220059a86bffc16ebfd958aa6b0e347807a839a65159bf8a12605fbfa30aee9b61c022053dfda65277510f55aea29175e1924dfb97d7a2366127d8a2ee2a2b4f4047e4e01473044022042b425ee8c87131533f768082ff6a71a7f925584b5cb74c035c57835eb06341502203e8377f7cec26f2f1caeff25b839e546822b6afdd622e1c87ccc1518c112fb7a01483045022100b77d30ec7d764c419386fc275ec3e93e8cb6a266959086b8d86a93c0044a91af02201201982a9f5cac00178df3bce02d82d46457772a7fa8c532fc4c9b6bf245c51d0147304402204aa6268dbafcea94e29c61fdcb5b88b2d5a95ccf7101ae81c0534c4db159676f02203ade8e9ebecbd0ffba249450fa6dd993f28a83d2ef0b422d5fc18495d5a693aa01483045022100de920a940de7035d34e60cdfcc8f2ed794498fb5fbc807a0f53339da35e5628502207f869279372b9051e8443e4159fa720c352870758b5e5cdc364a3d66aa768d5701473044022026121b6c5c99c94d85815c56f586f77f74f56bf49731e891a2d4fba1ad4d31c1022045fa621c1bd25209a91951c1e7638ec87c311b450299b19c264c9887e617e40b01473044022068300807e73176ae94f9352ec3051f23bcc6a131f449061a33c2925ffffcfc480220483e63ae743d14a9472dd861bf5f79f15a7cc12f00e8bad61f5cf49a7e2cf61201483045022100d06cce8c8ae2e3ab382dd62159d222bb77040beaa7a19f8f2b21b24b699e12e302201027ca2f03aeaa1414cbb8969e9acf63814129872c9a94d0a4e55342cf456c5601483045022100b24778fa3a1f87fb5dd164454514ad8f97dc507e4bcb50d1fc68cd4f44ecd24d02200e5720e4e941cfe39d8e43ef77db5b4497dfca4327ecaae62ebbd9c0515c878201483045022100979c49b69c006dd7d0d6a0f18f05d87f40c8cbb513530580d20c6511e86e0e88022029b9ef179ad3fdeaec91f90fcda2a44dc95b839e67528ebe2e3826b11b4871de014d01025f2103bb20b056809acb091b3e3d1833681cb80f7b5f09bd9c5a229f5ff00edfcdee112103912a8f07b60de8f0b2800f1088f9b016059219cc63beeb4bf26e1bd5e7da5319210309b80e44b9ee837a2ef8e839cce1d6bb7c1408646143fb9b59569f39669e3049210262f6426d6942332874d20899b44c136b0b56c66b876de9658a97182ad1cafc79210201d07233d7c1c63d2004ba28e11a0cbab4802b7d70fce644564c3067e8100b712103c86a1fe7530c538d640692ebe24eefdec35d64759952ec69ffb616f1bc73fbcd2102f1404a0a192ce18c471448cc4f26f80252aaed299854c3b86dc4b90167493df0210234f078300980ffcb54957386634300660f84519a9731b5ffd9b1b629a0c0f6d42103ba77c9108cf392030d4ef801cc7ee1bc404acd704ed61eb945622f8377c76e55210332881699bec210e2e0e15cb861864e88a27195f84855df789f44c9e68ae763bc21025007b55de10f834b1b7b75d02ebed4ddf2df8f2a370a883290daf2cbf40fd612210321ea75cc48cb17e35b8d2b2e0383181fc85950f896ef7ffe6658c3b2f3f6872821021ea187ea5868b053a1a91e4e7135f6cf4f9caf0a8cada43b8ff14c87d4cadce02102f164a27945a02a791f682a7f5cef88f95b2f8e273d75fb94b39d3fb17284a6db210294db8e8e09ee6d70436e9a01246cf94db741f0cd14fcb8f37964281a3bcb60d05faeffffffff0110270000000000001976a9144a087d89f8ad16ca029c675b037c02fd1c5f9aec88ac00000000'

    def test_missing_pubkey(self):
        self.setup_mnemonic_nopin_nopassphrase()

        # key1 = self.client.get_public_node([1])
        # key2 = self.client.get_public_node([2])
        # key3 = self.client.get_public_node([3])

        # pubkeys:
        #    0338d78612e990f2eea0c426b5e48a8db70b9d7ed66282b3b26511e0b1c75515a6
        #    038caebd6f753bbbd2bb1f3346a43cd32140648583673a31d62f2dfb56ad0ab9e3
        #    03477b9f0f34ae85434ce795f0c5e1e90c9420e5b5fad084d7cce9a487b94a7902

        # multisig address: 3E7GDtuHqnqPmDgwH59pVC7AvySiSkbibz

        # xpub:
        # print(bip32.serialize(self.client.get_public_node([]).node))
        # xpub661MyMwAqRbcF1zGijBb2K6x9YiJPh58xpcCeLvTxMX6spkY3PcpJ4ABcCyWfskq5DDxM3e6Ez5ePCqG5bnPUXR4wL8TZWyoDaUdiWW7bKy
        node = bip32.deserialize('xpub661MyMwAqRbcF1zGijBb2K6x9YiJPh58xpcCeLvTxMX6spkY3PcpJ4ABcCyWfskq5DDxM3e6Ez5ePCqG5bnPUXR4wL8TZWyoDaUdiWW7bKy')

        multisig = proto.MultisigRedeemScriptType(
            pubkeys=[
                proto.HDNodePathType(node=node, address_n=[1]),
                proto.HDNodePathType(node=node, address_n=[2]),
                proto.HDNodePathType(node=node, address_n=[3])
            ],
            signatures=[b'', b'', b''],
            m=2,
        )

        # Let's go to sign with key 10, which is NOT in pubkeys
        inp1 = proto.TxInputType(
            address_n=[10],
            prev_hash=TXHASH_c6091a,
            prev_index=1,
            script_type=proto.InputScriptType.SPENDMULTISIG,
            multisig=multisig,
        )

        out1 = proto.TxOutputType(
            address='12iyMbUb4R2K3gre4dHSrbu5azG5KaqVss',
            amount=100000,
            script_type=proto.OutputScriptType.PAYTOADDRESS
        )

        with pytest.raises(CallException) as exc:
            self.client.sign_tx('Bitcoin', [inp1, ], [out1, ])

        assert exc.value.args[0] == proto.FailureType.DataError
        assert exc.value.args[1].endswith('Pubkey not found in multisig script')
