"""Sanity-check a scraped ETCC CSV before it replaces the committed copy.

Checks each row's structure rather than exact column names: the ETCC have
changed the format before (a header row appeared in 2024-08), so pinning the
header would cause false alarms. HTML error/challenge pages, empty responses
and mangled rows are rejected.
"""

import csv
import re
import sys
from pathlib import Path

MIN_FIELDS = 8  # transform.py reads fields 0-7
CALLSIGN = re.compile(r"[A-Z0-9]+", re.IGNORECASE)


def validate(path: str | Path) -> list[str]:
    """Return a list of problems with the CSV at path (empty if it looks OK)."""
    try:
        with open(path, encoding="utf-8", newline="") as f:
            rows = list(enumerate(csv.reader(f, strict=True), start=1))
    except (UnicodeDecodeError, csv.Error) as e:
        return [f"Could not parse as CSV: {e}"]

    # Optional header row
    if rows and rows[0][1] and rows[0][1][0].strip().lower() == "callsign":
        rows = rows[1:]

    if not rows:
        return ["No data rows"]

    problems = []
    for lineno, row in rows:
        if len(row) < MIN_FIELDS:
            problems.append(f"Line {lineno}: {len(row)} fields, expected at least {MIN_FIELDS}")
        elif not CALLSIGN.fullmatch(row[0].strip()):
            problems.append(f"Line {lineno}: unexpected callsign {row[0][:50]!r}")

    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("Usage: validate.py FILE", file=sys.stderr)
        return 2

    problems = validate(argv[0])
    for problem in problems[:10]:
        print(f"{argv[0]}: {problem}", file=sys.stderr)
    if len(problems) > 10:
        print(f"{argv[0]}: ...and {len(problems) - 10} more", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
