import json
import os
import subprocess


# Write config to file
config = {
    "api_key": os.environ["API_KEY"],
    "workspace": os.environ["WORKSPACE"],
    "start_date": os.environ.get("START_DATE") or "2020-01-01T00:00:00Z"
}
with open("config.json", "w") as f:
    f.write(json.dumps(config))

# Run discovery and write default catalog
catalog = subprocess.run(
    ["tap-clockify", "-c", "config.json", "--discover"],
    capture_output=True
)
with open("catalog.json", "w") as f:
    f.write(catalog.stdout.decode("utf-8"))


# Run the tap and print to Docker logs
subprocess.run(
    ["tap-clockify", "-c", "config.json", "--catalog", "catalog.json"]
)