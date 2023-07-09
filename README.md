# etcc-csv-scrape

The [Radio Society of Great Britain (RSGB)]()'s [Emerging Technology Co-ordination Committee (ETCC)](https://ukrepeater.net/about.html)
publishes CSV files of assorted registrations at https://ukrepeater.net/csvfiles.html

This repository uses GitHub Actions to scrape and record these,
and transform them into [GeoJSON](https://geojson.org/) for convenience.

# Notes

* Scraping inspired by https://simonwillison.net/2020/Oct/9/git-scraping/
* Recording GeoJSON inspired by Tom M0LTE's packet map https://packetnodes.spots.radio/etcc-packet-map.html
* This uses data published by the ETCC, but is otherwise unconnected with the ETCC
