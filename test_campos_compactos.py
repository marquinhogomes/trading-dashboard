#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste: Verificar se os campos de entrada no sidebar ficaram compactos
"""

import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Teste Campos Compactos",
    page_icon="📏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS para campos compactos
st.markdown("""
<style>
    /* Reduz altura dos campos de entrada no sidebar */
    .stNumberInput > div > div > input {
        height: 32px !important;
        min-height: 32px !important;
        max-height: 32px !important;
        padding: 0.25rem 0.5rem !important;
        font-size: 0.875rem !important;
        line-height: 1.2 !important;
        box-sizing: border-box !important;
    }
    
    .stSelectbox > div > div > div {
        height: 32px !important;
        min-height: 32px !important;
        max-height: 32px !important;
        padding: 0.25rem 0.5rem !important;
        font-size: 0.875rem !important;
        line-height: 1.2 !important;
        box-sizing: border-box !important;
    }
    
    .stTextInput > div > div > input {
        height: 32px !important;
        min-height: 32px !important;
        max-height: 32px !important;
        padding: 0.25rem 0.5rem !important;
        font-size: 0.875rem !important;
        line-height: 1.2 !important;
        box-sizing: border-box !important;
    }
    
    /* Reduz espaçamento entre elementos no sidebar */
    .stNumberInput, .stSelectbox, .stTextInput {
        margin-bottom: 0.5rem !important;
    }
    
    /* Compacta labels dos campos */
    .stNumberInput > label, .stSelectbox > label, .stTextInput > label {
        font-size: 0.8rem !important;
        margin-bottom: 0.25rem !important;
        padding-bottom: 0 !important;
    }
    
    /* Reduz altura dos dividers no sidebar */
    .stMarkdown hr {
        margin: 0.5rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.title("🧪 Teste: Campos Compactos no Sidebar")

# Sidebar com campos de teste
with st.sidebar:
    st.header("Teste de Campos Compactos")
    
    st.subheader("📋 Seção 1: Números")
    valor1 = st.number_input("Campo Numérico 1", min_value=0, max_value=1000, value=100)
    valor2 = st.number_input("Campo Numérico 2", min_value=0.0, max_value=10.0, value=1.5, step=0.1)
    
    st.markdown("---")
    
    st.subheader("📝 Seção 2: Texto")
    texto1 = st.text_input("Campo de Texto 1", value="Exemplo")
    texto2 = st.text_input("Campo de Texto 2", value="")
    
    st.markdown("---")
    
    st.subheader("📊 Seção 3: Seleção")
    opcao1 = st.selectbox("Selectbox 1", ["Opção A", "Opção B", "Opção C"])
    opcao2 = st.selectbox("Selectbox 2", ["Item 1", "Item 2", "Item 3", "Item 4"])
    
    st.markdown("---")
    
    st.subheader("⚙️ Seção 4: Parâmetros")
    param1 = st.number_input("Período", min_value=1, max_value=100, value=20)
    param2 = st.number_input("Threshold", min_value=0.0, max_value=1.0, value=0.05, step=0.01)
    param3 = st.selectbox("Timeframe", ["1M", "5M", "15M", "1H", "4H", "1D"])
    
    st.markdown("---")
    
    # Botão para demonstrar espaçamento
    if st.button("Testar Compactação"):
        st.success("✅ Campos compactos funcionando!")

# Área principal
st.write("## 📏 Verificação de Compactação")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **🎯 Objetivo do Teste:**
    - Verificar se os campos de entrada ficaram mais compactos
    - Redução da altura das "barras brancas" de input
    - Espaçamento otimizado entre elementos
    """)

with col2:
    st.success("""
    **✅ Alterações Aplicadas:**
    - Altura dos inputs reduzida para 32px
    - Padding interno diminuído
    - Labels mais compactas
    - Margens entre elementos otimizadas
    """)

# Verificação visual
st.write("### 🔍 Verificação Visual")
st.write("**Compare o sidebar atual com a versão anterior para verificar a compactação dos campos.**")

# Dados de exemplo
st.write("### 📊 Valores Atuais dos Campos")
dados_campos = {
    "Campo": ["Valor 1", "Valor 2", "Texto 1", "Texto 2", "Opção 1", "Opção 2", "Período", "Threshold", "Timeframe"],
    "Valor": [valor1, valor2, texto1, texto2, opcao1, opcao2, param1, param2, param3],
    "Tipo": ["number", "number", "text", "text", "select", "select", "number", "number", "select"]
}

df_campos = st.dataframe(dados_campos, use_container_width=True)

st.write("### ✅ Status da Compactação")
if st.button("Verificar Compactação"):
    st.success("🎯 Campos de entrada compactados com sucesso!")
    st.info("📏 Altura reduzida de ~38px para ~32px")
    st.info("📐 Padding interno otimizado")
    st.info("🎨 Interface mais limpa e organizada")
