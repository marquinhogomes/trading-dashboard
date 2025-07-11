#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard Trading Pro - Versão Simplificada
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Trading Dashboard Pro - MT5 Real",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS básico
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
</style>
""", unsafe_allow_html=True)

class TradingSystemSimple:
    """Sistema de Trading Simplificado"""
    
    def __init__(self):
        self.mt5_connected = False
        self.running = False
        self.logs = []
        self.sinais_ativos = []
        
    def log(self, mensagem: str):
        """Adiciona log com timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {mensagem}"
        self.logs.append(log_entry)
        print(log_entry)

# Inicializa sistema
if 'trading_system' not in st.session_state:
    st.session_state.trading_system = TradingSystemSimple()

def render_header_simple():
    """Header simplificado"""
    st.title("📈 Trading Dashboard Pro - MT5 Real")
    
    col1, col2, col3, col4 = st.columns(4)
    
    sistema = st.session_state.trading_system
    
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

def render_sidebar_simple():
    """Sidebar simplificada"""
    st.sidebar.title("⚙️ Configurações")
    
    sistema = st.session_state.trading_system
    
    # Simulação de conexão MT5
    st.sidebar.markdown("### 🔌 Conexão MT5")
    if st.sidebar.button("🔗 Simular Conexão MT5"):
        sistema.mt5_connected = not sistema.mt5_connected
        status = "conectado" if sistema.mt5_connected else "desconectado"
        sistema.log(f"MT5 {status}")
        st.rerun()
    
    # Simulação de sistema
    st.sidebar.markdown("### 🎮 Sistema")
    if st.sidebar.button("🚀 Simular Sistema"):
        sistema.running = not sistema.running
        status = "iniciado" if sistema.running else "parado"
        sistema.log(f"Sistema {status}")
        st.rerun()

def main_simple():
    """Função principal simplificada"""
    
    # Header
    render_header_simple()
    
    # Sidebar
    render_sidebar_simple()
    
    # Conteúdo principal
    tab1, tab2, tab3 = st.tabs(["📊 Status", "📋 Logs", "🧪 Teste"])
    
    sistema = st.session_state.trading_system
    
    with tab1:
        st.markdown("### 📊 Status do Sistema")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("MT5", "Conectado" if sistema.mt5_connected else "Desconectado")
            st.metric("Sistema", "Rodando" if sistema.running else "Parado")
        
        with col2:
            st.metric("Logs", len(sistema.logs))
            st.metric("Sinais", len(sistema.sinais_ativos))
    
    with tab2:
        st.markdown("### 📋 Logs do Sistema")
        
        if sistema.logs:
            for log in sistema.logs[-10:]:  # Últimos 10 logs
                st.text(log)
        else:
            st.info("Nenhum log disponível")
    
    with tab3:
        st.markdown("### 🧪 Teste de Funcionalidades")
        
        if st.button("🔄 Gerar Log de Teste"):
            sistema.log("Teste de log executado com sucesso")
            st.success("Log gerado!")
            st.rerun()
        
        if st.button("📊 Simular Sinais"):
            sistema.sinais_ativos = [
                {"par": "PETR4/VALE3", "zscore": 2.5, "sinal": "VENDA"},
                {"par": "ITUB4/BBDC4", "zscore": -2.1, "sinal": "COMPRA"}
            ]
            sistema.log(f"Gerados {len(sistema.sinais_ativos)} sinais de teste")
            st.success("Sinais simulados!")
            st.rerun()

# Execução
if __name__ == "__main__":
    main_simple()
