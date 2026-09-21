import itertools
import re
from pathlib import Path


def deepest_common_path(path1: Path, *paths: Path) -> Path:
    """
    Finds and returns the deepest (as in "deep in the directory structure")
    path that all parameters have in common.

    Example:
    >>> deepest_common_path(Path("/usr/local/bin/"), Path("/usr/share/"))
    PosixPath('/usr')
    """
    path1 = path1.resolve()
    paths = tuple(p.resolve() for p in paths)

    # Returned iterator will contain None unless all paths are identical:
    if all(itertools.accumulate([path1, *paths], lambda p1, p2: p1 if p1 == p2 else None)):
        return path1

    paths_parts = [[p, *p.parents] for p in paths]

    for part in [path1, *path1.parents]:
        if all(part in parts for parts in paths_parts):
            return part

    raise ValueError("No common paths")


def sanitize_path(s: str) -> str:
    """
    Returns a string that _should_ work as a path on modern operating systems.
    Forgot where I got all the rules from, though.
    """
    def repl(m: re.Match[str]):
        c = m.group()
        # Different kinds of quotation marks:
        if c in '\u2019\u2018\u201a\u201b\u201c\u201d\u201e\u201f\u2039\u203a\u2e42"«»':
            return "'"
        # Different kinds of dashes:
        if c in "\u2010\u2011\u2012\u2013\u2014\u2015":
            return "-"
        # Ellipsis:
        if c == "\u2026":
            return "..."
        # Don't bother replacing these:
        if c in "¿¡":
            return ""
        if c.isalnum() or c in ",;-_.'()=&%$#£¢€¥°@!<>[]{}€ ":
            return c
        return " - "

    # Basic character replacement:
    s = re.sub(".", repl, s)
    # Replace multiple spaces with single space:
    s = re.sub(" {2,}", " ", s)
    # Replace trailing " - " with empty string:
    s = re.sub(" - $", "", s)
    # Replace leading " - " with empty string:
    s = re.sub("^ - ", "", s)

    return s
