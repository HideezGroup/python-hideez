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

import time
from hideezlib import messages as proto


@pytest.mark.skip
class TestMsgApplysettings(HideezTest):

    def test_apply_settings(self):
        self.setup_mnemonic_pin_passphrase()
        assert self.client.features.label == 'test'

        with self.client:
            self.client.set_expected_responses([proto.Success(),
                                                proto.Features()])
            self.client.apply_settings(label='new label')

        assert self.client.features.label == 'new label'

    def test_apply_settings_passphrase(self):
        self.setup_mnemonic_pin_nopassphrase()

        assert self.client.features.passphrase_protection is False

        with self.client:
            self.client.set_expected_responses([proto.Success(),
                                                proto.Features()])
            self.client.apply_settings(use_passphrase=True)

        assert self.client.features.passphrase_protection is True

        with self.client:
            self.client.set_expected_responses([proto.Success(),
                                                proto.Features()])
            self.client.apply_settings(use_passphrase=False)

        assert self.client.features.passphrase_protection is False

        with self.client:
            self.client.set_expected_responses([proto.Success(),
                                                proto.Features()])
            self.client.apply_settings(use_passphrase=True)

        assert self.client.features.passphrase_protection is True
