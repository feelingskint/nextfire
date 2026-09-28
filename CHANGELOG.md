# Changelog

## Unreleased

- Clearer error message for out-of-range values.
- Syntax errors exit with status 2 (was 1), like other CLI usage errors.

## 0.5.0

- Step values on ranges, e.g. `1-30/5`.
- `--explain` lists up to six times before falling back to a minute/hour summary.

## 0.4.0

- `--json` prints the upcoming runs as a JSON list.
- README examples for `--explain` and the `@` aliases.

## 0.3.0

- `--explain` prints a plain-English description of the expression.
- Ctrl-C exits quietly instead of printing a traceback.

## 0.2.0

- Month and weekday names (`jan`, `MON`, ...) are accepted.
- `@daily`, `@hourly`, `@weekly`, `@monthly` and `@yearly` aliases.

## 0.1.0

- First release.
