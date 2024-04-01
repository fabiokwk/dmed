import pandas as pd

# Ler o arquivo separado por "|"
caminho_arquivo = 'C:\\Users\\L805958\\Documents\\Pycis\\CIS_INTG_HEMERA_20191025.csv'
df = pd.read_csv(caminho_arquivo, sep='|')

# Para a exclusão de colunas
colunas_para_excluir = ['NOME_CLI', 'REGISTRO_CLI', 'ATIVIDADE_CLI', 'CONTROLADOR_CLI', 
                        'ENDERECO_CLI', 'CEP_CLI', 'CIDADE_CLI', 'ESTADO_CLI', 'PAIS_CLI', 'NOME_PM', 'ATIVIDADE_PM', 
                        'ENDERECO_PM', 'CEP_PM', 'CIDADE_PM', 'ESTADO_PM', 'PAIS_PM', 'NOME_MED', 
                        'SERIAL_MED', 'MODELO_MED', 'DATA_INICIAL', 'DATA_FINAL', 'CONF_TARIFARIA_MED', 'TIPO_INST_MED', 'FASES_MED', 
                        'TIPO_MED', 'RTC_MED', 'RTP_MED', 'KE_MED']


df = df.drop(columns=colunas_para_excluir)

df.rename(columns={
    df.columns[0]: 'UC',
    df.columns[1]: 'LATITUDE',
}, inplace=True)

print(df)
# Salvar o dataframe filtrado em um arquivo CSV
caminho_saida_csv = 'loc_uc.csv'
df.to_csv(caminho_saida_csv, index=False)
print("Dados filtrados e salvos com sucesso em", caminho_saida_csv)
