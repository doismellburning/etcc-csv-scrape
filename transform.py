import csv
import json
import sys
import maidenhead as mh


def transform(infile, outfile):
    features = []

    with open(infile) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            callsign = row[0]
            keeper = row[1]
            band = row[2]
            frequency = row[3]
            polarisation = row[4]
            region = row[5]
            ngr = row[6]
            maidenhead = row[7]

            print(f"Processing {callsign} at {maidenhead}")

            lat, lon = mh.to_location(maidenhead, center=True)

            feature = {
                "type": "Feature",
                "geometry": {
                    "coordinates": [lon, lat],
                    "type": "Point",
                },
                "properties": {
                    "callsign": callsign,
                    "keeper": keeper,
                    "band": band,
                    "frequency": frequency,
                    "polarisation": polarisation,
                    "region": region,
                    "ngr": ngr,
                    "maidenhead": maidenhead,
                },
            }

            features.append(feature)

    geo = {
        "type": "FeatureCollection",
        "features": features,
    }

    with open(outfile, "w") as jsonfile:
        json.dump(geo, jsonfile)

    print(f"Written GeoJSON to {outfile}")


if __name__ == "__main__":
    transform(sys.argv[1], sys.argv[2])
