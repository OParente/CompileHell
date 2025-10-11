import json, os

def load_scene(path):
    # minimal loader: treat .resxx as JSON for template purposes
    with open(path, 'r') as f:
        data = json.load(f)
    return data
