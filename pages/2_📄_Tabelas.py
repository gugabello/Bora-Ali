import streamlit as st
import pandas as pd
from data_processing import carregar_dados_completos
import streamlit as st
from utils_style import aplicar_estilo_padrao # <--- Importa

st.set_page_config(layout="wide", page_title="...") # <--- Configura

aplicar_estilo_padrao() # <--- APLICA O CSS

# 1. Configuração e Estilo (Igual ao Dashboard para consistência)
st.set_page_config(layout="wide", page_title="Relatórios de Dados")

st.markdown("""
    <style>
        .block-container {padding-top: 1.5rem; padding-bottom: 1rem;}
        h1 {font-size: 2.2rem;}
        h3 {font-size: 1.4rem; color: #2c3e50;}
        .stDataFrame {border: 1px solid #f0f2f6; border-radius: 5px;}
    </style>
""", unsafe_allow_html=True)

st.title("📄 Relatórios Analíticos")
st.markdown("Acesso aos dados detalhados, formatados e prontos para exportação.")

# 2. Carga de Dados
df_anac_mensal, df_integrado, df_ipca = carregar_dados_completos()

if df_integrado is None:
    st.error("Erro ao carregar dados.")
    st.stop()

# Preparação de Datas para exibição (Cria coluna DATA limpa)
for df in [df_anac_mensal, df_integrado]:
    if df is not None and not df.empty:
        df['DATA_REF'] = pd.to_datetime(df['ANO'].astype(str) + '-' + df['MES'].astype(str)).dt.date

if df_ipca is not None:
     df_ipca['DATA_REF'] = pd.to_datetime(df_ipca['ANO'].astype(str) + '-' + df_ipca['MES'].astype(str)).dt.date

# ===================================================================
# 3. ESTRUTURA EM ABAS (TABS)
# ===================================================================
# Isso substitui a rolagem infinita por uma interface organizada
tab1, tab2, tab3 = st.tabs(["✈️ Tarifas (ANAC)", "🌡️ Clima & Preço (Integrado)", "📈 Economia (IPCA)"])

# --- ABA 1: DADOS DA ANAC ---
with tab1:
    st.subheader("Relatório de Tarifas Aéreas")
    st.caption("Dados consolidados de tarifa média mensal por capital.")
    
    if df_anac_mensal is not None:
        # Métricas de Resumo da Tabela
        c1, c2, c3 = st.columns(3)
        c1.info(f"**Registros:** {len(df_anac_mensal)} linhas")
        c2.info(f"**Cidades:** {df_anac_mensal['CIDADE'].nunique()}")
        c3.info(f"**Período:** {df_anac_mensal['DATA_REF'].min()} a {df_anac_mensal['DATA_REF'].max()}")
        
        # Tabela com Formatação Profissional
        st.dataframe(
            df_anac_mensal,
            use_container_width=True,
            hide_index=True,
            column_order=["DATA_REF", "CIDADE", "UF", "TARIFA"],
            column_config={
                "DATA_REF": st.column_config.DateColumn("Data Referência", format="MM/YYYY"),
                "CIDADE": "Capital",
                "UF": "Estado",
                "TARIFA": st.column_config.NumberColumn(
                    "Tarifa Média",
                    format="R$ %.2f" # Formatação de Moeda
                )
            }
        )
        
        # Botão de Download
        csv = df_anac_mensal.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar CSV (ANAC)", data=csv, file_name="anac_tarifas.csv", mime="text/csv")

# --- ABA 2: DADOS INTEGRADOS ---
with tab2:
    st.subheader("Dataset Integrado (Tarifa + Clima)")
    st.caption("Cruzamento de dados onde cada linha representa o preço e a temperatura de uma cidade em um mês específico.")
    
    if df_integrado is not None:
        c1, c2 = st.columns(2)
        c1.info(f"**Registros Integrados:** {len(df_integrado)}")
        c2.info(f"**Correlação Geral:** {df_integrado['TARIFA'].corr(df_integrado['TEMP_MEDIA']):.2f}")

        st.dataframe(
            df_integrado,
            use_container_width=True,
            hide_index=True,
            column_order=["DATA_REF", "CIDADE", "TARIFA", "TEMP_MEDIA"],
            column_config={
                "DATA_REF": st.column_config.DateColumn("Data", format="MM/YYYY"),
                "CIDADE": "Capital",
                "TARIFA": st.column_config.NumberColumn("Tarifa", format="R$ %.2f"),
                "TEMP_MEDIA": st.column_config.NumberColumn(
                    "Temp. Média",
                    format="%.1f °C" # Formatação de Temperatura
                )
            }
        )
        
        csv_int = df_integrado.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar CSV (Integrado)", data=csv_int, file_name="dados_integrados.csv", mime="text/csv")

# --- ABA 3: DADOS IPCA ---
with tab3:
    st.subheader("Histórico de Inflação e Preço Médio")
    st.caption("Comparativo macroeconômico nacional.")
    
    if df_ipca is not None:
        st.dataframe(
            df_ipca,
            use_container_width=True,
            hide_index=True,
            column_order=["DATA_REF", "IPCA", "TARIFA"],
            column_config={
                "DATA_REF": st.column_config.DateColumn("Mês/Ano", format="MM/YYYY"),
                "IPCA": st.column_config.NumberColumn(
                    "Índice IPCA",
                    format="%.2f %%" # Formatação de Porcentagem
                ),
                "TARIFA": st.column_config.NumberColumn(
                    "Média Nacional (Capitais)",
                    format="R$ %.2f",
                    help="Média aritmética das tarifas das capitais selecionadas neste mês"
                )
            }
        )
        
        csv_ipca = df_ipca.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar CSV (Economia)", data=csv_ipca, file_name="ipca_tarifas.csv", mime="text/csv")