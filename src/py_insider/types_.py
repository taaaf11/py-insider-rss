from __future__ import annotations

from argparse import (OPTIONAL, SUPPRESS, ZERO_OR_MORE,
                      ArgumentDefaultsHelpFormatter,
                      RawDescriptionHelpFormatter)
from gettext import gettext as _
from typing import TYPE_CHECKING, Any, override

if TYPE_CHECKING:
    from typing import TypeAlias

Entry: TypeAlias = dict[str, Any]


class MyHelpFormatter(
    ArgumentDefaultsHelpFormatter,
    RawDescriptionHelpFormatter,
):
    """ArgumentParser formatter class for showing custom
    help messages for argument defaults and retaining formation
    of description.
    """

    @override
    def _get_help_string(self, action):
        help = action.help

        if help is None:
            help = ""

        if "%(default)" not in help:
            if action.default is not SUPPRESS and action.default is not None:
                defaulting_nargs = [OPTIONAL, ZERO_OR_MORE]
                if action.option_strings or action.nargs in defaulting_nargs:
                    help += _(" (Defaults to: %(default)s)")
        return help
