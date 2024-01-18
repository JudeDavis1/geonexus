import requests

from geopy.distance import geodesic


def main():
    pass

def get_coords(address):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={address}, Slough, UK"
    response = requests.get(url)
    # results = 


if __name__ == "__main__":
    main()