from __future__ import annotations

import sys
import typing
from argparse import ArgumentParser

import feedparser

from .types_ import MyHelpFormatter
from .utils import print_entries_table, print_entry

if typing.TYPE_CHECKING:
    from argparse import Namespace

    from .types_ import Entry

URL = "https://blog.python.org/feeds/posts/default?alt=rss"

PROG = "py-insider"
PROG_DESC = """\
██████╗ ██╗   ██╗     ██╗███╗   ██╗███████╗██╗██████╗ ███████╗██████╗
██╔══██╗╚██╗ ██╔╝     ██║████╗  ██║██╔════╝██║██╔══██╗██╔════╝██╔══██╗
██████╔╝ ╚████╔╝█████╗██║██╔██╗ ██║███████╗██║██║  ██║█████╗  ██████╔╝
██╔═══╝   ╚██╔╝ ╚════╝██║██║╚██╗██║╚════██║██║██║  ██║██╔══╝  ██╔══██╗
██║        ██║        ██║██║ ╚████║███████║██║██████╔╝███████╗██║  ██║
╚═╝        ╚═╝        ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝

Read python insiders blog in your terminal.\
"""
PROG_AUTHOR = "Muhammad Altaaf <taafuuu@gmail.com>"
PROG_VER = "1.0.0"
PROG_EPILOG = f"""\
Version: {PROG_VER}
Written by: {PROG_AUTHOR}
"""


def load_entries() -> list[Entry]:
    """Get entries from blog."""

    feed = feedparser.parse(URL)
    entries = feed["entries"]
    return entries


def parse_opts() -> Namespace:
    """Parse command line options and return Namespace object."""

    o_parser = ArgumentParser(
        prog=PROG,
        description=PROG_DESC,
        epilog=PROG_EPILOG,
        formatter_class=MyHelpFormatter,
    )
    add_opt = o_parser.add_argument
    ln_group = o_parser.add_mutually_exclusive_group()

    ln_group.add_argument(
        "-n",
        dest="number",
        metavar="NUMBER",
        default=None,
        type=int,
        help="Show an rss feed with number NUMBER. To see all numbers,"
        " run program without arguments.",
    )
    ln_group.add_argument(
        "-l",
        dest="latest",
        action="store_true",
        default=False,
        help="Show the latest rss feed. Suppresses -n option.",
    )
    add_opt(
        "-c",
        dest="civil",
        action="store_true",
        default=False,
        help="Show time in civil format (with am/pm).",
    )
    add_opt(
        "-u",
        dest="human",
        action="store_true",
        default=False,
        help="Show time in human format.",
    )
    add_opt(
        "-p",
        dest="paginate",
        action="store_true",
        default=False,
        help="Paginate the output.",
    )
    add_opt(
        "-s",
        dest="styles",
        action="store_true",
        default=False,
        help="Enable styles with paginator.",
    )

    options = o_parser.parse_args()
    return options


def main() -> None:
    options = parse_opts()
    entries = load_entries()

    # user wants to read
    read_req = options.latest or options.number

    if not read_req:
        print_entries_table(entries, options.paginate, options.styles, options.civil, options.human)
        sys.exit(0)

    else:
        c_entry_map = dict(enumerate(entries, start=1))
        entry_keys = sorted(c_entry_map.keys())
        entry_number: int

        entry_number = entry_keys[0] if options.latest else options.number

        if entry_number not in entry_keys:
            print(
                "Please enter valid entry number.\n"
                "To see all valid numbers, run "
                "program without arguments.",
                file=sys.stderr,
            )
            sys.exit(1)

        entry = c_entry_map.get(entry_number)
        print_entry(entry, options.paginate, options.styles, options.civil,  options.civil)


if __name__ == "__main__":
    main()
