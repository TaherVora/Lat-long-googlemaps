import requests
import polyline
import math
import folium
import csv
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance
def interpolate_coordinates(lat1, lon1, lat2, lon2, fraction):
    """Interpolate between two coordinates"""
    return lat1 + fraction * (lat2 - lat1), lon1 + fraction * (lon2 - lon1)
def generate_coordinates_for_segment(lat1, lon1, lat2, lon2, speed_kph, freq_seconds):
    """Generate coordinates for a segment of the path"""
    segment_distance = haversine_distance(lat1, lon1, lat2, lon2)
    total_time_for_segment = (segment_distance / speed_kph) * 3600  # in seconds
    num_points = int(total_time_for_segment / freq_seconds)
    return [interpolate_coordinates(lat1, lon1, lat2, lon2, i / num_points) for i in range(num_points)]
def get_route_coordinates_via_polyline(origin, destination, api_key, speed_kph, freq_seconds):
    endpoint = "https://maps.googleapis.com/maps/api/directions/json?"
    nav_request = "origin={}&destination={}&key={}".format(origin, destination, api_key)
    request = endpoint + nav_request
    response = requests.get(request).json()
    # Extract and decode the overview_polyline
    if not response.get('routes'):
        return []
    encoded_polyline = response['routes'][0]['overview_polyline']['points']
    decoded_path = polyline.decode(encoded_polyline)
    # Iterate over path and generate coordinates
    coords = []
    for i in range(1, len(decoded_path)):
        segment_coords = generate_coordinates_for_segment(decoded_path[i - 1][0], decoded_path[i - 1][1],
                                                          decoded_path[i][0], decoded_path[i][1],
                                                          speed_kph, freq_seconds)
        coords.extend(segment_coords)
    return coords
def save_to_csv(coords, filename="coordinates_ht_mx_fdx_tenesse_30secs.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Latitude", "Longitude"])  # Writing the headers
        writer.writerows(coords)
api_key = "api-key"
origin = "Hyundai Translead Tijuana Plant, Cam. Vecinal, Parque Industrial El Florido I, 22237 Tijuana, B.C., Mexico"
destination = "FedEx, 2810 Democrat Rd, Memphis, TN 38118, United States"
speed_kph = 100  # Average speed
freq_seconds = 30
coords = get_route_coordinates_via_polyline(origin, destination, api_key, speed_kph, freq_seconds)
for coord in coords:
    print(coord)
print(len(coords))
m = folium.Map(location=[(coords[0][0] + coords[-1][0]) / 2, (coords[0][1] + coords[-1][1]) / 2], zoom_start=7)
folium.PolyLine(coords, color="blue", weight=2.5, opacity=1).add_to(m)
m.save("route_map2.html")
save_to_csv(coords, "coordinates_ht_mx_fdx_tenesse_60secs.csv")