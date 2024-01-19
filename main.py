import asyncio
import ssl

import aiohttp
import certifi
from geopy.distance import geodesic

from src.app_config import app_config
from src.data import roads
from src.integrations.opencage import RoadData, get_oc_model

assert app_config.OC_API_KEY != None, "OpenCage API key doesn't exist."

DistanceMap = dict[str, float]


async def main():
    # Use an ssl context for requests
    distance_map = dict()
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl_context)
    ) as session:
        target_road = await get_oc_model(session, "Northern Road, Slough")

        # Process 10 shards of roads concurrently
        for shard in make_shards(roads, 10):
            # Concurrently generate
            request_routines = [
                get_oc_model(session, f"{road_string}, Slough, UK")
                for road_string in shard
            ]
            request_results = await asyncio.gather(*request_routines)

            distance_routines = [
                get_distance_from_target(result, target_road)
                for result in request_results
            ]
            distance_results = await asyncio.gather(*distance_routines)

            # Update the distance map
            for d in distance_results:
                distance_map.update(d)

    distance_map = sorted(distance_map.items(), key=lambda item: item[1])
    print("\nTop closest roads:")
    for road, distance in distance_map[:10]:
        print(f"\t{road}: {distance}")


async def get_distance_from_target(
    road_data: RoadData,
    target: RoadData,
) -> DistanceMap:
    distance = geodesic(
        (road_data.geometry.lat, road_data.geometry.lng),
        (target.geometry.lat, target.geometry.lng),
    ).miles

    return {road_data.formatted: distance}


def make_shards(input_list, n):
    """
    Make list of sharded inputs,
    where each shard is of length `n` (the remainder is retained).
    """

    return [input_list[i : i + n] for i in range(0, len(input_list), n)]


if __name__ == "__main__":
    asyncio.run(main())
