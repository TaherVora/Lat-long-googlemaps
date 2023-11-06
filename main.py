# Address: Cam. Vecinal, Parque Industrial El Florido I, 22237 Tijuana, B.C., Mexico
import requests
import pandas as pd
def get_route_points(api_key, origin, destination):
    base_url = "https://maps.googleapis.com/maps/api/directions/json"

    params = {
        "origin": origin,
        "destination": destination,
        "key": api_key
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["status"] == "OK":
        route_steps = data["routes"][0]["legs"][0]["steps"]

        for step in route_steps:
            lat = step["start_location"]["lat"]
            lng = step["start_location"]["lng"]
            lat1 = step["end_location"]["lat"]
            lng1 = step["end_location"]["lng"]
            yield lat, lng, lat1, lng1
    else:
        print("Directions not found.")

# Replace with your Google Maps API key
api_key = "*******"
data=[]
origin = "Cam. Vecinal, Parque Industrial El Florido I, 22237 Tijuana, B.C., Mexico"
destination = "3225 N Harbor Dr, San Diego, CA 92101"

for lat, lng, lat1, lng1 in get_route_points(api_key, origin, destination):
    data.append({"Latitude": lat, "Longitude": lng})
    data.append({"Latitude": lat1, "Longitude": lng1})
df = pd.DataFrame(data)
print(df)
df.to_csv("routeData.csv", index=False)
print("saved successfully.")
