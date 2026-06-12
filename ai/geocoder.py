from geopy.geocoders import Nominatim
import time

geolocator = Nominatim(user_agent="crisislens-ai")


def get_coordinates(location):
    try:
        loc = geolocator.geocode(location)
        time.sleep(1)
        if loc:
            return loc.latitude, loc.longitude
        return None, None
    except:
        return None, None
