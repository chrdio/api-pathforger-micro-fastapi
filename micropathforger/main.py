import json
import time
from fastapi import FastAPI, BackgroundTasks, Request
from pathforger import getProgression, fixProgression, GRAPH_DICT, NODES, Progression
from transport import ensure_progression_bg, ProgressionRequest

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    TITLE = config["title"]
    PORT = config["port"]
    HOST = config["host"]
    RELOAD = config["reload"]

app = FastAPI(
    docs_url="/",
    title=TITLE,
)
@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = round((time.time() - start_time) * 10**6)
    print(f"Process time: {process_time}µs")
    return response


@app.post("/generate/{length}")
def generate_progression(
    length: int,
    request: ProgressionRequest,
    background_tasks: BackgroundTasks,
    ):
    progression = getProgression(length, GRAPH_DICT[request.graph], NODES)
    background_tasks.add_task(ensure_progression_bg, progression)
    return progression


@app.post("/amend/{index}")
def amend_progression(
    index: int,
    progression: Progression,
    background_tasks: BackgroundTasks,
    ):
    return_progression = fixProgression(progression, index, GRAPH_DICT[progression.graph], NODES)
    background_tasks.add_task(ensure_progression_bg, return_progression)
    
    return return_progression


if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=RELOAD, debug=True)
