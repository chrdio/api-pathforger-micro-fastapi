import time
from fastapi import FastAPI, BackgroundTasks, Request, Response
from pathforger import getProgression, fixProgression, GRAPH_DICT, NODES, Progression
from chrdiotypes.musical import ProgressionRequest
from ..transport import register_with_database


app = FastAPI(
    docs_url="/",
)


@app.middleware("http")
async def add_process_time(request: Request, call_next):
    """Spits out the processing time for every request."""

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
    ) -> Progression:
    """Generates a pathforger-native Progression object
    based on options specified in a request.
    Returns it and then
    registers it with the database microservice.
    """

    progression = getProgression(length, GRAPH_DICT[request.graph.value], NODES)
    background_tasks.add_task(register_with_database, progression)
    return progression


@app.post("/amend/{index}")
def amend_progression(
    index: int,
    progression: Progression,
    background_tasks: BackgroundTasks,
) -> Progression:
    """Re-generates a node under the specified index
    in the specified pathforger-native Progression object.
    Returns the result and then
    registers it with the database microservice.
    """
    return_progression = fixProgression(
        progression, index, GRAPH_DICT[progression.graph.value], NODES
    )
    background_tasks.add_task(register_with_database, return_progression)

    return return_progression


@app.get("/healthcheck")
async def healthcheck():
    """An enpoint to make sure this instance is up-and-running."""
    return Response(status_code=200)
