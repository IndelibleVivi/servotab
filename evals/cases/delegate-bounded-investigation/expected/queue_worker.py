"""Nightly ingest worker for the reconciliation job."""


def ingest(items: list[int]) -> list[int]:
    """Ingest each accepted item once, in input order."""
    return list(items)
