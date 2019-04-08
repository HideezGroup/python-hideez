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

import time
import pytest

from .common import HideezTest
from hideezlib import messages as proto
from hideezlib.client import PinException, CallException


@pytest.mark.skip
class TestProtectCall(HideezTest):

    def _some_protected_call(self, button, pin, passphrase):
        # This method perform any call which have protection in the device
        res = self.client.ping(
            'random data',
            button_protection=button,
            pin_protection=pin,
            passphrase_protection=passphrase
        )
        assert res == 'random data'

    def test_passphrase_protection(self):
        self.setup_mnemonic_nopin_passphrase()

        with self.client:
            self.client.set_expected_responses([proto.PassphraseRequest(), proto.PassphraseStateRequest(), proto.Success()])
            self._some_protected_call(False, True, True)
