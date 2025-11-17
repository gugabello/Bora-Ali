# pages/2_📄_Tabelas.py
import streamlit as st
from data_processing import carregar_dados_completos

st.set_page_config(layout="wide")
st.title("📄 Tabelas de Dados")
st.markdown("Dados filtrados e pré-agregados para todas as capitais brasleiras.")

# --- Helper de Paginação ---
def mostrar_tabela_paginada(df, key_prefix):
    if df is None or df.empty:
        st.warning("Não há dados para exibir nesta tabela.")
        return
    st.info(f"A tabela completa tem **{len(df)}** linhas.")
    
    # Reorganiza colunas para 'CIDADE' vir primeiro
    if 'CIDADE' in df.columns:
        cols = ['CIDADE'] + [col for col in df.columns if col not in ['CIDADE', 'UF']]
        # Remove UF se ela ainda existir e não for desejada
        if 'UF' in cols:
            cols.remove('UF')
        df_display = df[cols]
    else:
        df_display = df

    col1, col2 = st.columns(2)
    max_rows = len(df_display)
    start_row = col1.number_input("Mostrar a partir da linha:", 0, max_rows - 1, 0, 100, key=f"start_{key_prefix}")
    end_row = col2.number_input("Até a linha:", start_row, max_rows, min(start_row + 100, max_rows), 100, key=f"end_{key_prefix}")
    
    st.dataframe(df_display.iloc[int(start_row):int(end_row)])

# --- Carregar Dados e Exibir Tabelas ---
df_anac_mensal, df_integrado, df_ipca = carregar_dados_completos()

st.header("1. Tabela de Tarifa Média por Cidade (ANAC)")
st.markdown("Média mensal de tarifa da ANAC (arquivo `ANAC_CAPITAIS_UF_MENSAL.csv`).")
mostrar_tabela_paginada(df_anac_mensal, "anac")

st.header("2. Tabela Integrada (ANAC + INMET)")
st.markdown("Média mensal de tarifa e temperatura por cidade.")
mostrar_tabela_paginada(df_integrado, "integrado")

st.header("3. Tabela de Inflação (IPCA vs. Tarifa Média)")
st.markdown("Comparativo da tarifa aérea média (das 4 capitais) com o IPCA.")
mostrar_tabela_paginada(df_ipca, "ipca")