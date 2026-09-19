"""Parse the five fields of a crontab expression into sets of allowed values."""

from __future__ import annotations

from dataclasses import dataclass

MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
DAYS = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]

ALIASES = {
    "@yearly": "0 0 1 1 *",
    "@annually": "0 0 1 1 *",
    "@monthly": "0 0 1 * *",
    "@weekly": "0 0 * * 0",
    "@daily": "0 0 * * *",
    "@midnight": "0 0 * * *",
    "@hourly": "0 * * * *",
}


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
            raise CronSyntaxError(f"{self.name}: {v} is out of range (allowed {self.lo}-{self.hi})")
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
        rng, _, step_text = part.partition("/")
        step = 1
        if step_text:
            if not step_text.isdigit() or int(step_text) == 0:
                raise CronSyntaxError(f"{field.name}: bad step {step_text!r}")
            step = int(step_text)
        if rng == "*":
            values.update(range(field.lo, field.hi + 1, step))
        elif "-" in rng:
            first, last = rng.split("-", 1)
            lo, hi = field.value(first), field.value(last)
            if lo > hi:
                raise CronSyntaxError(f"{field.name}: range {rng!r} goes backwards")
            values.update(range(lo, hi, step))
        elif step_text:
            raise CronSyntaxError(f"{field.name}: a step needs a range or '*', got {part!r}")
        else:
            values.add(field.value(rng))
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
    text = ALIASES.get(source.lower(), source)
    if text.startswith("@"):
        raise CronSyntaxError(f"unknown alias {source!r}")
    parts = text.split()
    if len(parts) != 5:
        raise CronSyntaxError(f"expected 5 fields, got {len(parts)}")
    minutes, hours, days, months, weekdays = (parse_field(p, f) for p, f in zip(parts, FIELDS))
    return Cron(minutes, hours, days, months, weekdays,
                any_day=parts[2] == "*", any_weekday=parts[4] == "*", source=source)
