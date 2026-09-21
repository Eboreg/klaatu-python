from collections.abc import Iterable


def fancy_join(parts: Iterable, operator: str = "and", oxford_comma: bool = True):
    strings = [str(part) for part in parts]

    if len(strings) == 0:
        return ""
    if len(strings) == 1:
        return str(strings[0])
    if len(strings) == 2:
        return f"{strings[0]} {operator} {strings[1]}"

    last_part = f"{',' if oxford_comma else ''} {operator} {strings.pop()}"

    return ", ".join(strings) + last_part
