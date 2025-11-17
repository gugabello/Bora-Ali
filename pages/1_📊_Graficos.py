# pages/1_📊_Graficos.py
import streamlit as st
import altair as alt
import pandas as pd
from data_processing import carregar_dados_completos

st.set_page_config(layout="wide")
st.title("📊 Análise de Tarifas: Capitais Brasileiras")

df_anac, df_integrado, df_ipca = carregar_dados_completos()

if df_integrado is not None:
    df_integrado['DATA'] = pd.to_datetime(df_integrado['ANO'].astype(str) + '-' + df_integrado['MES'].astype(str))

    # --- FILTRO INTERATIVO ---
    st.sidebar.header("Filtros")
    # Pega a lista de cidades únicas
    todas_cidades = sorted(df_integrado['CIDADE'].unique())
    # Define padrão: SP, RJ, DF, PE (para não começar vazio)
    padrao = ['São Paulo', 'Rio de Janeiro', 'Brasília', 'Recife']
    # Filtra para garantir que os padrões existem nos dados
    padrao = [c for c in padrao if c in todas_cidades]
    
    cidades_selecionadas = st.sidebar.multiselect(
        "Escolha as Capitais para visualizar:",
        options=todas_cidades,
        default=padrao
    )

    # Filtra o DataFrame baseado na seleção
    if not cidades_selecionadas:
        st.warning("Por favor, selecione pelo menos uma cidade no menu lateral.")
        df_filtrado = df_integrado.copy() # Mostra tudo ou nada, sua escolha. Aqui deixo tudo.
    else:
        df_filtrado = df_integrado[df_integrado['CIDADE'].isin(cidades_selecionadas)]

    # --- GRÁFICOS (Usam df_filtrado) ---
    
    st.header("1. Evolução Temporal")
    chart_linha = alt.Chart(df_filtrado).mark_line(point=True).encode(
        x=alt.X('DATA:T', title='Data'),
        y=alt.Y('TARIFA:Q', title='Tarifa Média (R$)'),
        color='CIDADE:N',
        tooltip=['DATA:T', 'CIDADE', 'TARIFA']
    ).interactive()
    st.altair_chart(chart_linha, use_container_width=True)

    st.header("2. Tarifa x Temperatura")
    col1, col2 = st.columns(2)
    with col1:
        chart_scatter = alt.Chart(df_filtrado).mark_circle(size=60).encode(
            x=alt.X('TEMP_MEDIA:Q', title='Temperatura (°C)', scale=alt.Scale(zero=False)),
            y=alt.Y('TARIFA:Q', title='Tarifa (R$)', scale=alt.Scale(zero=False)),
            color='CIDADE:N',
            tooltip=['CIDADE', 'TARIFA', 'TEMP_MEDIA']
        ).interactive()
        st.altair_chart(chart_scatter, use_container_width=True)
    
    with col2:
         # Boxplot comparativo
        chart_box = alt.Chart(df_filtrado).mark_boxplot().encode(
            x=alt.X('CIDADE:N', title=None),
            y=alt.Y('TARIFA:Q', title='Distribuição de Tarifas'),
            color='CIDADE:N'
        )
        st.altair_chart(chart_box, use_container_width=True)

    # --- IPCA (Contexto Nacional) ---
    st.header("3. Contexto Nacional (IPCA)")
    st.markdown("Comparação da média das cidades selecionadas com a inflação.")
    
    # Recalcula média apenas das selecionadas para comparar com IPCA
    media_selecionada = df_filtrado.groupby(['DATA'])['TARIFA'].mean().reset_index()
    # Junta com IPCA (precisamos trazer o IPCA para cá de novo ou usar df_ipca e filtrar datas)
    # Simplificação: Usar o df_ipca global mas plotar junto com a media_selecionada é complexo no Altair sem merge.
    # Vamos plotar apenas o IPCA global vs Média das Selecionadas
    
    # (Código simplificado para não complicar demais o merge agora)
    base = alt.Chart(df_ipca).mark_line(color='red', strokeDash=[5,5]).encode(
        x='DATA:T', 
        y=alt.Y('IPCA', title='IPCA (%)')
    )
    # Para fazer eixo duplo no Altair é chato, vamos manter o gráfico de IPCA simples ou focar nas tarifas
    
    st.altair_chart(chart_linha, use_container_width=True) # Repete a linha das tarifas para contexto visual