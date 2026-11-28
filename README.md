# etcc-csv-scrape

The [Radio Society of Great Britain (RSGB)]()'s [Emerging Technology Co-ordination Committee (ETCC)](https://ukrepeater.net/about.html)
publishes CSV files of assorted registrations at https://ukrepeater.net/csvfiles.html

This repository uses GitHub Actions to scrape and record these,
and transform them into [GeoJSON](https://geojson.org/) for convenience.

> [!NOTE]
> Since 2026-10-26, ukrepeater.net has not served the CSV to automated requests,
> so the data here is from the last successful fetch.

See the data in map form at https://github.com/doismellburning/packet-map/ / https://doismellburning.github.io/packet-map/etcc-packet-map.html,
or copy-paste it into https://geojson.io/ for exploration.

# Notes

* Scraping inspired by https://simonwillison.net/2020/Oct/9/git-scraping/
* Recording GeoJSON inspired by Tom M0LTE's packet map https://packetnodes.spots.radio/etcc-packet-map.html
* This uses data published by the ETCC, but is otherwise unconnected with the ETCC

# Development

Uses [uv](https://docs.astral.sh/uv/), based on https://github.com/doismellburning/python-template

* `make bootstrap` to install dependencies
* `make check` to run formatting, lint and type checks (`make fix` to auto-fix)
* `make test` to run tests with coverage
