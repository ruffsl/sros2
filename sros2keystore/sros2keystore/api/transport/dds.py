# Copyright 2016-2017 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""DDS Transport API."""

from .common import TransportInterface


class DdsTransportInterface(TransportInterface):
    """Transport interface for keystore archive."""

    def __init__(self, config):
        """Initlise interface from config dict."""
        super().__init__()

    def init(self, config):
        """Initlise archive from config dict."""
        pass

    def build(self, config):
        """Initlise archive from config dict."""
        pass
