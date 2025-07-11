#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste dos Controles do Sistema - Novo Formato
Demonstra botões Iniciar/Parar Sistema no mesmo formato dos botões MT5
"""

import streamlit as st
import sys
import os

# Configuração da página
st.set_page_config(
    page_title="Teste Controles Sistema",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS dos botões (copiado do dashboard principal)
st.markdown("""
<style>
    /* Botões de status do Sistema */
    .system-status-running {
        background-color: #28a745 !important;
        color: white !important;
        border: 2px solid #28a745 !important;
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
    
    .system-status-stopped {
        background-color: #6c757d !important;
        color: white !important;
        border: 2px solid #6c757d !important;
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
    
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #dee2e6;
    }
    
    .test-box {
        border: 2px dashed #28a745;
        padding: 0.5rem;
        margin: 0.25rem 0;
        background: rgba(40, 167, 69, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Estado do sistema simulado
if 'system_running' not in st.session_state:
    st.session_state.system_running = False

st.title("🎮 Teste dos Controles do Sistema")

st.markdown("""
### 🎯 Objetivo: Controles do Sistema no mesmo formato dos botões MT5

**📊 Especificações:**
- **Layout:** Botão de ação à esquerda, status à direita
- **Cores:** Verde (rodando) / Cinza (parado)
- **Tamanhos:** Idênticos aos botões MT5 (38px altura)
- **Comportamento:** Alternância inteligente Iniciar ↔ Parar
""")

st.markdown("---")

# Interface na sidebar
st.sidebar.markdown("## 🎮 Teste Controles")
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.markdown("### 🎮 Controles do Sistema")

# Estado atual
is_running = st.session_state.system_running

# Área de teste destacada
st.sidebar.markdown('<div class="test-box">', unsafe_allow_html=True)
st.sidebar.markdown("**🔍 Área de Teste - Controles Uniformes:**")
col_btn, col_status = st.sidebar.columns([1, 1])

with col_btn:
    if is_running:
        # Quando rodando, botão vira "Parar Sistema"
        if st.button("⏹️ Parar Sistema", use_container_width=True, help="Sistema rodando - clique para parar"):
            st.session_state.system_running = False
            st.success("⏹️ Sistema Parado!")
            st.rerun()
    else:
        # Quando parado, botão normal "Iniciar Sistema"
        if st.button("▶️ Iniciar Sistema", use_container_width=True, help="Sistema parado - clique para iniciar"):
            st.session_state.system_running = True
            st.success("▶️ Sistema Iniciado!")
            st.rerun()

with col_status:
    if is_running:
        # Botão verde quando sistema rodando
        st.markdown("""
        <div class="system-status-running">
            Rodando
        </div>
        """, unsafe_allow_html=True)
    else:
        # Botão cinza quando sistema parado
        st.markdown("""
        <div class="system-status-stopped">
            Parado
        </div>
        """, unsafe_allow_html=True)

st.sidebar.markdown('</div>', unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Painel de verificação no corpo principal
st.markdown("### 🔍 Status e Verificação")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎛️ Estado Atual")
    
    if is_running:
        st.success("🟢 **SISTEMA: RODANDO**")
        st.markdown("""
        **Botão Esquerdo (Ação):**
        - Texto: "⏹️ Parar Sistema"
        - Função: Parar o sistema
        - Cor: Padrão Streamlit
        
        **Botão Direito (Status):**
        - Texto: "Rodando"
        - Cor: Verde #28a745
        - Estado: Ativo/Executando
        """)
    else:
        st.error("🔴 **SISTEMA: PARADO**")
        st.markdown("""
        **Botão Esquerdo (Ação):**
        - Texto: "▶️ Iniciar Sistema"
        - Função: Iniciar o sistema
        - Cor: Padrão Streamlit
        
        **Botão Direito (Status):**
        - Texto: "Parado"
        - Cor: Cinza #6c757d
        - Estado: Inativo/Parado
        """)

with col2:
    st.markdown("#### ⚖️ Comparação com MT5")
    
    st.markdown("""
    **🔌 Botões MT5:**
    - Conectar/Desconectar ↔ Verde/Vermelho
    - Altura: 38px exatos
    - Layout: [Ação] | [Status]
    
    **🎮 Botões Sistema:**
    - Iniciar/Parar ↔ Verde/Cinza
    - Altura: 38px exatos  
    - Layout: [Ação] | [Status]
    
    **✅ Uniformidade Conseguida:**
    - ✅ Mesmo tamanho e altura
    - ✅ Mesma estrutura de layout
    - ✅ Mesmo comportamento
    - ✅ CSS consistente
    """)

st.markdown("---")

# Demonstração visual
st.markdown("### 🧪 Teste Visual Interativo")

st.markdown("""
**🔄 Clique nos botões para alternar entre os estados:**

1. **🔴 Sistema Parado:** "Iniciar Sistema" + Status "Parado" (cinza)
2. **🟢 Sistema Rodando:** "Parar Sistema" + Status "Rodando" (verde)

**📋 Validações:**
- Ambos os botões sempre mantêm o mesmo tamanho
- A troca entre "Iniciar/Parar" não altera dimensões
- O botão de status muda cor automaticamente
- O alinhamento é perfeito em ambos os estados
""")

# Comparação lado a lado
st.markdown("### 📊 Comparação Lado a Lado")

col_mt5, col_sistema = st.columns(2)

with col_mt5:
    st.markdown("#### 🔌 Formato MT5")
    st.markdown("""
    ```
    ┌─────────────────┬─────────────────┐
    │  🔗 Conectar    │   Conectado     │
    │    (ação)       │   (status)      │
    └─────────────────┴─────────────────┘
    ```
    
    **Estados:**
    - 🔴 Desconectado: Conectar + Vermelho
    - 🟢 Conectado: Desconectar + Verde
    """)

with col_sistema:
    st.markdown("#### 🎮 Formato Sistema")
    st.markdown("""
    ```
    ┌─────────────────┬─────────────────┐
    │ ▶️ Iniciar Sist. │    Parado       │
    │    (ação)       │   (status)      │
    └─────────────────┴─────────────────┘
    ```
    
    **Estados:**
    - 🔴 Parado: Iniciar + Cinza
    - 🟢 Rodando: Parar + Verde
    """)

st.markdown("---")
st.markdown("**🎉 Resultado: Controles perfeitamente uniformes com os botões MT5!**")
