# data_processing.py
import streamlit as st
import pandas as pd
import os

# Arquivos novos (Brasil completo)
ARQUIVO_ANAC = "ANAC_BRASIL_MENSAL.csv"
ARQUIVO_INMET = "INMET_BRASIL_MENSAL.csv"
ARQUIVO_IPCA = "IPCAUNIFICADO.csv"

@st.cache_data
def carregar_dados_completos():
    # 1. Carregar
    try:
        anac_path = os.path.join("pages", ARQUIVO_ANAC)
        df_anac = pd.read_csv(anac_path)
        
        inmet_path = os.path.join("pages", ARQUIVO_INMET)
        df_inmet = pd.read_csv(inmet_path)
        
        ipca_path = os.path.join("pages", ARQUIVO_IPCA)
        df_ipca = pd.read_csv(ipca_path)
    except FileNotFoundError:
        return None, None, None

    # 2. Integrar (Merge por UF)
    # A coluna CIDADE já existe nos arquivos, então incluímos no merge ou deixamos duplicar e removemos depois
    df_integrado = pd.merge(
        df_anac, 
        df_inmet, 
        on=['UF', 'ANO', 'MES', 'CIDADE'], # Usamos CIDADE também para garantir
        how='inner'
    )
    
    # 3. IPCA (Média Nacional das Capitais)
    df_ipca_tarifa = None
    if not df_integrado.empty:
        media_nac = df_integrado.groupby(['ANO', 'MES'])['TARIFA'].mean().reset_index()
        df_ipca_tarifa = pd.merge(media_nac, df_ipca, on=['ANO', 'MES'])
        df_ipca_tarifa.rename(columns={'IPCA_MENSAL': 'IPCA'}, inplace=True)
        df_ipca_tarifa['DATA'] = pd.to_datetime(df_ipca_tarifa['ANO'].astype(str) + '-' + df_ipca_tarifa['MES'].astype(str))

    return df_anac, df_integrado, df_ipca_tarifa