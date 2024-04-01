import csv
import pandas as pd
import folium
import webbrowser
from geopy.distance import geodesic
from heapq import nsmallest
from tkinter import *
from tkinter import messagebox
from branca.element import Template, MacroElement
from folium.plugins import FloatImage
from folium.features import DivIcon

# Caminho da lista de UC's com as localizações
LocCsv = 'analise-de-telemetrias\\Pycis\\assets\\csv\\loc_uc.csv'

# Função que pega a UC dada pelo usuário e acha a latitude e a longitude correspondente na lista de UC's
def buscar_lat_lon(uc):
    with open(LocCsv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['UC'] == uc:
                return float(row['LATITUDE']), float(row['LONGITUDE'])
    return None, None

# Encontra as 5 antenas mais próximas da UC dada
def encontrar_antenas_mais_proximas(uc_lat, uc_lon, data, n=5):
    distancias_antenas = []
    for index, row in data.iterrows():
        antena_lat = row['Latitude']
        antena_lon = row['Longitude']

        # Calcula a distância da UC até todas as antenas da lista
        distancia = geodesic((uc_lat, uc_lon), (antena_lat, antena_lon)).kilometers
        distancias_antenas.append((distancia, (antena_lat, antena_lon, row['OP'], distancia)))

    # Usa a função "nsmallest" que busca as 5 antenas com as menores distâncias da UC
    antenas_mais_proximas = nsmallest(n, distancias_antenas, key=lambda x: x[0])
    return [antena[1] for antena in
            antenas_mais_proximas]  # Retorna apenas as informações da antena, sem a distância usada para a ordenação

def calcular_ponto_medio(lat1, lon1, lat2, lon2):
    """Calcula um ponto médio aproximado entre dois pontos geográficos."""
    lat_medio = (lat1 + lat2) / 2
    lon_medio = (lon1 + lon2) / 2
    return lat_medio, lon_medio

# Caminho para a lista de antenas do Paraná
file_path = 'analise-de-telemetrias\\Pycis\\assets\\excel\\Jan24_PR.xlsx'

data = pd.read_excel(file_path)

# Função para lidar com o botão "Buscar"
def buscar():
    uc = entry.get()
    latitude_uc, longitude_uc = buscar_lat_lon(uc)

    if latitude_uc is not None and longitude_uc is not None:
        antenas_proximas = encontrar_antenas_mais_proximas(latitude_uc, longitude_uc, data)
        if antenas_proximas:
            # Centraliza o Paraná no mapa
            parana_map = folium.Map(location=[-25.2521, -52.0215], zoom_start=7)

            for antena in antenas_proximas:
                distancia_km = antena[3]

                # Informações da antena no mapa
                popup_text = f"Operadora: {antena[2]}\nDistância até a UC: {distancia_km:.2f} km"
                folium.Marker((antena[0], antena[1]), popup=popup_text, icon=folium.Icon(color='blue')).add_to(
                    parana_map)

            # Marcador da UC no mapa
            folium.Marker([latitude_uc, longitude_uc], popup=f'UC: {uc}', icon=folium.Icon(color='green')).add_to(
                parana_map)

            cores_operadoras = {
                'TIM': 'blue',
                'Claro': 'red',
                'Vivo': 'purple',
                'Sercomtel': 'orange'
            }

            for antena in antenas_proximas:
                distancia_km = antena[3]
                operadora = antena[2]
                cor_icone = cores_operadoras.get(operadora,
                                                 'gray')  # 'gray' é usado como cor padrão se a operadora não estiver no dicionário

                # Informações da antena no mapa
                popup_text = f"Operadora: {operadora}\nDistância até a UC: {distancia_km:.2f} km"
                folium.Marker(
                    (antena[0], antena[1]),
                    popup=popup_text,
                    icon=folium.Icon(color=cor_icone)  # Usa a cor correspondente à operadora
                ).add_to(parana_map)

            # Linhas ligadas na UC
            for antena in antenas_proximas:
                folium.PolyLine(locations=[(latitude_uc, longitude_uc), (antena[0], antena[1])],
                                color='red').add_to(parana_map)

                # Calcula ponto intermediário
                ponto_medio_lat, ponto_medio_lon = calcular_ponto_medio(latitude_uc, longitude_uc, antena[0],
                                                                        antena[1])
                # Distância formatada
                distancia_km = antena[3]
                texto_distancia = f"{distancia_km:.2f} km"

                # Adiciona o texto de distância no ponto intermediário usando DivIcon
                folium.map.Marker((ponto_medio_lat, ponto_medio_lon),
                                icon=DivIcon(
                                icon_size=(150, 36),
                                icon_anchor=(0, 0),
                                # Aumenta o tamanho da fonte e define a fonte para negrito
                                html=f'<div style="font-size: 12pt; font-weight: bold">{texto_distancia}</div>',
                                  )
                                  ).add_to(parana_map)

            # Template para a legenda de cores
            template = """
            {% macro html(this, kwargs) %}
            <div style="position: fixed; 
                        bottom: 50px; left: 50px; width: 150px; height: 175px; 
                        border:2px solid grey; z-index:9999; font-size:14px;
                        ">&nbsp; Legenda <br>
                        &nbsp; UC &nbsp; <i class="fa fa-map-marker fa-2x" style="color:green"></i><br>
                        &nbsp; TIM &nbsp; <i class="fa fa-map-marker fa-2x" style="color:blue"></i><br>
                        &nbsp; CLARO &nbsp; <i class="fa fa-map-marker fa-2x" style="color:red"></i><br>
                        &nbsp; VIVO &nbsp; <i class="fa fa-map-marker fa-2x" style="color:purple"></i><br>
                        &nbsp; SERCOMTEL &nbsp; <i class="fa fa-map-marker fa-2x" style="color:orange"></i>
            </div>
            {% endmacro %}
            """

            macro = MacroElement()
            macro._template = Template(template)

            parana_map.get_root().add_child(macro)

            # Caminho para a imagem da rosa dos ventos
            rosa_dos_ventos = 'imagens/rosa_dos_ventos.png'

            # Adiciona a rosa dos ventos redimensionada ao mapa
            FloatImage(rosa_dos_ventos, bottom=5, right=10, left=80, z_index=5000).add_to(parana_map)

            # Salvando o mapa
            parana_map.save(
                "analise-de-telemetrias\\Pycis\\assets\\html\\mapa_uc_e_antenas_proximas.html")

            messagebox.showinfo("UC encontrada","Mapa gerado com sucesso!")
            webbrowser.open_new_tab(
                'analise-de-telemetrias\\Pycis\\assets\\html\\mapa_uc_e_antenas_proximas.html')
        else:
            messagebox.showinfo("Erro", "Não foi possível encontrar as antenas mais próximas!")
    else:
        messagebox.showinfo("Erro", "UC não encontrada!")

def center_window(root, width=400, height=200):
    # Obtém a largura e altura da tela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calcula x e y coordenadas para posicionar a janela no centro da tela
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

# Configuração da janela principal
root = Tk()
root.title("Buscar antenas próximas")

# Define a cor de fundo da janela principal
root.configure(bg='darkblue')

center_window(root, 320, 70)

# Frame para o campo de entrada com cor de fundo azul
frame = Frame(root, bg='darkblue')
frame.pack(padx=10, pady=10)

# Campo de entrada para a UC com cor de fundo azul e texto branco
label = Label(frame, text="Digite um número de UC:", bg='darkblue', fg='white')
label.grid(row=0, column=0)

entry = Entry(frame)
entry.grid(row=0, column=1)

# Botão de busca com cor de fundo azul e texto branco
buscar_button = Button(frame, text="Buscar", bg='black', fg='white', command=buscar)
buscar_button.grid(row=1, columnspan=2, pady=5)

root.mainloop()
