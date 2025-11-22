import streamlit as st
import base64
import os
from utils_style import aplicar_estilo_padrao

# 1. Configuração da Página
st.set_page_config(layout="wide", page_title="Sobre Nós")
aplicar_estilo_padrao()

# 2. CSS Personalizado para os "Cartões de Equipe"
st.markdown("""
    <style>
        /* Estilo do Cartão (Card) */
        .team-card {
            background-color: #FFFFFF;
            border-radius: 15px;
            padding: 30px 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            text-align: center; /* Centraliza tudo */
            border: 1px solid #E5E7EB;
            transition: transform 0.3s ease;
            height: 100%; /* Tenta uniformizar altura */
        }
        
        .team-card:hover {
            transform: translateY(-5px); /* Efeito de flutuar ao passar o mouse */
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border-color: #0068C9;
        }

        /* Estilo da Foto Redonda */
        .team-img {
            width: 120px;
            height: 120px;
            object-fit: cover;
            border-radius: 50%;
            border: 4px solid #F0F2F6;
            margin-bottom: 15px;
        }

        /* Tipografia */
        .team-name {
            font-size: 1.2rem;
            font-weight: 700;
            color: #111827;
            margin-bottom: 5px;
        }

        .team-role {
            font-size: 0.9rem;
            font-weight: 600;
            color: #0068C9; /* Azul destaque */
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 15px;
        }

        .team-desc {
            font-size: 0.85rem;
            color: #6B7280;
            line-height: 1.5;
        }
    </style>
""", unsafe_allow_html=True)

st.title("👥 Nossa Equipe")
st.markdown("Conheça os especialistas por trás deste projeto.")
st.write("") # Espaço

# --- 3. FUNÇÃO PARA CARREGAR IMAGEM LOCAL NO HTML ---
def get_img_as_base64(file_path):
    """Lê uma imagem local e converte para string base64 para usar no HTML"""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# --- 4. LISTA DE DADOS DOS MEMBROS (EDITAR AQUI) ---
# Coloque os nomes reais dos arquivos das fotos aqui
# Lista de membros para facilitar a edição
membros = [
    {
        "nome": "Aline de Lucca",
        "cargo": "Engenheiro de Dados",
        "desc": "Responsável pela extração e tratamento dos dados da ANAC.",
        "foto": "foto_aline.png"
    },
    {
        "nome": "Ana Barbara Moura",
        "cargo": "Cientista de Dados",
        "desc": "Realizou as análises estatísticas e correlações climáticas.",
        "foto": "foto_anab.png"
    },
    {
        "nome": "Carlos Sousa",
        "cargo": "Desenvolvedor Streamlit",
        "desc": "Criou a interface interativa e os gráficos do dashboard.",
        "foto": "foto_carlos.png"
    },
    {
        "nome": "Gustavo Bello",
        "cargo": "Analista de BI",
        "desc": "Definiu os KPIs de negócio e indicadores de sucesso.",
        "foto": "foto_gustavo.png"
    },
    {
        "nome": "Igor Albuquerque",
        "cargo": "Cargo / Função",
        "desc": "Descrição da atividade no grupo.",
        "foto": "foto_igor.png"
    },
    {
        "nome": "Leonardo França",
        "cargo": "Cargo / Função",
        "desc": "Descrição da atividade no grupo.",
        "foto": "foto_leo.png"
    },
    {
        "nome": "Marina Jeronymo",
        "cargo": "Cargo / Função",
        "desc": "Descrição da atividade no grupo.",
        "foto": "foto_marina.png"
    },
    {
        "nome": "Sofia Toledo",
        "cargo": "Cargo / Função",
        "desc": "Descrição da atividade no grupo.",
        "foto": "foto_sofia.png"
    },
]

# --- 5. RENDERIZAÇÃO DO GRID ---

# Define quantas colunas por linha (4 é um bom número para desktop)
cols_per_row = 4 
rows = [membros[i:i + cols_per_row] for i in range(0, len(membros), cols_per_row)]

for row in rows:
    cols = st.columns(cols_per_row)
    for index, membro in enumerate(row):
        with cols[index]:
            # Processa a imagem
            img_path = os.path.join(os.getcwd(), membro["foto"])
            img_base64 = get_img_as_base64(img_path)
            
            # Se achou a imagem, usa ela. Se não, usa um placeholder cinza.
            if img_base64:
                img_src = f"data:image/jpeg;base64,{img_base64}"
            else:
                img_src = "https://via.placeholder.com/150?text=Foto"

            # Cria o HTML do Cartão
            html_card = f"""
            <div class="team-card">
                <img src="{img_src}" class="team-img">
                <div class="team-name">{membro['nome']}</div>
                <div class="team-role">{membro['cargo']}</div>
                <div class="team-desc">{membro['desc']}</div>
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)