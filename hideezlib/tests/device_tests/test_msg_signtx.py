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

from hideezlib import coins
from hideezlib import messages as proto
from hideezlib.client import CallException
from hideezlib.tools import parse_path

TxApiTestnet = coins.tx_api['Testnet']


TXHASH_157041 = unhexlify('1570416eb4302cf52979afd5e6909e37d8fdd874301f7cc87e547e509cb1caa6')
TXHASH_39a29e = unhexlify('39a29e954977662ab3879c66fb251ef753e0912223a83d1dcb009111d28265e5')
TXHASH_4a7b7e = unhexlify('4a7b7e0403ae5607e473949cfa03f09f2cd8b0f404bf99ce10b7303d86280bf7')
TXHASH_54aa56 = unhexlify('54aa5680dea781f45ebb536e53dffc526d68c0eb5c00547e323b2c32382dfba3')
TXHASH_58497a = unhexlify('58497a7757224d1ff1941488d23087071103e5bf855f4c1c44e5c8d9d82ca46e')
TXHASH_6f90f3 = unhexlify('6f90f3c7cbec2258b0971056ef3fe34128dbde30daa9c0639a898f9977299d54')
TXHASH_c63e24 = unhexlify('c63e24ed820c5851b60c54613fbc4bcb37df6cd49b4c96143e99580a472f79fb')
TXHASH_c6be22 = unhexlify('c6be22d34946593bcad1d2b013e12f74159e69574ffea21581dad115572e031c')
TXHASH_d5f65e = unhexlify('d5f65ee80147b4bcc70b75e4bbf2d7382021b871bd8867ef8fa525ef50864882')
TXHASH_d6da21 = unhexlify('d6da21677d7cca5f42fbc7631d062c9ae918a0254f7c6c22de8e8cb7fd5b8236')
TXHASH_d2dcda = unhexlify('d2dcdaf547ea7f57a713c607f15e883ddc4a98167ee2c43ed953c53cb5153e24')
TXHASH_e5040e = unhexlify('e5040e1bc1ae7667ffb9e5248e90b2fb93cd9150234151ce90e14ab2f5933bcd')
TXHASH_50f6f1 = unhexlify('50f6f1209ca92d7359564be803cb2c932cde7d370f7cee50fd1fad6790f6206d')


