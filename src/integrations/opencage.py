from typing import Optional
from urllib.parse import quote

import aiohttp
from pydantic import BaseModel

from src.app_config import app_config


class OCGeometry(BaseModel):
    lat: float
    lng: float


class RoadData(BaseModel):
    geometry: OCGeometry
    formatted: str


async def get_oc_model(
    session: aiohttp.ClientSession,
    search_string: str,
) -> Optional[RoadData]:
    url = f"https://api.opencagedata.com/geocode/v1/json?q={quote(search_string)}&key={app_config.OC_API_KEY}"

    res = await session.get(url)
    if res.status != 200:
        return None

    data = await res.json()
    if not data["results"]:
        return None

    oc_res = RoadData(**data["results"][0])
    return oc_res
