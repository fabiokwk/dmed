import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
caminho_do_arquivo_csv = 'relatorio_disponibilidade.csv'

# Input dos dados do relatório de disponibilidade
dados_disponibilidade = pd.read_csv(caminho_do_arquivo_csv, sep=',', skiprows=11, encoding='utf-8')

# Mostra a planilha atual
print(dados_disponibilidade)

# Padrões para excluir colunas
padroes_excluir_inicio = [
    '^Cliente',
    '^CAS',
    '^Medidor',
    '^Disponibilidade',
    '^Telemetria',
    '^Hemera',
    '^Filtros:',
    '^0'
]

padroes_excluir = [
    '^Ip',
    '^Endereço',
    '^Porta',
]

# Remove colunas que atendem a qualquer um dos padrões da lista
dados_disponibilidade = dados_disponibilidade.loc[:, ~dados_disponibilidade.columns.str.contains('|'.join(padroes_excluir))]
mask = ~dados_disponibilidade.iloc[:, 0].astype(str).str.contains('|'.join(padroes_excluir_inicio))
dados_disponibilidade = dados_disponibilidade[mask]

# Remove linhas que não tem nada em nenhuma célula
dados_disponibilidade = dados_disponibilidade.dropna(how='all')

# Renomeia as colunas
dados_disponibilidade.rename(columns={
    dados_disponibilidade.columns[0]: 'Regiao',
    dados_disponibilidade.columns[1]: 'Void',
    dados_disponibilidade.columns[2]: 'PontoDeMedicao',
    dados_disponibilidade.columns[3]: 'Medidor',
    dados_disponibilidade.columns[4]: 'Telemetria (MIN)',
    dados_disponibilidade.columns[5]: 'Void',
    dados_disponibilidade.columns[6]: 'Void',
    dados_disponibilidade.columns[7]: 'Void',
    dados_disponibilidade.columns[8]: 'Void',
    dados_disponibilidade.columns[9]: 'Void',
    dados_disponibilidade.columns[10]: 'Disponibilidade',
}, inplace=True)

# Exclui as colunas "Void" pois estão sobrando/vazias
dados_disponibilidade.drop(dados_disponibilidade.filter(like='Void').columns, axis=1, inplace=True)

# Dividir a coluna "PontoDeMedicao" em duas colunas usando o delimitador "-"
dados_disponibilidade[['UC', 'Cliente']] = dados_disponibilidade['PontoDeMedicao'].str.split('-', n=1, expand=True)

# Remover a coluna original "PontoDeMedicao" se desejar
dados_disponibilidade.drop('PontoDeMedicao', axis=1, inplace=True)

# Extrai a parte desejada da coluna "Regiao"
dados_disponibilidade['Regiao'] = dados_disponibilidade['Regiao'].str.extract(r'([A-Z]+-[A-Z]+)')

# Nomeia as colunas extraídas
dados_disponibilidade[['Macrorregião', 'Regional']] = dados_disponibilidade['Regiao'].str.split('-', n=1, expand=True)

# Exclui a coluna original
dados_disponibilidade.drop('Regiao', axis=1, inplace=True)

# Reorganiza as colunas
novas_colunas = ['Macrorregião','Regional','UC', 'Cliente','Medidor', 'Telemetria (MIN)', 'Disponibilidade']
dados_disponibilidade = dados_disponibilidade[novas_colunas]

# Obtenha a data de 1 dia antes da data atual
data_anterior = (datetime.now() - timedelta(days=1)).date()
data_anterior_formatada = data_anterior.strftime('%d/%m/%Y')
dados_disponibilidade['Data'] = data_anterior_formatada

# # Salva o DataFrame modificado em um novo arquivo CSV
# disponibilidade = r'C:\Users\L805958\Documents\Pycis\Testes Disponibilidade'
# pasta_do_arquivo = os.path.dirname(disponibilidade)
# novo_combinado_csv = os.path.join(pasta_do_arquivo, 'Relatorio_Disponibilidade.csv')
# dados_disponibilidade.to_csv(novo_combinado_csv, index=False)

# Salva o DataFrame modificado em um novo arquivo xlsx
# disponibilidade = r'C:\Users\L805958\Documents\Pycis\Testes Disponibilidade'
# pasta_do_arquivo = os.path.dirname(disponibilidade)
# novo_combinado = os.path.join(pasta_do_arquivo, 'relatorio_disponibilidade.xlsx')
# dados_disponibilidade.to_excel(novo_combinado, index=False, engine='openpyxl')
dados_disponibilidade.to_csv('dados_disponibilidade', sep= ',')
print("Dados Modificados:")
print(dados_disponibilidade)
print("\n")
