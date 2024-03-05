import folium
import sqlite3
import json


def conectar_extrair():
    input_municipio = input("Enter the municipality: ").strip()

    # Connect to the SQLite database
    with sqlite3.connect('../Aplications/proximidade_antenas') as conn:
        cursor = conn.cursor()

        # Retrieve data from the 'ucs_grupo_a' table
        cursor.execute("""
            SELECT uc, municipio_uc, latitude_uc, longitude_uc
            FROM ucs_grupo_a;
        """)
        ucs = cursor.fetchall()

        # Retrieve data from the 'antenas_parana' table
        cursor.execute("""
            SELECT estacao, latitude_antena, longitude_antena
            FROM antenas_parana
            WHERE lower(municipio_antena) = ?;
        """, (input_municipio.lower(),))  # Pass input as a parameter

        antenas = cursor.fetchall()

    return ucs, antenas



# Call the function to get ucs and antenas
ucs, antenas = conectar_extrair()

# Create a list of dictionaries containing station data
antenas_data = [
    {
        'estacao': estacao,
        'Latitude': lat,
        'Longitude': lon,
    }
    for estacao, lat, lon in antenas
]

# Initialize a Folium map
my_map = folium.Map(location=[-23.49239, -50.62056], zoom_start=6, tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', attr='My Data Attribution')

# Add markers (icons) for each station
for location in antenas_data:
    folium.Marker(
        location=[location['Latitude'], location['Longitude']],
        popup=location['estacao'],
        icon=folium.Icon(icon='cloud')  # You can customize the icon here
    ).add_to(my_map)

# Add a layer control to the map
folium.LayerControl().add_to(my_map)

# Save the map as an HTML file
my_map.save('antenas_parana.html')
