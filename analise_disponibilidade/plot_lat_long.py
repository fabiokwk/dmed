import folium
import random
import sqlite3

def conectar_extrair():
    with sqlite3.connect('../Aplications/proximidade_antenas') as conn:  # Added the extension of the database file
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT uc, municipio_uc, latitude_uc, longitude_uc
                        FROM ucs_grupo_a;
                       """)
        ucs = cursor.fetchall()

        cursor.execute("SELECT estacao, operadora, municipio_antena, latitude_antena, longitude_antena, tecs FROM antenas_parana")
        antenas = cursor.fetchall()

    return ucs, antenas
#chamar variáveis
ucs, antenas = conectar_extrair()

uc_list = []
uc_lat = []
uc_long = []

antena_list = []
antena_lat = []
antena_long = []

for uc in ucs:
    uc_list.append(uc[0])
    uc_lat.append(uc[2])
    uc_long.append(uc[3])

for antena in antenas:
    antena_list.append(antena[0])
    antena_lat.append(antena[3])
    antena_long.append(antena[4])

print(antena_list)
print(antena_lat)
print(antena_long)

# Create a list of dictionaries with randomly assigned 'Type'
# ucs_data = [
#     {
#         'uc': uc,
#         'Latitude': lat,
#         'Longitude': lon,
#     }
#     for uc, lat, lon in zip(uc_list, uc_lat, uc_long)
# ]


antenas_data = [
    {
        'estacao': estacao,
        'Latitude': lat,
        'Longitude': lon,
    }
    for estacao, lat, lon in zip(antena_list, antena_lat, antena_long)
]
# Create a folium map centered around the average coordinates
average_lat = sum(location['Latitude'] for location in antenas_data) / len(antena_list)
average_lon = sum(location['Longitude'] for location in antenas_data) / len(antena_list)

mymap = folium.Map(location=[average_lat, average_lon], zoom_start=6, tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', attr='My Data Attribution')

# Create separate layers for each type of location
ucs = folium.FeatureGroup(name='UC')
antenas = folium.FeatureGroup(name='Antena')

# Add markers for each location to the corresponding layer
# for location in ucs_data:
#     folium.Marker(
#         location=[location['Latitude'], location['Longitude']],
#         popup=location['uc'],
#         icon=folium.Icon(icon='home',color='orange')
#     ).add_to(ucs)

for location in antenas_data:
    latitude = location['Latitude']
    longitude = location['Longitude']
    location_tuple = (latitude, longitude)

    folium.Marker(
        location=location_tuple,
        popup=location['estacao'],
        icon=folium.Icon(icon='home',color='orange')
        # icon=folium.CircleMarker(location=location_tuple, radius=5, color='blue', fill=True, fill_color='blue', fill_opacity=1.0)
    ).add_to(antenas)



# Add the layers to the map
ucs.add_to(mymap)
antenas.add_to(mymap)

# Add LayerControl to toggle between layers
folium.LayerControl().add_to(mymap)

# Save the map to an HTML file or display it
mymap.save("my_map_with_types.html")
