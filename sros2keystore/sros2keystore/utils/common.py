
# Copyright 2014 Open Source Robotics Foundation, Inc.
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


def mkdir_p(path):
    """Equivalent to UNIX mkdir -p ."""
    if os.path.exists(path):
        return
    else:
        return os.makedirs(path, exist_ok=True)


def getcwd(symlinks=True):
    """Get the current working directory.

    :param symlinks: If True, then get the path considering symlinks. If false,
    resolve the path to the actual path.
    :type symlinks: bool
    :returns: the current working directory
    :rtype: str
    """
    cwd = ''

    # Get the real path
    realpath = os.getcwd()

    # The `PWD` environment variable should contain the path that we took to
    # get here, includng symlinks
    if symlinks:
        cwd = os.environ.get('PWD', '')

    # Fallback on `getcwd` if the `PWD` variable is wrong
    if not cwd or not os.path.exists(cwd) or os.path.realpath(cwd) != realpath:
        cwd = realpath

    return cwd
