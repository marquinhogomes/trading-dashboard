#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Final da Interface MT5 - SEM Emojis de Bola
Demonstra a interface limpa com apenas texto no botão de status
"""

import streamlit as st
import sys
import os

# Configuração da página
st.set_page_config(
    page_title="Interface MT5 - Sem Emojis",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS dos botões MT5 
st.markdown("""
<style>
    .status-button-connected {
        background-color: #27ae60 !important;
        color: white !important;
        border: 2px solid #27ae60 !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
        text-align: center !important;
        font-weight: bold !important;
        cursor: default !important;
    }
    
    .status-button-disconnected {
        background-color: #e74c3c !important;
        color: white !important;
        border: 2px solid #e74c3c !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
        text-align: center !important;
        font-weight: bold !important;
        cursor: default !important;
    }
</style>
""", unsafe_allow_html=True)

# Estado da conexão
if 'mt5_connected' not in st.session_state:
    st.session_state.mt5_connected = False

st.title("🔌 Interface MT5 - Versão Final")

st.markdown("""
### ✨ **MUDANÇA APLICADA:**
- ❌ **Removido:** Emojis 🟢 e 🔴 dos botões de status
- ✅ **Mantido:** Fundo colorido (verde/vermelho) totalmente preenchido
- ✅ **Mantido:** Texto "Conectado" / "Desconectado"
- ✅ **Mantido:** Posicionamento (Conectar à esquerda, Status à direita)

### 🎨 **RESULTADO VISUAL:**
Interface mais limpa e profissional, com cores vibrantes mas sem emojis distrativos.
""")

st.markdown("---")

# Interface na sidebar
st.sidebar.markdown("## 🔌 Interface Limpa MT5")

is_connected = st.session_state.mt5_connected

if not is_connected:
    mt5_login = st.sidebar.number_input("Login", value=12345, format="%d")
    mt5_password = st.sidebar.text_input("Senha", type="password", value="senha123")
    mt5_server = st.sidebar.text_input("Servidor", value="Demo-Server")

# Botões lado a lado
col_btn, col_status = st.sidebar.columns([1, 1])

with col_btn:
    if is_connected:
        if st.button("🔌 Desconectar", use_container_width=True):
            st.session_state.mt5_connected = False
            st.success("Desconectado!")
            st.rerun()
    else:
        if st.button("🔗 Conectar", use_container_width=True):
            st.session_state.mt5_connected = True
            st.success("Conectado!")
            st.rerun()

with col_status:
    if is_connected:
        # Botão verde SEM emoji
        st.markdown("""
        <div class="status-button-connected">
            Conectado
        </div>
        """, unsafe_allow_html=True)
    else:
        # Botão vermelho SEM emoji
        st.markdown("""
        <div class="status-button-disconnected">
            Desconectado
        </div>
        """, unsafe_allow_html=True)

# Status no corpo principal
st.markdown("### 📊 Comparação Visual:")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ❌ **ANTES (com emojis):**")
    st.markdown("""
    ```
    ┌─────────────────┬─────────────────┐
    │  🔗 Conectar    │ 🟢 Conectado    │
    │    (azul)       │    (verde)      │
    └─────────────────┴─────────────────┘
    ```
    """)

with col2:
    st.markdown("#### ✅ **AGORA (sem emojis):**")
    st.markdown("""
    ```
    ┌─────────────────┬─────────────────┐
    │  🔗 Conectar    │   Conectado     │
    │    (azul)       │   (verde)       │
    └─────────────────┴─────────────────┘
    ```
    """)

st.markdown("---")

# Demonstração interativa
if is_connected:
    st.success("🟢 **STATUS ATUAL:** Conectado")
    st.markdown("**🎨 Observação:** Botão de status com fundo verde sólido, sem emoji.")
else:
    st.error("🔴 **STATUS ATUAL:** Desconectado")
    st.markdown("**🎨 Observação:** Botão de status com fundo vermelho sólido, sem emoji.")

st.markdown("""
### 🔧 **BENEFÍCIOS DA MUDANÇA:**
1. **Interface mais limpa** - Menos elementos visuais competindo por atenção
2. **Foco no conteúdo** - Texto claro "Conectado/Desconectado"
3. **Profissional** - Visual mais sério e corporativo
4. **Cores mantidas** - Verde/vermelho ainda indicam status claramente
5. **Consistência** - Emojis apenas nos botões de ação (🔗🔌), não no status

**✅ RESULTADO:** Interface moderna, limpa e funcional!
""")

st.markdown("---")
st.markdown("**🎯 Teste a funcionalidade alternando entre Conectar/Desconectar na sidebar**")
