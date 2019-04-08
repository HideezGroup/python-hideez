# This file is part of the Trezor project.
#
# Copyright (C) 2012-2018 SatoshiLabs and contributors
# Copyright (C) 2019      Drynode
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

import logging
import requests
import binascii
from io import BytesIO
import struct

from .. import mapping
from .. import protobuf
from . import Transport, TransportException


LOG = logging.getLogger(__name__)


BRIDGE_URI = 'http://127.0.0.1:21525'


def get_error(resp):
    return ' (error=%d str=%s)' % (resp.status_code, resp.text)


class BridgeTransport(Transport):
    '''
    BridgeTransport implements transport through Hideez Bridge.
    '''

    PATH_PREFIX = 'bridge'
    HEADERS = {'Origin': 'http://hideez.com'}
    URL_PREFIX = ''

    def __init__(self, device):
        super().__init__()

        self.device = device
        self.conn = requests.Session()
        self.session = None
        self.response = None

    def get_path(self):
        return '%s:%s' % (self.PATH_PREFIX, self.device['path'])

    @classmethod
    def enumerate(cls):
        try:
            req_url = '%s%s%s' % (BRIDGE_URI, cls.URL_PREFIX, '/enumerate')
            r = requests.post(req_url, headers=cls.HEADERS)
            if r.status_code != 200:
                raise TransportException('bridge: Could not enumerate '
                                         'devices' + get_error(r))
            return [BridgeTransport(dev) for dev in r.json()]
        except Exception as e:
            return []

    def open(self):
        req_url = '%s%s%s' % (BRIDGE_URI, self.URL_PREFIX, '/acquire/%s/null')
        r = self.conn.post(req_url % self.device['path'], headers=self.HEADERS)
        if r.status_code != 200:
            raise TransportException('bridge: Could not acquire '
                                     'session' + get_error(r))
        self.session = r.json()['session']

    def authenticate(self):
        LOG.debug('authenticate session: {}'.format(self.session))
        data = b'\0'*49
        data = binascii.hexlify(data).decode()
        req_url = '%s%s%s' % (BRIDGE_URI, self.URL_PREFIX, '/authenticate/%s')
        r = self.conn.post(req_url % self.session, data=data,
                           headers=self.HEADERS)
        if r.status_code != 200:
            raise TransportException('bridge: Could not '
                                     'authenticate' + get_error(r))
        self.response = r.text

    def close(self):
        if not self.session:
            return
        req_url = '%s%s%s' % (BRIDGE_URI, self.URL_PREFIX, '/release/%s')
        r = self.conn.post(req_url % self.session, headers=self.HEADERS)
        if r.status_code != 200:
            raise TransportException('bridge: Could not release '
                                     'session' + get_error(r))
        self.session = None

    def write(self, msg, nowait=False):
        LOG.debug('sending message: {}'.format(msg.__class__.__name__),
                  extra={'protobuf': msg})
        data = BytesIO()
        protobuf.dump_message(data, msg)
        ser = data.getvalue()
        header = struct.pack('>HL', mapping.get_type(msg), len(ser))
        data = binascii.hexlify(header + ser).decode()
        method = 'post' if nowait else 'call'
        req_url = '%s%s%s' % (BRIDGE_URI, self.URL_PREFIX, '/%s/%s')
        LOG.debug('call %s with data:\n%s' %
              (req_url % (method, self.session), data))
        r = self.conn.post(req_url % (method, self.session),
                           data=data, headers=self.HEADERS)
        if r.status_code != 200:
            raise TransportException('bridge: Could not write '
                                     'message' + get_error(r))
        self.response = r.text

    def read(self):
        if self.response is None:
            raise TransportException('No response stored')
        data = binascii.unhexlify(self.response)
        LOG.debug('read response from bridge:\n%s' % self.response)
        headerlen = struct.calcsize('>HL')
        (msg_type, datalen) = struct.unpack('>HL', data[:headerlen])
        LOG.debug('msg_type %s, datalen %s' % (msg_type, datalen))
        data = BytesIO(data[headerlen:headerlen + datalen])
        msg = protobuf.load_message(data, mapping.get_class(msg_type))
        LOG.debug('received message: {}'.format(msg.__class__.__name__),
                  extra={'protobuf': msg})
        self.response = None
        return msg

    def debug_wipe(self):
        LOG.debug('wiping device')
        req_url = '%s%s%s' % (BRIDGE_URI, self.URL_PREFIX, '/debug/wipe/%s')
        r = self.conn.post(req_url % self.session, data='',
                           headers=self.HEADERS)
        if r.status_code != 200:
            raise TransportException('bridge: Could not run '
                                     'debug_wipe' + get_error(r))

    def debug_load(self, mnemonic):
        LOG.debug('loading device')
        req_url = '%s%s%s' % (BRIDGE_URI, self.URL_PREFIX,
                              '/debug/mnemonic/%s')
        data = '["%s"]' % '", "'.join(mnemonic.split())
        r = self.conn.post(req_url % self.session, data=data,
                           headers=self.HEADERS)
        if r.status_code != 200:
            raise TransportException('bridge: Could not run '
                                     'debug_load' + get_error(r))


TRANSPORT = BridgeTransport
