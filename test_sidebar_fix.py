#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste para verificar se o botão de conectar MT5 aparece na sidebar
"""

import streamlit as st
import sys
import os

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurações básicas do Streamlit
st.set_page_config(
    page_title="🧪 Teste Sidebar MT5",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded"
)

def test_mt5_button_logic():
    """Testa a lógica do botão MT5 sem dependencies pesadas"""
    
    st.title("🧪 Teste da Lógica do Botão MT5")
    
    # Simula o estado de conexão
    if 'mt5_connected' not in st.session_state:
        st.session_state.mt5_connected = False
    
    # SIDEBAR - Seção MT5
    st.sidebar.markdown("### 🔌 Conexão MT5")
    
    is_connected = st.session_state.mt5_connected
    
    # Campos de login (só aparecem quando desconectado)
    if not is_connected:
        mt5_login = st.sidebar.number_input("Login", value=12345, format="%d")
        mt5_password = st.sidebar.text_input("Senha", type="password", value="test123")
        mt5_server = st.sidebar.text_input("Servidor", value="MetaQuotes-Demo")
    else:
        mt5_login = 12345
        mt5_password = "***"
        mt5_server = "MetaQuotes-Demo"
    
    # Interface de conexão
    col_btn, col_status = st.sidebar.columns([1, 1])
    
    with col_btn:
        if is_connected:
            # Quando conectado, botão vira "Desconectar"
            if st.button("🔌 Desconectar", use_container_width=True):
                st.session_state.mt5_connected = False
                st.success("🔌 Desconectado!")
                st.rerun()
        else:
            # Quando desconectado, botão normal "Conectar"
            if st.button("🔗 Conectar", use_container_width=True):
                # Simula conexão bem-sucedida
                st.session_state.mt5_connected = True
                st.success("✅ MT5 Conectado com sucesso!")
                st.rerun()
    
    with col_status:
        if is_connected:
            st.markdown("""
            <div style="background-color: #28a745; color: white; padding: 8px; border-radius: 4px; text-align: center; font-size: 12px;">
                Conectado
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background-color: #dc3545; color: white; padding: 8px; border-radius: 4px; text-align: center; font-size: 12px;">
                Desconectado
            </div>
            """, unsafe_allow_html=True)
    
    # CONTEÚDO PRINCIPAL
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Status Atual")
        st.write(f"**Conexão MT5:** {'🟢 Conectado' if is_connected else '🔴 Desconectado'}")
        st.write(f"**Login:** {mt5_login}")
        st.write(f"**Servidor:** {mt5_server}")
    
    with col2:
        st.markdown("### 🔧 Debug Info")
        st.write(f"**Session State:** {st.session_state}")
        st.write(f"**Botão esperado:** {'Desconectar' if is_connected else 'Conectar'}")
        
        if st.button("🔄 Reset Estado"):
            st.session_state.mt5_connected = False
            st.rerun()

if __name__ == "__main__":
    test_mt5_button_logic()
