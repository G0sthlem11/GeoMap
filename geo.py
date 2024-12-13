from geopy.geocoders import Nominatim
import folium
from folium.plugins import MarkerCluster
import branca

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
mymap = folium.Map(
    location=map_center, 
    zoom_start=6, 
    tiles='https://tile.jawg.io/jawg-matrix/{z}/{x}/{y}{r}.png?access-token=z2gKyqiWPtDHngPXWVSxLpd0LvoCR9J2AW1d1Icbw3cTF1QSFGCTGRhfzn2wRXdV', 
    attr='Jawg'
)
colors = {"Warehouses": "blue", "Customers": "green", "Suppliers": "red"}

marker_cluster = MarkerCluster().add_to(mymap)

for category, places in coordinates.items():
    for name, coord in places.items():
        folium.Marker(
            location=coord,
            popup=f"{name} ({category})",
            icon=folium.Icon(color=colors[category])
        ).add_to(marker_cluster)

# Step 3: Add a fancy legend to the map
legend_html = """
<div style="
    position: fixed; 
    bottom: 50px; left: 50px; width: 220px; height: 160px; 
    border: 3px solid grey; z-index: 9999; font-size: 14px;
    background: linear-gradient(to bottom, #ffffff, #e6e6e6); opacity: 0.9; border-radius: 8px;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
">
    <div style="padding: 10px;">
        <h4 style="margin-top: 0; text-align: center;">Legend</h4>
        <div style="display: flex; align-items: center; margin-top: 10px;">
            <i class="fa fa-map-marker fa-2x" style="color:lightblue"></i>
            <span style="margin-left: 10px; font-weight: bold;">Warehouses</span>
        </div>
        <div style="display: flex; align-items: center; margin-top: 10px;">
            <i class="fa fa-map-marker fa-2x" style="color:lightgreen"></i>
            <span style="margin-left: 10px; font-weight: bold;">Customers</span>
        </div>
        <div style="display: flex; align-items: center; margin-top: 10px;">
            <i class="fa fa-map-marker fa-2x" style="color:darkred"></i>
            <span style="margin-left: 10px; font-weight: bold;">Suppliers</span>
        </div>
    </div>
</div>
"""
mymap.get_root().html.add_child(folium.Element(legend_html))

# Save the map to an HTML file
mymap.save("index.html")