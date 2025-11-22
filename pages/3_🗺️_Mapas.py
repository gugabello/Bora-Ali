import streamlit as st
import pandas as pd
import plotly.express as px # A biblioteca nova
from data_processing import carregar_dados_completos
import streamlit as st
from utils_style import aplicar_estilo_padrao # <--- Importa

st.set_page_config(layout="wide", page_title="...") # <--- Configura

aplicar_estilo_padrao() # <--- APLICA O CSS

# 1. Configuração da Página
st.set_page_config(layout="wide", page_title="Mapa Geográfico")

# CSS para dar um ar profissional e limpar as margens
st.markdown("""
    <style>
        .block-container {padding-top: 1.5rem; padding-bottom: 1rem;}
        h1 {font-size: 2.2rem;}
    </style>
""", unsafe_allow_html=True)

st.title("🗺️ Mapa de Tarifas e Clima")
st.markdown("Visualização espacial. O **tamanho** do círculo indica o preço da tarifa.")

# 2. Dados e Coordenadas
df_anac, df_integrado, df_ipca = carregar_dados_completos()

if df_integrado is None or df_integrado.empty:
    st.error("Erro ao carregar dados.")
    st.stop()

# --- INJEÇÃO DE COORDENADAS (Essencial pois seus dados não têm Lat/Lon) ---
COORDENADAS_CAPITAIS = {
    'AC': [-9.97, -67.81], 'AL': [-9.66, -35.73], 'AP': [0.03, -51.07],
    'AM': [-3.10, -60.02], 'BA': [-12.97, -38.51], 'CE': [-3.71, -38.54],
    'DF': [-15.78, -47.93], 'ES': [-20.31, -40.31], 'GO': [-16.68, -49.25],
    'MA': [-2.53, -44.30], 'MT': [-15.60, -56.09], 'MS': [-20.44, -54.64],
    'MG': [-19.92, -43.93], 'PA': [-1.45, -48.50], 'PB': [-7.11, -34.86],
    'PR': [-25.42, -49.27], 'PE': [-8.05, -34.88], 'PI': [-5.09, -42.80],
    'RJ': [-22.90, -43.17], 'RN': [-5.79, -35.20], 'RS': [-30.03, -51.23],
    'RO': [-8.76, -63.90], 'RR': [2.82, -60.67], 'SC': [-27.59, -48.54],
    'SP': [-23.55, -46.63], 'SE': [-10.94, -37.07], 'TO': [-10.17, -48.33]
}

def get_lat(uf): return COORDENADAS_CAPITAIS.get(uf, [0,0])[0]
def get_lon(uf): return COORDENADAS_CAPITAIS.get(uf, [0,0])[1]

# Prepara coluna de data
df_integrado['DATA_OBJ'] = pd.to_datetime(df_integrado['ANO'].astype(str) + '-' + df_integrado['MES'].astype(str))

# ===================================================================
# 3. FILTRO DE TEMPO (BARRA LATERAL)
# ===================================================================
st.sidebar.header("Configuração")

datas_unicas = sorted(df_integrado['DATA_OBJ'].unique(), reverse=True)
opcoes_datas = [d.strftime("%m/%Y") for d in datas_unicas]

data_selecionada_str = st.sidebar.selectbox("Mês de Referência:", options=opcoes_datas)

# Filtragem
mes_sel, ano_sel = map(int, data_selecionada_str.split('/'))
df_mapa = df_integrado[
    (df_integrado['MES'] == mes_sel) & 
    (df_integrado['ANO'] == ano_sel)
].copy()

# Adiciona Lat/Lon ao DF filtrado
df_mapa['lat'] = df_mapa['UF'].apply(get_lat)
df_mapa['lon'] = df_mapa['UF'].apply(get_lon)

# ===================================================================
# 4. VISUALIZAÇÃO PLOTLY (BUBBLE MAP)
# ===================================================================

# Layout em colunas para métricas e mapa
col_info, col_mapa = st.columns([1, 4])

with col_info:
    st.subheader("Resumo do Mês")
    
    maior_valor = df_mapa['TARIFA'].max()
    cidade_cara = df_mapa.loc[df_mapa['TARIFA'].idxmax()]['CIDADE']
    
    menor_valor = df_mapa['TARIFA'].min()
    cidade_barata = df_mapa.loc[df_mapa['TARIFA'].idxmin()]['CIDADE']
    
    st.metric("Capital Mais Cara", cidade_cara, f"R$ {maior_valor:.2f}", delta_color="inverse")
    st.metric("Capital Mais Barata", cidade_barata, f"R$ {menor_valor:.2f}", delta_color="off")
    
    st.info(f"""
    **Legenda:**
    
    🔵 **Tamanho:** Preço da Passagem
    
    🎨 **Cor:** Temperatura Média
    """)

with col_mapa:
    # Criação do Mapa com Plotly Express
    fig = px.scatter_mapbox(
        df_mapa,
        lat="lat",
        lon="lon",
        size="TARIFA",        # O tamanho da bolha é a tarifa
        color="TEMP_MEDIA",   # A cor é a temperatura
        hover_name="CIDADE",
        hover_data={
            "lat": False, "lon": False,
            "TARIFA": ":.2f", # Formatação R$
            "TEMP_MEDIA": ":.1f" # Formatação °C
        },
        color_continuous_scale=px.colors.diverging.RdYlBu_r, # Azul (Frio) -> Vermelho (Quente)
        size_max=40, # Tamanho máximo da bolha
        zoom=3,
        center={"lat": -15.78, "lon": -47.93}, # Centro do Brasil
        height=600
    )

    # Estilo do mapa (OpenStreetMap é gratuito e limpo)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) # Remove margens brancas
    
    # Ajuste das legendas
    fig.update_coloraxes(colorbar_title="Temp (°C)")

    st.plotly_chart(fig, use_container_width=True)

# Tabela de Apoio
with st.expander("Ver dados detalhados deste mapa"):
    st.dataframe(
        df_mapa[['CIDADE', 'UF', 'TARIFA', 'TEMP_MEDIA']].sort_values('TARIFA', ascending=False),
        use_container_width=True,
        hide_index=True,
        column_config={
            "TARIFA": st.column_config.NumberColumn("Tarifa", format="R$ %.2f"),
            "TEMP_MEDIA": st.column_config.NumberColumn("Temp", format="%.1f °C"),
        }
    )