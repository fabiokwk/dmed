import pandas as pd

def valor_unico(df, coluna):
    # Verifica se os valores da coluna são únicos
    if df[coluna].nunique() == df.shape[0]:
        print(f"Os valores da coluna '{coluna}' são únicos.")
    else:
        print(f"Os valores da coluna '{coluna}' não são únicos.")

def explorar(df):
    print("\nInformações sobre o DataFrame:")
    print(df.info())
    print("\nQuantidade:")
    print(df.shape)
    print("\nValores nulos:")
    print(df.isnull().sum())
def renomear_colunas(df):
    # Renomear as colunas
    novo_nome_colunas = {'Estacao': 'estacao',
                         'Operadora': 'operadora',
                         'Municipio': 'municipio',
                         'Latitude': 'latitude_antena',
                         'Longitude': 'longitude_antena',
                         'Tecs': 'tecs',
                     
                    }
    
    df.rename(columns=novo_nome_colunas, inplace=True)

def __main__():
    df = pd.read_excel('antenas_ago_23.xlsx') #Lê arquivo excel
    renomear_colunas(df)
    explorar(df)
    valor_unico(df, 'estacao')
    
    df.to_csv('antenas_parana.csv', index=False) #exporta para csv

if __name__ == "__main__":
    __main__()