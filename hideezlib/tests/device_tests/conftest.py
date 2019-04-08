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

import functools
import os
import pytest

from hideezlib.transport import get_transport
from hideezlib.client import DebugHideezClient
from hideezlib import log, coins


def get_device():
    path = os.environ.get('HIDEEZ_PATH')
    return get_transport(path)


@pytest.fixture(scope="function")
def client():
    wirelink = get_device()
    client = DebugHideezClient(wirelink)
    client.set_tx_api(coins.tx_api['Bitcoin'])
    client.debug_wipe()
    client.transport.session_begin()

    yield client

    client.transport.session_end()


def setup_client(mnemonic=None, pin='', passphrase=False):
    if mnemonic is None:
        mnemonic = ' '.join(['all'] * 23 + ['magic'])

    def client_decorator(function):
        @functools.wraps(function)
        def wrapper(client, *args, **kwargs):
            client.debug_load(mnemonic=mnemonic, pin=pin, passphrase_protection=passphrase, label='test', language='english')
            return function(client, *args, **kwargs)
        return wrapper

    return client_decorator


def pytest_configure(config):
    if config.getoption('verbose'):
        log.enable_debug_output()


def pytest_addoption(parser):
    parser.addini("run_xfail", "List of markers that will run even if marked as xfail", "args", [])


def pytest_runtest_setup(item):
    """
    Called for each test item (class, individual tests).

    Performs custom processing, mainly useful for trezor CI testing:
    * allows to 'runxfail' tests specified by 'run_xfail' in pytest.ini
    """
    xfail = item.get_marker("xfail")
    run_xfail = any(item.get_marker(marker) for marker in item.config.getini("run_xfail"))
    if xfail and run_xfail:
        # Deep hack: pytest's private _evalxfail helper determines whether the test should xfail or not.
        # The helper caches its result even before this hook runs.
        # Here we force-set the result to False, meaning "test does NOT xfail, run as normal"
        # IOW, this is basically per-item "--runxfail"
        item._evalxfail.result = False
