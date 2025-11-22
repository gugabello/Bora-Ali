import streamlit as st
import altair as alt
import pandas as pd
from data_processing import carregar_dados_completos
from utils_style import aplicar_estilo_padrao

st.set_page_config(layout="wide", page_title="Dashboard Analítico")
aplicar_estilo_padrao() # <--- ISSO É OBRIGATÓRIO AGORA

# 1. Configuração da Página e Estilo Profissional
st.set_page_config(layout="wide", page_title="Dashboard Analítico")

# CSS para ajustar espaçamentos e deixar com cara de "App"
st.markdown("""
    <style>
        .block-container {padding-top: 1.5rem; padding-bottom: 1rem;}
        h1 {font-size: 2.2rem;}
        h3 {font-size: 1.4rem; color: #2c3e50;}
        .stMetric {background-color: #f8f9fa; padding: 10px; border-radius: 5px; border: 1px solid #e9ecef;}
    </style>
""", unsafe_allow_html=True)

st.title("✈️ Dashboard Analítico de Tarifas Aéreas")
st.markdown("Visão estratégica com **controles independentes** por seção de análise.")

# 2. Carga de Dados
df_anac, df_integrado, df_ipca = carregar_dados_completos()

if df_integrado is None or df_integrado.empty:
    st.error("Erro crítico: Dados não carregados. Verifique o data_processing.py.")
    st.stop()

# Preparação de Datas
df_integrado['DATA'] = pd.to_datetime(df_integrado['ANO'].astype(str) + '-' + df_integrado['MES'].astype(str))
todas_cidades = sorted(df_integrado['CIDADE'].unique())
padrao_cidades = ['São Paulo', 'Rio de Janeiro', 'Brasília', 'Recife']
# Garante que o padrão existe nos dados
padrao_inicial = [c for c in padrao_cidades if c in todas_cidades] 
if not padrao_inicial: padrao_inicial = todas_cidades[:3]

# ===================================================================
# 3. BLOCO DE KPIs (PANORAMA DE MERCADO)
# ===================================================================
# Aqui mostramos a média de TODAS as cidades disponíveis para dar contexto
st.markdown("### 🌎 Panorama de Mercado (Todas as Capitais)")

df_ultimo_mes = df_integrado[df_integrado['DATA'] == df_integrado['DATA'].max()]
df_penultimo_mes = df_integrado[df_integrado['DATA'] == (df_integrado['DATA'].max() - pd.DateOffset(months=1))]

# Cálculos
kpi_tarifa = df_ultimo_mes['TARIFA'].mean()
kpi_tarifa_ant = df_penultimo_mes['TARIFA'].mean() if not df_penultimo_mes.empty else kpi_tarifa
delta_tarifa = kpi_tarifa - kpi_tarifa_ant

kpi_temp = df_ultimo_mes['TEMP_MEDIA'].mean()
kpi_temp_ant = df_penultimo_mes['TEMP_MEDIA'].mean() if not df_penultimo_mes.empty else kpi_temp
delta_temp = kpi_temp - kpi_temp_ant

# Colunas de KPI
k1, k2, k3, k4 = st.columns(4)
k1.metric("Tarifa Média Global", f"R$ {kpi_tarifa:.2f}", f"{delta_tarifa:.2f} R$", delta_color="inverse")
k2.metric("Temperatura Média Global", f"{kpi_temp:.1f} °C", f"{delta_temp:.1f} °C", delta_color="off")

# IPCA (Mais recente disponível)
if df_ipca is not None:
    df_ipca['DATA'] = pd.to_datetime(df_ipca['ANO'].astype(str) + '-' + df_ipca['MES'].astype(str))
    ipca_atual = df_ipca.iloc[-1]['IPCA']
    ipca_delta = ipca_atual - df_ipca.iloc[-2]['IPCA'] if len(df_ipca) > 1 else 0
    k3.metric("IPCA (Último)", f"{ipca_atual:.2f}%", f"{ipca_delta:.2f} p.p", delta_color="inverse")

# Cidade mais cara
cidade_cara = df_ultimo_mes.loc[df_ultimo_mes['TARIFA'].idxmax()]
k4.metric("Capital Mais Cara (Mês)", cidade_cara['CIDADE'], f"R$ {cidade_cara['TARIFA']:.2f}", delta_color="off")

st.divider()

# ===================================================================
# 4. SEÇÃO 1: ANÁLISE TEMPORAL (FILTRO INDIVIDUAL)
# ===================================================================
st.subheader("📈 Evolução de Preços")

# Layout: Filtro na esquerda (pequeno), Gráfico na direita (grande)
c1_filtro, c1_grafico = st.columns([1, 3])

with c1_filtro:
    st.markdown("**Configuração:**")
    filtro_tempo = st.multiselect(
        "Comparar Cidades:",
        options=todas_cidades,
        default=padrao_inicial,
        key="filtro_tempo"
    )

