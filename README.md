# klaatu-python

<img width="400" alt="thisprojectwascodedbyahumanbeing-wordart" src="https://github.com/user-attachments/assets/2e36f279-91d9-4f65-9c8f-fd8e6b179f7a" />

A bunch of more or less useful Python utils without _any_ 3rd party dependencies.

## Development install

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Inclusion in projects

In `pyproject.toml`:
```
[project]
dependencies = [
    "klaatu-python",
    ...
]
```
