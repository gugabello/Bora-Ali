# pages/1_📊_Graficos.py
import streamlit as st
import altair as alt
import pandas as pd
from data_processing import carregar_dados_completos

st.set_page_config(layout="wide")
st.title("📊 Gráficos Interativos")
st.markdown("Análises visuais para os destinos: **São Paulo, Rio de Janeiro, Recife e Brasília**.")

# --- Carregar Dados ---
df_anac, df_integrado, df_ipca = carregar_dados_completos()

# --- Gráficos da Tabela Integrada ---
if df_integrado is None or df_integrado.empty:
    st.error("Não foi possível gerar os gráficos. O DataFrame integrado (ANAC+INMET) está vazio.")
else:
    df_integrado['DATA'] = pd.to_datetime(df_integrado['ANO'].astype(str) + '-' + df_integrado['MES'].astype(str))
    
    st.header("Evolução da Tarifa e Temperatura Média Mensal")
    df_long = df_integrado.melt(
        id_vars=['DATA', 'UF'], value_vars=['TARIFA', 'TEMP_MEDIA'],
        var_name='Métrica', value_name='Valor'
    )
    chart1 = alt.Chart(df_long).mark_line(point=True).encode(
        x=alt.X('DATA:T', title='Data'),
        y=alt.Y('Valor:Q', title='Valor'),
        color='Métrica:N',
        strokeDash='Métrica:N',
        row='UF:N',
        tooltip=['DATA:T', 'UF:N', 'Métrica:N', 'Valor:Q']
    ).resolve_scale(y='independent').interactive()
    st.altair_chart(chart1, use_container_width=True)

    st.header("Correlação: Tarifa vs. Temperatura")
    chart2 = alt.Chart(df_integrado).mark_circle(size=60).encode(
        x=alt.X('TEMP_MEDIA:Q', title='Temperatura Média (°C)'),
        y=alt.Y('TARIFA:Q', title='Tarifa Média (R$)'),
        color='UF:N',
        tooltip=['DATA:T', 'UF:N', 'TARIFA:Q', 'TEMP_MEDIA:Q']
    ).interactive()
    st.altair_chart(chart2, use_container_width=True)

# --- Gráficos do IPCA ---
if df_ipca is None or df_ipca.empty:
    st.error("Não foi possível gerar o gráfico de inflação (IPCA).")
else:
    st.header("Evolução da Tarifa Média (4 Capitais) vs. IPCA Nacional")
    df_ipca_long = df_ipca.melt(
        id_vars=['DATA'], value_vars=['TARIFA', 'IPCA'],
        var_name='Métrica', value_name='Valor'
    )
    chart3 = alt.Chart(df_ipca_long).mark_line(point=True).encode(
        x=alt.X('DATA:T', title='Data'),
        y=alt.Y('Valor:Q', title='Valor'),
        color='Métrica:N',
        tooltip=['DATA:T', 'Métrica:N', 'Valor:Q']
    ).resolve_scale(y='independent').interactive()
    st.altair_chart(chart3, use_container_width=True)