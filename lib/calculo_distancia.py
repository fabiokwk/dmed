from geopy.distance import geodesic
import sqlite3
from multiprocessing import Pool, cpu_count
import time

def conectar_extrair():
    with sqlite3.connect('../Aplications/proximidade_antenas') as conn:  # Added the extension of the database file
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT uc, municipio_uc, latitude_uc, longitude_uc, macroregiao, regional
                        FROM ucs_grupo_a
                        WHERE lower(macroregiao) = lower('sdo')
                        AND NOT lower(regional) = lower('fbl')
                        OR lower(regional) = lower('pto')                      
                       ;""")
        ucs = cursor.fetchall()

        cursor.execute("SELECT estacao, operadora, municipio_antena, latitude_antena, longitude_antena, tecs FROM antenas_parana")
        antenas = cursor.fetchall()

    return ucs, antenas

def calcular_distancia(args):
    cliente, antena = args
    distancia = geodesic(cliente[2:4], antena[3:5]).km
    if distancia <= 100:
        # Database insertion code
        with sqlite3.connect('../Aplications/proximidade_antenas') as conn:
            cursor = conn.cursor()

            try:
                cursor.executemany("""
                    INSERT OR IGNORE INTO distancia_uc_antena (uc, estacao, distancia)
                    VALUES (?, ?, ?)
                """, [(cliente[0], antena[0], distancia)])

            finally:
                # Commit the changes
                conn.commit()

    return cliente[0], antena[0], distancia


def escrever_distancia(distancia_calculada):
    with sqlite3.connect('../Aplications/proximidade_antenas') as conn:
        cursor = conn.cursor()

        try:
            cursor.executemany("""
                INSERT INTO OR IGNORE distancia_uc_antena (uc, estacao, distancia)
                VALUES (?, ?, ?)
            """, distancia_calculada)

        finally:
            # Commit the changes
            conn.commit()

    
def __main__():
    print('começou o main')
    inicio = time.time()
    print('começou o cronometro')
    ucs, antenas = conectar_extrair()
    print('começou o conectar_extrair')
    # lista de argumentos para cada combinação de cliente e antena
    args_list = [(cliente, antena) for cliente in ucs for antena in antenas]

    # pool de processos para calcular distâncias em paralelo
    num_cores = cpu_count()
    print(len(ucs))
    print(len(antenas))
    print(num_cores)

    input('continuar?')
    with Pool(processes=4) as pool:
        resultados = pool.map(calcular_distancia, args_list)

    # distâncias 
    ucs_com_antena_proxima = []
        
    for distancia_calculada in resultados:
        ucs_com_antena_proxima.append(distancia_calculada)
        print(distancia_calculada)  

    print('terminou o calculo')
    print(f"Total de resultados: {len(ucs_com_antena_proxima)}")

   

    fim = time.time()
    tempo_total = fim - inicio
    print(f"Tempo total de execução: {tempo_total:.2f} segundos")

if __name__ == '__main__':
    __main__()
