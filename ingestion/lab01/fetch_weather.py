import json
from pathlib import Path

import requests

URL = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 48.85,
    "longitude": 2.35,
    "current": "temperature_2m,wind_speed_10m",
    "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    "timezone": "auto",
    "forecast_days": 3,
}

response = requests.get(URL, params=params, timeout=30)
print("Status code:", response.status_code)
response.raise_for_status()

data = response.json()

out = Path("data/raw/paris.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(data, indent=2))
print(f"Saved {out} ({out.stat().st_size} bytes)")