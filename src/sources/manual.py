import json

def get_jobs(path="data/manual_jobs.json"):
    with open(path, "r") as file:
        return json.load(file)