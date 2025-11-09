# data_processing.py
import streamlit as st
import pandas as pd
import os

# Nomes dos novos arquivos LEVES
ARQUIVO_ANAC = "ANAC_CAPITAIS.csv"
ARQUIVO_INMET = "INMET_CAPITAIS.csv"
ARQUIVO_IPCA = "IPCAUNIFICADO.csv"

@st.cache_data # O cache guarda os dados na memória
def carregar_dados_completos():
    """
    Carrega os arquivos CSV LEVES e PRÉ-FILTRADOS da pasta 'pages'.
    Faz a integração final (merge) e retorna os DFs.
    """
    
    # --- 1. Carregar Dados Pré-Filtrados ---
    try:
        anac_path = os.path.join("pages", ARQUIVO_ANAC)
        df_anac = pd.read_csv(anac_path)
        
        inmet_path = os.path.join("pages", ARQUIVO_INMET)
        df_inmet = pd.read_csv(inmet_path)
        
        ipca_path = os.path.join("pages", ARQUIVO_IPCA)
        df_ipca = pd.read_csv(ipca_path)
        
    except FileNotFoundError as e:
        st.error(f"Erro Crítico: Arquivo não encontrado na pasta 'pages' -> {e.filename}")
        st.info("Certifique-se de que 'ANAC_CAPITAIS.csv', 'INMET_CAPITAIS.csv' e 'IPCAUNIFICADO.csv' estão na pasta 'pages'.")
        return None, None, None

    # --- 2. Preparar para Integração ---
    
    # ANAC: Agrega por mês/ano/UF (calculando a tarifa média)
    anac_mensal = df_anac.groupby(['UF', 'ANO', 'MES'])['TARIFA'].mean().reset_index()

    # INMET: Agrega por mês/ano/UF (calculando a temp média)
    # (O INMETLIMPO já está por dia, então agrupamos)
    inmet_mensal = df_inmet.groupby(['UF', 'ANO', 'MES'])['TEMP_MEDIA'].mean().reset_index()

    # --- 3. Integrar ANAC + INMET ---
    df_integrado = pd.merge(anac_mensal, inmet_mensal, on=['UF', 'ANO', 'MES'], how='inner')
    if df_integrado.empty:
        st.warning("A integração ANAC+INMET não encontrou dados correspondentes (mesmo ANO, MÊS, UF).")
    
    # --- 4. Integrar IPCA ---
    df_ipca_tarifa = None
    if not df_integrado.empty:
        # Média de tarifa das 4 capitais
        tarifa_media_nacional = df_integrado.groupby(['ANO', 'MES'])['TARIFA'].mean().reset_index()
        
        # Junta com IPCA
        df_ipca_tarifa = pd.merge(tarifa_media_nacional, df_ipca, on=['ANO', 'MES'], how='inner')
        df_ipca_tarifa.rename(columns={'IPCA_MENSAL': 'IPCA'}, inplace=True)
        df_ipca_tarifa['DATA'] = pd.to_datetime(df_ipca_tarifa['ANO'].astype(str) + '-' + df_ipca_tarifa['MES'].astype(str))

    # Retorna os 3 DataFrames prontos para o app
    return df_anac, df_integrado, df_ipca_tarifa