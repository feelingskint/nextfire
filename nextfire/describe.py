"""Describe a parsed cron expression in plain English."""

from __future__ import annotations

from .fields import HOUR, MINUTE, Cron, Field

DAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"]
MAX_TIMES = 6


def _step(values: frozenset[int], field: Field) -> int | None:
    """The step if `values` is every Nth value of the field, starting at its minimum."""
    vals = sorted(values)
    if len(vals) < 2 or vals[0] != field.lo:
        return None
    step = vals[1] - vals[0]
    return step if vals == list(range(field.lo, field.hi + 1, step)) else None


def _every(n: int, unit: str) -> str:
    return f"every {unit}" if n == 1 else f"every {n} {unit}s"


def _join(words: list[str]) -> str:
    return words[0] if len(words) == 1 else ", ".join(words[:-1]) + " and " + words[-1]


def _time(cron: Cron) -> str:
    minute_step = _step(cron.minutes, MINUTE)
    hour_step = _step(cron.hours, HOUR)
    if minute_step and hour_step == 1:
        return _every(minute_step, "minute").capitalize()
    if len(cron.minutes) == 1 and hour_step:
        (minute,) = cron.minutes
        text = _every(hour_step, "hour").capitalize()
        return text if minute == 0 else f"{text} at minute {minute}"
    if len(cron.minutes) * len(cron.hours) <= MAX_TIMES:
        return "At " + _join([f"{h:02d}:{m:02d}" for h in sorted(cron.hours) for m in sorted(cron.minutes)])
    return (f"At minute {_join([str(m) for m in sorted(cron.minutes)])}"
            f" past hour {_join([str(h) for h in sorted(cron.hours)])}")


def _weekdays(days: frozenset[int]) -> str:
    order = sorted(days, key=lambda d: (d - 1) % 7)  # Monday first
    keys = [(d - 1) % 7 for d in order]
    if len(order) >= 3 and keys == list(range(keys[0], keys[-1] + 1)):
        return f"{DAY_NAMES[order[0]]} through {DAY_NAMES[order[-1]]}"
    return _join([DAY_NAMES[d] for d in order])


def describe(cron: Cron) -> str:
    parts = [_time(cron)]
    if not cron.any_day:
        parts.append(f"on day {_join([str(d) for d in sorted(cron.days)])} of the month")
    if not cron.any_weekday:
        parts.append(f"on {_weekdays(cron.weekdays)}")
    if len(cron.months) < 12:
        parts.append(f"in {_join([MONTH_NAMES[m - 1] for m in sorted(cron.months)])}")
    return ", ".join(parts)
