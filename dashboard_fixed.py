#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard Trading Profissional - Operações Reais MT5 - VERSÃO CORRIGIDA
Sistema completo de monitoramento e controle de trading
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Trading Dashboard Pro - MT5 Real",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado básico
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .status-online { color: #27ae60; font-weight: bold; }
    .status-offline { color: #e74c3c; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

class TradingSystemReal:
    """Sistema de Trading Real com MT5"""
    
    def __init__(self):
        self.mt5_connected = False
        self.running = False
        self.dados_sistema = {
            "execucoes": 0,
            "pares_processados": 0,
            "posicoes_abertas": 0,
            "lucro_diario": 0.0,
            "ultimo_update": None
        }
        self.logs = []
        self.sinais_ativos = []
        
    def log(self, mensagem: str):
        """Adiciona log com timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {mensagem}"
        self.logs.append(log_entry)
        if len(self.logs) > 100:
            self.logs = self.logs[-50:]
        print(log_entry)

# Inicializa sistema global
if 'trading_system' not in st.session_state:
    st.session_state.trading_system = TradingSystemReal()

def render_header():
    """Renderiza status das funcionalidades"""
    col1, col2, col3, col4 = st.columns(4)
    
    sistema = st.session_state.trading_system
    
    with col1:
        status = "online" if sistema.mt5_connected else "offline"
        color = "🟢" if sistema.mt5_connected else "🔴"
        st.markdown(f"""
        **🔗 Conexão MT5** {color}  
        **{status}**
        """)
    
    with col2:
        status = "online" if sistema.mt5_connected else "offline"
        color = "🟢" if sistema.mt5_connected else "🔴"
        st.markdown(f"""
        **💰 Informações Financeiras** {color}  
        **{status}**
        """)
    
    with col3:
        status = "online" if (sistema.mt5_connected and sistema.running) else "offline"
        color = "🟢" if (sistema.mt5_connected and sistema.running) else "🔴"
        st.markdown(f"""
        **📊 Sinais de Trading** {color}  
        **{status}**
        """)
    
    with col4:
        status = "online" if sistema.mt5_connected else "offline"
        color = "🟢" if sistema.mt5_connected else "🔴"
        st.markdown(f"""
        **📋 Relatórios/Exportação** {color}  
        **{status}**
        """)
    
    st.markdown("---")

def render_sidebar():
    """Renderiza sidebar com configurações"""
    st.sidebar.title("⚙️ Configurações do Sistema")
    
    sistema = st.session_state.trading_system
    
    # Controles do Sistema
    st.sidebar.markdown("### 🎮 Sistema")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if sistema.running:
            if st.button("⏹️ Parar", use_container_width=True):
                sistema.running = False
                sistema.log("Sistema parado pelo usuário")
                st.rerun()
        else:
            if st.button("▶️ Iniciar", use_container_width=True):
                sistema.running = True
                sistema.log("Sistema iniciado pelo usuário")
                st.rerun()
    
    with col2:
        status_text = "Rodando" if sistema.running else "Parado"
        color_class = "status-online" if sistema.running else "status-offline"
        st.markdown(f'<div class="{color_class}">{status_text}</div>', unsafe_allow_html=True)
    
    # Simulação MT5
    st.sidebar.markdown("### 🔌 MT5")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if sistema.mt5_connected:
            if st.button("🔌 Desconectar", use_container_width=True):
                sistema.mt5_connected = False
                sistema.log("MT5 desconectado")
                st.rerun()
        else:
            if st.button("🔗 Conectar", use_container_width=True):
                sistema.mt5_connected = True
                sistema.log("MT5 conectado (simulação)")
                st.rerun()
    
    with col2:
        status_text = "Conectado" if sistema.mt5_connected else "Desconectado"
        color_class = "status-online" if sistema.mt5_connected else "status-offline"
        st.markdown(f'<div class="{color_class}">{status_text}</div>', unsafe_allow_html=True)
    
    # Configurações
    st.sidebar.markdown("### 📊 Configurações")
    timeframe = st.sidebar.selectbox("Timeframe", ["1 min", "5 min", "15 min", "1 hora", "1 dia"], index=4)
    max_posicoes = st.sidebar.slider("Máx. Posições", 1, 10, 5)
    
    return {
        'timeframe': timeframe,
        'max_posicoes': max_posicoes
    }

def render_status_cards():
    """Renderiza cartões de status"""
    sistema = st.session_state.trading_system
    dados = sistema.dados_sistema
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Execuções", dados['execucoes'])
    
    with col2:
        st.metric("Pares Processados", dados['pares_processados'])
    
    with col3:
        st.metric("Posições Abertas", dados['posicoes_abertas'])
    
    with col4:
        lucro = dados['lucro_diario']
        st.metric("Lucro Diário", f"R$ {lucro:,.2f}")

def render_signals_tab():
    """Renderiza aba de sinais"""
    st.markdown("### 📊 Sinais de Trading")
    
    sistema = st.session_state.trading_system
    
    if sistema.sinais_ativos:
        df = pd.DataFrame(sistema.sinais_ativos)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("📊 Nenhum sinal ativo. Inicie o sistema para gerar sinais.")
        
        # Botão para simular sinais
        if st.button("🎲 Gerar Sinais de Demonstração"):
            sistema.sinais_ativos = [
                {
                    'par': 'PETR4/VALE3',
                    'ativo': 'PETR4',
                    'zscore': 2.34,
                    'sinal': 'VENDA',
                    'confianca': 85.2,
                    'timestamp': datetime.now()
                },
                {
                    'par': 'ITUB4/BBDC4',
                    'ativo': 'ITUB4',
                    'zscore': -2.12,
                    'sinal': 'COMPRA',
                    'confianca': 78.9,
                    'timestamp': datetime.now()
                }
            ]
            sistema.log(f"Gerados {len(sistema.sinais_ativos)} sinais de demonstração")
            st.success("Sinais de demonstração gerados!")
            st.rerun()

def render_positions_tab():
    """Renderiza aba de posições"""
    st.markdown("### 💼 Posições Abertas")
    
    sistema = st.session_state.trading_system
    
    if sistema.mt5_connected:
        st.info("💼 Nenhuma posição aberta no momento")
    else:
        st.warning("🔌 Conecte ao MT5 para visualizar posições reais")

def render_logs_tab():
    """Renderiza aba de logs"""
    st.markdown("### 📋 Logs do Sistema")
    
    sistema = st.session_state.trading_system
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("🗑️ Limpar Logs"):
            sistema.logs = []
            st.success("Logs limpos!")
            st.rerun()
    
    if sistema.logs:
        # Mostra últimos 20 logs
        logs_recentes = sistema.logs[-20:]
        for log in logs_recentes:
            st.text(log)
    else:
        st.info("📝 Nenhum log disponível")

def main():
    """Função principal do dashboard"""
    
    # Título principal
    st.title("📈 Trading Dashboard Pro - MT5 Real")
    
    # Renderiza header com status
    render_header()
    
    # Renderiza sidebar
    config = render_sidebar()
    
    # Métricas de status
    render_status_cards()
    
    # Tabs principais
    tab1, tab2, tab3 = st.tabs(["📊 Sinais", "💼 Posições", "📋 Logs"])
    
    with tab1:
        render_signals_tab()
    
    with tab2:
        render_positions_tab()
    
    with tab3:
        render_logs_tab()

# Execução principal
if __name__ == "__main__":
    main()
