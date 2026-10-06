import json
from pathlib import Path


raw = '{"city": "Paris", "temps": [18.2, 19.5, null], "sunny": true}'

data = json.loads(raw)

print(type(data))
print(data["city"])
print(data["temps"][1])
print(data["temps"][2])

data["country"] = "France"
print(json.dumps(data, indent=4))


out = Path("data/raw/sample.json")
out.parent.mkdir(parents=True, exist_ok=True)

with open(out, "w") as f:
    json.dump(data, f, indent=2)
    
with open(out) as f:
    loaded = json.load(f)
    
print(loaded == data)