import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(page_title="Dashboard IoT", layout="wide")

st.title('Dashboard de Temperaturas IoT')
st.write("A tentar ligar ao banco de dados...")

try:
    # Conexão com o banco de dados
    engine = create_engine('postgresql+psycopg2://postgres:sua_senha@localhost:5432/postgres')
    
    # Testar a ligação antes de continuar
    with engine.connect() as conn:
        st.success("Ligação ao banco de dados estabelecida com sucesso!")

    def load_data(view_name):
        return pd.read_sql(f"SELECT * FROM {view_name}", engine)

    # Gráfico 1
    st.header('Média de Temperatura por Dispositivo')
    st.write("A carregar os dados do Gráfico 1...")
    df_avg_temp = load_data('avg_temp_por_dispositivo')
    fig1 = px.bar(df_avg_temp, x='device_id', y='avg_temp')
    st.plotly_chart(fig1)

    # Gráfico 2
    st.header('Leituras por Hora do Dia')
    st.write("A carregar os dados do Gráfico 2...")
    df_leituras_hora = load_data('leituras_por_hora')
    fig2 = px.line(df_leituras_hora, x='hora', y='contagem')
    st.plotly_chart(fig2)

    # Gráfico 3
    st.header('Temperaturas Máximas e Mínimas por Dia')
    st.write("A carregar os dados do Gráfico 3...")
    df_temp_max_min = load_data('temp_max_min_por_dia')
    fig3 = px.line(df_temp_max_min, x='data', y=['temp_max', 'temp_min'])
    st.plotly_chart(fig3)

except Exception as e:
    st.error(f"Ocorreu um erro: {e}")