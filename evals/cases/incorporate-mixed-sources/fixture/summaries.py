def card_excerpt(text, limit=80):
    if limit <= 0:
        raise ValueError("positive limit required")
    return text.strip()[:limit]


def search_excerpt(text, limit=80):
    if limit <= 0:
        raise ValueError("positive limit required")
    return text[:limit]


def export_text(text):
    return text
