"""Deserializes json-file into registry of valid endpoint objects."""

import json
from .schemas import Endpoint

with open(".endpoints.json", "r") as endpoints_file:
    endpoints = json.load(endpoints_file)
    ENDPOINTS = {endpoint["name"]: Endpoint(**endpoint) for endpoint in endpoints}
