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

from sros2.api.keystore import sign
from sros2.verb import VerbExtension
# from sros2.verb.keystore import NamespaceCompleter


class SignVerb(VerbExtension):
    """Sign keystore entry for given namespaces."""

    def add_arguments(self, parser, cli_name):
        """Add sign arguments."""
        arg = parser.add_argument(
            '-f', '--force',
            action='store_true',
            help='replace existing entry')
        arg = parser.add_argument(
            '-u', '--unsigned',
            action='store_true',
            help='path of policy config')
        arg = parser.add_argument(
            '-n', '--namespace',
            nargs='+',
            required=True,
            help='namespaces to create')
        # arg.completer = NamespaceCompleter()

    def main(self, *, args):
        """Call sign function."""
        success = sign(args)
        return 0 if success else 1
