"""Ingest landast data

Usage: python ingest_landsat.py http://localhost:8082
"""
import json
import sys
from pathlib import Path
from urllib.parse import urljoin
import os
import requests

workingdir = Path(__file__).parent.absolute()
landsatdata = workingdir.parent / "stac_fastapi" / "testdata" / "landsat"

app_host = sys.argv[1]

if not app_host:
    raise Exception("You must include full path/port to stac instance")


def post_or_put(url: str, data: dict):
    """Post or put data to url."""
    r = requests.post(url, json=data)
    if r.status_code == 409:
        new_url = url if data["type"] == "Collection" else url + f"/{data['id']}"
        # Exists, so update
        r = requests.put(new_url, json=data)
        # Unchanged may throw a 404
        if not r.status_code == 404:
            r.raise_for_status()
    else:
        r.raise_for_status()


def ingest_landsat_data(app_host: str = app_host, data_dir: Path = landsatdata):
    """ingest data."""

    with open(data_dir / "landsat-c2l1.json") as f:
        collection = json.load(f)

    post_or_put(urljoin(app_host, "/collections"), collection)

    scenes = os.listdir(data_dir / "items")

    for scene in scenes:
        print(scene)
        with open(data_dir / f"items/{scene}") as f:
            feat = json.load(f)
            post_or_put(urljoin(app_host, f"collections/{collection['id']}/items"), feat)


if __name__ == "__main__":
    ingest_landsat_data()
