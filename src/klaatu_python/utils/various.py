from typing import Any


def get_binary_reply(prompt: str, default: bool | None = None) -> bool:
    if default:
        prompt += " [Y/n] "
    elif default is None:
        prompt += " [y/n] "
    else:
        prompt += " [y/N] "

    while True:
        reply = input(prompt).lower().strip()
        if reply == "" and default is not None:
            return default
        if reply in ("y", "n"):
            return reply == "y"
        print("Wrong answer, try again.")


def is_truthy(value: Any) -> bool:
    """
    Basically does `bool(value)`, except it also returns False for string
    values "false", "no", and "0" (case insensitive).
    """
    if isinstance(value, str) and value.lower() in ("false", "no", "0"):
        return False
    return bool(value)
