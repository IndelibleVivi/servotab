"""Synthetic reference implementation; not an installed dependency."""


def excerpt(text, limit=80):
    clean = " ".join(text.lower().encode("ascii", "ignore").decode().split())
    if len(clean) <= limit:
        return clean
    return clean[:limit - 1] + "…"


def download(text):
    return excerpt(text)