class TestMsgSigntx(HideezTest):
    def test_one_one_fee(self):
        self.setup_mnemonic_nopin_nopassphrase()

        # tx: d5f65ee80147b4bcc70b75e4bbf2d7382021b871bd8867ef8fa525ef50864882
        # input 0: 0.0039 BTC

        inp1 = proto.TxInputType(
            address_n=[0],  # 14LmW5k4ssUrtbAB4255zdqv3b4w1TuX9e
            # amount=390000,
            prev_hash=TXHASH_d5f65e,
            prev_index=0,
        )

        out1 = proto.TxOutputType(
            address='1MJ2tj2ThBE62zXbBYA5ZaN3fdve5CPAz1',
            amount=390000 - 10000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=TXHASH_d5f65e)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_d5f65e)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_d5f65e)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_d5f65e)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])

            (signatures, serialized_tx) = self.client.sign_tx('Bitcoin', [inp1, ], [out1, ])

        # Accepted by network: tx fd79435246dee76b2f159d2db08032d666c95adc544de64c8c49f474df4a7fee
        assert hexlify(serialized_tx) == b'010000000182488650ef25a58fef6788bd71b8212038d7f2bbe4750bc7bcb44701e85ef6d5000000006b4830450221009f1572bd4715486f1a3c1c0972a112f62976baba85dcb218663737704789677e02207ad85ba1571b3438ff5223a5e7b4c77cfd3492bc86c123e3a4afd2980a864eca012103bb20b056809acb091b3e3d1833681cb80f7b5f09bd9c5a229f5ff00edfcdee11ffffffff0160cc0500000000001976a914de9b2a8da088824e8fe51debea566617d851537888ac00000000'

    def test_testnet_one_two_fee(self):
        self.setup_mnemonic_allallall()
        # see 87be0736f202f7c2bff0781b42bad3e0cdcb54761939da69ea793a3735552c56

        # tx: e5040e1bc1ae7667ffb9e5248e90b2fb93cd9150234151ce90e14ab2f5933bcd
        # input 0: 0.31 BTC
        inp1 = proto.TxInputType(
            address_n=parse_path("44'/1'/0'/0/0"),
            # amount=31000000,
            prev_hash=TXHASH_e5040e,
            prev_index=0,
        )

        out1 = proto.TxOutputType(
            address='msj42CCGruhRsFrGATiUuh25dtxYtnpbTx',
            amount=30090000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        out2 = proto.TxOutputType(
            address_n=parse_path("44'/1'/0'/1/0"),
            amount=900000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        with self.client:
            self.client.set_tx_api(TxApiTestnet)
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=TXHASH_e5040e)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_e5040e)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_e5040e)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_e5040e)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures, serialized_tx) = self.client.sign_tx('Testnet', [inp1, ], [out1, out2])
        assert hexlify(serialized_tx) == b'0100000001cd3b93f5b24ae190ce5141235091cd93fbb2908e24e5b9ff6776aec11b0e04e5000000006a47304402201f8085db0c9f3f0b783818d6f13d44be13156934598b9c549d3085e4fef008550220375cb0e34bfa68273b6c4f25f10954b61c31e0d377b6dcac1c2b3925c0cd6e4b012103bdee2a7f093263ff63132b1d98bb9ebedca6d406b4f8e96ea80c3ba0d88bfc2effffffff021023cb01000000001976a91485eb47fe98f349065d6f044e27a4ac541af79ee288aca0bb0d00000000001976a9146f9f5ad2de144fffdcd3901f0ab4be195fd94dfe88ac00000000'

    def test_testnet_fee_too_high(self):
        self.setup_mnemonic_nopin_nopassphrase()

        # tx: 6f90f3c7cbec2258b0971056ef3fe34128dbde30daa9c0639a898f9977299d54
        # input 1: 10.00000000 BTC
        inp1 = proto.TxInputType(
            address_n=[0],  # mirio8q3gtv7fhdnmb3TpZ4EuafdzSs7zL
            # amount=1000000000,
            prev_hash=TXHASH_6f90f3,
            prev_index=1,
        )

        out1 = proto.TxOutputType(
            address='mfiGQVPcRcaEvQPYDErR34DcCovtxYvUUV',
            amount=1000000000 - 500000000 - 100000000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        out2 = proto.TxOutputType(
            address_n=[2],
            amount=500000000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        with self.client:
            self.client.set_tx_api(TxApiTestnet)
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=TXHASH_6f90f3)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_6f90f3)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_6f90f3)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_6f90f3)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_6f90f3)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures, serialized_tx) = self.client.sign_tx('Testnet', [inp1, ], [out1, out2])

        assert hexlify(serialized_tx) == b'0100000001549d2977998f899a63c0a9da30dedb2841e33fef561097b05822eccbc7f3906f010000006a4730440220331520a7402c31ba66de545ad79ccbc5a942166c3d5464c94edc1626230f067e02200fff6eddf1f8671eeca28ff726db3ed5175fd5a171dad06adac47a946ea9cfe1012103bb20b056809acb091b3e3d1833681cb80f7b5f09bd9c5a229f5ff00edfcdee11ffffffff020084d717000000001976a9140223b1a09138753c9cb0baf95a0a62c82711567a88ac0065cd1d000000001976a91455ee2725795b074cfaf4d930349e4586997a3ce788ac00000000'

    def test_one_two_fee(self):
        self.setup_mnemonic_allallall()

        # tx: c275c333fd1b36bef4af316226c66a8b3693fbfcc081a5e16a2ae5fcb09e92bf

        inp1 = proto.TxInputType(
            address_n=parse_path("m/44'/0'/0'/0/5"),  # 1GA9u9TfCG7SWmKCveBumdA1TZpfom6ZdJ
            # amount=50000,
            prev_hash=TXHASH_50f6f1,
            prev_index=1,
        )

        out1 = proto.TxOutputType(
            address_n=parse_path("m/44'/0'/0'/1/3"),  # 1EcL6AyfQTyWKGvXwNSfsWoYnD3whzVFdu
            amount=30000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        out2 = proto.TxOutputType(
            address='1Up15Msx4sbvUCGm8Xgo2Zp5FQim3wE59',
            amount=10000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=TXHASH_50f6f1)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_50f6f1)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_50f6f1)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_50f6f1)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures, serialized_tx) = self.client.sign_tx('Bitcoin', [inp1, ], [out1, out2])

        assert hexlify(serialized_tx) == b'01000000016d20f69067ad1ffd50ee7c0f377dde2c932ccb03e84b5659732da99c20f1f650010000006b4830450221008e6db24ec151b5ec48c1d3debc2711fa16e81ef9099656cc36a32bd422d014a002201d43c9abbc7cfe97de4cfaddf2e2f0e00036d4318b2ce209b76f5da97934def6012102468c20b64031a8b993b8c4d9a8552abaa30f2d25d9cf4b5832f54f16369bc62bffffffff0230750000000000001976a9143d87d23258532aab5a482583c156782f1b035c3188ac10270000000000001976a91405427736705cfbfaff76b1cff48283707fb1037088ac00000000'

    def test_one_three_fee(self):
        self.setup_mnemonic_nopin_nopassphrase()

        # tx: d5f65ee80147b4bcc70b75e4bbf2d7382021b871bd8867ef8fa525ef50864882
        # input 0: 0.0039 BTC

        inp1 = proto.TxInputType(
            address_n=[0],  # 14LmW5k4ssUrtbAB4255zdqv3b4w1TuX9e
            # amount=390000,
            prev_hash=TXHASH_d5f65e,
            prev_index=0,
        )

        out1 = proto.TxOutputType(
            address='1MJ2tj2ThBE62zXbBYA5ZaN3fdve5CPAz1',
            amount=390000 - 80000 - 12000 - 10000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        out2 = proto.TxOutputType(
            address='13uaUYn6XAooo88QvAqAVsiVvr2mAXutqP',
            amount=12000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        out3 = proto.TxOutputType(
            address_n=[1],
            amount=80000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=TXHASH_d5f65e)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_d5f65e)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_d5f65e)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_d5f65e)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=2)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=2)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=2)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures, serialized_tx) = self.client.sign_tx('Bitcoin', [inp1, ], [out1, out2, out3])

        assert hexlify(serialized_tx) == b'010000000182488650ef25a58fef6788bd71b8212038d7f2bbe4750bc7bcb44701e85ef6d5000000006b483045022100e6c93013e7b7ab9c3145ea08c812bf200be842bfa4faec3bc6b8ec140442627b0220158cf9d32b358a94d31cb2a66248198c58043f2b32f201484202fccf7c819342012103bb20b056809acb091b3e3d1833681cb80f7b5f09bd9c5a229f5ff00edfcdee11ffffffff0300650400000000001976a914de9b2a8da088824e8fe51debea566617d851537888ace02e0000000000001976a9141fe1d337fb81afca42818051e12fd18245d1b17288ac80380100000000001976a914f29c4e4678b08b6fb05c73e8e8fabd89daed60a488ac00000000'

    def test_two_two(self):
        self.setup_mnemonic_nopin_nopassphrase()

        # tx: c6be22d34946593bcad1d2b013e12f74159e69574ffea21581dad115572e031c
        # input 1: 0.0010 BTC
        # tx: 58497a7757224d1ff1941488d23087071103e5bf855f4c1c44e5c8d9d82ca46e
        # input 1: 0.0011 BTC

        inp1 = proto.TxInputType(
            address_n=[1],  # 1CK7SJdcb8z9HuvVft3D91HLpLC6KSsGb
            # amount=100000,
            prev_hash=TXHASH_c6be22,
            prev_index=1,
        )

        inp2 = proto.TxInputType(
            address_n=[2],  # 15AeAhtNJNKyowK8qPHwgpXkhsokzLtUpG
            # amount=110000,
            prev_hash=TXHASH_58497a,
            prev_index=1,
        )

        out1 = proto.TxOutputType(
            address='15Jvu3nZNP7u2ipw2533Q9VVgEu2Lu9F2B',
            amount=210000 - 100000 - 10000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        out2 = proto.TxOutputType(
            address_n=[3],  # 1CmzyJp9w3NafXMSEFH4SLYUPAVCSUrrJ5
            amount=100000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=TXHASH_c6be22)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_c6be22)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_c6be22)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_c6be22)),

                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=TXHASH_58497a)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_58497a)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_58497a)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_58497a)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
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
            ])
            (signatures, serialized_tx) = self.client.sign_tx('Bitcoin', [inp1, inp2], [out1, out2])

        # Accepted by network: tx c63e24ed820c5851b60c54613fbc4bcb37df6cd49b4c96143e99580a472f79fb
        assert hexlify(serialized_tx) == b'01000000021c032e5715d1da8115a2fe4f57699e15742fe113b0d2d1ca3b594649d322bec6010000006b483045022100f6d1d813d7bb141f001b3b9a990f15ddf7044561352fe2e6949634d7731609ba0220233139b8adb153b589cc6901d8b5b6cdf4e014294a5ef3769da9849249585725012103912a8f07b60de8f0b2800f1088f9b016059219cc63beeb4bf26e1bd5e7da5319ffffffff6ea42cd8d9c8e5441c4c5f85bfe50311078730d2881494f11f4d2257777a4958010000006b483045022100a31c3b72041fccd2301b70c647c66f669b100d90ee505b9d0c8aafe6d53cc2a602207933c16ee4cdbb1a2f9f43f55d14b9a7173b5c306ce16426dd90be6d6c77770a01210309b80e44b9ee837a2ef8e839cce1d6bb7c1408646143fb9b59569f39669e3049ffffffff02a0860100000000001976a9142f4490d5263906e4887ca2996b9e207af3e7824088aca0860100000000001976a9147d4306427f382ee93b9af6bdf6ba466f2323d91788ac00000000'

    def test_lots_of_outputs(self):
        self.setup_mnemonic_nopin_nopassphrase()

        # Tests if device implements serialization of len(outputs) correctly

        # tx: c63e24ed820c5851b60c54613fbc4bcb37df6cd49b4c96143e99580a472f79fb
        # index 1: 0.0010 BTC
        # tx: 39a29e954977662ab3879c66fb251ef753e0912223a83d1dcb009111d28265e5
        # index 1: 0.0254 BTC

        inp1 = proto.TxInputType(
            address_n=[3],  # 1CmzyJp9w3NafXMSEFH4SLYUPAVCSUrrJ5
            # amount=100000,
            prev_hash=TXHASH_c63e24,
            prev_index=1,
        )

        inp2 = proto.TxInputType(
            address_n=[3],  # 1CmzyJp9w3NafXMSEFH4SLYUPAVCSUrrJ5
            # amount=2540000,
            prev_hash=TXHASH_39a29e,
            prev_index=1,
        )

        outputs = []
        cnt = 255
        for _ in range(cnt):
            out = proto.TxOutputType(
                address='1NwN6UduuVkJi6sw3gSiKZaCY5rHgVXC2h',
                amount=(100000 + 2540000 - 39000) // cnt,
                script_type=proto.OutputScriptType.PAYTOADDRESS,
            )
            outputs.append(out)

        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=TXHASH_c63e24)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_c63e24)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_c63e24)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_c63e24)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_c63e24)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=TXHASH_39a29e)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_39a29e)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_39a29e)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_39a29e)),
            ] + [
                item for items in zip(
                    [proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=I)) for I in range(cnt)],
                ) for item in items
            ] + [
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=1)),
            ] + [
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=I)) for I in range(cnt)
            ] + [
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=1)),
            ] + [
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=I)) for I in range(cnt)
            ] + [
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=I)) for I in range(cnt)
            ] + [
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures, serialized_tx) = self.client.sign_tx('Bitcoin', [inp1, inp2], outputs)

        if cnt == 255:
            assert hexlify(serialized_tx) == b'0100000002fb792f470a58993e14964c9bd46cdf37cb4bbc3f61540cb651580c82ed243ec6010000006b483045022100bec18c499fa86c31a875a39720283d759bd1d7181cb0166668cfe2016c4d036a022056175983b9981bac404a83e5d974c1c42c4b645c14d5440a81652b1c2ae8fc5701210262f6426d6942332874d20899b44c136b0b56c66b876de9658a97182ad1cafc79ffffffffe56582d2119100cb1d3da8232291e053f71e25fb669c87b32a667749959ea239010000006a47304402200bfd72daf2a6ef400f85b7bae718855e4bc9a7e446a33181a2b7975d806447c30220009a3c08de32ecf90aea6fd0623cc6efd61cae4e00485dbd93298d4c134f2a6201210262f6426d6942332874d20899b44c136b0b56c66b876de9658a97182ad1cafc79fffffffffdff00' + b'd8270000000000001976a914f0a2b64e56ee2ff57126232f84af6e3a41d4055088ac' * cnt + b'00000000'

    def test_fee_too_high(self):
        self.setup_mnemonic_nopin_nopassphrase()

        # tx: 1570416eb4302cf52979afd5e6909e37d8fdd874301f7cc87e547e509cb1caa6
        # input 0: 1.0 BTC

        inp1 = proto.TxInputType(
            address_n=[0],  # 1HWDaLTpTCTtRWyWqZkzWx1wex5NKyncLW
            # amount=100000000,
            prev_hash=TXHASH_157041,
            prev_index=0,
        )

        out1 = proto.TxOutputType(
            address='1MJ2tj2ThBE62zXbBYA5ZaN3fdve5CPAz1',
            amount=100000000 - 510000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=TXHASH_157041)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_157041)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_157041)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_157041)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures, serialized_tx) = self.client.sign_tx('Bitcoin', [inp1, ], [out1, ])

        assert hexlify(serialized_tx) == b'0100000001a6cab19c507e547ec87c1f3074d8fdd8379e90e6d5af7929f52c30b46e417015000000006b483045022100ca9cbb454280a2b87b7f5830446df4fccb6d0be5b3bed61ff6e01c68e59d57230220358222216ec4d1904f2e78b2bc8b220f5bcb77999cb272c8d163481430e88c34012103bb20b056809acb091b3e3d1833681cb80f7b5f09bd9c5a229f5ff00edfcdee11ffffffff01d018ee05000000001976a914de9b2a8da088824e8fe51debea566617d851537888ac00000000'

    def test_not_enough_funds(self):
        self.setup_mnemonic_nopin_nopassphrase()

        # tx: d5f65ee80147b4bcc70b75e4bbf2d7382021b871bd8867ef8fa525ef50864882
        # input 0: 0.0039 BTC

        inp1 = proto.TxInputType(
            address_n=[0],  # 14LmW5k4ssUrtbAB4255zdqv3b4w1TuX9e
            # amount=390000,
            prev_hash=TXHASH_d5f65e,
            prev_index=0,
        )

        out1 = proto.TxOutputType(
            address='1MJ2tj2ThBE62zXbBYA5ZaN3fdve5CPAz1',
            amount=400000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=TXHASH_d5f65e)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_d5f65e)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_d5f65e)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_d5f65e)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.Failure(code=proto.FailureType.NotEnoughFunds)
            ])

            with pytest.raises(CallException) as exc:
                self.client.sign_tx('Bitcoin', [inp1, ], [out1, ])
            assert exc.value.args[0] == proto.FailureType.NotEnoughFunds

    def test_p2sh(self):
        self.setup_mnemonic_nopin_nopassphrase()

        inp1 = proto.TxInputType(
            address_n=[0],  # 14LmW5k4ssUrtbAB4255zdqv3b4w1TuX9e
            # amount=400000,
            prev_hash=TXHASH_54aa56,
            prev_index=1,
        )

        out1 = proto.TxOutputType(
            address='3DKGE1pvPpBAgZj94MbCinwmksewUNNYVR',  # p2sh
            amount=400000 - 10000,
            script_type=proto.OutputScriptType.PAYTOSCRIPTHASH,
        )

        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=TXHASH_54aa56)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_54aa56)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_54aa56)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_54aa56)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures, serialized_tx) = self.client.sign_tx('Bitcoin', [inp1, ], [out1, ])

        # Accepted by network: tx 8cc1f4adf7224ce855cf535a5104594a0004cb3b640d6714fdb00b9128832dd5
        assert hexlify(serialized_tx) == b'0100000001a3fb2d38322c3b327e54005cebc0686d52fcdf536e53bb5ef481a7de8056aa54010000006b4830450221008147eed3a11d062e02dedc4157f49206cbe0584482b148be00194aa9cd9c681e0220626a5be7f286018cb4edf7b025fe53b9478b4716535e32d10138115e482d745c012103bb20b056809acb091b3e3d1833681cb80f7b5f09bd9c5a229f5ff00edfcdee11ffffffff0170f305000000000017a9147f844bdb0b8fd54b64e3d16c85dc1170f1ff97c18700000000'

    def test_attack_change_outputs(self):
        # This unit test attempts to modify data sent during ping-pong of streaming signing.
        # Because device is asking for human confirmation only during first pass (first input),
        # device must detect that data has been modified during other passes and fail to sign
        # such modified data (which has not been confirmed by the user).

        # Test firstly prepare normal transaction and send it to device. Then it send the same
        # transaction again, but change amount of output 1 during signing the second input.

        self.setup_mnemonic_nopin_nopassphrase()

        inp1 = proto.TxInputType(
            address_n=[1],  # 1CK7SJdcb8z9HuvVft3D91HLpLC6KSsGb
            # amount=100000,
            prev_hash=TXHASH_c6be22,
            prev_index=1,
        )

        inp2 = proto.TxInputType(
            address_n=[2],  # 15AeAhtNJNKyowK8qPHwgpXkhsokzLtUpG
            # amount=110000,
            prev_hash=TXHASH_58497a,
            prev_index=1,
        )

        out1 = proto.TxOutputType(
            address='15Jvu3nZNP7u2ipw2533Q9VVgEu2Lu9F2B',
            amount=210000 - 100000 - 10000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        out2 = proto.TxOutputType(
            address_n=[3],  # 1CmzyJp9w3NafXMSEFH4SLYUPAVCSUrrJ5
            amount=100000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        global run_attack
        run_attack = False

        def attack_processor(req, msg):
            global run_attack

            if req.details.tx_hash is not None:
                return msg

            if req.details.request_index != 1:
                return msg

            if req.request_type != proto.RequestType.TXOUTPUT:
                return msg

            if not run_attack:
                run_attack = True
                return msg

            msg.outputs[0].amount = 9999999  # Sign output with another amount
            return msg

        # Test if the transaction can be signed normally
        (_, serialized_tx) = self.client.sign_tx('Bitcoin', [inp1, inp2], [out1, out2])

        # Accepted by network: tx c63e24ed820c5851b60c54613fbc4bcb37df6cd49b4c96143e99580a472f79fb
        assert hexlify(serialized_tx) == b'01000000021c032e5715d1da8115a2fe4f57699e15742fe113b0d2d1ca3b594649d322bec6010000006b483045022100f6d1d813d7bb141f001b3b9a990f15ddf7044561352fe2e6949634d7731609ba0220233139b8adb153b589cc6901d8b5b6cdf4e014294a5ef3769da9849249585725012103912a8f07b60de8f0b2800f1088f9b016059219cc63beeb4bf26e1bd5e7da5319ffffffff6ea42cd8d9c8e5441c4c5f85bfe50311078730d2881494f11f4d2257777a4958010000006b483045022100a31c3b72041fccd2301b70c647c66f669b100d90ee505b9d0c8aafe6d53cc2a602207933c16ee4cdbb1a2f9f43f55d14b9a7173b5c306ce16426dd90be6d6c77770a01210309b80e44b9ee837a2ef8e839cce1d6bb7c1408646143fb9b59569f39669e3049ffffffff02a0860100000000001976a9142f4490d5263906e4887ca2996b9e207af3e7824088aca0860100000000001976a9147d4306427f382ee93b9af6bdf6ba466f2323d91788ac00000000'

        # Now run the attack, must trigger the exception
        with pytest.raises(CallException) as exc:
            self.client.sign_tx('Bitcoin', [inp1, inp2], [out1, out2], debug_processor=attack_processor)
        assert exc.value.args[0] in (proto.FailureType.ProcessError, proto.FailureType.DataError)
        assert exc.value.args[1].endswith('Transaction has changed during signing')

    def test_attack_change_input_address(self):
        # This unit test attempts to modify input address after the Trezor checked
        # that it matches the change output

        self.setup_mnemonic_allallall()
        self.client.set_tx_api(TxApiTestnet)

        inp1 = proto.TxInputType(
            address_n=parse_path("44'/1'/4'/0/0"),
            # moUJnmge8SRXuediK7bW6t4YfrPqbE6hD7
            prev_hash=TXHASH_d2dcda,
            prev_index=1,
            script_type=proto.InputScriptType.SPENDADDRESS,
        )

        out1 = proto.TxOutputType(
            address='mwue7mokpBRAsJtHqEMcRPanYBmsSmYKvY',
            amount=100000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        out2 = proto.TxOutputType(
            address_n=parse_path("44'/1'/12345'/1/0"),
            amount=123400000 - 5000 - 100000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        global run_attack
        run_attack = True

        def attack_processor(req, msg):
            global run_attack

            if req.details.tx_hash is not None:
                return msg

            if req.request_type != proto.RequestType.TXINPUT:
                return msg

            if req.details.request_index != 0:
                return msg

            if not run_attack:
                return msg

            msg.inputs[0].address_n[2] = 12345 + 0x80000000
            run_attack = False
            return msg

        # Test if the transaction can be signed normally
        (_, serialized_tx) = self.client.sign_tx('Testnet', [inp1], [out1, out2])

        assert hexlify(serialized_tx) == b'0100000001243e15b53cc553d93ec4e27e16984adc3d885ef107c613a7577fea47f5dadcd2010000006a473044022047e2866fc234c6cb1e21c0bf4de3d83d0cfffd4a349519622c181764a782f45802201746a7edc34eeb88ffa86d2623c87fcf37a538414f144980c2e97fb8b0cb7548012102fd9783d73e9acaf32dabeafdd2caec6240c55605c4d9448e667bd56d4f4f3810ffffffff02a0860100000000001976a914b3cc67f3349974d0f1b50e9bb5dfdf226f888fa088ac18555907000000001976a914c90424273ef74a86fc45fd56c2230d577946700888ac00000000'

        # Now run the attack, must trigger the exception
        with self.client:
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=TXHASH_d2dcda)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_d2dcda)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_d2dcda)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_d2dcda)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.Failure(code=proto.FailureType.ProcessError),
            ])
            # Now run the attack, must trigger the exception
            with pytest.raises(CallException) as exc:
                self.client.sign_tx('Testnet', [inp1], [out1, out2], debug_processor=attack_processor)

            assert exc.value.args[0] == proto.FailureType.ProcessError
            #assert exc.value.args[1].endswith('Transaction has changed during signing')
            assert exc.value.args[1].endswith('Failed to compile input')

    def test_spend_coinbase(self):
        # 25 TEST generated to m/1 (mfiGQVPcRcaEvQPYDErR34DcCovtxYvUUV)
        # tx: d6da21677d7cca5f42fbc7631d062c9ae918a0254f7c6c22de8e8cb7fd5b8236
        # input 0: 25.0027823 BTC

        self.setup_mnemonic_nopin_nopassphrase()

        inp1 = proto.TxInputType(
            address_n=[1],  # mfiGQVPcRcaEvQPYDErR34DcCovtxYvUUV
            # amount=390000,
            prev_hash=TXHASH_d6da21,
            prev_index=0,
        )

        out1 = proto.TxOutputType(
            address='mm6FM31rM5Vc3sw5D7kztiBg3jHUzyqF1g',
            amount=2500278230 - 10000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        with self.client:
            self.client.set_tx_api(TxApiTestnet)
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=TXHASH_d6da21)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_d6da21)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_d6da21)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])
            (signatures, serialized_tx) = self.client.sign_tx('Testnet', [inp1, ], [out1, ])

        # Accepted by network: tx
        assert hexlify(serialized_tx) == b'010000000136825bfdb78c8ede226c7c4f25a018e99a2c061d63c7fb425fca7c7d6721dad6000000006b483045022100a75b25bad8229ac5552ea16f01c14194bef10662b85abb05a29a600eeeeddac002204e8e80a83b19e78dcb809ef3ffb39c1de14dbf1d5095f74c09115ac5ae3ae80d012103912a8f07b60de8f0b2800f1088f9b016059219cc63beeb4bf26e1bd5e7da5319ffffffff01c6100795000000001976a9143d2496e67f5f57a924353da42d4725b318e7a8ea88ac00000000'

    def test_two_changes(self):
        self.setup_mnemonic_allallall()
        # see 87be0736f202f7c2bff0781b42bad3e0cdcb54761939da69ea793a3735552c56

        # tx: e5040e1bc1ae7667ffb9e5248e90b2fb93cd9150234151ce90e14ab2f5933bcd
        # input 0: 0.31 BTC
        inp1 = proto.TxInputType(
            address_n=parse_path("44'/1'/0'/0/0"),
            # amount=31000000,
            prev_hash=TXHASH_e5040e,
            prev_index=0,
        )

        out1 = proto.TxOutputType(
            address='msj42CCGruhRsFrGATiUuh25dtxYtnpbTx',
            amount=30090000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        out_change1 = proto.TxOutputType(
            address_n=parse_path("44'/1'/0'/1/0"),
            amount=900000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        out_change2 = proto.TxOutputType(
            address_n=parse_path("44'/1'/0'/1/1"),
            amount=10000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        with self.client:
            self.client.set_tx_api(TxApiTestnet)
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=TXHASH_e5040e)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_e5040e)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_e5040e)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_e5040e)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=2)),

                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=2)),

                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=2)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])

            self.client.sign_tx('Testnet', [inp1, ], [out1, out_change1, out_change2])

    def test_change_on_main_chain_allowed(self):
        self.setup_mnemonic_allallall()
        # see 87be0736f202f7c2bff0781b42bad3e0cdcb54761939da69ea793a3735552c56

        # tx: e5040e1bc1ae7667ffb9e5248e90b2fb93cd9150234151ce90e14ab2f5933bcd
        # input 0: 0.31 BTC
        inp1 = proto.TxInputType(
            address_n=parse_path("44'/1'/0'/0/0"),
            # amount=31000000,
            prev_hash=TXHASH_e5040e,
            prev_index=0,
        )

        out1 = proto.TxOutputType(
            address='msj42CCGruhRsFrGATiUuh25dtxYtnpbTx',
            amount=30090000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        # change on main chain is allowed => treated as a change
        out_change = proto.TxOutputType(
            address_n=parse_path("44'/1'/0'/0/0"),
            amount=900000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        with self.client:
            self.client.set_tx_api(TxApiTestnet)
            self.client.set_expected_responses([
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXMETA, details=proto.TxRequestDetailsType(tx_hash=TXHASH_e5040e)),
                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_e5040e)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0, tx_hash=TXHASH_e5040e)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1, tx_hash=TXHASH_e5040e)),

                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),

                proto.TxRequest(request_type=proto.RequestType.TXINPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),

                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=0)),
                proto.TxRequest(request_type=proto.RequestType.TXOUTPUT, details=proto.TxRequestDetailsType(request_index=1)),
                proto.TxRequest(request_type=proto.RequestType.TXFINISHED),
            ])

            self.client.sign_tx('Testnet', [inp1, ], [out1, out_change])
