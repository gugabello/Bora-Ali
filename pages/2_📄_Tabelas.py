# pages/2_📄_Tabelas.py
import streamlit as st
from data_processing import carregar_dados_completos

st.set_page_config(layout="wide")
st.title("📄 Tabelas de Dados")
st.markdown("Dados filtrados para os destinos: **São Paulo, Rio de Janeiro, Recife e Brasília**.")

# --- Helper de Paginação ---
def mostrar_tabela_paginada(df, key_prefix):
    if df is None or df.empty:
        st.warning("Não há dados para exibir nesta tabela.")
        return
    st.info(f"A tabela completa tem **{len(df)}** linhas.")
    col1, col2 = st.columns(2)
    max_rows = len(df)
    start_row = col1.number_input("Mostrar a partir da linha:", 0, max_rows - 1, 0, 100, key=f"start_{key_prefix}")
    end_row = col2.number_input("Até a linha:", start_row, max_rows, min(start_row + 1000, max_rows), 100, key=f"end_{key_prefix}")
    st.dataframe(df.iloc[int(start_row):int(end_row)])

# --- Carregar Dados e Exibir Tabelas ---
df_anac, df_integrado, df_ipca = carregar_dados_completos()

st.header("1. Tabela de Voos (ANAC Pré-Filtrada)")
st.markdown("Dados brutos de voos da ANAC, já filtrados para as 4 capitais (arquivo `ANAC_CAPITAIS.csv`).")
mostrar_tabela_paginada(df_anac, "anac")

st.header("2. Tabela Integrada (ANAC + INMET)")
st.markdown("Média mensal de tarifa e temperatura, resultado da junção dos dados.")
mostrar_tabela_paginada(df_integrado, "integrado")

st.header("3. Tabela de Inflação (IPCA vs. Tarifa Média)")
st.markdown("Comparativo da tarifa aérea média (das 4 capitais) com o IPCA.")
mostrar_tabela_paginada(df_ipca, "ipca")