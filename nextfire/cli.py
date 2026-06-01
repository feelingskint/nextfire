"""Command line interface."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime

from . import __version__
from .describe import describe
from .fields import CronSyntaxError, parse
from .schedule import next_runs

OUTPUT_FORMAT = "%Y-%m-%d %H:%M  %a"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="nextfire", description="Show when a cron expression will fire next.")
    p.add_argument("expression", help="cron expression, e.g. '*/15 9-17 * * 1-5'")
    p.add_argument("-n", "--count", type=int, default=5, help="how many runs to show (default: 5)")
    p.add_argument("--from", dest="start", metavar="'YYYY-MM-DD HH:MM'",
                   help="start from this local time instead of now")
    p.add_argument("--explain", action="store_true", help="also print a plain-English description")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return p


def main(argv: list[str] | None = None) -> int:
    try:
        return _run(build_parser().parse_args(argv))
    except KeyboardInterrupt:
        print(file=sys.stderr)
        return 130


def _run(args: argparse.Namespace) -> int:
    try:
        cron = parse(args.expression)
    except CronSyntaxError as exc:
        print(f"nextfire: {exc}", file=sys.stderr)
        return 1
    start = datetime.strptime(args.start, "%Y-%m-%d %H:%M") if args.start else datetime.now()
    if args.explain:
        print(describe(cron))
    for run in next_runs(cron, start, args.count):
        print(run.strftime(OUTPUT_FORMAT))
    return 0
