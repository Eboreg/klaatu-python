from collections.abc import Callable, Iterable, Iterator, Sequence
from typing import TypeVar


_T = TypeVar("_T")
_T2 = TypeVar("_T2")


def filter_values_not_null(d: dict[_T, _T2 | None]) -> dict[_T, _T2]:
    return {k: v for k, v in d.items() if v is not None}


def group_by(sequence: Sequence[_T], pred: Callable[[_T], _T2]) -> dict[_T2, list[_T]]:
    """
    Groups `sequence` by the result of `pred` on each item. Returns dict with
    those results as keys and sublists of `sequence` as values.
    """
    result: dict[_T2, list[_T]] = {}
    for item in sequence:
        key = pred(item)
        if key not in result:
            result[key] = [item]
        else:
            result[key].append(item)
    return result


def group_dicts(
    dicts: Iterable[dict[str, _T]],
    keys: list[str],
    data_key: str = "data",
) -> list[dict[str, _T | list[dict[str, _T]]]]:
    """
    In:
        dicts = [
            {"slug": "musikensmakt", "name": "Musikens Makt", "date": "2025-04-01", "count": 60},
            {"slug": "musikensmakt", "name": "Musikens Makt", "date": "2025-04-02", "count": 64},
            {"slug": "apanap", "name": "Apan Ap", "date": "2025-04-01", "count": 2},
        ]
        keys = ["slug", "name"]
        data_key = "dätä"
    Out: [
        {
            "slug": "musikensmakt",
            "name": "Musikens Makt",
            "dätä": [{"date": "2025-04-01", "count": 60}, {"date": "2025-04-02", "count": 64}],
        },
        {
            "slug": "apanap",
            "name": "Apan Ap",
            "dätä": [{"date": "2025-04-01", "count": 2}],
        },
    ]
    """
    result: dict[tuple[_T, ...], list] = {}

    for d in dicts:
        dd = d.copy()
        d_key = tuple(d[key] for key in keys)
        if d_key not in result:
            result[d_key] = []
        for key in keys:
            del dd[key]
        result[d_key].append(dd)

    return [{data_key: v, **{keys[i]: k[i] for i in range(len(keys))}} for k, v in result.items()]


def zip_dicts(*dicts: dict) -> dict:
    """
    Combines dicts into one dict. On duplicate keys, dicts later in the
    sequence have priority.
    """
    return {k: v for d in dicts for k, v in d.items()}


def zip_dict_lists(dict_lists: Iterable[Iterable[dict]], strict: bool = False) -> Iterator[dict]:
    """
    Zips a list of dict lists and combines them into single dicts.
    I.e. given dict_lists = [
        [{a1: 1, a2: 2}, {b1: 3, b2: 4}],
        [{a3: 5, a4: 6}, {b3: 7, b4: 8}],
    ],
    these dicts will be yielded:
    {a1: 1, a2: 2, a3: 5, a4: 6}
    {b1: 3, b2: 4, b3: 7, b4: 8}
    """
    for dicts in zip(*dict_lists, strict=strict):
        yield zip_dicts(*dicts)
