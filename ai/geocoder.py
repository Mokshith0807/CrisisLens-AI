from geopy.geocoders import Nominatim
import time

# Create geocoder
geolocator = Nominatim(
    user_agent="crisislens_ai"
)


def get_coordinates(location):
    """
    Convert a location name into latitude and longitude.
    """

    try:
        time.sleep(1)

        place = geolocator.geocode(
            location
        )

        if place:
            return (
                place.latitude,
                place.longitude
            )

        return None

    except Exception:
        return None
