import uvicorn
import json
from micropathforger import APP

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    TITLE = config["title"]
    PORT = config["port"]
    HOST = config["host"]
    RELOAD = config["reload"]

uvicorn.run(APP, host=HOST, port=PORT, debug=True)
