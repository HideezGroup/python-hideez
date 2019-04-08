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


@pytest.mark.skip
class TestMsgClearsession(HideezTest):

    def test_clearsession(self):
        self.setup_mnemonic_nopin_passphrase()
        self.client.set_passphrase('passphrase')

        with self.client:
            self.client.set_expected_responses([proto.PassphraseRequest(), proto.PassphraseStateRequest(), proto.Address()])
            res = self.client.get_address('Bitcoin', [])
            assert res == '15fiTDFwZd2kauHYYseifGi9daH2wniDHH'

        with self.client:
            # passphrase are cached
            self.client.set_expected_responses([proto.Address()])
            res = self.client.get_address('Bitcoin', [])
            assert res == '15fiTDFwZd2kauHYYseifGi9daH2wniDHH'

        self.client.clear_session()

        # session cache is cleared
        with self.client:
            self.client.set_expected_responses([proto.PassphraseRequest(), proto.PassphraseStateRequest(), proto.Address()])
            res = self.client.get_address('Bitcoin', [])
            assert res == '15fiTDFwZd2kauHYYseifGi9daH2wniDHH'

        with self.client:
            # pin and passphrase are cached
            self.client.set_expected_responses([proto.Address()])
            res = self.client.get_address('Bitcoin', [])
            assert res == '15fiTDFwZd2kauHYYseifGi9daH2wniDHH'
