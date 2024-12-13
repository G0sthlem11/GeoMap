from geopy.geocoders import Nominatim
import folium
from folium.plugins import MarkerCluster

# Step 1: Geocode the locations
locations = {
    "Warehouses": {
        "North Warehouse": "Seattle, WA",
        "Central Warehouse": "San Diego, CA"
    },
    "Customers": {
        "S-Mart": "Malibu, CA",
        "Auto Bros": "Long Beach, CA",
        "Car Fix": "Tijuana, Mexico",
        "CostKing": "San Francisco, CA"
    },
    "Suppliers": {
        "Oilco": "Tecate, Mexico",
        "Packit": "Indio, CA",
        "Corrugated": "Tijuana, Mexico"
    }
}

geolocator = Nominatim(user_agent="geomap_creator")
coordinates = {}

for category, places in locations.items():
    coordinates[category] = {}
    for name, address in places.items():
        location = geolocator.geocode(address)
        if location:
            coordinates[category][name] = (location.latitude, location.longitude)

# Step 2: Create the map
map_center = [36.7783, -119.4179]  # California center
mymap = folium.Map(location=map_center, zoom_start=6, tiles='https://tile.jawg.io/jawg-matrix/{z}/{x}/{y}{r}.png?', attr='Jawg')

colors = {"Warehouses": "blue", "Customers": "green", "Suppliers": "red"}

marker_cluster = MarkerCluster().add_to(mymap)

for category, places in coordinates.items():
    for name, coord in places.items():
        folium.Marker(
            location=coord,
            popup=f"{name} ({category})",
            icon=folium.Icon(color=colors[category])
        ).add_to(marker_cluster)

# Save the map to an HTML file
mymap.save("index.html")