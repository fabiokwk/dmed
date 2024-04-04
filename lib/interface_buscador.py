import tkinter as tk
from tkinter import messagebox
import threading
import rpa_buscador_lat_long

def center_window(root, width=400, height=500):
    # Obtém a largura e altura da tela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calcula x e y coordenadas para posicionar a janela no centro da tela
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

def salvar_list_ucs():
    # Obtém os itens da caixa de entrada e os converte em uma lista
    ucs = entrada.get("1.0", tk.END).splitlines()

    # Verifica se a lista está vazia
    if not ucs or all(item.strip() == '' for item in ucs):
        messagebox.showinfo("Aviso", "Lista vazia! Não há itens para salvar.")
    else:
        # Abre o arquivo 'busca_ucs.txt' em modo de escrita e escreve os itens no arquivo
        with open('assets/txt/busca_ucs.txt', 'w') as arquivo:
            arquivo.write('\n'.join(ucs))

        # Limpa a caixa de entrada após salvar os itens
        messagebox.showinfo("Sucesso", "Lista salva com sucesso!")

def executar_acao():
    t = threading.Thread(target=rpa_buscador_lat_long.main)
    t.start()

# Cria a janela principal
janela = tk.Tk()       
center_window(janela, 400, 240)

janela.title("Buscar lat e long UC")
janela.configure(bg="darkblue")  # Altera o background da janela principal para lightgrey

# Cria o rótulo acima da caixa de entrada de texto
rotulo = tk.Label(janela, font="Calibri, 12", text="Coloque abaixo a lista de UCS", bg="darkblue", fg="white")
rotulo.pack(padx=10, pady=5)

# Cria um quadro para conter a caixa de entrada de texto e os botões
frame = tk.Frame(janela, bg="darkblue")
frame.pack(padx=10, pady=10)

# Cria a caixa de entrada de texto dentro do quadro
entrada = tk.Text(frame, height=14, width=30, bg="white", fg="black")
entrada.pack(side=tk.LEFT, padx=5, pady=5)

# Cria o botão para executar ação dentro do quadro
botao_executar = tk.Button(frame, text="Executar", command=executar_acao, bg="black", font="Calibri, 10", fg="white")
botao_executar.pack(side=tk.TOP, padx=5, pady=5)

# Cria o botão para salvar a lista dentro do quadro
botao_salvar = tk.Button(frame, text="Salvar", command=salvar_list_ucs, bg="black", font="Calibri, 10", fg="white")
botao_salvar.pack(side=tk.TOP, padx=5, pady=5)

# Inicia o loop principal da interface gráfica
janela.mainloop()
