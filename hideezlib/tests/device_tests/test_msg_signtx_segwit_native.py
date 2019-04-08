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
from ..support.ckd_public import deserialize
from hideezlib import coins
from hideezlib import messages as proto
from hideezlib.tools import parse_path

TxApiTestnet = coins.tx_api['Testnet']


class TestMsgSigntxSegwitNative(HideezTest):

    def test_send_p2sh(self):
        self.setup_mnemonic_allallall()
        self.client.set_tx_api(TxApiTestnet)
        inp1 = proto.TxInputType(
            address_n=parse_path("49'/1'/0'/1/0"),
            # 2N1LGaGg836mqSQqiuUBLfcyGBhyZbremDX
            amount=123456789,
            prev_hash=unhexlify('20912f98ea3ed849042efed0fdac8cb4fc301961c5988cba56902d8ffb61c337'),
            prev_index=0,
            script_type=proto.InputScriptType.SPENDP2SHWITNESS,
        )
        out1 = proto.TxOutputType(
            address='tb1qqzv60m9ajw8drqulta4ld4gfx0rdh82un5s65s',
            amount=12300000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )
        out2 = proto.TxOutputType(
            address='2N1LGaGg836mqSQqiuUBLfcyGBhyZbremDX',
            script_type=proto.OutputScriptType.PAYTOADDRESS,
            amount=123456789 - 11000 - 12300000,
        )
        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures, serialized_tx) = self.client.sign_tx('Testnet', [inp1], [out1, out2])

        assert hexlify(serialized_tx) == b'0100000000010137c361fb8f2d9056ba8c98c5611930fcb48cacfdd0fe2e0449d83eea982f91200000000017160014824fb1037552b4bd2bb84d7f13c5a2aa4b2ab0d2ffffffff02e0aebb00000000001600140099a7ecbd938ed1839f5f6bf6d50933c6db9d5c3df39f060000000017a91458b53ea7f832e8f096e896b8713a8c6df0e892ca870247304402206625dab306dc21345b7efc382817e0825624d66d886b2fd5e47b52c33c88dc10022071da5b080e72e3424ff8b4dc358015200bae8d71569810e39a2ab773c3295993012103fea49c7079e5de753d11cd49ac47938cc95fcb1a40cb50ee41cce82e2283c51900000000'

    def test_send_p2sh_change(self):
        self.setup_mnemonic_allallall()
        self.client.set_tx_api(TxApiTestnet)
        inp1 = proto.TxInputType(
            address_n=parse_path("49'/1'/0'/1/0"),
            # 2N1LGaGg836mqSQqiuUBLfcyGBhyZbremDX
            amount=123456789,
            prev_hash=unhexlify('20912f98ea3ed849042efed0fdac8cb4fc301961c5988cba56902d8ffb61c337'),
            prev_index=0,
            script_type=proto.InputScriptType.SPENDP2SHWITNESS,
        )
        out1 = proto.TxOutputType(
            address='tb1qqzv60m9ajw8drqulta4ld4gfx0rdh82un5s65s',
            amount=12300000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )
        out2 = proto.TxOutputType(
            address_n=parse_path("49'/1'/0'/1/0"),
            script_type=proto.OutputScriptType.PAYTOP2SHWITNESS,
            amount=123456789 - 11000 - 12300000,
        )
        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures, serialized_tx) = self.client.sign_tx('Testnet', [inp1], [out1, out2])

        assert hexlify(serialized_tx) == b'0100000000010137c361fb8f2d9056ba8c98c5611930fcb48cacfdd0fe2e0449d83eea982f91200000000017160014824fb1037552b4bd2bb84d7f13c5a2aa4b2ab0d2ffffffff02e0aebb00000000001600140099a7ecbd938ed1839f5f6bf6d50933c6db9d5c3df39f060000000017a91451e29d52c5b62da357b34fdbec72b4a150a0fd398702483045022100d95d31aad21f2a5210a2a984e1d039fdb24d0b46ac404d40715222eb43a7364d022029709b28a15162c9f2042529c0b872fd91bf7fccb57481a65a6dbccbb4e65a55012103fea49c7079e5de753d11cd49ac47938cc95fcb1a40cb50ee41cce82e2283c51900000000'

    def test_send_native(self):
        self.setup_mnemonic_allallall()
        self.client.set_tx_api(TxApiTestnet)
        inp1 = proto.TxInputType(
            address_n=parse_path("49'/1'/0'/0/0"),
            # tb1qqzv60m9ajw8drqulta4ld4gfx0rdh82un5s65s
            amount=12300000,
            prev_hash=unhexlify('09144602765ce3dd8f4329445b20e3684e948709c5cdcaf12da3bb079c99448a'),
            prev_index=0,
            script_type=proto.InputScriptType.SPENDWITNESS,
        )
        out1 = proto.TxOutputType(
            address='2N4Q5FhU2497BryFfUgbqkAJE87aKHUhXMp',
            amount=5000000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )
        out2 = proto.TxOutputType(
            address='tb1q694ccp5qcc0udmfwgp692u2s2hjpq5h407urtu',
            script_type=proto.OutputScriptType.PAYTOADDRESS,
            amount=12300000 - 11000 - 5000000,
        )
        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures, serialized_tx) = self.client.sign_tx('Testnet', [inp1], [out1, out2])

        assert hexlify(serialized_tx) == b'010000000001018a44999c07bba32df1cacdc50987944e68e3205b4429438fdde35c76024614090000000000ffffffff02404b4c000000000017a9147a55d61848e77ca266e79a39bfc85c580a6426c987a8386f0000000000160014d16b8c0680c61fc6ed2e407455715055e41052f502483045022100cdff526cbb19c26e52d3ef0d43039c8662f4144bcbe9688a4bb88fcf0edf37d6022041347e1eabb5c14c7676282f56c6dd9d93c02de810cc59ba5156efdb19e0a2d1012102d96aa150a2a60cc2c2c640816567945289feaadd68abeec410386846cb14147a00000000'

    def test_send_native_change(self):
        self.setup_mnemonic_allallall()
        self.client.set_tx_api(TxApiTestnet)
        inp1 = proto.TxInputType(
            address_n=parse_path("49'/1'/0'/0/0"),
            # tb1qqzv60m9ajw8drqulta4ld4gfx0rdh82un5s65s
            amount=12300000,
            prev_hash=unhexlify('09144602765ce3dd8f4329445b20e3684e948709c5cdcaf12da3bb079c99448a'),
            prev_index=0,
            script_type=proto.InputScriptType.SPENDWITNESS,
        )
        out1 = proto.TxOutputType(
            address='2N4Q5FhU2497BryFfUgbqkAJE87aKHUhXMp',
            amount=5000000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )
        out2 = proto.TxOutputType(
            address_n=parse_path("49'/1'/0'/1/0"),
            script_type=proto.OutputScriptType.PAYTOWITNESS,
            amount=12300000 - 11000 - 5000000,
        )
        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures, serialized_tx) = self.client.sign_tx('Testnet', [inp1], [out1, out2])

        assert hexlify(serialized_tx) == b'010000000001018a44999c07bba32df1cacdc50987944e68e3205b4429438fdde35c76024614090000000000ffffffff02404b4c000000000017a9147a55d61848e77ca266e79a39bfc85c580a6426c987a8386f0000000000160014824fb1037552b4bd2bb84d7f13c5a2aa4b2ab0d202473044022059b0adc1b30f8abed085b75cbe3144c01e40fd2e2d2622cc01c3488c202e160002200383f27e478784c3e93d9dcab9b1781a274c103244f64f4c7f74ac1540a7ef61012102d96aa150a2a60cc2c2c640816567945289feaadd68abeec410386846cb14147a00000000'

    def test_send_both(self):
        self.setup_mnemonic_allallall()
        self.client.set_tx_api(TxApiTestnet)
        inp1 = proto.TxInputType(
            address_n=parse_path("49'/1'/0'/1/0"),
            # 2N1LGaGg836mqSQqiuUBLfcyGBhyZbremDX
            amount=111145789,
            prev_hash=unhexlify('09144602765ce3dd8f4329445b20e3684e948709c5cdcaf12da3bb079c99448a'),
            prev_index=1,
            script_type=proto.InputScriptType.SPENDP2SHWITNESS,
        )
        inp2 = proto.TxInputType(
            address_n=parse_path("49'/1'/0'/1/0"),
            # tb1q694ccp5qcc0udmfwgp692u2s2hjpq5h407urtu
            amount=7289000,
            prev_hash=unhexlify('65b811d3eca0fe6915d9f2d77c86c5a7f19bf66b1b1253c2c51cb4ae5f0c017b'),
            prev_index=1,
            script_type=proto.InputScriptType.SPENDWITNESS,
        )
        out1 = proto.TxOutputType(
            address='tb1q54un3q39sf7e7tlfq99d6ezys7qgc62a6rxllc',
            amount=12300000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )
        out2 = proto.TxOutputType(
            # address_n=parse_path("44'/1'/0'/0/0"),
            # script_type=proto.OutputScriptType.PAYTOP2SHWITNESS,
            address='2N6UeBoqYEEnybg4cReFYDammpsyDw8R2Mc',
            script_type=proto.OutputScriptType.PAYTOADDRESS,
            amount=45600000,
        )
        out3 = proto.TxOutputType(
            address='mvbu1Gdy8SUjTenqerxUaZyYjmveZvt33q',
            amount=111145789 + 7289000 - 11000 - 12300000 - 45600000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=2)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=2)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures, serialized_tx) = self.client.sign_tx('Testnet', [inp1, inp2], [out1, out2, out3])

        # 0e480a97c7a545c85e101a2f13c9af0e115d43734e1448f0cac3e55fe8e7399d
        assert hexlify(serialized_tx) == b'010000000001028a44999c07bba32df1cacdc50987944e68e3205b4429438fdde35c76024614090100000017160014824fb1037552b4bd2bb84d7f13c5a2aa4b2ab0d2ffffffff7b010c5faeb41cc5c253121b6bf69bf1a7c5867cd7f2d91569fea0ecd311b8650100000000ffffffff03e0aebb0000000000160014a579388225827d9f2fe9014add644487808c695d00cdb7020000000017a91491233e24a9bf8dbb19c1187ad876a9380c12e787870d859b03000000001976a914a579388225827d9f2fe9014add644487808c695d88ac024730440220685a8bd6321cdd279c811a87352ebe42720c0a723cbb9a2562cc88756a14a97802203c546b433d073df26244db4762c82ce12049e48fb9dcf7ecf9dec9c340b55cca012103fea49c7079e5de753d11cd49ac47938cc95fcb1a40cb50ee41cce82e2283c5190248304502210089ed4a2756995190534911c575f9e119cc8be00f5d13b84f43f654885961c7a402202c1e3997a53331d087eb1c9fa156cf6921c00244f80d1cb19453ac0907cb8d99012103fea49c7079e5de753d11cd49ac47938cc95fcb1a40cb50ee41cce82e2283c51900000000'

    def test_send_multisig_1(self):
        self.setup_mnemonic_allallall()
        self.client.set_tx_api(TxApiTestnet)
        nodes = [self.client.get_public_node(parse_path("999'/1'/%d'" % index)) for index in range(1, 4)]
        multisig = proto.MultisigRedeemScriptType(
            pubkeys=list(map(lambda n: proto.HDNodePathType(node=deserialize(n.xpub), address_n=[2, 0]), nodes)),
            signatures=[b'', b'', b''],
            m=2,
        )

        inp1 = proto.TxInputType(
            address_n=parse_path("999'/1'/1'/2/0"),
            prev_hash=unhexlify('9c31922be756c06d02167656465c8dc83bb553bf386a3f478ae65b5c021002be'),
            prev_index=1,
            script_type=proto.InputScriptType.SPENDP2SHWITNESS,
            multisig=multisig,
            amount=1610436
        )

        out1 = proto.TxOutputType(
            address='tb1qch62pf820spe9mlq49ns5uexfnl6jzcezp7d328fw58lj0rhlhasge9hzy',
            amount=1605000,
            script_type=proto.OutputScriptType.PAYTOADDRESS
        )

        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures1, _) = self.client.sign_tx('Testnet', [inp1], [out1])
            # store signature
            inp1.multisig.signatures[0] = signatures1[0]
            # sign with third key
            inp1.address_n[2] = 0x80000003
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures2, serialized_tx) = self.client.sign_tx('Testnet', [inp1], [out1])

        # f41cbedd8becee05a830f418d13aa665125464547db5c7a6cd28f21639fe1228
        assert hexlify(serialized_tx) == b'01000000000101be0210025c5be68a473f6a38bf53b53bc88d5c46567616026dc056e72b92319c0100000023220020832e06e5eede5e5c8e2af21b33bf5d4a953b95e7457c034f0bc1fb8028cc5b9bffffffff01887d180000000000220020c5f4a0a4ea7c0392efe0a9670a73264cffa90b19107cd8a8e9750ff93c77fdfb0400483045022100b4c59881e3e9491aa40a1d2bb4932e1fc7ffcc90c5150270e5ef2f95376c77c302203c9cf4b0ed841135aee07c84357b4e8550f14fad87c44b8ee58952acc177a82e0147304402204c100f179c99fab2a2f510652b717debfdeba5cd4a1dc22d3e7ab1b58902deda0220018bc0129026920c8757ba7de9a1c7fb50bd16d7ca5e22c6af75c31afe993cb60169522102cea51fb0aa19715665ac367725c4ea0bac2b7f3371df16e58c3538b788260fe12102cd496a185be36b20cf1400d296a221fd05bfc46adc04e7ba4ebd8f47f037ae682103caaabaa9876547cf014dcb93a73af348e32af5cbf29d436b9fa922232432f03153ae00000000'

    def test_send_multisig_2(self):
        self.setup_mnemonic_allallall()
        self.client.set_tx_api(TxApiTestnet)
        nodes = [self.client.get_public_node(parse_path("999'/1'/%d'" % index)) for index in range(1, 4)]
        multisig = proto.MultisigRedeemScriptType(
            pubkeys=list(map(lambda n: proto.HDNodePathType(node=deserialize(n.xpub), address_n=[2, 1]), nodes)),
            signatures=[b'', b'', b''],
            m=2,
        )

        inp1 = proto.TxInputType(
            address_n=parse_path("999'/1'/2'/2/1"),
            prev_hash=unhexlify('f41cbedd8becee05a830f418d13aa665125464547db5c7a6cd28f21639fe1228'),
            prev_index=0,
            script_type=proto.InputScriptType.SPENDWITNESS,
            multisig=multisig,
            amount=1605000
        )

        out1 = proto.TxOutputType(
            address='tb1qr6xa5v60zyt3ry9nmfew2fk5g9y3gerkjeu6xxdz7qga5kknz2ssld9z2z',
            amount=1604000,
            script_type=proto.OutputScriptType.PAYTOADDRESS
        )

        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures1, _) = self.client.sign_tx('Testnet', [inp1], [out1])
            # store signature
            inp1.multisig.signatures[1] = signatures1[0]
            # sign with first key
            inp1.address_n[2] = 0x80000001
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures2, serialized_tx) = self.client.sign_tx('Testnet', [inp1], [out1])

        # c9348040bbc2024e12dcb4a0b4806b0398646b91acf314da028c3f03dd0179fc
        assert hexlify(serialized_tx) == b'010000000001012812fe3916f228cda6c7b57d5464541265a63ad118f430a805eeec8bddbe1cf40000000000ffffffff01a0791800000000002200201e8dda334f11171190b3da72e526d441491464769679a319a2f011da5ad312a10400483045022100ed4a2a483f65888a1f3c705ce602d0a2d49e1de07c135fe3ffc1d434ed8df7cc02201fdfae3cab18cce2bb45b4951524e59c531a545d8d4130744724a1da747ffed60147304402202aa1ea471f5bf86cd817fa8def692afc93948604eb9d81b3e8f79a88e5cd313902201005f28a55f309021f86100c37e22f8f2aff72d11e6ebbb81e37e34faa22557d016952210344dedfd45a83764a830caa704e1d08e72a7fca35e05567bf1bc055381bf5ca3b21026a56ffbb409323325e6ad1da94793affc1fe7783579ed0bdb19361c723414a702103b6ef0db28a5bf481c4d89b3b48208765de1bee59351e86134c8c8167406101d153ae00000000'

    def test_send_multisig_3_change(self):
        self.setup_mnemonic_allallall()
        self.client.set_tx_api(TxApiTestnet)
        nodes = [self.client.get_public_node(parse_path("999'/1'/%d'" % index)) for index in range(1, 4)]
        multisig = proto.MultisigRedeemScriptType(
            pubkeys=list(map(lambda n: proto.HDNodePathType(node=deserialize(n.xpub), address_n=[2, 0]), nodes)),
            signatures=[b'', b'', b''],
            m=2,
        )
        multisig2 = proto.MultisigRedeemScriptType(
            pubkeys=list(map(lambda n: proto.HDNodePathType(node=deserialize(n.xpub), address_n=[1, 1]), nodes)),
            signatures=[b'', b'', b''],
            m=2,
        )

        inp1 = proto.TxInputType(
            address_n=parse_path("999'/1'/1'/2/0"),
            prev_hash=unhexlify('c9348040bbc2024e12dcb4a0b4806b0398646b91acf314da028c3f03dd0179fc'),
            prev_index=0,
            script_type=proto.InputScriptType.SPENDWITNESS,
            multisig=multisig,
            amount=1604000
        )

        out1 = proto.TxOutputType(
            address_n=parse_path("999'/1'/1'/1/1"),
            amount=1603000,
            multisig=multisig2,
            script_type=proto.OutputScriptType.PAYTOP2SHWITNESS
        )

        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures1, _) = self.client.sign_tx('Testnet', [inp1], [out1])
            # store signature
            inp1.multisig.signatures[0] = signatures1[0]
            # sign with third key
            inp1.address_n[2] = 0x80000003
            out1.address_n[2] = 0x80000003
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures2, serialized_tx) = self.client.sign_tx('Testnet', [inp1], [out1])

        # 31bc1c88ce6ae337a6b3057a16d5bad0b561ad1dfc047d0a7fbb8814668f91e5
        assert hexlify(serialized_tx) == b'01000000000101fc7901dd033f8c02da14f3ac916b6498036b80b4a0b4dc124e02c2bb408034c90000000000ffffffff01b87518000000000017a9149ac59a48a4403831984629e6cef243874295e25f8704004830450221008c02ac568cb1acabf7a1f2004bd20f2af0f624662199d962e7fdadf55448f8c3022073da0769479fe983dcca7317e2280cbdf3add9a4380e927b2c525faf689ae96701473044022067cbd98e86f22d2d6f4cd82926b28a51900a331aeb2c7b38c71ce2988e08af6102203c3cbf04944439bd898a16f3ca7526895329c3169cf9a81992242f23a79208a20169522102cea51fb0aa19715665ac367725c4ea0bac2b7f3371df16e58c3538b788260fe12102cd496a185be36b20cf1400d296a221fd05bfc46adc04e7ba4ebd8f47f037ae682103caaabaa9876547cf014dcb93a73af348e32af5cbf29d436b9fa922232432f03153ae00000000'

    def test_send_multisig_4_change(self):
        self.setup_mnemonic_allallall()
        self.client.set_tx_api(TxApiTestnet)
        nodes = [self.client.get_public_node(parse_path("999'/1'/%d'" % index)) for index in range(1, 4)]
        multisig = proto.MultisigRedeemScriptType(
            pubkeys=list(map(lambda n: proto.HDNodePathType(node=deserialize(n.xpub), address_n=[1, 1]), nodes)),
            signatures=[b'', b'', b''],
            m=2,
        )
        multisig2 = proto.MultisigRedeemScriptType(
            pubkeys=list(map(lambda n: proto.HDNodePathType(node=deserialize(n.xpub), address_n=[1, 2]), nodes)),
            signatures=[b'', b'', b''],
            m=2,
        )

        inp1 = proto.TxInputType(
            address_n=parse_path("999'/1'/1'/1/1"),
            prev_hash=unhexlify('31bc1c88ce6ae337a6b3057a16d5bad0b561ad1dfc047d0a7fbb8814668f91e5'),
            prev_index=0,
            script_type=proto.InputScriptType.SPENDP2SHWITNESS,
            multisig=multisig,
            amount=1603000
        )

        out1 = proto.TxOutputType(
            address_n=parse_path("999'/1'/1'/1/2"),
            amount=1602000,
            multisig=multisig2,
            script_type=proto.OutputScriptType.PAYTOWITNESS
        )

        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures1, _) = self.client.sign_tx('Testnet', [inp1], [out1])
            # store signature
            inp1.multisig.signatures[0] = signatures1[0]
            # sign with third key
            inp1.address_n[2] = 0x80000003
            out1.address_n[2] = 0x80000003
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures2, serialized_tx) = self.client.sign_tx('Testnet', [inp1], [out1])

        # c0bf56060a109624b4635222696d94a7d533cacea1b3f8245417a4348c045829
        assert hexlify(serialized_tx) == b'01000000000101e5918f661488bb7f0a7d04fc1dad61b5d0bad5167a05b3a637e36ace881cbc310000000023220020a4bd311ad9f0c99fd00dae2073c708f37999d4fb25bc8a39b9ccfbb43917c570ffffffff01d071180000000000220020041c9609b4d7003148fb714a8e2a1002fcf582cc2867d331e787d1658f0eee2e0400473044022033845a1a36f30acfda8bc29834bdb7b2ac6214968c749773ccef8fb097b3815c022060c7d56cf6e8d6f83ec3b3dfcf3e0bfecc9f3c9dba910ab27605763c3e2a53a101483045022100c44552abccdea92ae9af4bacf30788d78a9bd24729f1f3d8cef422f2a71ba89702200969d28cc9ea49bcb3113979b90050a44d0f41122fce5c4379da31bf66e6157f01695221022af8e5bbb3091ae655d64f2444776eb9bd4ab750dbbec1f50a8a779bef97e19821029d7f2e3cdcd413b7423a7f5ffbdce524c177e3bf995b4b9d2b50c291e661d4902102663d3ba942719a6ef3a25427c908e653fba13056388b989cdd912e82cd68baa253ae00000000'
