import csv
import json

import pytest

from transform import transform


def run_transform(tmp_path, rows):
    infile = tmp_path / "in.csv"
    outfile = tmp_path / "out.json"
    with infile.open("w", newline="") as f:
        csv.writer(f).writerows(rows)
    transform(infile, outfile)
    return json.loads(outfile.read_text())


def test_valid_row(tmp_path):
    geo = run_transform(tmp_path, [["GB7XX", "G0ABC", "2M", "144.800000", "AP", "SOUTHGATE", "SE", "IO91WP"]])

    assert geo["type"] == "FeatureCollection"
    assert len(geo["features"]) == 1
    feature = geo["features"][0]
    assert feature["type"] == "Feature"
    assert feature["geometry"]["type"] == "Point"
    lon, lat = feature["geometry"]["coordinates"]
    assert lon == pytest.approx(-0.125)
    assert lat == pytest.approx(51.6458333)
    assert feature["properties"] == {
        "callsign": "GB7XX",
        "keeper": "G0ABC",
        "band": "2M",
        "frequency": "144.800000",
        "polarisation": "AP",
        "region": "SOUTHGATE",
        "ngr": "SE",
        "maidenhead": "IO91WP",
    }


def test_invalid_locator_falls_back_to_null_island(tmp_path):
    geo = run_transform(tmp_path, [["MB7TF", "G0ABC", "2M", "144.800000", "AP", "SOMEWHERE", "SE", "J0O2AL"]])

    assert geo["features"][0]["geometry"]["coordinates"] == [0, 0]
    assert geo["features"][0]["properties"]["maidenhead"] == "J0O2AL"


def test_multiple_rows(tmp_path):
    row = ["GB7XX", "G0ABC", "2M", "144.800000", "AP", "SOUTHGATE", "SE", "IO91WP"]
    geo = run_transform(tmp_path, [row, row])

    assert len(geo["features"]) == 2


def test_header_row_is_skipped(tmp_path):
    header = ["Callsign", "Sysop", "Band", "TX", "Type", "Where", "Region", "Locator", "lat", "lon", ""]
    row = ["GB7XX", "G0ABC", "2M", "144.800000", "AP", "SOUTHGATE", "SE", "IO91WP", "51.63", "-0.138", ""]
    geo = run_transform(tmp_path, [header, row])

    assert [f["properties"]["callsign"] for f in geo["features"]] == ["GB7XX"]
