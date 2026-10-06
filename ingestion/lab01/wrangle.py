import json

def columns_to_records(columns: dict) -> list[dict]:
    """Turn {'a': [1, 2], 'b': [3, 4]} into [{'a': 1, 'b': 3}, {'a': 2, 'b': 4}]."""
    keys = list(columns.keys())
    return [dict(zip(keys, row)) for row in zip(*columns.values())]


def enrich(record: dict, city: str, data: dict) -> dict:
    date, hour = record["time"].split("T")
    temp_c = record.get("temperature_2m")
    return {
        "city": city,
        "latitude": data["latitude"],
        "longitude": data["longitude"],
        "timestamp": record["time"],
        "date": date,
        "hour": int(hour.split(":")[0]),
        "temperature_c": temp_c,
        "temperature_f": round(temp_c * 9 / 5 + 32, 1) if temp_c is not None else None,
        "humidity_pct": record.get("relative_humidity_2m"),
        "wind_kmh": record.get("wind_speed_10m"),
    }
    
def quality_report(records: list[dict]) -> dict:
    report = {}
    for field in records[0].keys():
        missing = sum(1 for r in records if r[field] is None)
        report[field] = missing
    return report


if __name__=="__main__":
    with open("data/raw/paris.json") as f:
        data = json.load(f)
    
    records = columns_to_records(data["hourly"])
    print(f"{len(records)} records")
    print(json.dumps(records[:2], indent=2))
    
    clean = [enrich(r, "Paris", data) for r in records]
    print(json.dumps(clean[0], indent=2))
    
    print("Quality report:", quality_report(clean))
    