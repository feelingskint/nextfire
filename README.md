# nextfire

[![CI](https://github.com/FlamminSoftware/nextfire/actions/workflows/ci.yml/badge.svg)](https://github.com/FlamminSoftware/nextfire/actions/workflows/ci.yml)

Show when a cron expression will fire next.

```console
$ nextfire '30 6 * * *' -n 3
2026-03-05 06:30  Thu
2026-03-06 06:30  Fri
2026-03-07 06:30  Sat
```

## Install

```sh
pipx install git+https://github.com/FlamminSoftware/nextfire
```

or `pip install --user git+https://github.com/FlamminSoftware/nextfire`.

## Usage

    nextfire EXPRESSION [-n COUNT] [--from 'YYYY-MM-DD HH:MM'] [--explain] [--json]

Times are shown in your local timezone.

Steps work on ranges as well as on `*`: `0 8-18/2 * * *` runs every other hour
during the working day.

The usual aliases work too: `@hourly`, `@daily` (or `@midnight`), `@weekly`,
`@monthly` and `@yearly` (or `@annually`).

```console
$ nextfire --explain '0 9 * * mon,wed,fri' -n 2 --from '2026-03-04 10:07'
At 09:00, on Monday, Wednesday and Friday
2026-03-06 09:00  Fri
2026-03-09 09:00  Mon
```

## Development

No dependencies beyond the standard library.

```sh
python -m unittest
```

## License

MIT
