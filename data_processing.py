# data_processing.py
import streamlit as st
import pandas as pd
import os

# Nomes dos novos arquivos LEVES baseados em UF
ARQUIVO_ANAC = "ANAC_CAPITAIS_UF_MENSAL.csv"
ARQUIVO_INMET = "INMET_CAPITAIS_UF_MENSAL.csv"
ARQUIVO_IPCA = "IPCAUNIFICADO.csv"

# O mapa de "tradução" que usaremos no final
MAPA_UF_PARA_CIDADE = {
    'SP': 'São Paulo',
    'RJ': 'Rio de Janeiro',
    'PE': 'Recife',
    'DF': 'Brasília'
}

@st.cache_data
def carregar_dados_completos():
    """
    Carrega os arquivos CSV LEVES e PRÉ-AGREGADOS POR UF.
    """
    
    # --- 1. Carregar Dados Pré-Agregados ---
    try:
        anac_path = os.path.join("pages", ARQUIVO_ANAC)
        df_anac_mensal = pd.read_csv(anac_path)
        
        inmet_path = os.path.join("pages", ARQUIVO_INMET)
        df_inmet_mensal = pd.read_csv(inmet_path)
        
        ipca_path = os.path.join("pages", ARQUIVO_IPCA)
        df_ipca = pd.read_csv(ipca_path)
        
    except FileNotFoundError as e:
        st.error(f"Erro Crítico: Arquivo não encontrado na pasta 'pages' -> {e.filename}")
        return None, None, None

    # --- 2. Integrar ANAC + INMET (A chave é a UF) ---
    df_integrado = pd.merge(
        df_anac_mensal, 
        df_inmet_mensal, 
        on=['UF', 'ANO', 'MES'], # <- A chave confiável
        how='inner'
    )
    if df_integrado.empty:
        st.warning("A integração ANAC+INMET não encontrou dados correspondentes.")
        
    # === A MÁGICA ===
    # 3. Criar a coluna CIDADE a partir da UF
    # Adicionamos 'CIDADE' ao df_anac_mensal para a Tabela 1
    df_anac_mensal['CIDADE'] = df_anac_mensal['UF'].map(MAPA_UF_PARA_CIDADE)
    # Adicionamos 'CIDADE' ao df_integrado para as Tabelas 2 e Gráficos
    df_integrado['CIDADE'] = df_integrado['UF'].map(MAPA_UF_PARA_CIDADE)
    # === FIM DA MÁGICA ===
    
    # --- 4. Integrar IPCA ---
    df_ipca_tarifa = None
    if not df_integrado.empty:
        tarifa_media_nacional = df_integrado.groupby(['ANO', 'MES'])['TARIFA'].mean().reset_index()
        df_ipca_tarifa = pd.merge(tarifa_media_nacional, df_ipca, on=['ANO', 'MES'], how='inner')
        df_ipca_tarifa.rename(columns={'IPCA_MENSAL': 'IPCA'}, inplace=True)
        df_ipca_tarifa['DATA'] = pd.to_datetime(df_ipca_tarifa['ANO'].astype(str) + '-' + df_ipca_tarifa['MES'].astype(str))

    # Retorna os 3 DataFrames
    return df_anac_mensal, df_integrado, df_ipca_tarifa