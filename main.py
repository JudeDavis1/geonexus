import os
import time
import json
import aiohttp
import asyncio

from dotenv import load_dotenv, find_dotenv
from geopy.distance import geodesic
from typing import Optional
from pydantic import BaseModel
from urllib.parse import quote

from src.data import roads


load_dotenv(find_dotenv('.env'))

API_KEY = os.getenv("OC_API_KEY")
assert API_KEY != None

async def main():
    async with aiohttp.ClientSession() as session:
        target_road = await get_oc_model(session, "Northern Road")

        start = time.time()
        for shard in make_shards(roads, 5):
            routines = [
                get_oc_model(
                    session,
                    f"{road_string}, Slough, UK"
                ) for road_string in shard
            ]
            results = await asyncio.gather(*routines)
        
        end = time.time()
        print("ASYNC")
        print(end - start)

        start = time.time()
        for shard in make_shards(roads, 5):
            for road_string in shard:
                await get_oc_model(
                    session,
                    f"{road_string}, Slough, UK"
                )
        
        end = time.time()

        print("SYNC")
        print(end - start)

class OCGeometry(BaseModel):
    lat: float
    lng: float

class OCResponse(BaseModel):
    geometry: OCGeometry
    formatted: str

async def get_oc_model(
    session: aiohttp.ClientSession,
    search_string: str,
) -> Optional[OCResponse]:
    url = f"https://api.opencagedata.com/geocode/v1/json?q={quote(search_string)}&key={API_KEY}"
    
    res = await session.get(url)
    if res.status != 200:
        return None
    
    data = await res.json()
    if not data["results"]:
        return None
    
    oc_res = OCResponse(**data["results"][0])
    return oc_res

def make_shards(input_list, n):
    return [input_list[i:i + n] for i in range(0, len(input_list), n)]


if __name__ == "__main__":
    asyncio.run(main())