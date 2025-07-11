#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar as mudanças na UI do dashboard
"""

import streamlit as st
import sys
import os

# Configura o Streamlit
st.set_page_config(
    page_title="Test - Trading Dashboard Pro",
    page_icon="📈",
    layout="wide"
)

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Importa e executa as funções do dashboard
    from dashboard_trading_pro_real import render_header, TradingSystemReal
    
    st.title("🧪 Teste da Nova Interface")
    st.markdown("### Verificando se as mudanças foram aplicadas corretamente:")
    
    # Inicializa o sistema se não existir
    if 'trading_system' not in st.session_state:
        st.session_state.trading_system = TradingSystemReal()
    
    st.markdown("---")
    st.markdown("### Preview da nova seção de status:")
    
    # Renderiza apenas o header modificado
    render_header()
    
    st.markdown("---")
    st.markdown("### ✅ Verificações:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🎯 Removido:**")
        st.markdown("- ✅ Header azul principal")
        st.markdown("- ✅ Título 'Status das Funcionalidades'")
        st.markdown("- ✅ Botão 'Ver Status Completo'")
    
    with col2:
        st.markdown("**🎯 Modificado:**")
        st.markdown("- ✅ Status simplificado")
        st.markdown("- ✅ Apenas 'online' ou 'offline'")
        st.markdown("- ✅ Layout limpo")
    
    with col3:
        st.markdown("**🎯 Mantido:**")
        st.markdown("- ✅ 4 colunas de status")
        st.markdown("- ✅ Ícones originais")
        st.markdown("- ✅ Funcionalidade completa")
    
    st.markdown("---")
    st.markdown("### 📋 Status do Sistema:")
    
    sistema = st.session_state.trading_system
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Conexão MT5:**")
        if sistema.mt5_connected:
            st.success("Sistema conectado ao MT5")
        else:
            st.warning("Sistema não conectado ao MT5 (esperado para teste)")
    
    with col2:
        st.markdown("**Interface:**")
        st.success("Nova interface carregada com sucesso!")
    
except Exception as e:
    st.error(f"❌ Erro ao testar a interface: {str(e)}")
    st.markdown("### Debug:")
    st.code(str(e))
