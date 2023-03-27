import json

file_name = "src/config.json"
with open(file_name, "r") as conf:
    CONFIG = json.load(conf)
