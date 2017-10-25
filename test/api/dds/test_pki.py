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

import os
import unittest

from sros2.api.dds import pki

resources_dir = 'resources'
key_path = os.path.join(resources_dir, 'key.pem')
key2_path = os.path.join(resources_dir, 'key2.pem')
cert_path = os.path.join(resources_dir, 'cert.pem')
cert2_path = os.path.join(resources_dir, 'cert2.pem')


class TestPKI(unittest.TestCase):

    def _test_load_key(self, path):
        key = pki.utils.load_key(key_path=path)
        key_dump = pki.utils._dump_key(key=key)
        with open(path, 'rb') as fd:
            self.assertEqual(key_dump, fd.read())
        return key

    def _test_load_cert(self, path):
        cert = pki.utils.load_cert(cert_path=path)
        cert_dump = pki.utils._dump_cert(cert=cert)
        with open(path, 'rb') as fd:
            self.assertEqual(cert_dump, fd.read())
        return cert

    def test_check_public_keys_match(self):
        key = self._test_load_key(key_path)
        key2 = self._test_load_key(key2_path)
        cert = self._test_load_cert(cert_path)
        cert2 = self._test_load_cert(cert2_path)
        self.assertTrue(pki.utils.check_public_keys_match([key, cert]))
        self.assertTrue(pki.utils.check_public_keys_match([key2, cert2]))
        self.assertFalse(pki.utils.check_public_keys_match([key, cert2]))
        self.assertFalse(pki.utils.check_public_keys_match([key2, cert]))


if __name__ == '__main__':
    unittest.main()
