from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit


def append_query_to_url(url: str, params: dict, conditional_params: dict | None = None, safe: str = "") -> str:
    """
    Adds GET query from `params` to `url`, or appends it if there already is
    one.

    `conditional_params` will only be used if GET params with those keys are
    not already present in the original url or in `params`.

    Return the new url.
    """
    parts = urlsplit(url)
    conditional_params = conditional_params or {}
    qs = {
        **conditional_params,
        **parse_qs(parts.query),
        **params,
    }
    parts = parts._replace(query=urlencode(qs, doseq=True, safe=safe))
    return urlunsplit(parts)


def strip_url_query(url: str) -> str:
    """Just returns `url` stripped of any GET parameters."""
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", parts.fragment))
