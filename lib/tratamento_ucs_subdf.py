import pandas as pd

def explorar(df):
    print("\nInformações sobre o DataFrame:")
    print(df.info())
    print("\nQuantidade:")
    print(df.shape)
    print("\nValores nulos:")
    print(df.isnull().sum())

caminho_do_arquivo = 'ucs.csv' #caminho txt com ucs
df = pd.read_csv(caminho_do_arquivo, sep='|') # leitor do txt com ucs
# df['macroregiao'] = df.iloc[:, 0].str.slice(0, 3)
# df['regional'] = df.iloc[:, 0].str.slice(4, 7)
print(df.columns)

# df.to_csv('ucs.csv', sep = ',' ,  index=False)
