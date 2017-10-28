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
"""This module implements a class for representing a keystore workspace context."""

import os
import re
import sys

from . import metadata

from .common import getcwd
# from .common import printed_fill
# from .common import remove_ansi_escape
# from .common import terminal_width

from .metadata import find_enclosing_workspace

# from .resultspace import get_resultspace_environment

# from .terminal_color import ColorMapper

# color_mapper = ColorMapper()
# clr = color_mapper.clr


class Context(object):
    """Encapsulates a catkin workspace's settings which affect build results.

    This class will validate some of the settings on assignment using the
    filesystem, but it will never modify the filesystem. For instance, it will
    raise an exception if the source space does not exist, but it will not
    create a folder for the build space if it does not already exist.
    This context can be locked, so that changing the members is prevented.
    """

    DEFAULT_INSTALL_SPACE = 'install'
    DEFAULT_LOG_SPACE = 'log'
    DEFAULT_PARTICIPANT_SPACE = 'participant'
    DEFAULT_PRIVATE_SPACE = 'private'
    DEFAULT_PUBLIC_SPACE = 'public'
    DEFAULT_SHARE_SPACE = 'share'

    STORED_KEYS = [
        'extend_path',
        'source_space',
        'log_space',
        'build_space',
        'devel_space',
        'install_space',
        'devel_layout',
        'install',
        'isolate_install',
        'cmake_args',
        'make_args',
        'jobs_args',
        'use_internal_make_jobserver',
        'use_env_cache',
        'catkin_make_args',
        'whitelist',
        'blacklist',
    ]

    KEYS = STORED_KEYS + [
        'workspace',
        'profile',
        'space_suffix',
    ]

    @classmethod
    def load(
        cls,
        workspace_hint=None,
        profile=None,
        opts=None,
        strict=False,
        append=False,
        remove=False,
        load_env=True
    ):
        """Load a context from a given workspace and profile with optional modifications.

        This function will try to load a given context from the specified
        workspace with the following resolution strategy:
         - existing workspace enclosing given workspace path
         - existing workspace enclosing "."
         - given workspace path
         - "."
        If a workspace cannot be found, it will assume that the user is
        specifying a new workspace, unless `strict=True` is given. In this
        latter case, this function will return None.
        :param workspace_hint: The hint used to find a workspace (see description for more details)
        :type workspace_hint: str
        :param profile: The profile to load the context from, if the profile is None, the active profile is used
        :type profile: str
        :param opts: An argparse options namespace containing context keys to override stored context keys
        :type opts: namespace
        :param strict: Causes this function to return None if a workspace isn't found
        :type strict: bool
        :param append: Appends any list-type opts to existing opts
        :type append: bool
        :param remove: Removes any list-type opts from existing opts
        :type remove: bool
        :param load_env: Control whether the context loads the resultspace
        environment for the full build context
        :type load_env: bool
        :returns: A potentially valid Context object constructed from the given arguments
        :rtype: Context
        """
        # Initialize dictionary version of opts namespace
        opts_vars = vars(opts) if opts else {}

        # Get the workspace (either the given directory or the enclosing ws)
        workspace_hint = workspace_hint or opts_vars.get('workspace', None) or getcwd()
        workspace = find_enclosing_workspace(workspace_hint)
        if not workspace:
            if strict or not workspace_hint:
                return None
            else:
                workspace = workspace_hint
        opts_vars['workspace'] = workspace

        # Get the active profile
        profile = profile or opts_vars.get('profile', None) or metadata.get_active_profile(workspace)
        opts_vars['profile'] = profile

        # Initialize empty metadata/args
        config_metadata = {}
        context_args = {}

        # Get the metadata stored in the workspace if it was found
        if workspace:
            config_metadata = metadata.get_metadata(workspace, profile, 'config')
            context_args.update(config_metadata)

        # User-supplied args are used to update stored args
        # Only update context args with given opts which are not none
        for (k, v) in opts_vars.items():
            if k in Context.KEYS and v is not None:
                # Handle list-type arguments with append/remove functionality
                if type(context_args.get(k, None)) is list and type(v) is list:
                    if append:
                        context_args[k] += v
                    elif remove:
                        context_args[k] = [w for w in context_args[k] if w not in v]
                    else:
                        context_args[k] = v
                else:
                    context_args[k] = v

        # Create the build context
        ctx = Context(**context_args)

        # Don't load the cmake config if it's not needed
        # if load_env:
        #     ctx.load_env()

        return ctx


    def __init__(
        self,
        workspace=None,
        profile=None,
        extend_path=None,
        participant_space=None,
        private_space=None,
        public_space=None,
        share_space=None,
        log_space=None,
        install_space=None,
        install=False,
        space_suffix=None,
        whitelist=None,
        blacklist=None,
        **kwargs
    ):
        """Creates a new Context object, optionally initializing with parameters
        :param workspace: root of the workspace, defaults to the enclosing workspace
        :type workspace: str
        :param profile: profile name, defaults to the default profile
        :type profile: str
        :param extend_path: catkin result-space to extend
        :type extend_path: str
        :param source_space: relative location of source space, defaults to '<workspace>/src'
        :type source_space: str
        :param log_space: relative location of log space, defaults to '<workspace>/logs'
        :type log_space: str
        :param build_space: relativetarget location of build space, defaults to '<workspace>/build'
        :type build_space: str
        :param devel_space: relative target location of devel space, defaults to '<workspace>/devel'
        :type devel_space: str
        :param install_space: relative target location of install space, defaults to '<workspace>/install'
        :type install_space: str
        :param isolate_devel: each package will have its own develspace if True, default is False
        :type isolate_devel: bool
        :param install: packages will be installed by invoking ``make install``, defaults to False
        :type install: bool
        :param isolate_install: packages will be installed to separate folders if True, defaults to False
        :type isolate_install: bool
        :param cmake_args: extra cmake arguments to be passed to cmake for each package
        :type cmake_args: list
        :param make_args: extra make arguments to be passed to make for each package
        :type make_args: list
        :param jobs_args: -j and -l jobs args
        :type jobs_args: list
        :param use_internal_make_jobserver: true if this configuration should use an internal make jobserv
        :type use_internal_make_jobserver: bool
        :param use_env_cache: true if this configuration should cache job environments loaded from resultspaces
        :type use_env_cache: bool
        :param catkin_make_args: extra make arguments to be passed to make for each catkin package
        :type catkin_make_args: list
        :param space_suffix: suffix for build, devel, and install spaces which are not explicitly set.
        :type space_suffix: str
        :param whitelist: a list of packages to build by default
        :type whitelist: list
        :param blacklist: a list of packages to ignore by default
        :type blacklist: list
        :raises: ValueError if workspace or source space does not exist
        """
        self.__locked = False

        # Check for unhandled context options
        if len(kwargs) > 0:
            print('Warning: Unhandled config context options: {}'.format(kwargs), file=sys.stderr)

        # Validation is done on assignment
        # Handle *space assignment and defaults
        self.workspace = workspace

        self.extend_path = extend_path if extend_path else None
        ss = '' if space_suffix is None else space_suffix

        self.profile = profile

        self.participant_space = Context.DEFAULT_PARTICIPANT_SPACE if participant_space is None else participant_space
        self.public_space = Context.DEFAULT_PRIVATE_SPACE if public_space is None else public_space
        self.share_space = Context.DEFAULT_PUBLIC_SPACE if share_space is None else share_space
        self.share_space = Context.DEFAULT_SHARE_SPACE if share_space is None else share_space

        self.log_space = Context.DEFAULT_LOG_SPACE + ss if ss or log_space is None else log_space
        self.install_space = Context.DEFAULT_INSTALL_SPACE + ss if ss or install_space is None else install_space
        self.destdir = os.environ['DESTDIR'] if 'DESTDIR' in os.environ else None

        # Handle package whitelist/blacklist
        self.whitelist = whitelist or []
        self.blacklist = blacklist or []

        # List of warnings about the workspace is set internally
        self.warnings = []

        # Initialize environment settings set by load_env
        self.manual_cmake_prefix_path = None
        self.cached_cmake_prefix_path = None
        self.env_cmake_prefix_path = None
        self.cmake_prefix_path = None

    def load_env(self):
        pass

    def summary(self, notes=[]):
        # Add warnings (missing dirs in CMAKE_PREFIX_PATH, etc)
        summary_warnings = self.warnings
        if not self.initialized():
            summary_warnings += [clr(
                "Workspace `@{yf}{_Context__workspace}@|` is not yet "
                "initialized. Use the `catkin init` or run `catkin config "
                "--init`.")]
        if not self.source_space_exists():
            summary_warnings += [clr(
                "Source space `@{yf}{_Context__source_space_abs}@|` does not yet exist.")]

        summary = [
            [
                clr("@{cf}Profile:@|                     @{yf}{profile}@|"),
                clr("@{cf}Extending:@|        {extend_mode} @{yf}{extend}@|"),
                clr("@{cf}Workspace:@|                   @{yf}{_Context__workspace}@|"),
            ],
            [
                clr("@{cf}Source Space:@|      {source_missing} @{yf}{_Context__source_space_abs}@|"),
                clr("@{cf}Log Space:@|         {log_missing} @{yf}{_Context__log_space_abs}@|"),
                clr("@{cf}Build Space:@|       {build_missing} @{yf}{_Context__build_space_abs}@|"),
                clr("@{cf}Devel Space:@|       {devel_missing} @{yf}{_Context__devel_space_abs}@|"),
                clr("@{cf}Install Space:@|     {install_missing} @{yf}{_Context__install_space_abs}@|"),
                clr("@{cf}DESTDIR:@|           {destdir_missing} @{yf}{_Context__destdir}@|")
            ],
            [
                clr("@{cf}Devel Space Layout:@|          @{yf}{_Context__devel_layout}@|"),
                clr("@{cf}Install Space Layout:@|        @{yf}{install_layout}@|"),
            ],
            [
                clr("@{cf}Additional CMake Args:@|       @{yf}{cmake_args}@|"),
                clr("@{cf}Additional Make Args:@|        @{yf}{make_args}@|"),
                clr("@{cf}Additional catkin Make Args:@| @{yf}{catkin_make_args}@|"),
                clr("@{cf}Internal Make Job Server:@|    @{yf}{_Context__use_internal_make_jobserver}@|"),
                clr("@{cf}Cache Job Environments:@|      @{yf}{_Context__use_env_cache}@|"),
            ],
            [
                clr("@{cf}Whitelisted Packages:@|        @{yf}{whitelisted_packages}@|"),
                clr("@{cf}Blacklisted Packages:@|        @{yf}{blacklisted_packages}@|"),
            ]
        ]

        # Construct string for extend value
        if self.extend_path:
            extend_value = self.extend_path
            extend_mode = clr('@{gf}[explicit]@|')
        elif self.cached_cmake_prefix_path:
            extend_value = self.cmake_prefix_path
            extend_mode = clr('  @{gf}[cached]@|')
        elif (self.env_cmake_prefix_path and
                self.env_cmake_prefix_path != self.devel_space_abs and
                self.env_cmake_prefix_path != self.install_space_abs):
            extend_value = self.cmake_prefix_path
            extend_mode = clr('     @{gf}[env]@|')
        else:
            extend_value = 'None'
            extend_mode = clr('          ')

        def existence_str(path, used=True):
            if used:
                return clr(' @{gf}[exists]@|' if os.path.exists(path) else '@{rf}[missing]@|')
            else:
                return clr(' @{bf}[unused]@|')

        install_layout = 'None'
        if self.__install:
            install_layout = 'merged' if not self.__isolate_install else 'isolated'

        subs = {
            'profile': self.profile,
            'extend_mode': extend_mode,
            'extend': extend_value,
            'install_layout': install_layout,
            'cmake_prefix_path': (self.cmake_prefix_path or ['Empty']),
            'cmake_args': ' '.join(self.__cmake_args or ['None']),
            'make_args': ' '.join(self.__make_args + self.__jobs_args or ['None']),
            'catkin_make_args': ', '.join(self.__catkin_make_args or ['None']),
            'source_missing': existence_str(self.source_space_abs),
            'log_missing': existence_str(self.log_space_abs),
            'build_missing': existence_str(self.build_space_abs),
            'devel_missing': existence_str(self.devel_space_abs),
            'install_missing': existence_str(self.install_space_abs, used=self.__install),
            'destdir_missing': existence_str(self.destdir, used=self.destdir),
            'whitelisted_packages': ' '.join(self.__whitelist or ['None']),
            'blacklisted_packages': ' '.join(self.__blacklist or ['None']),
        }
        subs.update(**self.__dict__)
        # Get the width of the shell
        width = terminal_width()
        max_length = 0
        groups = []
        for group in summary:
            for index, line in enumerate(group):
                group[index] = line.format(**subs)
                max_length = min(width, max(max_length, len(remove_ansi_escape(group[index]))))
            groups.append("\n".join(group))
        divider = clr('@{pf}' + ('-' * max_length) + '@|')
        warning_divider = clr('@{rf}' + ('-' * max_length) + '@|')

        # Format warnings
        if len(summary_warnings) == 0:
            notes = [clr("@!@{cf}Workspace configuration appears valid.@|")] + notes
            warnings_joined = ''
        else:
            warnings_formatted = [
                printed_fill(clr('@!@{rf}WARNING:@| ') + sw.format(**subs), max_length)
                for sw in summary_warnings]
            warnings_joined = (
                "\n\n" + warning_divider + "\n" +
                ("\n" + warning_divider + "\n").join(warnings_formatted) +
                "\n" + warning_divider + "\n")

        return (divider + "\n" +
                ("\n" + divider + "\n").join(groups) + "\n" + divider + "\n" +
                ((("\n\n").join(notes) + "\n" + divider) if notes else '') +
                warnings_joined)

    @property
    def workspace(self):
        return self.__workspace

    @workspace.setter
    def workspace(self, value):
        if self.__locked:
            raise RuntimeError("Setting of context members is not allowed while locked.")
        # Validate Workspace
        if not os.path.exists(value):
            raise ValueError("Workspace path '{0}' does not exist.".format(value))
        self.__workspace = os.path.abspath(value)

    @property
    def extend_path(self):
        return self.__extend_path

    @extend_path.setter
    def extend_path(self, value):
        if value is not None:
            if not os.path.isabs(value):
                value = os.path.join(self.workspace, value)
            # remove double or trailing slashes
            value = os.path.normpath(value)
            if not os.path.exists(value):
                raise ValueError("Resultspace path '{0}' does not exist.".format(value))
        self.__extend_path = value

    @property
    def source_space_abs(self):
        return self.__source_space_abs

    @property
    def source_space(self):
        return self.__source_space

    @source_space.setter
    def source_space(self, value):
        if self.__locked:
            raise RuntimeError("Setting of context members is not allowed while locked.")
        self.__source_space = value
        self.__source_space_abs = os.path.join(self.__workspace, value)

    def source_space_exists(self):
        "Returns true if the source space exists"
        return os.path.exists(self.source_space_abs) and os.path.isdir(self.source_space_abs)

    def initialized(self):
        """Check if this context is initialized."""
        return self.workspace == find_enclosing_workspace(self.workspace)

    @property
    def participant_space_abs(self):
        return self.__participant_space_abs

    @property
    def participant_space(self):
        return self.__participant_space

    @participant_space.setter
    def participant_space(self, value):
        if self.__locked:
            raise RuntimeError("Setting of context members is not allowed while locked.")
        self.__participant_space = value
        self.__participant_space_abs = os.path.join(self.__workspace, value)

    @property
    def private_space_abs(self):
        return self.__private_space_abs

    @property
    def private_space(self):
        return self.__private_space

    @private_space.setter
    def private_space(self, value):
        if self.__locked:
            raise RuntimeError("Setting of context members is not allowed while locked.")
        self.__private_space = value
        self.__private_space_abs = os.path.join(self.__workspace, value)

    @property
    def public_space_abs(self):
        return self.__public_space_abs

    @property
    def public_space(self):
        return self.__public_space

    @public_space.setter
    def public_space(self, value):
        if self.__locked:
            raise RuntimeError("Setting of context members is not allowed while locked.")
        self.__public_space = value
        self.__public_space_abs = os.path.join(self.__workspace, value)

    @property
    def share_space_abs(self):
        return self.__share_space_abs

    @property
    def share_space(self):
        return self.__share_space

    @share_space.setter
    def share_space(self, value):
        if self.__locked:
            raise RuntimeError("Setting of context members is not allowed while locked.")
        self.__share_space = value
        self.__share_space_abs = os.path.join(self.__workspace, value)

    @property
    def log_space_abs(self):
        return self.__log_space_abs

    @property
    def log_space(self):
        return self.__log_space

    @log_space.setter
    def log_space(self, value):
        if self.__locked:
            raise RuntimeError("Setting of context members is not allowed while locked.")
        self.__log_space = value
        self.__log_space_abs = os.path.join(self.__workspace, value)

    @property
    def install_space_abs(self):
        return self.__install_space_abs

    @property
    def install_space(self):
        return self.__install_space

    @install_space.setter
    def install_space(self, value):
        if self.__locked:
            raise RuntimeError("Setting of context members is not allowed while locked.")
        self.__install_space = value
        self.__install_space_abs = os.path.join(self.__workspace, value)

    def metadata_path(self):
        """Get the path to the metadata directory for this profile."""
        profile_path, _ = metadata.get_paths(self.workspace, self.profile)
        return profile_path
