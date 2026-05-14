import io
import unittest
from contextlib import redirect_stderr, redirect_stdout

from nextfire.cli import main


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(list(argv))
    return code, out.getvalue(), err.getvalue()


class CliTests(unittest.TestCase):
    def test_lists_runs(self):
        code, out, _ = run("0 9 * * *", "-n", "2", "--from", "2026-03-04 10:07")
        self.assertEqual(code, 0)
        self.assertEqual(out.splitlines(), ["2026-03-05 09:00  Thu", "2026-03-06 09:00  Fri"])

    def test_explain(self):
        code, out, _ = run("0 9 * * *", "-n", "1", "--from", "2026-03-04 10:07", "--explain")
        self.assertEqual(code, 0)
        self.assertEqual(out.splitlines()[0], "At 09:00")

    def test_syntax_error(self):
        code, _, err = run("* * *")
        self.assertNotEqual(code, 0)
        self.assertIn("expected 5 fields", err)
