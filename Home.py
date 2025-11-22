import streamlit as st
from PIL import Image
from utils_style import aplicar_estilo_padrao

# 1. Configuração da Página
st.set_page_config(
    page_title="Home - Análise de Tarifas",
    page_icon="✈️",
    layout="wide"
)

# Aplica o estilo global
aplicar_estilo_padrao()

# CSS Específico para a Home (Cartões de Navegação)
st.markdown("""
    <style>
        .nav-card {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #E5E7EB;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            text-align: center;
            transition: transform 0.2s;
            height: 200px; /* Altura fixa para alinhamento */
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .nav-card:hover {
            transform: scale(1.02);
            border-color: #0078D4;
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        }
        .nav-icon {
            font-size: 3rem;
            margin-bottom: 10px;
        }
        .nav-title {
            font-weight: 700;
            color: #111827;
            font-size: 1.1rem;
            margin-bottom: 5px;
        }
        .nav-desc {
            font-size: 0.9rem;
            color: #6B7280;
        }
        
        /* Hero Section (Título Grande) */
        .hero-box {
            background: linear-gradient(135deg, #0078D4 0%, #005a9e 100%);
            padding: 40px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 20px rgba(0,120,212,0.2);
        }
        .hero-title { font-size: 2.5rem; font-weight: 800; margin: 0; color: white; }
        .hero-subtitle { font-size: 1.2rem; font-weight: 400; margin-top: 10px; opacity: 0.9; color: #f0f0f0; }
    </style>
""", unsafe_allow_html=True)

# ===================================================================
# 1. HERO SECTION (CABEÇALHO DE DESTAQUE)
# ===================================================================
st.markdown("""
    <div class="hero-box">
        <div class="hero-title">✈️ Monitor de Tarifas Aéreas</div>
        <div class="hero-subtitle">Inteligência de dados aplicada ao setor de aviação civil brasileiro</div>
    </div>
""", unsafe_allow_html=True)

# ===================================================================
# 2. INTRODUÇÃO
# ===================================================================
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("""
    ### 🎯 O que você vai encontrar aqui?
    
    Este portal consolida dados massivos de **três grandes fontes governamentais** para oferecer uma visão clara sobre o custo de viajar no Brasil.
    
    Nós monitoramos as rotas das capitais brasileiras para entender:
    * A evolução histórica dos preços.
    * A influência da sazonalidade e do clima.
    * O impacto da inflação no bolso do passageiro.
    """)

with c2:
    st.info("**Base de Dados Atualizada:**\n\nDados processados até o último mês disponível de 2025, integrando ANAC, INMET e IBGE.")

st.divider()

# ===================================================================
# 3. MENU VISUAL (CARTÕES)
# ===================================================================
st.subheader("🔍 Explore os Módulos")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="nav-card">
        <div class="nav-icon">📈</div>
        <div class="nav-title">Dashboard Executivo</div>
        <div class="nav-desc">KPIs, gráficos de tendência e correlações climáticas interativas.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="nav-card">
        <div class="nav-icon">📄</div>
        <div class="nav-title">Relatórios & Dados</div>
        <div class="nav-desc">Tabelas detalhadas com opção de download em CSV para Excel.</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="nav-card">
        <div class="nav-icon">🗺️</div>
        <div class="nav-title">Mapa Geográfico</div>
        <div class="nav-desc">Visualização espacial de preços e temperatura por região.</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="nav-card">
        <div class="nav-icon">👥</div>
        <div class="nav-title">Equipe & Projeto</div>
        <div class="nav-desc">Conheça os especialistas e a metodologia por trás do projeto.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("👈 Utilize a barra lateral para navegar entre as páginas.")