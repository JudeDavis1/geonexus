import json
import aiohttp
import asyncio

from geopy.distance import geodesic
from typing import Optional
from pydantic import BaseModel
from urllib.parse import quote

from src.data import roads


async def main():
    async with aiohttp.ClientSession() as session:
        target_road = await get_osm_model(session, "Northern Road")

        for shard in make_shards(roads, 5):
            results = await asyncio.gather(*[
                get_osm_model(
                    session,
                    f"{road_string}, Slough, UK"
                ) for road_string in shard
            ])

            print(results)


class OSMResponseCoords(BaseModel):
    lat: str
    lon: str
    display_name: str

async def get_osm_model(
    session: aiohttp.ClientSession,
    search_string: str,
) -> Optional[OSMResponseCoords]:
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={quote(search_string)}"
    
    res = await session.get(url)
    if res.status != 200:
        return None
    
    data = await res.json()
    if data == []:
        return None
    
    print(1)

    return OSMResponseCoords(**data[0])

def make_shards(input_list, n):
    return [input_list[i:i + n] for i in range(0, len(input_list), n)]


if __name__ == "__main__":
    asyncio.run(main())