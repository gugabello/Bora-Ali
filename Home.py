# Home.py
import streamlit as st

st.set_page_config(
    page_title="Página Inicial - Análise de Tarifas",
    layout="wide"
)

st.title("✈️ Análise de Tarifas Aéreas e Clima")
st.markdown(
    """
    Bem-vindo ao painel de análise de tarifas aéreas e sua relação com dados 
    climáticos e inflação para as principais capitais do Brasil: 
    **São Paulo, Rio de Janeiro, Recife e Brasília**.

    Use o menu ao lado para navegar entre as seções:

    - **📊 Gráficos:** Visualizações interativas dos dados integrados.
    - **📄 Tabelas:** Veja os dados brutos e processados que alimentam a análise.

    Este aplicativo é o resultado de um projeto de processamento e integração 
    de dados de múltiplas fontes (ANAC, INMET, IBGE).
    """
)