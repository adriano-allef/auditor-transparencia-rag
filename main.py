import pandas as pd
import os

arquivo = "dados/despesas.csv"

# Carrega os dados
df = pd.read_csv(arquivo, encoding='latin-1', sep=';') # mudando a codificação de utf-8 para a latin-1

# Mostra as primeiras linhas
print(df.head())

#1. Limpeza de dados (Data Cleaning)
# Acessa a coluna -> entra no modo string (.str) -> substitui

df['VALOR TRANSAÇÃO'] = df['VALOR TRANSAÇÃO'].str.replace(',','.')

#2. Conversão de TIpo (Casting)
#O Pandas tem uma função inteligente para virar número
df['VALOR TRANSAÇÃO'] = pd.to_numeric(df['VALOR TRANSAÇÃO'])

#Verificando se funcionou (Describe mostra estatísticas matemáticas)
print(df['VALOR TRANSAÇÃO'].describe())

print(df.head())

#1. Encontrar o valor máximo exato(dinamicamente)
valor_maximo = df['VALOR TRANSAÇÃO'].max()

#2. Filtrar a linha que tem esse valor
#Lê-se: "No dataframe DF, me traga as linhas ONDE a coluna valor é igual ao maior_valor"
#valores_mx_repetidos = df['VALOR TRANSAÇÃO'].count(valor_maximo) --> errei
#Correção
valor_max_repetido = df[df['VALOR TRANSAÇÃO'] == valor_maximo]

#3. Mostrar os detalhes
print("\n🏆 DETALHES DO MAIOR GASTO:")
print(valor_max_repetido[['NOME ÓRGÃO SUPERIOR', 'NOME ÓRGÃO', 'DATA TRANSAÇÃO', 'VALOR TRANSAÇÃO']])