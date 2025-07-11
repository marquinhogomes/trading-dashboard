#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher simples para testar o dashboard
"""

import streamlit as st
import sys
import os

# Configura a página
st.set_page_config(
    page_title="Dashboard Trading Pro - Teste",
    page_icon="📈",
    layout="wide"
)

st.title("🔧 Teste do Dashboard Trading Pro")

# Testa importação
try:
    from dashboard_trading_pro_real import TradingSystemReal
    st.success("✅ Importação da classe TradingSystemReal: OK")
    
    # Testa criação da instância
    if 'sistema_teste' not in st.session_state:
        st.session_state.sistema_teste = TradingSystemReal()
    
    st.success("✅ Criação da instância: OK")
    
    # Verifica métodos
    metodos = ['iniciar_sistema', 'parar_sistema', 'conectar_mt5', 'log']
    
    for metodo in metodos:
        if hasattr(st.session_state.sistema_teste, metodo):
            st.success(f"✅ Método '{metodo}': OK")
        else:
            st.error(f"❌ Método '{metodo}': NÃO ENCONTRADO")
    
    # Botão de teste
    if st.button("🧪 Testar Método iniciar_sistema"):
        if hasattr(st.session_state.sistema_teste, 'iniciar_sistema'):
            st.success("✅ Método iniciar_sistema encontrado e acessível!")
        else:
            st.error("❌ Método iniciar_sistema NÃO encontrado!")
    
    # Informações de debug
    st.markdown("### 🔍 Debug Info")
    st.write("Métodos disponíveis:")
    metodos_disponiveis = [method for method in dir(st.session_state.sistema_teste) if not method.startswith('_')]
    st.write(metodos_disponiveis)
    
    # Link para o dashboard real
    st.markdown("---")
    if st.button("🚀 Executar Dashboard Real"):
        st.markdown("Execute o comando: `streamlit run dashboard_trading_pro_real.py`")

except Exception as e:
    st.error(f"❌ Erro: {str(e)}")
    st.exception(e)
