import streamlit as st

def aplicar_estilo_padrao():
    st.markdown("""
        <style>
            /* --- IMPORTANDO FONTE ROBOTO --- */
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

            html, body, [class*="css"] {
                font-family: 'Roboto', sans-serif;
                color: #1F2937;
            }

            /* --- FUNDO E ESPAÇAMENTO --- */
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                max-width: 95rem;
            }

            /* --- TÍTULOS E CABEÇALHOS --- */
            h1 {
                color: #111827;
                font-weight: 700;
                font-size: 2.2rem;
                padding-bottom: 1rem;
                border-bottom: 1px solid #E5E7EB;
                margin-bottom: 2rem;
            }
            
            h3 {
                color: #374151;
                font-weight: 600;
                font-size: 1.2rem;
                margin-top: 1rem;
                margin-bottom: 1rem;
                padding-left: 0.5rem;
                border-left: 4px solid #0078D4; /* Detalhe azul na esquerda */
            }

            /* --- TRANSFORMAÇÃO: KPI CARDS (ST.METRIC) --- */
            /* Isso transforma o número solto em um cartão profissional */
            div[data-testid="metric-container"] {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 15px 20px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                transition: all 0.2s ease;
            }

            div[data-testid="metric-container"]:hover {
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                border-color: #0078D4;
            }

            div[data-testid="metric-container"] label {
                font-size: 0.85rem;
                color: #6B7280;
                font-weight: 500;
            }

            div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
                font-size: 1.8rem;
                font-weight: 700;
                color: #111827;
            }

            /* --- TRANSFORMAÇÃO: GRÁFICOS EM CARDS --- */
            /* Coloca um fundo branco atrás dos gráficos Altair/Plotly */
            .element-container:has(canvas), .element-container:has(iframe) {
                background-color: #FFFFFF;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #E5E7EB;
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                margin-bottom: 1rem;
            }

            /* --- TABELAS (DATAFRAME) --- */
            .stDataFrame {
                background-color: #FFFFFF;
                padding: 10px;
                border-radius: 8px;
                border: 1px solid #E5E7EB;
            }

            /* --- BARRA LATERAL --- */
            section[data-testid="stSidebar"] {
                background-color: #FFFFFF;
                border-right: 1px solid #E5E7EB;
            }
            
            /* Títulos na sidebar */
            section[data-testid="stSidebar"] h1, 
            section[data-testid="stSidebar"] h2, 
            section[data-testid="stSidebar"] h3 {
                border: none;
                padding: 0;
                margin-bottom: 10px;
                color: #4B5563;
            }

            /* --- ABAS (TABS) --- */
            .stTabs [data-baseweb="tab-list"] {
                gap: 20px;
                background-color: transparent;
                border-bottom: 1px solid #E5E7EB;
                margin-bottom: 20px;
            }

            .stTabs [data-baseweb="tab"] {
                height: 40px;
                background-color: transparent;
                border: none;
                color: #6B7280;
                font-weight: 500;
            }

            .stTabs [aria-selected="true"] {
                background-color: transparent;
                color: #0078D4;
                border-bottom: 2px solid #0078D4;
            }

            /* Remove padding extra do topo */
            .main .block-container {
                padding-top: 1rem;
            }
            
        </style>
    """, unsafe_allow_html=True)