import json
import requests

from pydantic import BaseModel
from geopy.distance import geodesic


def main():
    get_coords("Northern Road")


class OSMResponse(BaseModel):
    lat: str
    lon: str
    display_name: str

def get_coords(address):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={address}, Slough, UK"
    response = requests.get(url)
    json.loads(response.json()[0])
    OSMResponse.parse_raw()


if __name__ == "__main__":
    main()