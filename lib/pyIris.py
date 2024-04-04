import pyautogui as py
import time
from function import verificar_tela
import subprocess
import openpyxl
import pyperclip
from datetime import datetime
import os
import pandas as pd
import xlsxwriter

def localiza(DIRETORIO, precisao, tempo_limite_espera): #Aguarda até a imagem surgir na tela
    inicio_tempo = time.time()
    while not verificar_tela(DIRETORIO, precisao):
        decorrido = time.time() - inicio_tempo
        if  decorrido > tempo_limite_espera:
            print('Tempo limite atingido')
            inicio_tempo = time.time()
            exit()

def maximiza(tempo_limite_espera): #maximiza a janela de pesquisa
    localiza('imagens/tl_listagem_telemetrias.PNG', 0.8, tempo_limite_espera)
    py.moveRel(368,-176) 
    py.click()

def ver_mensagens():
    localiza('IRIS_IMAGENS/ver_mensagens.png', 0.8)
    py.moveRel(335,-267)
    py.click()
    localiza('IRIS_IMAGENS/hora.png', 0.8)
    py.click()
    localiza('IRIS_IMAGENS/chips.png', 0.8)
    py.click()
    localiza('IRIS_IMAGENS/teles.png', 0.8)
    py.click()
    py.hotkey('ctrl','a')

def maximiza_ver_mensagens():
    localiza('IRIS_IMAGENS/ver_mensagens.png', 0.8)
    py.moveRel(335,-267)
    py.click()

def escrever_prog(prog):#escreve o programa desejado no campo de comandos
    localiza('IRIS_IMAGENS/area_escrita_comandos.PNG', 0.8)
    # py.moveRel(335,-267)
    py.moveTo('IRIS_IMAGENS/area_escrita_comandos.PNG')
    py.click()
    py.write(prog)

def comando(comandos, tempo_limite_espera):
    py.moveRel(0,50)
    py.click()
    py.hotkey('ctrl','a')
    py.write(comandos)
    localiza('imagens/bt_enviar_comandos.PNG', 0.9, tempo_limite_espera)
    py.click()

def selecionar_todas_as_teles():#seleciona todas as teles dentro do 'ver mensagens' antes de escrever o comando
    maximiza_ver_mensagens()
    localiza('IRIS_IMAGENS/selecionar_todas_as_teles.png', 0.9)
    py.click()

def confirma_envio_comandos():#confirma envio dos comandos
    localiza('IRIS_IMAGENS/enviar.png', 0.9)
    py.click()

def cria_xlsx_status_teles():
   
    # Lista dos dados extraídos está armazenada como uma string grande, com base no seu uso anterior
    dados_extraidos = pyperclip.paste()
    # Agora vamos criar um novo Workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    # Dividindo o texto copiado em linhas e colunas
    linhas = dados_extraidos.strip().split('\n')  # separar cada linha pelo '\n'
    for i, linha in enumerate(linhas):
        # Dividindo cada linha em células baseadas na vírgula
        celulas = linha.split(' ')  # separar cada célula pela vírgula
        for j, celula in enumerate(celulas):
            # Escrever cada célula na planilha
            ws.cell(row=i+1, column=j+1, value=celula.strip())  # Adiciona os dados nas células

    # Salvar o arquivo no mesmo diretório onde o script está sendo executado
    data_hoje = datetime.now()
    diretorio = 'textos_tabelas/status_teles.xlsx'
    # Formate a data no formato que você deseja no nome do arquivo (por exemplo, '2023-11-07')
    data_formatada = data_hoje.strftime('%d_%m_%Y-%H-%M')

    caminho_completo = os.path.join(diretorio)


    wb.save(caminho_completo)

def auto_status_tele():
    py.hotkey('win','r')
    time.sleep(2)
    py.write('soffice.exe --calc')
    py.press('enter')
    time.sleep(8)
    py.hotkey('ctrl','v')
    time.sleep(1)
    py.hotkey('ctrl','s')
    time.sleep(1)
    py.write('status_teles')
    py.press('tab')
    time.sleep(1)
    py.write('ex')
    py.press('enter', presses=2, interval=1)
    time.sleep(1)
    py.hotkey('alt','f4')

def apagar_arquivos_diretorio(diretorio):
    # Obtém a lista de arquivos no diretório
    lista_arquivos = os.listdir(diretorio)

    # Itera sobre os arquivos e os remove
    for arquivo in lista_arquivos:
        caminho_arquivo = os.path.join(diretorio, arquivo)
        try:
            if os.path.isfile(caminho_arquivo):
                os.remove(caminho_arquivo)
                print(f"Arquivo {arquivo} removido com sucesso.")
        except Exception as e:
            print(f"Erro ao remover {arquivo}: {e}")

def verifica_se_cativo(tempo_limite_espera):
    localiza('imagens/col_porta_cliente.PNG', 0.9, tempo_limite_espera)
    py.moveRel(0, 10)
    py.click()
    py.hotkey('ctrl', 'c')
    while True:
        porta = pyperclip.paste()

        if porta != '-1' and porta != '0':
            print(porta)
            print('Cliente livre')
            exit()  
        else:
            print('Cliente cativo')
            break

def verifica_se_conectado(tempo_limite_espera):
    localiza('imagens/col_tipo_de_porta_de_conexao.PNG', 0.9, tempo_limite_espera)
    py.moveRel(0, 10)
    py.click()
    py.hotkey('ctrl', 'c')
    while True:
        tipo_conexao = pyperclip.paste()

        if tipo_conexao == 'Not connected':
            print(f'Status conexão: {tipo_conexao}')
            exit()  
        else:
            print(f'Status conexão: {tipo_conexao}')
            break