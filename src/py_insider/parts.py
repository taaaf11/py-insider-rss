from __future__ import annotations

import typing
from datetime import datetime

from markdownify import markdownify
from rich.markdown import Markdown
from rich.table import Table
from rich.text import Text

if typing.TYPE_CHECKING:
    from .types import Entry


def fmt_datetime(iso_datetime: str, civil: bool, human: bool) -> str:
    """Format date and time from entry data
    into local time.
    """

    if civil:
        if human:
            format_ = "%a %d-%b-%Y %I:%M:%S %p"
        else:
            format_ = "%Y-%m-%d %I:%M:%S %p"
    else:
        if human:
            format_ = "%a %d-%b-%Y %H:%M:%S"
        else:
            format_ = "%Y-%m-%d %H:%M:%S"

    dt = datetime.fromisoformat(iso_datetime)
    dt_local = dt.astimezone()
    return dt_local.strftime(format_)


def make_title(entry: Entry) -> Text:
    """Make title info renderable from entry data."""

    title = Text.assemble(("Title: ", "bold"), entry["title"])
    return title


def make_authors(entry: Entry) -> Text:
    """Make author info renderable from entry data."""

    authors_text = Text.assemble(("Authors: ", "bold"))

    for count, author in enumerate(entry["authors"], start=1):
        if count > 1:
            authors_text.append("\t")

        # name and email
        authors_text.append(f"{author['name']} <{author['email']}>")
        authors_text.append("\n")

    return authors_text


def make_last_updated(entry: Entry, date_civil: bool, date_human: bool) -> Text:
    """Make last update info renderable from entry data."""

    date_info = Text.assemble(
        ("Last updated: ", "bold"),
        fmt_datetime(entry["updated"]),
    )

    return date_info


def make_entries_table(entries: list[Entry], date_civil: bool, date_human: bool) -> Table:
    """Make a table with two columns: serial number
    and title of entry."""

    table = Table(show_header=True, header_style="magenta", expand=True)
    cols = ["Sr.", "Date", "Title"]

    for col in cols:
        table.add_column(col)

    for count, entry in enumerate(entries, start=1):
        title = Text(entry["title"])
        date_ = fmt_datetime(entry["date"], date_civil, date_human)
        table.add_row(str(count), date_, title)

    return table


def make_info(entry: Entry, date_civil: bool, date_human: bool) -> Text:
    """Wrapper around different info making
    functions.
    """

    title = make_title(entry)
    authors = make_authors(entry)
    last_updated = make_last_updated(entry, date_civil, date_human)
    newline = Text("\n")

    infos = [
        title,
        newline,
        authors,
        # newline,  # make_authors adds newline after each author
        last_updated,
        newline,
    ]

    info_text = Text()

    for info in infos:
        info_text.append(info)

    return info_text


def make_summary(entry: Entry) -> Markdown:
    """Make summary renderable from entry data."""

    # summary is in html format
    summary2md = Markdown(markdownify(entry["summary"]))

    return summary2md
