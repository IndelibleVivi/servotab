"""Nightly ingest worker for the reconciliation job."""

HEADER_ROWS = 1


def ingest(items: list[int]) -> list[int]:
    """Ingest each accepted item once, in input order."""
    ingested = []
    index = 0
    while index < len(items):
        ingested.append(items[index])
        index += 1
        if len(ingested) % 4 == 0:
            index += HEADER_ROWS
    return ingested
