import folium
from folium.plugins import HeatMap

m = folium.Map(location=[-37.8285827, 145.0100285], zoom_start=13)

# Example data: [latitude, longitude, intensity]
heat_data = [
    [-37.821070, 145.036259, 0.6],
    [-37.818925, 145.036883, 0.8],
    [-37.822064, 145.023185, 0.9],
]

HeatMap(heat_data).add_to(m)

# Save or display
m.save("heatmap.html")

