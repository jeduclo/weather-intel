import csv
import json
from collections import defaultdict
from pathlib import Path

import requests

from wrangle import columns_to_records, enrich

URL = "https://api.open-meteo.com/v1/forecast"

CITIES = [
    {"name": "Paris", "latitude": 48.85, "longitude": 2.35},
    {"name": "Tokyo", "latitude": 35.68, "longitude": 139.69},
    {"name": "Nairobi", "latitude": -1.29, "longitude": 36.82},
    {"name": "New York", "latitude": 40.71, "longitude": -74.01},
    {"name": "Sydney", "latitude": -33.87, "longitude": 151.21},
]

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/processed")


def extract(city: dict) -> dict:
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "auto",
        "forecast_days": 3,
    }
    resp = requests.get(URL, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # Always keep the untouched raw copy
    slug = city["name"].lower().replace(" ", "_")
    (RAW_DIR / f"{slug}.json").write_text(json.dumps(data))
    return data


def transform(city: dict, data: dict) -> list[dict]:
    return [enrich(r, city["name"], data) for r in columns_to_records(data["hourly"])]


def load(records: list[dict]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # JSON Lines: one JSON object per line (great for big data & streaming)
    with open(OUT_DIR / "weather_hourly.jsonl", "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    # CSV: opens in Excel / Google Sheets
    with open(OUT_DIR / "weather_hourly.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)


def summarize(records: list[dict]) -> None:
    temps = defaultdict(list)
    for r in records:
        if r["temperature_c"] is not None:
            temps[r["city"]].append(r["temperature_c"])

    print(f"\n{'City':<10} {'Min':>6} {'Max':>6} {'Avg':>6}")
    print("-" * 31)
    for city, values in sorted(temps.items()):
        avg = sum(values) / len(values)
        print(f"{city:<10} {min(values):>6.1f} {max(values):>6.1f} {avg:>6.1f}")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    all_records = []
    for city in CITIES:
        print(f"Fetching {city['name']}...")
        data = extract(city)
        all_records.extend(transform(city, data))
    load(all_records)
    print(f"\nSaved {len(all_records)} records to {OUT_DIR}/")
    summarize(all_records)


if __name__ == "__main__":
    main()