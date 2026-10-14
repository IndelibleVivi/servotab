def _display_excerpt(text, limit):
    if limit <= 0:
        raise ValueError("positive limit required")
    clean = " ".join(text.split())
    if len(clean) <= limit:
        return clean
    return clean[:limit - 1] + "…"


def card_excerpt(text, limit=80):
    return _display_excerpt(text, limit)


def search_excerpt(text, limit=80):
    return _display_excerpt(text, limit)


def export_text(text):
    return text
