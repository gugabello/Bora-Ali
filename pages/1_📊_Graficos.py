# pages/1_📊_Graficos.py
import streamlit as st
import altair as alt
import pandas as pd
from data_processing import carregar_dados_completos

st.set_page_config(layout="wide")
st.title("📊 Análise Gráfica das Tarifas Aéreas")
st.markdown("Análises interativas focadas em **São Paulo, Rio de Janeiro, Recife e Brasília**.")

# --- Carregar Dados ---
df_anac_mensal, df_integrado, df_ipca = carregar_dados_completos()

# --- Verifica se os dados principais foram carregados ---
if df_integrado is None or df_integrado.empty:
    st.error("Não foi possível gerar os gráficos. O DataFrame integrado (ANAC+INMET) está vazio.")
else:
    df_integrado['DATA'] = pd.to_datetime(df_integrado['ANO'].astype(str) + '-' + df_integrado['MES'].astype(str))

    # ===================================================================
    # SEÇÃO 1: VISÃO GERAL DAS TARIFAS
    # ===================================================================
    st.header("Seção 1: Visão Geral das Tarifas")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Tarifa Média por Cidade (Todo o Período)")
        df_tarifa_media_cidade = df_integrado.groupby('CIDADE')['TARIFA'].mean().reset_index()
        
        chart_bar_cidade = alt.Chart(df_tarifa_media_cidade).mark_bar().encode(
            x=alt.X('CIDADE', title='Cidade', sort='-y'),
            y=alt.Y('TARIFA', title='Tarifa Média (R$)'),
            color=alt.Color('CIDADE', title="Cidade", legend=None),
            tooltip=[
                alt.Tooltip('CIDADE', title='Cidade'),
                alt.Tooltip('TARIFA', title='Tarifa Média (R$)', format=',.2f')
            ]
        ).interactive()
        st.altair_chart(chart_bar_cidade, use_container_width=True)

    with col2:
        st.subheader("Distribuição das Tarifas Mensais por Cidade")
        chart_boxplot_cidade = alt.Chart(df_integrado).mark_boxplot(extent='min-max').encode(
            x=alt.X('CIDADE', title='Cidade'),
            y=alt.Y('TARIFA', title='Tarifa Média Mensal (R$)'),
            color=alt.Color('CIDADE', title="Cidade"),
            tooltip=[
                alt.Tooltip('CIDADE', title='Cidade'),
                alt.Tooltip('TARIFA', title='Tarifa Média (R$)', format=',.2f')
            ]
        ).interactive()
        st.altair_chart(chart_boxplot_cidade, use_container_width=True)

    # ===================================================================
    # SEÇÃO 2: ANÁLISE SAZONAL E TEMPORAL
    # ===================================================================
    st.header("Seção 2: Análise Sazonal e Temporal")
    st.subheader("Evolução da Tarifa Média Mensal por Cidade")
    
    chart_linha_tempo = alt.Chart(df_integrado).mark_line(point=True).encode(
        x=alt.X('DATA:T', title='Data'),
        y=alt.Y('TARIFA:Q', title='Tarifa Média (R$)'),
        color=alt.Color('CIDADE:N', title="Cidade"),
        tooltip=[
            alt.Tooltip('DATA:T', title='Data', format='%Y-%m'),
            alt.Tooltip('CIDADE', title='Cidade'),
            alt.Tooltip('TARIFA', title='Tarifa Média (R$)', format=',.2f')
        ]
    ).interactive()
    st.altair_chart(chart_linha_tempo, use_container_width=True)

    st.subheader("Média Sazonal (Tarifa por Mês do Ano)")
    df_tarifa_media_mes = df_integrado.groupby('MES')['TARIFA'].mean().reset_index()
    
    chart_bar_mes = alt.Chart(df_tarifa_media_mes).mark_bar().encode(
        x=alt.X('MES:O', title='Mês', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('TARIFA', title='Tarifa Média (R$)'),
        tooltip=[
            alt.Tooltip('MES', title='Mês'),
            alt.Tooltip('TARIFA', title='Tarifa Média (R$)', format=',.2f')
        ]
    ).interactive()
    st.altair_chart(chart_bar_mes, use_container_width=True)

    # ===================================================================
    # SEÇÃO 3: ANÁLISE DE CORRELAÇÃO (CLIMA)
    # ===================================================================
    st.header("Seção 3: Relação entre Tarifa e Clima")
    st.subheader("Tarifa Média Mensal vs. Temperatura Média Mensal")
    
    chart_scatter_clima = alt.Chart(df_integrado).mark_circle(size=60).encode(
        x=alt.X('TEMP_MEDIA:Q', title='Temperatura Média (°C)', scale=alt.Scale(zero=False)),
        y=alt.Y('TARIFA:Q', title='Tarifa Média (R$)', scale=alt.Scale(zero=False)),
        color=alt.Color('CIDADE:N', title="Cidade"),
        tooltip=[
            alt.Tooltip('CIDADE', title='Cidade'),
            alt.Tooltip('DATA', title='Período', format='%Y-%m'),
            alt.Tooltip('TARIFA', title='Tarifa Média (R$)', format=',.2f'),
            alt.Tooltip('TEMP_MEDIA', title='Temp. Média (°C)', format=',.1f')
        ]
    ).interactive()
    st.altair_chart(chart_scatter_clima, use_container_width=True)
    
    st.subheader("Mapa de Correlação (Heatmap)")
    df_corr = df_integrado[['TARIFA', 'TEMP_MEDIA', 'ANO', 'MES']].corr().reset_index().melt('index')
    
    base = alt.Chart(df_corr).encode(
        x=alt.X('index', title=None),
        y=alt.Y('variable', title=None),
        tooltip=[
            alt.Tooltip('index', title='Variável 1'),
            alt.Tooltip('variable', title='Variável 2'),
            alt.Tooltip('value', title='Correlação', format=',.2f')
        ]
    )
    heatmap = base.mark_rect().encode(
        color=alt.Color('value', title='Correlação', scale=alt.Scale(range='diverging', domain=[-1, 1]))
    )
    text = base.mark_text().encode(
        text=alt.Text('value', format=',.2f'),
        color=alt.value('black')
    )
    chart_heatmap = heatmap + text
    st.altair_chart(chart_heatmap, use_container_width=True)

# --- Gráficos do IPCA ---
if df_ipca is None or df_ipca.empty:
    st.error("Não foi possível gerar o gráfico de inflação (IPCA).")
else:
    # ===================================================================
    # SEÇÃO 4: CONTEXTO ECONÔMICO (IPCA)
    # ===================================================================
    st.header("Seção 4: Contexto Econômico (Inflação)")
    st.subheader("Evolução da Tarifa Média vs. IPCA Nacional")
    
    df_ipca_long = df_ipca.melt(
        id_vars=['DATA'], value_vars=['TARIFA', 'IPCA'],
        var_name='Métrica', value_name='Valor'
    )
    
    chart_ipca = alt.Chart(df_ipca_long).mark_line(point=True).encode(
        x=alt.X('DATA:T', title='Data'),
        y=alt.Y('Valor:Q', title='Valor'),
        color=alt.Color('Métrica:N', title='Métrica'),
        tooltip=[
            alt.Tooltip('DATA:T', title='Data', format='%Y-%m'),
            alt.Tooltip('Métrica', title='Métrica'),
            alt.Tooltip('Valor', title='Valor', format=',.2f')
        ]
    ).resolve_scale(y='independent').interactive()
    st.altair_chart(chart_ipca, use_container_width=True)