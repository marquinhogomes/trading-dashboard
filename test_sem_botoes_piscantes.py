#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste: Verificação da Remoção dos Botões Piscantes
Confirma que os st.success foram removidos dos controles do sistema
"""

import streamlit as st
import sys
import os

# Configuração da página
st.set_page_config(
    page_title="Teste Sem Botões Piscantes",
    page_icon="🚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS dos botões
st.markdown("""
<style>
    .system-status-running {
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
    
    .system-status-stopped {
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
    
    .sem-piscar {
        border: 2px solid #28a745;
        background: rgba(40, 167, 69, 0.1);
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Estado do sistema simulado
if 'sistema_rodando' not in st.session_state:
    st.session_state.sistema_rodando = False

st.title("🚫 Teste: Interface Sem Botões Piscantes")

st.markdown("""
### ✅ Correção Implementada:

**❌ PROBLEMA ANTERIOR:**
- Botões `st.success("Sistema Iniciado!")` piscavam na tela
- Causavam poluição visual
- Atrapalhavam a experiência do usuário

**✅ SOLUÇÃO APLICADA:**
- Removidos todos os `st.success()` dos controles
- Status agora é visual apenas (botão colorido)
- Interface limpa e estável
- Sem elementos piscantes ou temporários
""")

st.markdown("---")

# SIDEBAR - CONTROLES SEM BOTÕES PISCANTES
st.sidebar.markdown("## ⚙️ Configurações do Sistema")

st.sidebar.markdown('<div class="sidebar-section sem-piscar">', unsafe_allow_html=True)
st.sidebar.markdown("### 🎮 Controles do Sistema")
st.sidebar.markdown("**🚫 SEM BOTÕES PISCANTES**")

# Interface de controle no mesmo formato MT5
is_running = st.session_state.sistema_rodando

# Interface de controle compacta
col_btn, col_status = st.sidebar.columns([1, 1])

with col_btn:
    if is_running:
        # Quando rodando, botão vira "Parar Sistema"
        if st.button("⏹️ Parar Sistema", use_container_width=True, help="Clique para parar o sistema"):
            st.session_state.sistema_rodando = False
            # SEM st.success() aqui - evita botão piscante
            st.rerun()
    else:
        # Quando parado, botão normal "Iniciar Sistema"
        if st.button("▶️ Iniciar Sistema", use_container_width=True, help="Clique para iniciar o sistema"):
            st.session_state.sistema_rodando = True
            # SEM st.success() aqui - evita botão piscante
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
        # Botão vermelho quando sistema parado
        st.markdown("""
        <div class="system-status-stopped">
            Parado
        </div>
        """, unsafe_allow_html=True)

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# VERIFICAÇÃO NO CORPO PRINCIPAL
st.markdown("### 🔍 Verificação da Interface")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎯 Status Atual:")
    
    if st.session_state.sistema_rodando:
        st.success("🟢 **SISTEMA RODANDO**")
        st.markdown("""
        **✅ Comportamento Correto:**
        - Botão esquerdo: "⏹️ Parar Sistema"
        - Botão direito: "Rodando" (verde)
        - SEM mensagens piscantes
        - Interface estável
        """)
    else:
        st.error("🔴 **SISTEMA PARADO**")
        st.markdown("""
        **✅ Comportamento Correto:**
        - Botão esquerdo: "▶️ Iniciar Sistema"
        - Botão direito: "Parado" (vermelho)
        - SEM mensagens piscantes
        - Interface estável
        """)

with col2:
    st.markdown("#### 🚫 Elementos Removidos:")
    
    st.markdown("""
    **❌ ANTES (com problemas):**
    ```python
    if st.button("▶️ Iniciar Sistema"):
        sistema.iniciar()
        st.success("Sistema Iniciado!")  # ← PISCAVA
        st.rerun()
    ```
    
    **✅ AGORA (corrigido):**
    ```python
    if st.button("▶️ Iniciar Sistema"):
        sistema.iniciar()
        # SEM st.success() aqui
        st.rerun()
    ```
    
    **🎯 Benefícios:**
    - Interface limpa
    - Sem poluição visual
    - Status visual consistente
    - Experiência mais profissional
    """)

st.markdown("---")

# TESTE INTERATIVO
st.markdown("### 🧪 Teste Interativo:")

st.markdown("""
**🔄 Clique nos botões da sidebar para testar:**

1. **Clique "Iniciar Sistema":**
   - Botão vira "Parar Sistema"
   - Status fica verde "Rodando"
   - SEM mensagem piscante

2. **Clique "Parar Sistema":**
   - Botão vira "Iniciar Sistema"
   - Status fica vermelho "Parado"
   - SEM mensagem piscante

3. **Observe a estabilidade:**
   - Interface não pisca
   - Status é apenas visual
   - Experiência limpa e profissional
""")

# COMPARAÇÃO VISUAL
st.markdown("### 📊 Comparação Visual:")

col_antes, col_depois = st.columns(2)

with col_antes:
    st.markdown("#### ❌ ANTES (Problemático)")
    st.code("""
# Interface com botões piscantes
if botao_clicado:
    st.success("Sistema Iniciado!")  # ← PISCA
    st.success("Sistema Parado!")    # ← PISCA
    st.rerun()

# Resultado: Interface instável
""", language='python')

with col_depois:
    st.markdown("#### ✅ DEPOIS (Corrigido)")
    st.code("""
# Interface limpa sem piscadas
if botao_clicado:
    # Apenas atualiza o estado
    st.rerun()

# Status visual sempre presente
# Resultado: Interface estável
""", language='python')

st.markdown("---")
st.markdown("**🎉 Resultado: Interface limpa e estável, sem elementos piscantes!**")
