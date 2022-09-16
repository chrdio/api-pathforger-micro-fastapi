import uvicorn
import json
from micropathforger import APP

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    TITLE = config["title"]
    PORT = config["port"]
    HOST = config["host"]
    RELOAD = config["reload"]
APP.title = TITLE

if __name__ == "__main__":
    uvicorn.run(
        "main:APP",
        host=HOST,
        port=PORT,
        reload=RELOAD,
        debug=True,
        )
