# Copyright 2017 Open Source Robotics Foundation, Inc.
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

import unittest

from sros2.api.dds import pki


key_path = 'resources/key.pem'
cert_path = 'resources/cert.pem'
file_path = "resources/governance.xml"
out_file = "resources/governance.p7s"


class TestPKI(unittest.TestCase):

    def test_load_key(self):
        key = pki.utils.load_key(key_path=key_path)
        key_dump = pki.utils._dump_key(key=key)
        with open(key_path, 'rb') as fd:
            self.assertEqual(key_dump, fd.read())

    def test_load_cert(self):
        cert = pki.utils.load_cert(cert_path=cert_path)
        cert_dump = pki.utils._dump_cert(cert=cert)
        with open(cert_path, 'rb') as fd:
            self.assertEqual(cert_dump, fd.read())


if __name__ == '__main__':
    unittest.main()
