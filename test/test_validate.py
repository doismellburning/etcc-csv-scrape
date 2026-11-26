import csv

import pytest

from validate import main, validate

HEADER = ["Callsign", "Sysop", "Band", "TX", "Type", "Where", "Region", "Locator", "lat", "lon", ""]
ROW = ["GB7XX", "G0ABC", "2M", "144.800000", "AP", "SOUTHGATE", "SE", "IO91WP", "51.63", "-0.138", ""]

# Abridged version of what ukrepeater.net served from 2026-10-26
CLOUDFLARE = (
    '<!DOCTYPE html><html lang="en-US"><head><title>Just a moment...</title>'
    '<meta name="robots" content="noindex,nofollow"><meta name="viewport" content="width=device-width,initial-scale=1">'
    "<style>*{box-sizing:border-box;margin:0;padding:0}html{font-family:system-ui,-apple-system,BlinkMacSystemFont,"
    '"Segoe UI",Roboto,"Helvetica Neue",Arial}</style></head><body></body></html>\n'
)


def write_csv(tmp_path, rows):
    path = tmp_path / "packetlist.csv"
    with path.open("w", newline="") as f:
        csv.writer(f).writerows(rows)
    return path


def write_text(tmp_path, text):
    path = tmp_path / "packetlist.csv"
    path.write_text(text)
    return path


@pytest.fixture
def good(tmp_path):
    return write_csv(tmp_path, [HEADER, ROW, ROW])


def test_good_file(good):
    assert validate(good) == []


def test_header_is_optional(tmp_path):
    # Pre-2024-08 format: no header, 9 fields
    assert validate(write_csv(tmp_path, [ROW[:9], ROW[:9]])) == []


def test_header_names_may_change(tmp_path):
    assert validate(write_csv(tmp_path, [[" CALLSIGN ", "Keeper", "Something new"], ROW])) == []


def test_lowercase_callsign(tmp_path):
    assert validate(write_csv(tmp_path, [["gb7xx", *ROW[1:]]])) == []


def test_cloudflare_page(tmp_path):
    [problem] = validate(write_text(tmp_path, CLOUDFLARE))
    assert problem.startswith("Line 1: unexpected callsign '<!DOCTYPE html>")


def test_empty_file(tmp_path):
    assert validate(write_text(tmp_path, "")) == ["No data rows"]


def test_header_only(tmp_path):
    assert validate(write_csv(tmp_path, [HEADER])) == ["No data rows"]


def test_blank_line(tmp_path):
    assert validate(write_text(tmp_path, "\n")) == ["Line 1: 0 fields, expected at least 8"]


def test_not_utf8(tmp_path):
    path = tmp_path / "packetlist.csv"
    path.write_bytes(b"\xff\xfe\x00garbage")
    [problem] = validate(path)
    assert problem.startswith("Could not parse as CSV")


def test_truncated_mid_quote(tmp_path):
    [problem] = validate(write_text(tmp_path, 'GB7XX,"truncated mid-quote\n'))
    assert problem.startswith("Could not parse as CSV")


def test_short_row(tmp_path):
    assert validate(write_csv(tmp_path, [HEADER, ROW, ROW[:3]])) == ["Line 3: 3 fields, expected at least 8"]


def test_empty_callsign(tmp_path):
    assert validate(write_csv(tmp_path, [HEADER, ["", *ROW[1:]]])) == ["Line 2: unexpected callsign ''"]


def test_main_ok(good):
    assert main([str(good)]) == 0


def test_main_problems(tmp_path, capsys):
    assert main([str(write_text(tmp_path, CLOUDFLARE))]) == 1
    assert "unexpected callsign" in capsys.readouterr().err


def test_main_truncates_long_output(tmp_path, capsys):
    assert main([str(write_csv(tmp_path, [["x"]] * 15))]) == 1
    err = capsys.readouterr().err
    assert err.count("fields, expected") == 10
    assert "...and 5 more" in err


def test_main_usage(capsys):
    assert main([]) == 2
    assert "Usage" in capsys.readouterr().err
