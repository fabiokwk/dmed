'''


'''

import pandas as pd
import threading
import queue
import time
import numpy as np

# Marcando o tempo
start_time = time.time()

# Caminhos
loc_uc = r"C:\Users\L805958\Documents\analise-de-telemetrias\Pycis\assets\csv\test_uc.csv"
antenas_pr = r"C:\Users\L805958\Documents\analise-de-telemetrias\Pycis\assets\excel\Jan24_PR.xlsx"

# dataFrames
ucs_df = pd.read_csv(loc_uc, delimiter=',')
antenas_df = pd.read_excel(antenas_pr)

# Extrai coordenadas
ucs_coords = ucs_df[['LATITUDE', 'LONGITUDE']].to_numpy()
antenas_coords = antenas_df[['Latitude', 'Longitude']].to_numpy()

# Função que calcula as distancias
def calcula_dist(lat1, lon1, lat2, lon2):

    # Converte coordenadas de graus para radianos
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    # Fórmula de Haversine
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6371 * c
    return km


def worker(uc_queue, resultados):
    while not uc_queue.empty():
        try:
            uc_index = uc_queue.get_nowait()
        except queue.Empty:
            break

        uc_coords = ucs_coords[uc_index]
        distancias = calcula_dist(uc_coords[0], uc_coords[1], antenas_coords[:, 0], antenas_coords[:, 1])
        closest_idxs = np.argsort(distancias)[:3]
        uc_id = ucs_df.iloc[uc_index]['UC']
        mais_de_5km = "Sim" if distancias[closest_idxs[0]] > 5 else "Não"
        resultados.append([uc_id, *antenas_df.iloc[closest_idxs]['OP'].values, mais_de_5km])

        uc_queue.task_done()

# Preparação e execução das threads
uc_queue = queue.Queue()
for i in range(len(ucs_df)):
    uc_queue.put(i)

resultados = []


n_threads = 14
threads = []

for _ in range(n_threads):
    thread = threading.Thread(target=worker, args=(uc_queue, resultados))
    thread.start()
    threads.append(thread)


for thread in threads:
    thread.join()


# Finalização e salvamento dos resultados
final_df = pd.DataFrame(resultados, columns=['UC', 'OP1', 'OP2', 'OP3', 'Mais de 5km'])
final_df.to_excel(r'C:\Users\L805958\Documents\analise-de-telemetrias\Pycis\assets\excel\resultado_antenas_proximas.xlsx', index=False)

end_time = time.time()
total_time = end_time - start_time

print(final_df.head())
print(f"Tempo total: {total_time} segundos")
