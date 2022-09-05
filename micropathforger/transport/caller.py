from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from aiohttp import ClientSession
from .endpoints import Endpoint


async def post_single_request(
    endpoint: Endpoint, payload: BaseModel, *, session: ClientSession
):
    serializable = jsonable_encoder(payload)
    async with session.post(
        str(endpoint), json=serializable, raise_for_status=True
    ) as response:
        # Tests provide no remote server connection
        return await response.text()  # pragma: no cover
