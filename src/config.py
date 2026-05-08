import yaml

def load_config(path="config/search_profile.yaml"):
    with open(path, "r") as file:
        return yaml.safe_load(file)