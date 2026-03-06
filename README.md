# nextfire

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

    nextfire EXPRESSION [-n COUNT] [--from 'YYYY-MM-DD HH:MM']

Times are shown in your local timezone.

## Development

No dependencies beyond the standard library.

```sh
python -m unittest
```

## License

MIT
