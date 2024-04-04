import tkinter as tk
from tkinter import filedialog
import subprocess
import threading
import pyIris
import pyautogui as py
import sys

tempo_limite_espera = 20
ver_conexao = """${SSN},SIGNAL,${TRY},${COUNT}
${SSN},VED,${TRY},${COUNT}
${SSN},TFS,${TRY},${COUNT}"""

def testar_telemetria(telemetria_valor, nio_medidor_valor, uc_valor, label_resultado):
    try:
        pyIris.localiza('imagens/campo_nome.PNG', 0.8, tempo_limite_espera)
        py.moveRel(0, 20)
        py.click()
        py.hotkey('ctrl', 'a')
        py.write(telemetria_valor)
        pyIris.localiza('imagens/bt_lupa.PNG', 0.9, tempo_limite_espera)
        py.click()
        pyIris.verifica_se_cativo(tempo_limite_espera)
        pyIris.verifica_se_conectado(tempo_limite_espera)
        pyIris.localiza('imagens/res_pesquisa_teste.PNG', 0.9, tempo_limite_espera)
        py.click()
        py.rightClick()
        py.press('down')
        py.press('enter')
        pyIris.localiza('imagens/ver_mensagens.PNG', 0.9, tempo_limite_espera)
        pyIris.localiza('imagens/bt_selecionar_teles.PNG', 0.9, tempo_limite_espera)
        py.click()
        pyIris.comando(ver_conexao, tempo_limite_espera)

        resultado = "Teste de Telemetria enviado!"
        label_resultado.config(text=f"Resultado: {resultado}")
    except Exception as e:
        label_resultado.config(text=f"Erro durante a automação: {str(e)}")

def executar_programa(entrada_telemetria, entrada_nio_medidor, entrada_uc, label_resultado):
    telemetria_valor = entrada_telemetria.get()
    nio_medidor_valor = entrada_nio_medidor.get()
    uc_valor = entrada_uc.get()

    thread_automacao = threading.Thread(
        target=testar_telemetria,
        args=(telemetria_valor, nio_medidor_valor, uc_valor, label_resultado)
    )
    thread_automacao.start()

def main():
    # Criar a janela principal
    janela = tk.Tk()
    janela.title("Testar Comunicação")

    # Criar campos de entrada
    tk.Label(janela, text="Telemetria:").grid(row=0, column=0, padx=10, pady=10)
    entrada_telemetria = tk.Entry(janela, width=50)
    entrada_telemetria.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(janela, text="NIO Medidor:").grid(row=1, column=0, padx=10, pady=10)
    entrada_nio_medidor = tk.Entry(janela, width=50)
    entrada_nio_medidor.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(janela, text="UC:").grid(row=2, column=0, padx=10, pady=10)
    entrada_uc = tk.Entry(janela, width=50)
    entrada_uc.grid(row=2, column=1, padx=10, pady=10)

    # Criar botão para executar o programa
    botao_executar = tk.Button(janela, text="Executar", command=lambda: executar_programa(entrada_telemetria, entrada_nio_medidor, entrada_uc, label_resultado))
    botao_executar.grid(row=3, column=0, columnspan=2, pady=20)

    # Rótulo para exibir o resultado
    label_resultado = tk.Label(janela, text="")
    label_resultado.grid(row=4, column=0, columnspan=2, pady=20)

    # Iniciar o loop principal da interface gráfica
    janela.mainloop()

if __name__ == '__main__':
    main()
