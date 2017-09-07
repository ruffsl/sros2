#!/usr/bin/env python3

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

import subprocess
import pkg_resources
import os

governance_xsd = pkg_resources.resource_filename(
    'sros2.resources.dds.security', 'governance.xsd')
permissions_xsd = pkg_resources.resource_filename(
    'sros2.resources.dds.security', 'permissions.xsd')
api_dir = pkg_resources.resource_filename(
    'sros2.api.dds', 'security')


def generateDS(outFilename, subclassFilename, xschemaFileName):
    cmd = ['generateDS',
           '-f',  # Force overwrite of output files.
           '--no-dates',  # Do not include the current date.
           '--no-versions',
           '-o', outFilename,
           '-s', subclassFilename,
           xschemaFileName]
    print('cmd:\n', cmd)
    subprocess.call(cmd)


for xschemaFile in [governance_xsd, permissions_xsd]:
    xschemaFileName = xschemaFile
    outFilename = os.path.join(api_dir, os.path.splitext(
        os.path.basename(xschemaFile))[0] + '.py')
    subclassFilename = os.path.join(api_dir, os.path.splitext(
        os.path.basename(xschemaFile))[0] + '_sub' + '.py')

    generateDS(outFilename, subclassFilename, xschemaFileName)
