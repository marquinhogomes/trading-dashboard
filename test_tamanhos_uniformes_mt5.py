#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Tamanhos Uniformes dos Botões MT5
Demonstra botões com exatamente o mesmo tamanho
"""

import streamlit as st
import sys
import os

# Configuração da página
st.set_page_config(
    page_title="Teste Tamanhos Uniformes MT5",
    page_icon="📏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS melhorado para garantir tamanhos iguais
st.markdown("""
<style>
    /* Botões de status MT5 com tamanhos fixos */
    .status-button-connected {
        background-color: #27ae60 !important;
        color: white !important;
        border: 2px solid #27ae60 !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
        height: 38px !important;
        min-height: 38px !important;
        max-height: 38px !important;
        text-align: center !important;
        font-weight: bold !important;
        cursor: default !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 0.875rem !important;
        line-height: 1.2 !important;
    }
    
    .status-button-disconnected {
        background-color: #e74c3c !important;
        color: white !important;
        border: 2px solid #e74c3c !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
        height: 38px !important;
        min-height: 38px !important;
        max-height: 38px !important;
        text-align: center !important;
        font-weight: bold !important;
        cursor: default !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 0.875rem !important;
        line-height: 1.2 !important;
    }
    
    /* Força botões do Streamlit a terem o mesmo tamanho */
    .stButton > button {
        height: 38px !important;
        min-height: 38px !important;
        max-height: 38px !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 0.875rem !important;
        line-height: 1.2 !important;
        padding: 0.5rem 1rem !important;
    }
    
    /* Garante que as colunas tenham o mesmo tamanho */
    .element-container {
        width: 100% !important;
    }
    
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #dee2e6;
    }
    
    /* Destacar medidas para teste */
    .test-box {
        border: 2px dashed #007bff;
        padding: 0.5rem;
        margin: 0.25rem 0;
        background: rgba(0, 123, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Estado de conexão simulado
if 'mt5_connected' not in st.session_state:
    st.session_state.mt5_connected = False

st.title("📏 Teste de Tamanhos Uniformes - Botões MT5")

st.markdown("""
### 🎯 Objetivo: Garantir que todos os botões tenham exatamente o mesmo tamanho

**📊 Especificações Técnicas:**
- **Altura fixa:** 38px para todos os botões
- **Largura:** 100% do container (dividido igualmente)
- **Box-sizing:** border-box para incluir bordas no cálculo
- **Display:** flex com alinhamento centralizado
- **Font-size:** 0.875rem uniforme
- **Line-height:** 1.2 uniforme
""")

st.markdown("---")

# Interface MT5 na sidebar
st.sidebar.markdown("## 📏 Teste de Tamanhos")
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.markdown("### 🔌 Interface MT5")

# Estado atual
is_connected = st.session_state.mt5_connected

if not is_connected:
    # Campos de login
    st.sidebar.number_input("Login", value=12345, format="%d")
    st.sidebar.text_input("Senha", type="password", value="senha123")
    st.sidebar.text_input("Servidor", value="Demo-Server")

# Botões em colunas iguais com destaque para teste
st.sidebar.markdown('<div class="test-box">', unsafe_allow_html=True)
st.sidebar.markdown("**🔍 Área de Teste - Botões Uniformes:**")
col_btn, col_status = st.sidebar.columns([1, 1])

with col_btn:
    if is_connected:
        if st.button("🔌 Desconectar", use_container_width=True, help="Botão de desconexão - 38px altura"):
            st.session_state.mt5_connected = False
            st.rerun()
    else:
        if st.button("🔗 Conectar", use_container_width=True, help="Botão de conexão - 38px altura"):
            st.session_state.mt5_connected = True
            st.rerun()

with col_status:
    if is_connected:
        # Botão verde
        st.markdown("""
        <div class="status-button-connected">
            Conectado
        </div>
        """, unsafe_allow_html=True)
    else:
        # Botão vermelho
        st.markdown("""
        <div class="status-button-disconnected">
            Desconectado
        </div>
        """, unsafe_allow_html=True)

st.sidebar.markdown('</div>', unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Painel de verificação no corpo principal
st.markdown("### 🔍 Verificação de Tamanhos")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📐 Especificações Aplicadas")
    
    if is_connected:
        st.success("🟢 **ESTADO: CONECTADO**")
        st.markdown("""
        **Botão Esquerdo (Desconectar):**
        - Altura: 38px (nativo Streamlit)
        - Largura: 50% do container
        - Padding: 0.5rem 1rem
        - Font-size: 0.875rem
        
        **Botão Direito (Status):**
        - Altura: 38px (CSS customizado)
        - Largura: 50% do container  
        - Padding: 0.5rem 1rem
        - Font-size: 0.875rem
        """)
    else:
        st.error("🔴 **ESTADO: DESCONECTADO**")
        st.markdown("""
        **Botão Esquerdo (Conectar):**
        - Altura: 38px (nativo Streamlit)
        - Largura: 50% do container
        - Padding: 0.5rem 1rem
        - Font-size: 0.875rem
        
        **Botão Direito (Status):**
        - Altura: 38px (CSS customizado)
        - Largura: 50% do container
        - Padding: 0.5rem 1rem
        - Font-size: 0.875rem
        """)

with col2:
    st.markdown("#### ✅ Checklist de Uniformidade")
    
    st.markdown("""
    **🎯 Altura Fixa:**
    - ✅ Todos os botões: 38px exatos
    - ✅ Min-height e max-height definidos
    - ✅ Box-sizing: border-box
    
    **📏 Largura Consistente:**
    - ✅ Colunas [1, 1] = 50% cada
    - ✅ Width: 100% do container
    - ✅ Element-container forçado
    
    **🎨 Alinhamento:**
    - ✅ Display: flex
    - ✅ Align-items: center
    - ✅ Justify-content: center
    
    **📝 Tipografia:**
    - ✅ Font-size: 0.875rem
    - ✅ Line-height: 1.2
    - ✅ Font-weight: bold
    """)

st.markdown("---")

# Demonstração visual
st.markdown("### 🧪 Teste Visual Interativo")

st.markdown("""
**🔄 Clique nos botões para alternar entre os estados e verificar que:**

1. **Ambos os botões sempre mantêm o mesmo tamanho**
2. **A troca entre "Conectar/Desconectar" não altera dimensões**
3. **O botão de status permanece fixo e uniforme**
4. **O alinhamento é perfeito em ambos os estados**

**📋 Estados para testar:**
- 🔴 Desconectado: "Conectar" + "Desconectado"
- 🟢 Conectado: "Desconectar" + "Conectado"
""")

# Medidas técnicas
st.markdown("### 📊 Medidas Técnicas Implementadas")

medidas_code = '''
/* CSS aplicado para uniformidade */
.stButton > button {
    height: 38px !important;           /* Altura fixa */
    min-height: 38px !important;       /* Altura mínima */
    max-height: 38px !important;       /* Altura máxima */
    box-sizing: border-box !important; /* Inclui bordas */
    display: flex !important;          /* Layout flexível */
    align-items: center !important;    /* Centralização vertical */
    justify-content: center !important;/* Centralização horizontal */
    font-size: 0.875rem !important;   /* Tamanho de fonte fixo */
    line-height: 1.2 !important;      /* Altura da linha */
}

.status-button-connected, .status-button-disconnected {
    height: 38px !important;           /* Mesma altura dos botões nativos */
    /* ... outras propriedades idênticas ... */
}
'''

st.code(medidas_code, language='css')

st.markdown("---")
st.markdown("**🎉 Resultado: Botões perfeitamente uniformes e alinhados!**")
