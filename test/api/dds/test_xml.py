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

from sros2.api.dds import xml

resources_dir = 'resources'
governance_name = 'governance.xml'
governance_path = os.path.join(resources_dir, governance_name)
permissions_name = 'permissions.xml'
permissions_path = os.path.join(resources_dir, permissions_name)


class TestXML(unittest.TestCase):
    """Test XML API."""

    def setUp(self):
        """Create temporary directory."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Remove temporary directory."""
        shutil.rmtree(self.test_dir)

    def _test_load_governance(self, path):
        """Test load governance XML."""
        governance = xml.governance.parse(inFileName=path, silence=True)

        outfile = os.path.join(self.test_dir, governance_name)
        with open(outfile, 'w') as raw:
            raw.write("""<?xml version="1.0" encoding="UTF-8"?>\n""")
            governance.export(outfile=raw, level=0, name_='dds')

        with open(path, 'r') as exp:
            exp_data = exp.read()
        with open(outfile, 'r') as raw:
            raw_data = raw.read()
        self.assertEqual(exp_data, raw_data)
        return governance

    def _test_load_permissions(self, path):
        """Test load permissions XML."""
        permissions = xml.permissions.parse(inFileName=path, silence=True)

        outfile = os.path.join(self.test_dir, permissions_name)
        with open(outfile, 'w') as raw:
            raw.write("""<?xml version="1.0" encoding="UTF-8"?>\n""")
            permissions.export(outfile=raw, level=0, name_='dds')

        with open(path, 'r') as exp:
            exp_data = exp.read()
        with open(outfile, 'r') as raw:
            raw_data = raw.read()
        self.assertEqual(exp_data, raw_data)
        return permissions

    def test_governance(self):
        """Test governance API."""
        governance = self._test_load_governance(governance_path)
        permissions = self._test_load_permissions(permissions_path)


if __name__ == '__main__':
    unittest.main()
