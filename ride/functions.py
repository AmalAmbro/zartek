from geopy.distance import geodesic

from ride.models import *



def find_available_drivers():
    available_drivers = User.objects.filter(is_driver=True, rides_as_driver__isnull=True)
    return available_drivers

def calculate_distance(driver_location, pickup_location):
    distance = geodesic(driver_location, pickup_location).kilometers
    return distance

def match_ride_with_driver(ride):
    available_drivers = find_available_drivers()

    if not available_drivers:
        return None

    best_driver = None
    min_distance = float('inf')

    for driver in available_drivers:
        driver_location = driver.location
        distance = calculate_distance(driver_location, ride.pickup_location)
        
        # Update best driver if closer than previous best
        if distance < min_distance:
            min_distance = distance
            best_driver = driver

    return best_driver

