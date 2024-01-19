import asyncio
import sys

from src.app_config import app_config
from src.distance import get_distance_map

assert app_config.OC_API_KEY != None, "OpenCage API key doesn't exist."


async def main():
    target_road_name = sys.argv[1]

    distance_map = await get_distance_map(target_road_name)
    distance_map = sorted(distance_map.items(), key=lambda item: item[1])
    print("\nTop closest roads:")
    for road, distance in distance_map[:10]:
        print(f"\t{road}: {distance}")


if __name__ == "__main__":
    asyncio.run(main())
