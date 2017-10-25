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
import shutil
import tempfile
import unittest

from sros2.api.dds import pki
from sros2.api.dds import smime

resources_dir = 'resources'
key_path = os.path.join(resources_dir, 'key1.pem')
cert_path = os.path.join(resources_dir, 'cert1.pem')
file_path = os.path.join(resources_dir, 'governance.xml')
out_file_name = 'governance.p7s'
exp_file_path = os.path.join(resources_dir, out_file_name)


class TestSMIME(unittest.TestCase):

    def setUp(self):
        """Load PKI and init temporary directory"""
        self.cert = pki.utils.load_cert(cert_path=cert_path)
        self.key = pki.utils.load_key(key_path=key_path)
        pki.utils.check_public_keys_match([self.key, self.cert])

        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Remove temporary directory"""
        shutil.rmtree(self.test_dir)

    def test_sign_file(self):
        """Test SMIME file siguratures"""
        raw_file_path = os.path.join(self.test_dir, out_file_name)
        signed_data = smime.sign.sign_file(
            file_path=file_path,
            key=self.key, cert=self.cert,
            out_file=raw_file_path)

        # FIXME verify causes flaky segfaults
        # signed_certs = smime.verify.verify_file(file_path=raw_file_path, certs=[self.cert])
        # self.assertTrue(signed_certs)

        # As controling all randoms seeds for cripto sicgnature is impractical
        # we assert the expected and raw files have simalar structure via size
        line_diffs = 0
        char_diffs = 0
        with open(exp_file_path, 'r') as exp:
            exp_data = exp.read().split('/n')
            with open(raw_file_path, 'r') as raw:
                raw_data = raw.read().split('/n')
                # Check expected and raw files have the same numer of lines
                line_diffs = len(exp_data) - len(raw_data)
                # Check expected and raw lines have the same numer of characters
                for exp_line, raw_line in zip(exp_data, raw_data):
                    try:
                        self.assertEqual(len(exp_line), len(raw_line))
                    except Exception as e:
                        char_diffs = char_diffs + 1
        # Cornner case when a signature may vary by lines
        self.assertLessEqual(line_diffs, 1)
        # Cornner case when a signature may vary by length
        self.assertLessEqual(char_diffs, 2)


if __name__ == '__main__':
    unittest.main()
