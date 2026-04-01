"""Parse the five fields of a crontab expression into sets of allowed values."""

from __future__ import annotations

from dataclasses import dataclass

MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
DAYS = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]


class CronSyntaxError(ValueError):
    """The expression is not valid crontab syntax."""


@dataclass(frozen=True)
class Field:
    name: str
    lo: int
    hi: int
    names: tuple[str, ...] = ()
    name_base: int = 0

    def value(self, token: str) -> int:
        t = token.lower()
        if t in self.names:
            return self.names.index(t) + self.name_base
        if not t.isdigit():
            raise CronSyntaxError(f"{self.name}: {token!r} is not a number")
        v = int(t)
        if not self.lo <= v <= self.hi:
            raise CronSyntaxError(f"{self.name}: {v} out of range")
        return v


MINUTE = Field("minute", 0, 59)
HOUR = Field("hour", 0, 23)
DAY = Field("day of month", 1, 31)
MONTH = Field("month", 1, 12, tuple(MONTHS), 1)
WEEKDAY = Field("day of week", 0, 7, tuple(DAYS))
FIELDS = (MINUTE, HOUR, DAY, MONTH, WEEKDAY)


def parse_field(text: str, field: Field) -> frozenset[int]:
    values: set[int] = set()
    for part in text.split(","):
        if not part:
            raise CronSyntaxError(f"{field.name}: empty list item in {text!r}")
        if part.startswith("*/"):
            step = part[2:]
            if not step.isdigit() or int(step) == 0:
                raise CronSyntaxError(f"{field.name}: bad step {step!r}")
            values.update(range(field.lo, field.hi + 1, int(step)))
        elif part == "*":
            values.update(range(field.lo, field.hi + 1))
        elif "-" in part:
            first, last = part.split("-", 1)
            lo, hi = field.value(first), field.value(last)
            if lo > hi:
                raise CronSyntaxError(f"{field.name}: range {part!r} goes backwards")
            values.update(range(lo, hi + 1))
        else:
            values.add(field.value(part))
    if field is WEEKDAY and 7 in values:
        values.discard(7)
        values.add(0)
    return frozenset(values)


@dataclass(frozen=True)
class Cron:
    minutes: frozenset[int]
    hours: frozenset[int]
    days: frozenset[int]
    months: frozenset[int]
    weekdays: frozenset[int]
    any_day: bool
    any_weekday: bool
    source: str


def parse(expr: str) -> Cron:
    source = expr.strip()
    parts = source.split()
    if len(parts) != 5:
        raise CronSyntaxError(f"expected 5 fields, got {len(parts)}")
    minutes, hours, days, months, weekdays = (parse_field(p, f) for p, f in zip(parts, FIELDS))
    return Cron(minutes, hours, days, months, weekdays,
                any_day=parts[2] == "*", any_weekday=parts[4] == "*", source=source)
