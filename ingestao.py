import pandas as pd
from sqlalchemy import create_engine, text

# 1. Ligação ao Banco de Dados
engine = create_engine('postgresql+psycopg2://postgres:sua_senha@localhost:5432/postgres')
caminho_csv = 'data/IOT-temp.csv'

# 2. Ler os dados do CSV
print("A ler o ficheiro CSV...")
df = pd.read_csv(caminho_csv)

# 3. Tratamento de dados
df = df.rename(columns={
    'room_id/id': 'device_id', 
    'temp': 'temperature',
    'noted_date': 'data_hora'
})

# Garantir que apagamos a coluna 'id' original para não haver confusões
if 'id' in df.columns:
    df = df.drop(columns=['id'])

df['data_hora'] = pd.to_datetime(df['data_hora'], dayfirst=True, format='mixed')

# 4. LIMPEZA PROFUNDA: Apagar views e tabela antigas à força
print("A limpar a base de dados antiga...")
with engine.begin() as conn:
    conn.execute(text("DROP VIEW IF EXISTS avg_temp_por_dispositivo CASCADE;"))
    conn.execute(text("DROP VIEW IF EXISTS leituras_por_hora CASCADE;"))
    conn.execute(text("DROP VIEW IF EXISTS temp_max_min_por_dia CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS temperature_readings CASCADE;"))

# 5. Enviar os dados novos
print("A enviar os dados corrigidos (sem duplicados)...")
df.to_sql('temperature_readings', engine, if_exists='replace', index=False)

# 6. Recriar as Views
views_sql = [
    """
    CREATE VIEW avg_temp_por_dispositivo AS
    SELECT device_id, AVG(temperature) as avg_temp
    FROM temperature_readings
    GROUP BY device_id;
    """,
    """
    CREATE VIEW leituras_por_hora AS
    SELECT EXTRACT(HOUR FROM data_hora) as hora, COUNT(*) as contagem
    FROM temperature_readings
    GROUP BY EXTRACT(HOUR FROM data_hora)
    ORDER BY hora;
    """,
    """
    CREATE VIEW temp_max_min_por_dia AS
    SELECT DATE(data_hora) as data, MAX(temperature) as temp_max, MIN(temperature) as temp_min
    FROM temperature_readings
    GROUP BY DATE(data_hora)
    ORDER BY data;
    """
]

print("A recriar as Views SQL...")
with engine.begin() as conn:
    for view in views_sql:
        conn.execute(text(view))
        
print("Sucesso Absoluto! A base de dados está limpa e renovada.")