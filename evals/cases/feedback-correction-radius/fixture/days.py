from datetime import datetime, timezone


def _utc_day(timestamp):
    value = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    if value.tzinfo is None:
        raise ValueError("timestamp must have a timezone")
    return value.astimezone(timezone.utc).date().isoformat()


def chart_day(timestamp, offset_minutes):
    return _utc_day(timestamp)


def detail_day(timestamp, offset_minutes):
    return _utc_day(timestamp)


def share_day(timestamp, offset_minutes):
    return timestamp[:10]


def audit_day(timestamp):
    return _utc_day(timestamp)
