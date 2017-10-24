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
from sros2.api.dds import smime


key_path = 'resources/key.pem'
cert_path = 'resources/cert.pem'
file_path = "resources/governance.xml"
out_file = "resources/governance.p7s"


class TestSIME(unittest.TestCase):

    def test_sign_file(self):
        cert = pki.utils.load_cert(cert_path=cert_path)
        key = pki.utils.load_key(key_path=key_path)
        pki.utils.check_public_keys_match([key, cert])

        signed_data = smime.sign.sign_file(file_path=file_path,
                                           key=key, cert=cert, out_file=out_file)

        print(signed_data)

        signed_certs = smime.verify.verify_file(file_path=out_file, certs=[cert])

        print(signed_certs)

        # with open(out_file, 'rb') as fd:
        #     self.assertEqual(signed_data, fd.read())


if __name__ == '__main__':
    unittest.main()
