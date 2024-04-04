import os
import pyautogui as py
from time import sleep
import csv

# Caminho do arquivo CSV
path_imgs_ladon = os.path.join('..', 'dmed', 'assets', 'imgs', 'ladon')
path_lista_portas = os.path.abspath('../dmed/assets/txt/lista_rec_nao_migrado')

def esperar_tela(imagem):
    while True:
        tela_encontrada = py.locateOnScreen(f"{path_imgs_ladon}/{imagem}", confidence=0.5)
        
        if tela_encontrada:
            print(f'Encontrado:{imagem}')
            return True
        else:
            print(f'Não encontrado:{imagem}')
def abrir_ladon():
    try:
        py.press('win')
        sleep(0.3)
        py.write('ladon')
        sleep(0.3)
        py.press('enter')
    except Exception as e:
        print(f"Erro ao abrir Ladon: {e}")
def cadastrar_porta(porta):
        py.moveTo(f'{path_imgs_ladon}/lapis.PNG')
        py.moveRel(-27,22)
        py.click()
        py.moveRel(64,16)
        py.click()
        py.moveTo(f'{path_imgs_ladon}/lapis.PNG')
        py.click()
        esperar_tela('gatilho_rg_selecionado.PNG')
        py.moveRel(642,350)
        py.click(clicks=3)
        py.write(porta)
        py.moveTo(f'{path_imgs_ladon}/disquete.PNG')
        py.click()
        py.press('enter')
def ir_aba_leitura():
    py.moveTo(f'{path_imgs_ladon}/aba_leitura.PNG')
    py.click()
    esperar_tela('tela_aba_leitura.PNG')
def enviar_comando():
    esperar_tela('campo_para_selecionar_comando.PNG')
    py.moveTo(f'{path_imgs_ladon}/campo_para_selecionar_comando.PNG')
    py.click()
    py.press('r', presses=2)
    py.press('tab', presses=2, interval=0.5)
    py.press('enter')
def main():

    with open(path_lista_portas, mode='r') as portas:
        for porta in portas: 
            print(porta)
            abrir_ladon()
            esperar_tela('tela_inicial_ladon.PNG')
            cadastrar_porta(porta)
            ir_aba_leitura()
            enviar_comando()
            input('continuar?')
            

if __name__ == "__main__":
    main()
