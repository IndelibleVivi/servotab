from datetime import datetime, timedelta, timezone


def _utc_day(timestamp):
    value = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    if value.tzinfo is None:
        raise ValueError("timestamp must have a timezone")
    return value.astimezone(timezone.utc).date().isoformat()


def _local_day(timestamp, offset_minutes):
    value = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    if value.tzinfo is None:
        raise ValueError("timestamp must have a timezone")
    offset = timezone(timedelta(minutes=offset_minutes))
    return value.astimezone(offset).date().isoformat()


def chart_day(timestamp, offset_minutes):
    return _local_day(timestamp, offset_minutes)


def detail_day(timestamp, offset_minutes):
    return _local_day(timestamp, offset_minutes)


def share_day(timestamp, offset_minutes):
    return _local_day(timestamp, offset_minutes)


def audit_day(timestamp):
    return _utc_day(timestamp)
