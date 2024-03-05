import pandas as pd

def explorar(df):
    print("\nInformações sobre o DataFrame:")
    print(df.info())
    print("\nQuantidade:")
    print(df.shape)
    print("\nValores nulos:")
    print(df.isnull().sum())
def numericos_unicos(df):
    is_numeric = pd.to_numeric(df['uc'], errors='coerce').notnull().all()# Verifica se só possui valores numéricos
    is_unique = df['uc'].nunique() == len(df['uc'])# Verifica se todos os valores são únicos
    # Resultados
    print(f'A coluna "uc" contém apenas valores numéricos: {is_numeric}')
    print(f'Todos os valores na coluna "uc" são únicos: {is_unique}')
def ucs(df):
    colunas_interesse = ['nome', 'uc', 'municipio_uc', 'latitude_uc', 'longitude_uc', 'macroregiao', 'regional']
    sub_df = df[colunas_interesse]
    sub_df.to_csv('ucs.csv', index=False) #exporta para csv
    print(sub_df.columns)
def renomear_colunas(df):
    # Renomear as colunas
    novo_nome_colunas = {'NOME_CLI': 'nome',
                         'CONTRATO_CLI': 'uc',
                         'CIDADE_PM': 'municipio_uc',
                         'LATITUDE_PM': 'latitude_uc',
                         'LONGITUDE': 'longitude_uc',
                                            
                    }
    
    df.rename(columns=novo_nome_colunas, inplace=True)
    df['macroregiao'] = df.iloc[:, 0].str.slice(0, 3)
    df['regional'] = df.iloc[:, 0].str.slice(4, 7)

def __main__():
    caminho_do_arquivo = 'CIS_INTG_HEMERA_20191025 (1).txt' #caminho txt com ucs
    df = pd.read_csv(caminho_do_arquivo, sep='|') # leitor do txt com ucs
    renomear_colunas(df)
    explorar(df)
    numericos_unicos(df)
    ucs(df)
    
if __name__ == '__main__':
    __main__()

