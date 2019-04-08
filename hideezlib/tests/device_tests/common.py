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

import os

from . import conftest

from hideezlib import coins
from hideezlib import tx_api
from hideezlib.client import DebugHideezClient

tests_dir = os.path.dirname(os.path.abspath(__file__))
tx_api.cache_dir = os.path.join(tests_dir, '../txcache')


class HideezTest:

    def setup_method(self, method):
        wirelink = conftest.get_device()
        self.client = DebugHideezClient(wirelink)
        self.client.set_tx_api(coins.tx_api['Bitcoin'])

        #                     1      2     3    4      5      6      7     8      9    10    11    12
        self.mnemonic12 = 'alcohol woman abuse must during monitor noble actual mixed trade anger aisle'
        self.mnemonic18 = 'owner little vague addict embark decide pink prosper true fork panda embody mixture exchange choose canoe electric jewel'
        self.mnemonic24 = 'dignity pass list indicate nasty swamp pool script soccer toe leaf photo multiply desk host tomato cradle drill spread actor shine dismiss champion exotic'
        self.mnemonic_all = ' '.join(['all'] * 23 + ['magic'])

        self.pin4 = '1010'
        self.pin6 = '100100'

        self.client.debug_wipe()
        self.client.transport.session_begin()

    def teardown_method(self, method):
        self.client.transport.session_end()
        self.client.close()

    def setup_mnemonic_allallall(self):
        self.client.debug_load(mnemonic=self.mnemonic_all, pin='', passphrase_protection=False, label='test', language='english')

    def setup_mnemonic_nopin_nopassphrase(self):
        self.client.debug_load(mnemonic=self.mnemonic24, pin='', passphrase_protection=False, label='test', language='english')

    def setup_mnemonic_nopin_passphrase(self):
        self.client.debug_load(mnemonic=self.mnemonic24, pin='', passphrase_protection=True, label='test', language='english')

    def setup_mnemonic_pin_nopassphrase(self):
        self.client.debug_load(mnemonic=self.mnemonic24, pin=self.pin4, passphrase_protection=False, label='test', language='english')

    def setup_mnemonic_pin_passphrase(self):
        self.client.debug_load(mnemonic=self.mnemonic24, pin=self.pin4, passphrase_protection=True, label='test', language='english')


def generate_entropy(strength, internal_entropy, external_entropy):
    '''
    strength - length of produced seed. Currently 256 bit
    random - binary stream of random data from external HRNG
    '''
    import hashlib

    if strength not in (256, ):
        raise ValueError("Invalid strength")

    if not internal_entropy:
        raise ValueError("Internal entropy is not provided")

    if len(internal_entropy) < 32:
        raise ValueError("Internal entropy too short")

    if not external_entropy:
        raise ValueError("External entropy is not provided")

    if len(external_entropy) < 32:
        raise ValueError("External entropy too short")

    entropy = hashlib.sha256(internal_entropy + external_entropy).digest()
    entropy_stripped = entropy[:strength // 8]

    if len(entropy_stripped) * 8 != strength:
        raise ValueError("Entropy length mismatch")

    return entropy_stripped