with c1_grafico:
    if not filtro_tempo:
        st.warning("Selecione cidades ao lado.")
    else:
        df_t1 = df_integrado[df_integrado['CIDADE'].isin(filtro_tempo)]
        
        chart_linha = alt.Chart(df_t1).mark_line(point=True, strokeWidth=3).encode(
            x=alt.X('DATA:T', title='Data', axis=alt.Axis(format='%b/%Y')),
            y=alt.Y('TARIFA:Q', title='Tarifa (R$)'),
            color=alt.Color('CIDADE:N', title='Cidade'),
            tooltip=['DATA:T', 'CIDADE', 'TARIFA']
        ).properties(height=350).interactive()
        st.altair_chart(chart_linha, use_container_width=True)

st.divider()

# ===================================================================
# 5. SEÇÃO 2: CORRELAÇÃO E DISTRIBUIÇÃO (FILTRO INDIVIDUAL)
# ===================================================================
st.subheader("🌡️ Análise de Clima & Distribuição")

c2_filtro, c2_grafico = st.columns([1, 3])

with c2_filtro:
    st.markdown("**Configuração:**")
    filtro_clima = st.multiselect(
        "Analisar Cidades:",
        options=todas_cidades,
        default=padrao_inicial[:2], # Padrão diferente (só 2 cidades) para focar
        key="filtro_clima"
    )

with c2_grafico:
    if not filtro_clima:
        st.warning("Selecione cidades ao lado.")
    else:
        df_t2 = df_integrado[df_integrado['CIDADE'].isin(filtro_clima)]
        
        # Usando tabs para organizar gráficos diferentes sem poluir
        tab_scatter, tab_box = st.tabs(["Dispersão (Preço x Clima)", "Boxplot (Variação de Preço)"])
        
        with tab_scatter:
            base = alt.Chart(df_t2).encode(
                x=alt.X('TEMP_MEDIA:Q', title='Temperatura (°C)', scale=alt.Scale(zero=False)),
                y=alt.Y('TARIFA:Q', title='Tarifa (R$)', scale=alt.Scale(zero=False)),
                color='CIDADE:N'
            )
            scatter = base.mark_circle(size=80, opacity=0.6).encode(tooltip=['CIDADE', 'DATA:T', 'TARIFA', 'TEMP_MEDIA'])
            regressao = base.transform_regression('TEMP_MEDIA', 'TARIFA', groupby=['CIDADE']).mark_line(size=2)
            st.altair_chart((scatter + regressao).interactive(), use_container_width=True)
            
        with tab_box:
            box = alt.Chart(df_t2).mark_boxplot(size=40).encode(
                x=alt.X('CIDADE:N', title=None),
                y=alt.Y('TARIFA:Q', title='Tarifa (R$)'),
                color=alt.Color('CIDADE:N', legend=None),
                tooltip=['CIDADE', 'TARIFA']
            ).interactive()
            st.altair_chart(box, use_container_width=True)

st.divider()

# ===================================================================
# 6. SEÇÃO 3: MACROECONOMIA (FILTRO INDIVIDUAL)
# ===================================================================
st.subheader("🇧🇷 Contexto Econômico (Inflação)")

c3_filtro, c3_grafico = st.columns([1, 3])

with c3_filtro:
    st.markdown("**Configuração:**")
    filtro_ipca = st.multiselect(
        "Compor média com:",
        options=todas_cidades,
        default=padrao_inicial,
        key="filtro_ipca"
    )

with c3_grafico:
    if not filtro_ipca or df_ipca is None:
        st.warning("Selecione cidades ou verifique dados do IPCA.")
    else:
        # Filtra e calcula média
        df_t3 = df_integrado[df_integrado['CIDADE'].isin(filtro_ipca)]
        media_sel = df_t3.groupby('DATA')['TARIFA'].mean().reset_index()
        
        # Filtra IPCA para bater datas
        df_ipca_recorte = df_ipca[(df_ipca['DATA'] >= media_sel['DATA'].min()) & (df_ipca['DATA'] <= media_sel['DATA'].max())]
        
        # Gráfico Dual Axis
        base = alt.Chart(media_sel).encode(x='DATA:T')
        line_price = base.mark_line(color='#2980b9', strokeWidth=3).encode(
            y=alt.Y('TARIFA', title='Média Selecionada (R$)', axis=alt.Axis(titleColor='#2980b9')),
            tooltip=[alt.Tooltip('TARIFA', title='Média R$', format=',.2f')]
        )
        
        base_ipca = alt.Chart(df_ipca_recorte).encode(x='DATA:T')
        line_inf = base_ipca.mark_line(color='#c0392b', strokeDash=[4,4]).encode(
            y=alt.Y('IPCA', title='IPCA (%)', axis=alt.Axis(titleColor='#c0392b')),
            tooltip=[alt.Tooltip('IPCA', title='Inflação %')]
        )
        
        chart_macro = alt.layer(line_inf, line_price).resolve_scale(y='independent').interactive()
        st.altair_chart(chart_macro, use_container_width=True)