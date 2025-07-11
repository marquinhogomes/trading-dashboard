#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Status Dashboard - Verificação das Funcionalidades
"""

import streamlit as st
import sys
import os

# Adiciona o diretório ao path
sys.path.append('.')

def test_header_status():
    """Testa se o header de status está funcionando corretamente"""
    
    st.title("🧪 Teste de Status das Funcionalidades")
    
    # Importa o sistema
    try:
        from dashboard_trading_pro_real import TradingSystemReal, render_header
        st.success("✅ Dashboard importado com sucesso")
    except Exception as e:
        st.error(f"❌ Erro ao importar dashboard: {str(e)}")
        return
    
    # Inicializa o sistema se não existir
    if 'trading_system' not in st.session_state:
        st.session_state.trading_system = TradingSystemReal()
        st.info("🔄 Sistema inicializado")
    
    sistema = st.session_state.trading_system
    
    # SEÇÃO DE TESTES
    st.markdown("## 🔍 Status Atual do Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Variáveis de Estado")
        st.write(f"**mt5_connected:** {sistema.mt5_connected}")
        st.write(f"**running:** {sistema.running}")
        st.write(f"**logs count:** {len(sistema.logs)}")
        st.write(f"**sinais_ativos:** {len(sistema.sinais_ativos)}")
    
    with col2:
        st.markdown("### Controles de Teste")
        
        if st.button("🔴 Simular MT5 OFF"):
            sistema.mt5_connected = False
            st.success("MT5 simulado como DESCONECTADO")
            st.rerun()
        
        if st.button("🟢 Simular MT5 ON"):
            sistema.mt5_connected = True
            st.success("MT5 simulado como CONECTADO")
            st.rerun()
            
        if st.button("🔄 Simular Sistema ON"):
            sistema.running = True
            st.success("Sistema simulado como RODANDO")
            st.rerun()
            
        if st.button("⏹️ Simular Sistema OFF"):
            sistema.running = False
            st.success("Sistema simulado como PARADO")
            st.rerun()
    
    st.markdown("---")
    
    # RENDERIZA O HEADER REAL
    st.markdown("## 📊 Render do Header (Real)")
    try:
        render_header()
        st.success("✅ Header renderizado com sucesso")
    except Exception as e:
        st.error(f"❌ Erro ao renderizar header: {str(e)}")
    
    # LÓGICA MANUAL PARA COMPARAR
    st.markdown("## 🧮 Lógica Manual (Para Comparação)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status = "🟢 online" if sistema.mt5_connected else "🔴 offline"
        st.markdown(f"**🔗 Conexão MT5**\n\n{status}")
    
    with col2:
        status = "🟢 online" if sistema.mt5_connected else "🔴 offline"
        st.markdown(f"**💰 Informações Financeiras**\n\n{status}")
    
    with col3:
        status = "🟢 online" if (sistema.mt5_connected and sistema.running) else "🔴 offline"
        st.markdown(f"**📊 Sinais de Trading**\n\n{status}")
    
    with col4:
        status = "🟢 online" if sistema.mt5_connected else "🔴 offline"
        st.markdown(f"**📋 Relatórios/Exportação**\n\n{status}")
    
    st.markdown("---")
    
    # LOGS DO SISTEMA
    st.markdown("## 📝 Logs do Sistema")
    if sistema.logs:
        logs_recentes = sistema.logs[-10:]  # Últimos 10 logs
        for log in logs_recentes:
            st.text(log)
    else:
        st.info("Nenhum log disponível")
    
    # AUTO-REFRESH
    if st.checkbox("🔄 Auto-refresh (5s)", value=False):
        import time
        time.sleep(5)
        st.rerun()

if __name__ == "__main__":
    test_header_status()
