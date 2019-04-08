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

from hideezlib import messages as proto


class TestMsgPing(HideezTest):

    def test_ping(self):
        self.setup_mnemonic_nopin_nopassphrase()

        with self.client:
            self.client.set_expected_responses([proto.Success()])
            res = self.client.ping('random data')
            assert res == 'random data'

    def test_ping_button_protect(self):
        self.setup_mnemonic_nopin_nopassphrase()

        with self.client:
            self.client.set_expected_responses([proto.Success()])
            res = self.client.ping('random data', button_protection=True)
            assert res == 'random data'


    @pytest.mark.skip
    def test_ping_passphrase_protect(self):
        self.setup_mnemonic_nopin_nopassphrase()
        with self.client:
            self.client.set_expected_responses([proto.Success()])
            res = self.client.ping('random data', passphrase_protection=True)
            assert res == 'random data'
