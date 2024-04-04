''' 
BUSCADOR DE LAT E LONG DE UC USANDO A SERIAL/NIO

O código basicamente usa SELENIUM e PYAUTOGUI para buscar no HEMERA a latitude e a longitude de uma UC.

Entra no site HEMERA, logga e vai clicando até encontrar a barra de pesquisa por serial. Ao encontrar, coloca uma lista de NIOS
que o programa pega do arquivo "busca_ucs.txt" e formata tudo junto e separado por ";" e pesquisa encontrando as UCs, vai clicando
e encontrando o numero da UC, latitude e longitude e armazenando em listas (pega também o nio e vai excluindo da lista no arquivo txt). Quando encerra, salva em um arquivo xlsx "ucs_encontradas.xlsx".
O log fica no arquivo log_uc_hemera, com o tempo e a conclusao de cada numero da lista.
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os.path import basename
import time
import pyautogui as py
import logging
import sys
import pyperclip
import pandas as pd
import openpyxl
from time import sleep
import subprocess
import os
velocidade = 0.7
stop_thread = False
tempo_limite_espera = 10
global ucs, latitudes, longitudes, UCs

ucs = []
latitudes = []
longitudes = []
UCs = ''
# Marcando o tempo
start_time = time.time()


logging.basicConfig(filename='log_uc_hemera.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


def verificar_tela(imagem, precisao):
    while True:
        sleep(velocidade)
        try:
            tela_encontrada = py.locateOnScreen(imagem, confidence=precisao)
            if tela_encontrada is not None:
                nome_imagem = basename(imagem)

                print(f"A tela {nome_imagem} foi encontrada.")
                py.moveTo(tela_encontrada)  # Move o cursor para o local da imagem encontrada
                return True
        except py.ImageNotFoundException:
            # Imagem não encontrada, continue tentando

            print(f"A tela {basename(imagem)} não foi encontrada, tentando novamente...")
            sleep(velocidade)  # Espera um pouco antes de tentar novamente
        except Exception as e:

            print(f"Ocorreu um erro: {e}")
            break  # Outras exceções podem indicar um problema que requer atenção

def localiza(DIRETORIO, precisao):
    tela_encontrada = False
    while not tela_encontrada:
        tela_encontrada = verificar_tela(DIRETORIO, precisao)
        if not tela_encontrada:

            print('Tentando novamente...')
            sleep(velocidade)

def nverificar_tela(imagem, precisao):
    try:
        tela_encontrada = py.locateOnScreen(imagem, confidence=precisao)
        if tela_encontrada is not None:
            print(f"A tela {basename(imagem)} foi encontrada.")
            py.moveTo(tela_encontrada)
            return True
    except py.ImageNotFoundException:
        print(f"A tela {basename(imagem)} não foi encontrada.")
    except Exception as e:
        print(f"Ocorreu um erro ao verificar a imagem: {e}")
    return False

# Ajuste na função 'nlocaliza' para usar 'nverificar_tela'
def nlocaliza(DIRETORIO, precisao):
    return nverificar_tela(DIRETORIO, precisao)

def stop_alterar():
    global stop_thread
    stop_thread = not stop_thread
    sys.exit()


def remover_linha_por_serial(arquivo_nome, serial):
    linhas_removidas = 0
    diretorio, nome_arquivo = os.path.split(arquivo_nome)  # Separa o diretório e o nome do arquivo
    temp_arquivo_nome = os.path.join(diretorio, 'temp_' + nome_arquivo)  # Cria caminho para o arquivo temporário no mesmo diretório

    with open(arquivo_nome, 'r') as arquivo_orig, open(temp_arquivo_nome, 'w') as arquivo_temp:
        for linha in arquivo_orig:
            if linha.strip() != serial:
                arquivo_temp.write(linha)
            else:
                linhas_removidas += 1

    # Substitui o arquivo original pelo temp
    os.replace(temp_arquivo_nome, arquivo_nome)
    if linhas_removidas > 0:
        print(f"Serial {serial} removido.")

def modificar_lista_uc(conteudo):
    # Remover espaços em branco e quebras de linha no início e fim, e dividir por quebras de linha
    ucs = conteudo.strip().split('\n')

    # Juntar as UCs usando ";" como separador
    ucs_modificadas = ';'.join(ucs)

    return ucs_modificadas

def verifica_e_encerra():
    # Verifica se o arquivo 'busca_ucs.txt' está vazio
    with open(r'assets\txt\busca_ucs.txt', 'r') as arquivo:
        if arquivo.read().strip() == '':
            # Se o arquivo estiver vazio, chama a função 'encerra'
            print("Lista vazia!" )
            stop_alterar()
        else:
            print('A lista não está vazia!')



def salvar_df():
    df = pd.DataFrame({
        'UC': ucs,
        'LATITUDE': latitudes,
        'LONGITUDE': longitudes
    })

    print(df)
    file_path = r'assets\excel\ucs_encontradas.xlsx'
    df.to_excel(file_path, index=False)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Tempo total: {total_time} segundos")
    logging.info(f"Tempo de execução:{total_time}")
    stop_alterar()

def main():
    verifica_e_encerra()
    options = Options()
    driver = webdriver.Firefox(options=options)
    # URL de login
    url_login = "http://10.4.6.237:8080/hemera/loginHemera.jsp"

    # Dados de login
    login = 'Robo1'
    senha = 'Sangue@laranja'

    # Abrir URL de login
    driver.get(url_login)

    # Localizar e preencher o campo de login
    campo_login = driver.find_element(By.NAME, "username")
    campo_login.clear()
    campo_login.send_keys(login)

    # Localizar e preencher o campo de senha
    campo_senha = driver.find_element(By.NAME, "password")
    campo_senha.clear()
    campo_senha.send_keys(senha)

    # Localizar e clicar no botão de login
    botao_login = driver.find_element(By.ID, "divCenterButton")
    botao_login.click()

    time.sleep(3)

    # Aguarde até que o primeiro botão esteja visível e clique nele
    botao_1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ext-gen104"))
    )
    botao_1.click()

    # Pode ser necessário adicionar uma espera explícita para garantir que a página ou elemento tenha tempo para responder
    time.sleep(2)  # Ajuste este tempo conforme necessário

    # Aguarde até que o segundo botão esteja visível e clique nele
    botao_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ext-gen56"))
    )
    botao_2.click()

    sleep(0.4)
    localiza(r'assets\imgs\ladon\med_hemera.png', 0.8)
    py.move(-27, -12)
    sleep(0.3)
    py.click()
    # procura_ucs(UCs)

        # Utiliza as UCs modificadas como antes
    localiza(r'assets\imgs\ladon\busc_serial.png', 0.8)
    py.click()
    py.write(procura_ucs(UCs))

    py.hotkey('enter')
    sleep(3)

    cria_uc_lat_long()


def procura_ucs(UCs):
    # Lê o arquivo e pega apenas as 40 primeiras linhas
    with open(r'assets\txt\busca_ucs.txt', 'r') as file:
        # Lê todas as linhas, remove espaços em branco/quebras de linha e pega as primeiras 40
        UCs = [linha.strip() for linha in file.readlines()[:40]]

    # Converte a lista de UCs em uma string, separada por ";"
    ucs_modificadas = ";".join(UCs)
    print(ucs_modificadas)
    return ucs_modificadas

def cria_uc_lat_long():

    n = 1



    for elemento in range(40):

        options = Options()
        # Você pode adicionar aqui alguma condição ou ação específica para cada elemento
        localiza(r'assets\imgs\ladon\pesquisa.png',0.7)
        py.click()
        for i in range(n):
            py.hotkey('down')

        if nlocaliza(r'assets\imgs\ladon\padrao.png', 0.8):
            logging.info(f"ERRO - UC:{ucs}")
            print("Imagem padrão encontrada, saindo do loop.")
            localiza(r'assets\imgs\ladon\sair_web.png', 0.8)
            py.move(40,0)
            py.click()
            salvar_df()

        # if nlocaliza(r'C:\Users\L805958\Documents\Projetos_chatbot\analise-de-telemetrias\Projetos_chatbot\Pycis\assets\imagens\proximos.png', 0.7):
        #     py.doubleClick()
        #     sleep(3)
        #     py.click()
        #     continue

        py.hotkey('enter')

        localiza(r'assets\imgs\ladon\lupinha.png', 0.75)
        py.click()

        localiza(r'assets\imgs\ladon\ponto_med.png', 0.8)
        py.click()

        # Pega serial
        localiza(r'assets\imgs\ladon\Serial.png', 0.8)
        sleep(0.4)
        py.move(265,0)
        py.doubleClick()
        py.hotkey('ctrl', 'c')
        serial = pyperclip.paste()
        remover_linha_por_serial(r'assets\txt\busca_ucs.txt', serial)

        # Pega UC
        localiza(r'assets\imgs\ladon\chaves_ext.png', 0.8)
        sleep(0.4)
        py.move(80, 0)
        py.doubleClick()
        py.hotkey('ctrl', 'c')
        UC_1 = pyperclip.paste()

        # Pega lat
        localiza(r'assets\imgs\ladon\busc_lat.png', 0.8)
        sleep(0.4)
        py.move(80, 0)
        py.tripleClick()
        py.hotkey('ctrl', 'c')
        lat = pyperclip.paste()

        # Pega Long
        localiza(r'assets\imgs\ladon\busc_long.png', 0.8)
        sleep(0.4)
        py.move(80, 0)
        py.tripleClick()
        py.hotkey('ctrl', 'c')
        long = pyperclip.paste()

        py.move(-600,0)
        py.scroll(1400)
        sleep(0.6)
        # Coloca os dados coletados em listas
        ucs.append(UC_1)
        latitudes.append(lat)
        longitudes.append(long)

        logging.info(f"SUCESSO - UC:{UC_1}")

        n = n+1

        if n > 40:
            print(ucs, latitudes, longitudes)
            localiza(r'assets\imgs\ladon\sair_web.png', 0.8)
            py.move(40,0)
            py.click()
            main()



if __name__ == '__main__':
    main()
