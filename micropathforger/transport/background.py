from aiohttp import ClientSession
from pathforger import Progression
from .caller import post_single_request
from .endpoints import ENDPOINTS
from .schemas import construct_path_transport

async def ensure_progression_bg(progression: Progression):
    session = ClientSession()
    endpoint = ENDPOINTS["microaccountant/music"]
    microaccountant_response = await post_single_request(endpoint, construct_path_transport(progression), session=session)

    await session.close()
    return microaccountant_response
