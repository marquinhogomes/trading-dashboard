#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste da Nova Organização da Sidebar - Controles no Topo
Demonstra a reorganização com Controles acima da Conexão MT5
"""

import streamlit as st
import sys
import os

# Configuração da página
st.set_page_config(
    page_title="Teste Nova Organização Sidebar",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS dos botões (igual ao dashboard principal)
st.markdown("""
<style>
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
    
    .ordem-section {
        border: 2px solid #007bff;
        background: rgba(0, 123, 255, 0.1);
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Estados simulados
if 'sistema_rodando' not in st.session_state:
    st.session_state.sistema_rodando = False

if 'mt5_conectado' not in st.session_state:
    st.session_state.mt5_conectado = False

st.title("🎮 Teste: Nova Organização da Sidebar")

st.markdown("""
### 📋 Reorganização Implementada:

**✅ NOVA ORDEM:**
1. **🎮 Controles** (Iniciar/Parar Sistema)
2. **🔌 Conexão MT5** (Conectar/Status)
3. **📊 Ativos Monitorados**
4. **🎯 Parâmetros de Trading**
5. **🔧 Utilidades** (Salvar/Reset)

**🎯 Objetivo:** Controles principais no topo para acesso rápido!
""")

st.markdown("---")

# SIDEBAR COM NOVA ORGANIZAÇÃO
st.sidebar.markdown("## ⚙️ Configurações do Sistema")

# 1. CONTROLES - AGORA NO TOPO
st.sidebar.markdown('<div class="sidebar-section ordem-section">', unsafe_allow_html=True)
st.sidebar.markdown("### 🎮 Controles")
st.sidebar.markdown("**🔝 POSIÇÃO 1 - PRIORIDADE MÁXIMA**")

col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("▶️ Iniciar Sistema", type="primary"):
        st.session_state.sistema_rodando = True
        st.success("Sistema Iniciado!")
        st.rerun()

with col2:
    if st.button("⏹️ Parar Sistema"):
        st.session_state.sistema_rodando = False
        st.success("Sistema Parado!")
        st.rerun()

# Status do sistema
if st.session_state.sistema_rodando:
    st.sidebar.success("🟢 Sistema Iniciado!")
else:
    st.sidebar.info("🔴 Sistema Parado")

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# 2. CONEXÃO MT5 - AGORA EM SEGUNDO
st.sidebar.markdown('<div class="sidebar-section ordem-section">', unsafe_allow_html=True)
st.sidebar.markdown("### 🔌 Conexão MT5")
st.sidebar.markdown("**🔝 POSIÇÃO 2 - CONEXÃO ESSENCIAL**")

# Campos de login apenas se desconectado
if not st.session_state.mt5_conectado:
    st.sidebar.number_input("Login", value=12345, format="%d")
    st.sidebar.text_input("Senha", type="password", value="senha123")
    st.sidebar.text_input("Servidor", value="Demo-Server")

# Botões de conexão
col_btn, col_status = st.sidebar.columns([1, 1])

with col_btn:
    if st.session_state.mt5_conectado:
        if st.button("🔌 Desconectar", use_container_width=True):
            st.session_state.mt5_conectado = False
            st.success("🔌 Desconectado!")
            st.rerun()
    else:
        if st.button("🔗 Conectar", use_container_width=True):
            st.session_state.mt5_conectado = True
            st.success("✅ Conectado!")
            st.rerun()

with col_status:
    if st.session_state.mt5_conectado:
        st.markdown("""
        <div class="status-button-connected">
            Conectado
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-button-disconnected">
            Desconectado
        </div>
        """, unsafe_allow_html=True)

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# 3. ATIVOS MONITORADOS
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.markdown("### 📊 Ativos Monitorados")
st.sidebar.markdown("**🔝 POSIÇÃO 3**")

st.sidebar.multiselect(
    "Segmentos", 
    ["Forex", "Índices", "Commodities", "Criptos"],
    default=["Forex"]
)

st.sidebar.multiselect(
    "Ativos Específicos",
    ["EURUSD", "GBPUSD", "USDJPY", "SP500"],
    default=["EURUSD"]
)

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# 4. PARÂMETROS DE TRADING
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.markdown("### 🎯 Parâmetros de Trading")
st.sidebar.markdown("**🔝 POSIÇÃO 4**")

st.sidebar.selectbox("Timeframe", ["1 min", "5 min", "15 min", "1 hora", "1 dia"], index=4)
st.sidebar.slider("Z-Score Threshold", 0.5, 3.0, 2.0, 0.1)
st.sidebar.slider("Máx. Posições", 1, 20, 6)

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# 5. UTILIDADES
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.markdown("### 🔧 Utilidades")
st.sidebar.markdown("**🔝 POSIÇÃO 5 - FINAL**")

if st.sidebar.button("💾 Salvar Perfil"):
    st.sidebar.success("Perfil salvo!")

if st.sidebar.button("🔄 Reset Completo"):
    st.session_state.sistema_rodando = False
    st.session_state.mt5_conectado = False
    st.sidebar.success("Sistema resetado!")

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# PAINEL PRINCIPAL - VERIFICAÇÃO
st.markdown("### 🔍 Verificação da Nova Organização")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ✅ Ordem Atual da Sidebar:")
    
    st.markdown("""
    **1️⃣ 🎮 Controles** 
    - ▶️ Iniciar Sistema
    - ⏹️ Parar Sistema
    - Status: Sistema rodando
    
    **2️⃣ 🔌 Conexão MT5**
    - Campos de login (se desconectado)
    - 🔗 Conectar/Desconectar
    - Status visual (verde/vermelho)
    
    **3️⃣ 📊 Ativos Monitorados**
    - Seleção de segmentos
    - Seleção de ativos
    
    **4️⃣ 🎯 Parâmetros**
    - Timeframe, Z-Score, etc.
    
    **5️⃣ 🔧 Utilidades**
    - Salvar, Reset, etc.
    """)

with col2:
    st.markdown("#### 🎯 Benefícios da Reorganização:")
    
    if st.session_state.sistema_rodando:
        st.success("🟢 **SISTEMA RODANDO**")
    else:
        st.error("🔴 **SISTEMA PARADO**")
    
    if st.session_state.mt5_conectado:
        st.success("🟢 **MT5 CONECTADO**")
    else:
        st.error("🔴 **MT5 DESCONECTADO**")
    
    st.markdown("""
    **✅ Vantagens:**
    - Controles principais no topo
    - Acesso imediato aos botões críticos
    - Sequência lógica de operação
    - Interface mais intuitiva
    - Fluxo de trabalho otimizado
    
    **🎮 Fluxo Ideal:**
    1. Conectar ao MT5
    2. Iniciar o sistema
    3. Configurar parâmetros
    4. Monitorar operações
    """)

st.markdown("---")

# INSTRUÇÕES DE TESTE
st.markdown("### 🧪 Instruções de Teste:")

st.markdown("""
1. **🔝 Observe a nova ordem na sidebar**
   - Controles estão no topo (posição de destaque)
   - MT5 em segundo lugar (conexão essencial)

2. **🎮 Teste os controles:**
   - Clique "Iniciar Sistema" (fica verde)
   - Clique "Parar Sistema" (fica vermelho)

3. **🔌 Teste a conexão MT5:**
   - Conecte/desconecte e veja o status
   - Campos aparecem/desaparecem conforme necessário

4. **✅ Verifique a hierarquia:**
   - Elementos mais importantes ficaram no topo
   - Acesso rápido aos controles principais
   - Interface mais lógica e intuitiva
""")

st.markdown("---")
st.markdown("**🎉 Resultado: Controles reorganizados com sucesso! Interface mais eficiente e intuitiva.**")
