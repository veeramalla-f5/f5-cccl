"""Provides a class for managing BIG-IP Virtual Address resources."""
# coding=utf-8
#
# Copyright (c) 2017,2018, F5 Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from copy import deepcopy
import logging

from f5_cccl.resource import Resource
from f5_cccl.utils.route_domain import normalize_address_with_route_domain


LOGGER = logging.getLogger(__name__)


class VirtualAddress(Resource):
    """VirtualAddress class for managing configuration on BIG-IP."""

    properties = dict(address=None,
                      autoDelete="false",
                      enabled=None,
                      description=None,
                      trafficGroup="/Common/traffic-group-1")

    def __init__(self, name, partition, default_route_domain, **properties):
        """Create a VirtualAddress instance."""
        super(VirtualAddress, self).__init__(name, partition, **properties)

        for key, value in list(self.properties.items()):
            self._data[key] = properties.get(key, value)
        if self._data['address'] is not None:
            self._data['address'] = normalize_address_with_route_domain(
                self._data['address'], default_route_domain)[0]

    def __eq__(self, other):
        if not isinstance(other, VirtualAddress):
            return False

        for key in self._data:
            if isinstance(self._data[key], list):
                if sorted(self._data[key]) != \
                        sorted(other.data.get(key, list())):
                    return False
                continue

            if self._data[key] != other.data.get(key):
                return False

        return True

    def _uri_path(self, bigip):
        return bigip.tm.ltm.virtual_address_s.virtual_address

    def update(self, bigip, data=None, modify=False):
        # 'address' is immutable, don't pass it in an update operation
        tmp_data = deepcopy(data) if data is not None else deepcopy(self.data)
        tmp_data.pop('address', None)
        super(VirtualAddress, self).update(bigip, data=tmp_data, modify=modify)


class IcrVirtualAddress(VirtualAddress):
    """Filter the iControl REST input to create the canonical representation"""
    pass


class ApiVirtualAddress(VirtualAddress):
    """Filter the CCCL API input to create the canonical representation"""
    pass
