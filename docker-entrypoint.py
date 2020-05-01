import json
import os
import pathlib
import subprocess


cwd = pathlib.Path().cwd()

# Write config to file
config = {
    "api_key": os.environ["API_KEY"],
    "workspace": os.environ["WORKSPACE"],
    "start_date": os.environ.get("START_DATE") or "2020-01-01T00:00:00Z"
}
cwd.joinpath("config.json").write_text(json.dumps(config))

# Run discovery and write default catalog
catalog = subprocess.run(
    ["tap-clockify", "-c", "config.json", "--discover"],
    capture_output=True
)
cwd.joinpath("catalog.json").write_text(catalog.stdout.decode("utf-8"))


# Run the tap and save output to file
tap = subprocess.run(
    ["tap-clockify", "-c", "config.json", "--catalog", "catalog.json"],
    capture_output=True
)
cwd.joinpath("tap_output.txt").write_text(tap.stdout.decode("utf-8"))
