import pandas as pd
from datetime import datetime
import os

# Carregar o arquivo JSONL
# Definir a pasta "coleta" como root
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
data_path = os.path.join(root_dir, 'data', 'data.jsonl')

# Carregar o arquivo JSONL
df = pd.read_json(data_path, lines=True)

# Configurações de exibição
pd.options.display.max_columns = None

# Adicionar colunas auxiliares
df['_source'] = "https://lista.mercadolivre.com.br/notebook"
df['_datetime'] = datetime.now()

# Tratar nulos
df['old_money'] = df['old_money'].fillna('0')
df['new_money'] = df['new_money'].fillna('0')
df['reviews_rating_number'] = df['reviews_rating_number'].fillna('0')
df['reviews_amount'] = df['reviews_amount'].fillna('0')

# Garantir que estão como strings antes de usar .str
df['old_money'] = df['old_money'].astype(str).str.replace('.', '', regex=False)
df['new_money'] = df['new_money'].astype(str).str.replace('.', '', regex=False)
df['reviews_amount'] = df['reviews_amount'].astype(str).str.replace(r'[\(\)]', '', regex=True)

# Verificar se os valores são válidos antes da conversão
df['old_money'] = pd.to_numeric(df['old_money'], errors='coerce').fillna(0)
df['new_money'] = pd.to_numeric(df['new_money'], errors='coerce').fillna(0)
df['reviews_rating_number'] = pd.to_numeric(df['reviews_rating_number'], errors='coerce').fillna(0)
df['reviews_amount'] = pd.to_numeric(df['reviews_amount'], errors='coerce').fillna(0)

# Filtrar os dados
df = df[
    (df['old_money'] >= 1000) & (df['old_money'] <= 10000) &
    (df['new_money'] >= 1000) & (df['new_money'] <= 10000) &
    (df['reviews_rating_number'] >= 0) & (df['reviews_rating_number'] <= 5)
]

# Exibir os primeiros resultados
print(df.head())