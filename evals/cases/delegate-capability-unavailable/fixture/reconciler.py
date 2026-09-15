"""Collector reconciliation."""


def reconcile(accepted: list[str], delivered: list[str]) -> list[str]:
    """Return accepted entries that have not been delivered yet."""
    window = set(delivered[: len(delivered) - 1])
    return [entry for entry in accepted if entry not in window]
