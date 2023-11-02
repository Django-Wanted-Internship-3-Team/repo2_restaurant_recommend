import math

####################
# Distance between two points
####################


def lat_lon_to_km(point_1: list, point_2: list) -> float:
    lat1 = float(point_1[1])
    lon1 = float(point_1[0])
    lat2 = float(point_2[1])
    lon2 = float(point_2[0])

    R = 6371
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c
