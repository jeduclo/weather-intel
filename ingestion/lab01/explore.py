import json


def describe(obj, indent=0, max_items=3):
    """Recursively print the shape of a JSON object."""
    pad = "   " * indent
    if isinstance(obj, dict):
        for key, value in obj.items():
            print(f"{pad}{key}: {type(value).__name__}", end="")
            if isinstance(value, list):
                print(f"(len={len(value)})")
            else:
                print()
            if isinstance(value, (dict, list)):
                describe(value, indent + 1, max_items)
    elif isinstance(obj, list) and obj:
        print(f"{pad}[0] sample: {obj[0]!r}")
        
with open("data/raw/paris.json") as f:
    data = json.load(f)

describe(data) 

print("Timezone:", data["timezone"])
print("Current temperature:", data["current"]["temperature_2m"],data["current_units"]["temperature_2m"])
print("Number of hourly readings:", len(data["hourly"]["time"]))
print("Max forecast temperature:", max(data["hourly"]["temperature_2m"]))