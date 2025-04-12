import pandas as pd

# Recarregar o CSV após reset do ambiente
file_path = "C:/Users/PC/Downloads/Detalhamento das Atividades - Passo a Passo.csv"
df = pd.read_csv(file_path)

# Mostrar as colunas para uso no script SQL
df.columns
