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

from .conftest import setup_client
import hideezlib.messages as m


@setup_client()
@pytest.mark.parametrize("message", [
    m.Ping(message="hello", button_protection=True),
    m.GetAddress(
        address_n=[0],
        coin_name="Bitcoin",
        script_type=m.InputScriptType.SPENDADDRESS,
        show_display=True
    ),
])
@pytest.mark.skip
def test_cancel_message(client, message):
    resp = client.call_raw(message)

    client.transport.write(m.Cancel())

    resp = client.transport.read()

    assert isinstance(resp, m.Failure)
    assert resp.code == m.FailureType.ActionCancelled
