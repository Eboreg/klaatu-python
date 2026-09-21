from collections.abc import Callable, Hashable, Iterable, Iterator, Sequence
from typing import Literal, TypeVar, overload


_T = TypeVar("_T")
_HashableT = TypeVar("_HashableT", bound=Hashable)


def circulate(lst: Iterable[_T], rounds: int) -> list[_T]:
    """
    Shifts `lst` left `rounds` times. Good for e.g. circulating colours in
    a graph.
    """
    if not isinstance(lst, list):
        lst = list(lst)
    if lst and rounds:
        for _ in range(rounds):
            val = lst.pop(0)
            lst.append(val)
    return lst


def first_not_null(*values: _T | None) -> _T:
    ret = first_not_null_or_null(*values)
    if ret is None:
        raise TypeError("All values are None")
    return ret


def first_not_null_or_null(*values: _T | None) -> _T | None:
    for value in values:
        if value is not None:
            return value
    return None


@overload
def getitem0(seq: Iterable[_T], cond: Callable[[_T], bool] | None, nullable: Literal[False]) -> _T: ...


@overload
def getitem0(seq: Iterable[_T], cond: Callable[[_T], bool] | None, nullable: Literal[True]) -> _T | None: ...


def getitem0(seq, cond=None, nullable=False):
    """
    @raises IndexError
    """
    try:
        if cond is None:
            return list(seq)[0]
        return [item for item in seq if cond(item)][0]
    except IndexError as e:
        if nullable:
            return None
        raise e


def getitem0_nullable(seq: Iterable[_T], cond: Callable[[_T], bool] | None = None) -> _T | None:
    return getitem0(seq, cond, True)


def getitem_nullable(seq: Iterable[_T], idx: int, cond: Callable[[_T], bool] | None = None) -> _T | None:
    """
    If `seq` has an item at position `idx`, return that item. Otherwise return
    None. Similar to how QuerySet's first() & last() operate.

    With `cond` set, it first filters `seq` for items where this function
    evaluates as True, then tries to get item `idx` from the resulting list.

    Example:

    seq = [23, 43, 12, 56, 75, 1]
    second_even = getitem_nullable(seq, 1, lambda item: item % 2 == 0)
    # second_even == 56
    seq = [1, 2, 3, 5, 7]
    second_even = getitem_nullable(seq, 1, lambda item: item % 2 == 0)
    # second_even == None
    """
    try:
        if cond is None:
            return list(seq)[idx]
        return [item for item in seq if cond(item)][idx]
    except IndexError:
        return None


def index_of_first(sequence: Sequence[_T], pred: Callable[[_T], bool]) -> int:
    """
    Tries to return the index of the first item in `sequence` for which the
    function `pred` returns True. If no such item is found, return -1.
    """
    try:
        return sequence.index(next(filter(pred, sequence)))
    except StopIteration:
        return -1


def most_common(values: Iterable[_HashableT]) -> tuple[_HashableT | None, int]:
    """
    Given a non-empty iterable, this will return a 2-tuple with the most
    commonly occurring value in said iterable, and the number of such
    occurances.

    Given an _empty_ iterable, it will return `(None, 0)`.
    """
    occurrences: dict[_HashableT, int] = {}

    for value in values:
        if value not in occurrences:
            occurrences[value] = 0
        occurrences[value] += 1

    if not occurrences:
        return None, 0

    return max(occurrences.items(), key=lambda tup: tup[1])


def nonulls(items: Iterable[_T | None]) -> list[_T]:
    """Just filters away None values from `items`."""
    return [item for item in items if item is not None]


def partition(items: Sequence[_T], length: int) -> Iterator[Sequence[_T]]:
    """Simply splits `items` into subsequences of max `length` items."""
    offset = 0
    while offset == 0 or offset < len(items):
        yield items[offset : offset + length]
        offset += length
