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


class TestMsgGetpublickey(HideezTest):

    def test_btc(self):
        self.setup_mnemonic_nopin_nopassphrase()
        assert bip32.serialize(self.client.get_public_node([]).node, 0x0488B21E) == 'xpub661MyMwAqRbcFW3NvPPCXr3RKSnks2UPNj543xvx3zKaWMTDH7rifpbTxgRbeavHFgke9vrfGZSb16ePwqWpguRYquYo8QtNRKcnVnPdmMp'
        assert self.client.get_public_node([], coin_name='Bitcoin').xpub == 'xpub661MyMwAqRbcFW3NvPPCXr3RKSnks2UPNj543xvx3zKaWMTDH7rifpbTxgRbeavHFgke9vrfGZSb16ePwqWpguRYquYo8QtNRKcnVnPdmMp'
        assert bip32.serialize(self.client.get_public_node([1]).node, 0x0488B21E) == 'xpub68Xmq6cbjD4BsFkMTBytapu9bvPmWdMvHYJA7UcWFzZc3eqTnap5gSreg4u62geiXJ2epgyeTwsvgZnyjnguxiEBes6BKmtpeAcNGAeEBvM'
        assert self.client.get_public_node([1], coin_name='Bitcoin').xpub == 'xpub68Xmq6cbjD4BsFkMTBytapu9bvPmWdMvHYJA7UcWFzZc3eqTnap5gSreg4u62geiXJ2epgyeTwsvgZnyjnguxiEBes6BKmtpeAcNGAeEBvM'
        assert bip32.serialize(self.client.get_public_node([0, -1]).node, 0x0488B21E) == 'xpub6A3HTryvyCCrRu4vmKdb1yRW12BVFHRWz4jrPrt262KxzfRGHDAMJTDJYn6MwHtFTgALobQ6jNDybC4wEpGABBgb1SbBGsrtb72TUVsioAZ'
        assert self.client.get_public_node([0, -1], coin_name='Bitcoin').xpub == 'xpub6A3HTryvyCCrRu4vmKdb1yRW12BVFHRWz4jrPrt262KxzfRGHDAMJTDJYn6MwHtFTgALobQ6jNDybC4wEpGABBgb1SbBGsrtb72TUVsioAZ'
        assert bip32.serialize(self.client.get_public_node([-9, 0]).node, 0x0488B21E) == 'xpub6AfNwrqseeg4U5ctU3PNRDfxjQ5ZopJRsiR9mRSgCeioBWzt4U39Uk35MSaQZzW3r5ZgBW2hBWtH9fUPoHKxqXtpuNqARs1bftToCyJGzsH'
        assert self.client.get_public_node([-9, 0], coin_name='Bitcoin').xpub == 'xpub6AfNwrqseeg4U5ctU3PNRDfxjQ5ZopJRsiR9mRSgCeioBWzt4U39Uk35MSaQZzW3r5ZgBW2hBWtH9fUPoHKxqXtpuNqARs1bftToCyJGzsH'
        assert bip32.serialize(self.client.get_public_node([0, 9999999]).node, 0x0488B21E) == 'xpub6A3HTrynfnJQpQ5uateMRhiLyr23qRtgZMn12maur2ztLGoZFFJp4ESTdciD3QLrkCaCXvVu7tBkZBzrYTocwhkjmvaR1H4U38MskQy5kSd'
        assert self.client.get_public_node([0, 9999999], coin_name='Bitcoin').xpub == 'xpub6A3HTrynfnJQpQ5uateMRhiLyr23qRtgZMn12maur2ztLGoZFFJp4ESTdciD3QLrkCaCXvVu7tBkZBzrYTocwhkjmvaR1H4U38MskQy5kSd'

    def test_ltc(self):
        self.setup_mnemonic_nopin_nopassphrase()
        assert bip32.serialize(self.client.get_public_node([]).node, 0x019DA462) == 'Ltub2SSUS19CirucVsKKWsPCPi9eQF7KcozXW1H2t3g4RVAHEj61w8MTVU5uKYwdJzKXquADk4FD7b5y7C1WrjcGXqCy93SFo6eQupP8QM5VAmQ'
        assert self.client.get_public_node([], coin_name='Litecoin').xpub == 'Ltub2SSUS19CirucVsKKWsPCPi9eQF7KcozXW1H2t3g4RVAHEj61w8MTVU5uKYwdJzKXquADk4FD7b5y7C1WrjcGXqCy93SFo6eQupP8QM5VAmQ'
        assert bip32.serialize(self.client.get_public_node([1]).node, 0x019DA462) == 'Ltub2UxtHjpdceNC7d2J3fytSh1NgiiLGQt4QpW8wZMcdVQJn2UGSbJpW6M62wR7h63y7WSEQpNCJyXJnfA6egnMoe1bwzydzTes8fNiAigaQWa'
        assert self.client.get_public_node([1], coin_name='Litecoin').xpub == 'Ltub2UxtHjpdceNC7d2J3fytSh1NgiiLGQt4QpW8wZMcdVQJn2UGSbJpW6M62wR7h63y7WSEQpNCJyXJnfA6egnMoe1bwzydzTes8fNiAigaQWa'
        assert bip32.serialize(self.client.get_public_node([0, -1]).node, 0x019DA462) == 'Ltub2WUPvWBxrdWrgGLsModasqXj5pW414wf7LwqDwd8TXAfj344wDf686hjuecPbhHW3tZvPineaPsMhHS49iMc27U1JaUdwZcw5bnoP6Hki98'
        assert self.client.get_public_node([0, -1], coin_name='Litecoin').xpub == 'Ltub2WUPvWBxrdWrgGLsModasqXj5pW414wf7LwqDwd8TXAfj344wDf686hjuecPbhHW3tZvPineaPsMhHS49iMc27U1JaUdwZcw5bnoP6Hki98'
        assert bip32.serialize(self.client.get_public_node([-9, 0]).node, 0x019DA462) == 'Ltub2X6VQW3uY5z4iStq4XPNH5nBpCQ8ZbpZzzd8bWBna9ZVutdgiUXtJPXWiK6SEPuJSHyFmdRF2YXfFkqWiBRQgTgFCWid6YmeAPE97VVYLMG'
        assert self.client.get_public_node([-9, 0], coin_name='Litecoin').xpub == 'Ltub2X6VQW3uY5z4iStq4XPNH5nBpCQ8ZbpZzzd8bWBna9ZVutdgiUXtJPXWiK6SEPuJSHyFmdRF2YXfFkqWiBRQgTgFCWid6YmeAPE97VVYLMG'
        assert bip32.serialize(self.client.get_public_node([0, 9999999]).node, 0x019DA462) == 'Ltub2WUPvWBpZDcR4mMrBNeMHZpa4eLcbDQpgdyyrrL2DXqb4eSMuFoYssvtzVEEhok7LQyn83tSxuq8fHMyTMu4ndYA54TsfxpWXd8DezaQ8yC'
        assert self.client.get_public_node([0, 9999999], coin_name='Litecoin').xpub == 'Ltub2WUPvWBpZDcR4mMrBNeMHZpa4eLcbDQpgdyyrrL2DXqb4eSMuFoYssvtzVEEhok7LQyn83tSxuq8fHMyTMu4ndYA54TsfxpWXd8DezaQ8yC'

    def test_tbtc(self):
        self.setup_mnemonic_nopin_nopassphrase()
        assert bip32.serialize(self.client.get_public_node([111, 42]).node, 0x043587CF) == 'tpubDAK5uDbv7PmdJji3veAHET9R2hNtiswU6QYqozDrdCi9mrUQB3ML3Vjwnanr8VJ58je6QHqeJF196ZDxAE25dyShZWdzePGG8waZRj8ggvn'
        assert self.client.get_public_node([111, 42], coin_name='Testnet').xpub == 'tpubDAK5uDbv7PmdJji3veAHET9R2hNtiswU6QYqozDrdCi9mrUQB3ML3Vjwnanr8VJ58je6QHqeJF196ZDxAE25dyShZWdzePGG8waZRj8ggvn'
