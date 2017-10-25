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

# This autogenerates the necessary xml parsing api from dds secureity .xsd files

import subprocess
import pkg_resources
import os

source_lib = 'sros2keystore.resources.dds.xml'
target_lib = 'sros2keystore.api.dds.xml'

governance_xsd = pkg_resources.resource_filename(
    source_lib, 'governance.xsd')
permissions_xsd = pkg_resources.resource_filename(
    source_lib, 'permissions.xsd')
api_dir = pkg_resources.resource_filename(
    target_lib, '')


def generateDS(outFilename, subclassFilename, xschemaFileName, superModule):
    cmd = ['generateDS',
           '-f',  # Force overwrite of output files.
           '--no-dates',  # Do not include the current date.
           '--no-versions',
           '--super={}'.format(superModule),
           '-o', outFilename,
           '-s', subclassFilename,
           xschemaFileName]
    print('cmd:\n', cmd)
    subprocess.call(cmd)


for xschemaFilePath in [governance_xsd, permissions_xsd]:
    xschemaFile = os.path.basename(xschemaFilePath)
    xschema = os.path.splitext(xschemaFile)[0]
    xschemaFileName = xschemaFilePath
    outFilename = os.path.join(api_dir, xschema + '.py')
    subclassFilename = os.path.join(api_dir, xschema + '_sub' + '.py')
    superModule = target_lib + '.' + xschema

    generateDS(outFilename, subclassFilename, xschemaFileName, superModule)
