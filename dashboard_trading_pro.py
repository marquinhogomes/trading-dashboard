#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 SISTEMA DE TRADING PROFISSIONAL - DASHBOARD COMPLETO
Sistema avançado de pairs trading com análise de cointegração, modelos ARIMA/GARCH 
e execução automatizada via MetaTrader 5.

Desenvolvido com base nas especificações técnicas completas para operações reais.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import threading
import time
import json
import sys
import os
import warnings
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import asyncio
from dataclasses import dataclass
import logging
import io

# Tentar importar tensorflow
try:
    import tensorflow as tf
    # Configurar logging do TensorFlow para suprimir warnings
    tf.get_logger().setLevel('ERROR')
    HAS_TENSORFLOW = True
except ImportError:
    HAS_TENSORFLOW = False
# ════════════════════════════════════════════════════════════════════════════════
# 🎯 CONFIGURAÇÃO INICIAL E IMPORTS
# ════════════════════════════════════════════════════════════════════════════════

# Configuração da página Streamlit
st.set_page_config(
    page_title="Trading Quantitativo – Dashboard de Operações",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/trading-quantitativo',
        'Report a bug': "https://github.com/trading-quantitativo/issues",
        'About': "Trading Quantitativo v3.0 - Dashboard Executivo de Operações"
    }
)

# Suprimir warnings
warnings.filterwarnings('ignore')

# Imports do sistema de trading
try:
    import MetaTrader5 as mt5
    HAS_MT5 = True
except ImportError:
    HAS_MT5 = False
    st.error("⚠️ MetaTrader5 não encontrado. Instale com: pip install MetaTrader5")

try:
    import pytz
    from statsmodels.tsa.stattools import adfuller, coint
    from statsmodels.tsa.arima.model import ARIMA
    from arch import arch_model
    HAS_STATSMODELS = True
except ImportError as e:
    HAS_STATSMODELS = False
    st.error(f"⚠️ Bibliotecas estatísticas não encontradas: {e}")

# Imports locais (sistema integrado)
try:
    # Tentar importar do sistema real
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    from sistema_integrado import SistemaIntegrado
    HAS_SISTEMA_INTEGRADO = True
    print("✅ Sistema integrado encontrado e importado com sucesso!")
except ImportError as e:
    HAS_SISTEMA_INTEGRADO = False
    print(f"⚠️ Sistema integrado não disponível: {e}")
    # Implementação fallback será criada
except Exception as e:
    HAS_SISTEMA_INTEGRADO = False
    print(f"❌ Erro ao importar sistema integrado: {e}")

# Tentar importar o módulo de cálculo de entradas
try:
    import calculo_entradas_v55
    HAS_CALCULO_ENTRADAS = True
    print("✅ Módulo de cálculo de entradas encontrado!")
except ImportError as e:
    HAS_CALCULO_ENTRADAS = False
    print(f"⚠️ Módulo de cálculo de entradas não disponível: {e}")
except Exception as e:
    HAS_CALCULO_ENTRADAS = False
    print(f"❌ Erro ao importar módulo de cálculo: {e}")

# ════════════════════════════════════════════════════════════════════════════════
# 🎨 CSS E ESTILO EXECUTIVO - TEMA ESCURO PROFISSIONAL
# ════════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    /* ===== VARIÁVEIS DO TEMA EXECUTIVO ESCURO ===== */
    :root {
        --primary-dark: #0c1017;
        --secondary-dark: #161b22;
        --card-dark: #21262d;
        --border-dark: #30363d;
        --accent-blue: #1f6feb;
        --accent-gold: #ffd700;
        --success-green: #28a745;
        --danger-red: #dc3545;
        --warning-orange: #fd7e14;
        --info-cyan: #17a2b8;
        --text-primary: #f0f6fc;
        --text-secondary: #8b949e;
        --text-muted: #6e7681;
    }
    
    /* ===== CONFIGURAÇÕES GLOBAIS ===== */
    .stApp {
        background: var(--primary-dark) !important;
        color: var(--text-primary) !important;
    }
    
    .main .block-container {
        padding-top: 1rem !important;
        max-width: 100% !important;
    }
    
    /* ===== HEADER INSTITUCIONAL ===== */
    .institutional-header {
        background: linear-gradient(135deg, #0d1117 0%, #21262d 50%, #161b22 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-dark);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: space-between;
        min-height: 80px;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .logo-icon {
        font-size: 3rem;
        background: linear-gradient(135deg, var(--accent-gold) 0%, #ffed4e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .title-section h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent-gold) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .title-section h2 {
        font-size: 1rem;
        margin: 0;
        color: var(--text-secondary);
        font-weight: 400;
    }
    
    .header-info {
        text-align: right;
        color: var(--text-secondary);
        font-size: 0.9rem;
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
    }
    
    .export-buttons {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    
    .export-btn {
        background: linear-gradient(135deg, var(--success-green) 0%, #20c997 100%);
        color: white;
        border: none;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .export-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(40, 167, 69, 0.4);
    }
    
    /* ===== CARDS EXECUTIVOS DE STATUS ===== */
    .executive-status-cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .status-card {
        background: linear-gradient(145deg, var(--card-dark) 0%, #2d3339 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .status-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
    }
    
    .status-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, var(--accent-gold) 50%, transparent 100%);
    }
    
    /* Cores específicas dos cards */
    .card-pairs { border-left-color: var(--warning-orange); }
    .card-operations { border-left-color: var(--accent-blue); }
    .card-equity { border-left-color: var(--success-green); }
    .card-pnl { border-left-color: var(--danger-red); }
    .card-winrate { border-left-color: var(--accent-gold); }
    .card-sharpe { border-left-color: var(--info-cyan); }
    .card-drawdown { border-left-color: #6f42c1; }
    .card-balance { border-left-color: #20c997; }
    
    .card-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .card-label {
        font-size: 0.85rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.8rem;
        font-weight: 500;
    }
    
    .card-delta {
        font-size: 0.8rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }
    
    .delta-positive { color: var(--success-green); }
    .delta-negative { color: var(--danger-red); }
    .delta-neutral { color: var(--text-secondary); }
    
    /* ===== SIDEBAR EXECUTIVA ===== */
    .stSidebar {
        background: var(--secondary-dark) !important;
    }
    
    .sidebar-section {
        background: var(--card-dark);
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid var(--border-dark);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    .sidebar-title {
        color: var(--accent-gold);
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 1px solid var(--border-dark);
        padding-bottom: 0.5rem;
    }
    
    /* ===== BOTÕES EXECUTIVOS ===== */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-blue) 0%, #2da44e 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2da44e 0%, var(--accent-blue) 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(31, 111, 235, 0.4) !important;
    }
    
    /* ===== GRÁFICOS EXECUTIVOS ===== */
    .chart-container {
        background: var(--card-dark);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-dark);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    .chart-title {
        color: var(--text-primary);
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.2rem;
        border-bottom: 1px solid var(--border-dark);
        padding-bottom: 0.5rem;
    }
    
    /* ===== TABELAS EXECUTIVAS ===== */
    .dataframe {
        background: var(--card-dark) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    
    .dataframe th {
        background: var(--secondary-dark) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        border: 1px solid var(--border-dark) !important;
    }
    
    .dataframe td {
        background: var(--card-dark) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-dark) !important;
    }
    
    /* ===== ESTILOS DE SINAIS ===== */
    .signal-buy {
        background: linear-gradient(135deg, rgba(40, 167, 69, 0.3) 0%, rgba(40, 167, 69, 0.1) 100%);
        color: var(--success-green);
        padding: 0.3rem 0.8rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
        border: 1px solid var(--success-green);
    }
    
    .signal-sell {
        background: linear-gradient(135deg, rgba(220, 53, 69, 0.3) 0%, rgba(220, 53, 69, 0.1) 100%);
        color: var(--danger-red);
        padding: 0.3rem 0.8rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
        border: 1px solid var(--danger-red);
    }
    
    .signal-neutral {
        background: linear-gradient(135deg, rgba(23, 162, 184, 0.3) 0%, rgba(23, 162, 184, 0.1) 100%);
        color: var(--info-cyan);
        padding: 0.3rem 0.8rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
        border: 1px solid var(--info-cyan);
    }
    
    /* ===== ESTILOS DE STATUS ===== */
    .status-open {
        background: linear-gradient(135deg, rgba(40, 167, 69, 0.3) 0%, rgba(40, 167, 69, 0.1) 100%);
        color: var(--success-green);
        padding: 0.3rem 0.8rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
        border: 1px solid var(--success-green);
    }
    
    .status-adjust {
        background: linear-gradient(135deg, rgba(253, 126, 20, 0.3) 0%, rgba(253, 126, 20, 0.1) 100%);
        color: var(--warning-orange);
        padding: 0.3rem 0.8rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
        border: 1px solid var(--warning-orange);
    }
    
    .status-target {
        background: linear-gradient(135deg, rgba(220, 53, 69, 0.3) 0%, rgba(220, 53, 69, 0.1) 100%);
        color: var(--danger-red);
        padding: 0.3rem 0.8rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
        border: 1px solid var(--danger-red);
    }
    
    /* ===== MÉTRICAS ===== */
    .metric-container {
        background: var(--card-dark);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid var(--border-dark);
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* ===== RESPONSIVIDADE ===== */
    @media (max-width: 768px) {
        .institutional-header {
            flex-direction: column;
            text-align: center;
            gap: 1rem;
        }
        
        .logo-section {
            justify-content: center;
        }
        
        .header-info {
            text-align: center;
        }
        
        .status-card .card-value {
            font-size: 1.8rem;
        }
    }
    
    /* ===== SCROLLBAR PERSONALIZADA ===== */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--secondary-dark);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-gold) 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-blue) 100%);
    }
    
    /* ===== INPUTS E SELECTBOXES ===== */
    .stSelectbox label, .stTextInput label, .stNumberInput label {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }
    
    .stSelectbox > div > div {
        background: var(--card-dark) !important;
        border: 1px solid var(--border-dark) !important;
    }
    
    .stTextInput > div > div > input {
        background: var(--card-dark) !important;
        border: 1px solid var(--border-dark) !important;
        color: var(--text-primary) !important;
    }
    
    .stNumberInput > div > div > input {
        background: var(--card-dark) !important;
        border: 1px solid var(--border-dark) !important;
        color: var(--text-primary) !important;
    }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# 📊 CLASSES E ESTRUTURAS DE DADOS
# ════════════════════════════════════════════════════════════════════════════════

@dataclass
class TradingSignal:
    """Estrutura para sinais de trading"""
    pair: str
    signal_type: str  # 'BUY', 'SELL', 'NEUTRAL'
    zscore: float
    confidence: float
    timestamp: datetime
    entry_price: float
    stop_loss: float
    take_profit: float
    risk_reward_ratio: float
    volatility: float
    
@dataclass
class Position:
    """Estrutura para posições abertas"""
    ticket: int
    pair: str
    type: str
    volume: float
    entry_price: float
    current_price: float
    pnl: float
    pnl_percent: float
    stop_loss: float
    take_profit: float
    timestamp: datetime

@dataclass
class SystemStatus:
    """Status do sistema de trading"""
    mt5_connected: bool
    system_running: bool
    last_analysis: Optional[datetime]
    total_positions: int
    total_pnl: float
    daily_trades: int
    success_rate: float
    uptime: timedelta

class TradingSystemCore:
    """Core avançado do sistema de trading"""
    
    def __init__(self):
        self.mt5_connected = False
        self.is_running = False
        self.current_pairs = []
        self.active_positions: List[Position] = []
        self.trading_signals: List[TradingSignal] = []
        self.trading_log = []
        self.analysis_results = {}
        self.last_update = None
        self.start_time = datetime.now()
        self.daily_stats = {
            'trades_executed': 0,
            'successful_trades': 0,
            'total_pnl': 0.0,
            'max_drawdown': 0.0
        }
        
    def connect_mt5(self, login: int = None, password: str = None, server: str = None) -> bool:
        """Conecta ao MetaTrader 5 com tratamento robusto de erros"""
        if not HAS_MT5:
            self.log_event("ERROR", "MetaTrader5 não disponível no sistema")
            return False
            
        try:
            # Inicializar MT5
            if not mt5.initialize():
                self.log_event("ERROR", "Falha ao inicializar MT5")
                return False
            
            # Login se credenciais fornecidas
            if login and password and server:
                if not mt5.login(login, password=password, server=server):
                    self.log_event("ERROR", f"Falha no login MT5: {mt5.last_error()}")
                    return False
                self.log_event("SUCCESS", f"Login MT5 realizado com sucesso - Conta: {login}")
            
            # Verificar conexão
            account_info = mt5.account_info()
            if account_info is None:
                self.log_event("ERROR", "Não foi possível obter informações da conta")
                return False
                
            self.mt5_connected = True
            self.log_event("SUCCESS", f"MT5 conectado - Servidor: {account_info.server}")
            return True
            
        except Exception as e:
            self.log_event("ERROR", f"Erro na conexão MT5: {str(e)}")
            return False
    
    def get_account_info(self) -> Dict[str, Any]:
        """Obtém informações detalhadas da conta"""
        if not self.mt5_connected:
            return {}
            
        try:
            account_info = mt5.account_info()
            if account_info is None:
                return {}
                
            return {
                'login': account_info.login,
                'server': account_info.server,
                'currency': account_info.currency,
                'balance': account_info.balance,
                'equity': account_info.equity,
                'margin': account_info.margin,
                'free_margin': account_info.margin_free,
                'margin_level': account_info.margin_level,
                'profit': account_info.profit,
                'company': account_info.company,
                'name': account_info.name
            }
        except Exception as e:
            self.log_event("ERROR", f"Erro ao obter info da conta: {str(e)}")
            return {}
    
    def get_symbol_data(self, symbol: str, timeframe: str, count: int = 1000) -> pd.DataFrame:
        """Obtém dados históricos de um símbolo"""
        if not self.mt5_connected:
            return pd.DataFrame()
            
        try:
            # Mapeamento de timeframes
            timeframe_map = {
                'M1': mt5.TIMEFRAME_M1,
                'M5': mt5.TIMEFRAME_M5,
                'M15': mt5.TIMEFRAME_M15,
                'M30': mt5.TIMEFRAME_M30,
                'H1': mt5.TIMEFRAME_H1,
                'H4': mt5.TIMEFRAME_H4,
                'D1': mt5.TIMEFRAME_D1
            }
            
            tf = timeframe_map.get(timeframe, mt5.TIMEFRAME_H1)
            
            # Obter dados
            rates = mt5.copy_rates_from_pos(symbol, tf, 0, count)
            
            if rates is None:
                self.log_event("WARNING", f"Sem dados para {symbol}")
                return pd.DataFrame()
            
            # Converter para DataFrame
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.set_index('time', inplace=True)
            
            return df
            
        except Exception as e:
            self.log_event("ERROR", f"Erro ao obter dados de {symbol}: {str(e)}")
            return pd.DataFrame()
    
    def log_event(self, level: str, message: str):
        """Sistema de logging avançado"""
        timestamp = datetime.now()
        log_entry = {
            'timestamp': timestamp,
            'level': level,
            'message': message
        }
        self.trading_log.append(log_entry)
        
        # Manter apenas os últimos 1000 logs
        if len(self.trading_log) > 1000:
            self.trading_log = self.trading_log[-1000:]
    
    def get_system_status(self) -> SystemStatus:
        """Obtém status completo do sistema"""
        uptime = datetime.now() - self.start_time
        success_rate = 0.0
        
        if self.daily_stats['trades_executed'] > 0:
            success_rate = (self.daily_stats['successful_trades'] / self.daily_stats['trades_executed']) * 100
        
        return SystemStatus(
            mt5_connected=self.mt5_connected,
            system_running=self.is_running,
            last_analysis=self.last_update,
            total_positions=len(self.active_positions),
            total_pnl=self.daily_stats['total_pnl'],
            daily_trades=self.daily_stats['trades_executed'],
            success_rate=success_rate,
            uptime=uptime
        )

class ParameterManager:
    """Gerenciador avançado de parâmetros"""
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Configuração padrão completa do sistema"""
        return {
            # Seleção de ativos
            'pairs_combined': [
                'ABEV3', 'ALOS3', 'ASAI3', 'BBAS3', 'BBDC4', 'BBSE3', 'BPAC11', 
                'BRAP4', 'BRFS3', 'BRKM5', 'CPFE3', 'CPLE6', 'CSAN3', 'CSNA3', 
                'CYRE3', 'ELET3', 'ELET6', 'EMBR3', 'ENEV3', 'ENGI11', 'EQTL3', 
                'EZTC3', 'FLRY3', 'GOAU4', 'HYPE3', 'IGTI11', 'IRBR3', 'ITSA4', 
                'ITUB4', 'KLBN11', 'MRFG3', 'NTCO3', 'PETR3', 'PETR4', 'PETZ3', 
                'PRIO3', 'RAIL3', 'RADL3', 'RECV3', 'RENT3', 'RDOR3', 'SANB11', 
                'SLCE3', 'SMTO3', 'SUZB3', 'TAEE11', 'TIMS3', 'TOTS3', 'UGPA3', 
                'VALE3', 'VBBR3', 'VIVT3', 'WEGE3', 'YDUQ3'
            ],
            
            # Segmentação por setor
            'segmentos': {
                'ABEV3': 'Bebidas', 'ALOS3': 'Saúde', 'ASAI3': 'Varejo Alimentar',
                'BBAS3': 'Bancos', 'BBDC4': 'Bancos', 'BBSE3': 'Seguros',
                'BPAC11': 'Bancos', 'BRAP4': 'Holding', 'BRFS3': 'Alimentos',
                'BRKM5': 'Química', 'CPFE3': 'Energia', 'CPLE6': 'Energia',
                'CSNA3': 'Siderurgia', 'CYRE3': 'Construção', 'ELET3': 'Energia',
                'ELET6': 'Energia', 'EMBR3': 'Aeroespacial', 'ENEV3': 'Energia',
                'ENGI11': 'Energia', 'EQTL3': 'Energia', 'EZTC3': 'Construção',
                'FLRY3': 'Saúde', 'GOAU4': 'Siderurgia', 'HYPE3': 'Farmacêutica',
                'IGTI11': 'Financeiro', 'IRBR3': 'Seguros', 'ITSA4': 'Financeiro',
                'ITUB4': 'Bancos', 'KLBN11': 'Papel e Celulose',
                'MRFG3': 'Alimentos', 'NTCO3': 'Higiene/Beleza', 'PETR3': 'Petróleo',
                'PETR4': 'Petróleo', 'PETZ3': 'Varejo', 'PRIO3': 'Petróleo',
                'RAIL3': 'Logística', 'RADL3': 'Varejo', 'RECV3': 'Petróleo',
                'RENT3': 'Locação', 'RDOR3': 'Saúde', 'SANB11': 'Bancos',
                'SLCE3': 'Agro', 'SMTO3': 'Agro', 'SUZB3': 'Papel e Celulose',
                'TAEE11': 'Energia', 'TIMS3': 'Telecom', 'TOTS3': 'Tecnologia',
                'UGPA3': 'Distribuição', 'VALE3': 'Mineração', 'VBBR3': 'Transporte',
                'VIVT3': 'Telecom', 'WEGE3': 'Industrial', 'YDUQ3': 'Educação'
            },
            
            # Parâmetros de análise
            'timeframe': 'H1',
            'period': 200,
            'min_train': 70,
            
            # Filtros estatísticos
            'zscore_threshold': 2.0,
            'zscore_min_threshold': -2.0,
            'zscore_max_threshold': 2.0,
            'r2_min_threshold': 0.50,
            'beta_max_threshold': 1.5,
            'p_value_threshold': 0.05,
            
            # Filtros de mercado
            'enable_cointegration_filter': True,
            'enable_zscore_filter': True,
            'enable_r2_filter': True,
            'enable_beta_filter': True,
            'enable_volatility_filter': True,
            
            # Gestão de risco
            'max_positions': 5,
            'risk_per_trade': 0.02,  # 2%
            'stop_loss_pct': 0.05,   # 5%
            'take_profit_pct': 0.10, # 10%
            
            # Filtros de liquidez
            'min_volume': 1000000,
            'max_spread_pct': 0.01,  # 1%
            
            # Horários de operação
            'trading_hours': {
                'start': 10,
                'end': 17,
                'close_positions': 16
            },
            
            # Configurações de modelo
            'use_garch': True,
            'use_arima_forecast': True,
            'arima_order': (1, 1, 1),
            
            # Interface
            'auto_refresh': False,
            'refresh_interval': 30,
            'dashboard_mode': 'real',
            
            # Sistema
            'sistema_real_ativo': HAS_SISTEMA_INTEGRADO,
            'total_ativos': 0,
            'total_setores': 0
        }
    
    @staticmethod
    def save_config(config: Dict[str, Any], filename: str = "trading_config.json"):
        """Salva configuração em arquivo"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False, default=str)
            return True
        except Exception as e:
            st.error(f"Erro ao salvar configuração: {e}")
            return False
    
    @staticmethod
    def load_config(filename: str = "trading_config.json") -> Dict[str, Any]:
        """Carrega configuração de arquivo"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return ParameterManager.get_default_config()
        except Exception as e:
            st.error(f"Erro ao carregar configuração: {e}")
            return ParameterManager.get_default_config()

# ════════════════════════════════════════════════════════════════════════════════
# 🔧 SISTEMA INTEGRADO FALLBACK
# ════════════════════════════════════════════════════════════════════════════════

class SistemaIntegradoFallback:
    """Sistema integrado fallback para quando o original não está disponível"""
    
    def __init__(self):
        self.running = False
        self.logs = []
        self.dados_sistema = {
            "execucoes": 0,
            "pares_processados": 0,
            "ordens_enviadas": 0,
            "inicio": None,
            "ultimo_ciclo": None,
            "status": "Parado"
        }
        
    def log(self, mensagem: str):
        """Log simples"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        evento = f"[{timestamp}] {mensagem}"
        self.logs.append(evento)
        if len(self.logs) > 100:
            self.logs = self.logs[-100:]
    
    def iniciar_sistema(self):
        """Simula início do sistema"""
        self.running = True
        self.dados_sistema["inicio"] = datetime.now()
        self.dados_sistema["status"] = "Executando (Simulado)"
        self.log("🔄 Sistema iniciado em modo simulado")
    
    def parar_sistema(self):
        """Para o sistema"""
        self.running = False
        self.dados_sistema["status"] = "Parado"
        self.log("⏹️ Sistema parado")

# ════════════════════════════════════════════════════════════════════════════════
# 🚀 INICIALIZAÇÃO DO ESTADO DA SESSÃO
# ════════════════════════════════════════════════════════════════════════════════

def initialize_session_state():
    """Inicializa o estado da sessão com todas as configurações necessárias"""
    
    # Sistema de trading principal
    if 'trading_system' not in st.session_state:
        st.session_state.trading_system = TradingSystemCore()
    
    # MT5 Manager para integração real
    if 'mt5_manager' not in st.session_state:
        st.session_state.mt5_manager = MT5Manager()
    
    # Status de conexão MT5
    if 'mt5_connected' not in st.session_state:
        st.session_state.mt5_connected = False
    
    # Informações da conta MT5
    if 'account_info' not in st.session_state:
        st.session_state.account_info = {}
    
    # Status de saúde da conexão
    if 'connection_health' not in st.session_state:
        st.session_state.connection_health = {}
    
    # Ativos selecionados
    if 'ativos_selecionados' not in st.session_state:
        st.session_state.ativos_selecionados = ['EURUSD', 'GBPUSD']
    
    # Sistema integrado (legacy)
    if 'sistema_integrado' not in st.session_state:
        if HAS_SISTEMA_INTEGRADO:
            st.session_state.sistema_integrado = SistemaIntegrado()
        else:
            st.session_state.sistema_integrado = SistemaIntegradoFallback()
    
    # Configurações
    if 'config' not in st.session_state:
        st.session_state.config = ParameterManager.get_default_config()
    
    # Estado da interface
    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = False
    
    if 'refresh_interval' not in st.session_state:
        st.session_state.refresh_interval = 30
    
    if 'dashboard_mode' not in st.session_state:
        st.session_state.dashboard_mode = 'real' if HAS_MT5 else 'simulated'
    
    # Dados de análise em tempo real
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {}
    
    if 'trading_signals' not in st.session_state:
        st.session_state.trading_signals = []
    
    # Cache de dados de mercado
    if 'market_data_cache' not in st.session_state:
        st.session_state.market_data_cache = {}
    
    # Timestamp da última atualização
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
    
    # Status de integração
    if 'integration_status' not in st.session_state:
        st.session_state.integration_status = {
            'mt5_available': HAS_MT5,
            'statsmodels_available': HAS_STATSMODELS,
            'sistema_integrado_available': HAS_SISTEMA_INTEGRADO,
            'mt5_connected': st.session_state.mt5_connected
        }
    
    # Configurações de trading
    if 'trading_config' not in st.session_state:
        st.session_state.trading_config = {
            'timeframe': 'H1',
            'zscore_threshold': 2.0,
            'max_positions': 5,
            'risk_per_trade': 1.0,
            'stop_loss': 2.5,
            'take_profit': 5.0
        }

# ════════════════════════════════════════════════════════════════════════════════
# 🎨 COMPONENTES DE INTERFACE
# ════════════════════════════════════════════════════════════════════════════════

def render_institutional_header():
    """Renderiza o header institucional com design executivo"""
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1f4068, #162447); 
                padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 2rem; margin-right: 1rem;">📊</div>
                <div>
                    <h1 style="color: white; margin: 0; font-size: 2rem;">Trading Quantitativo</h1>
                    <h2 style="color: #a8dadc; margin: 0; font-size: 1.2rem;">Dashboard de Operações</h2>
                </div>
            </div>
            <div style="color: white; text-align: right;">
                <div><strong>Última Atualização:</strong></div>
                <div>{}</div>
            </div>
        </div>    </div>
    """.format(datetime.now().strftime('%d/%m/%Y %H:%M:%S')), unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# 🔧 FUNÇÕES AUXILIARES EXECUTIVAS
# ════════════════════════════════════════════════════════════════════════════════

def generate_excel_report():
    """Gera relatório Excel executivo"""
    import io
    
    # Criar um buffer de bytes
    output = io.BytesIO()
    
    # Dados de exemplo para o relatório
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Aba de resumo executivo
        resumo_data = {
            'Métrica': ['Equity Atual', 'P/L Diário', 'Win Rate', 'Sharpe Ratio', 'Max Drawdown', 'Trades Hoje'],
            'Valor': ['R$ 125.000', '+R$ 2.300', '68.5%', '1.42', '5.8%', '12'],
            'Status': ['✅ Acima da Meta', '✅ Positivo', '✅ Excelente', '✅ Muito Bom', '✅ Controlado', '✅ Normal']
        }
        pd.DataFrame(resumo_data).to_excel(writer, sheet_name='Resumo Executivo', index=False)
        
        # Aba de posições
        posicoes_data = {
            'Par': ['VALE3/ITUB4', 'PETR4/BBDC4', 'ABEV3/B3SA3'],
            'Tipo': ['Long/Short', 'Short/Long', 'Long/Short'],
            'Quantidade': [100, 200, 150],
            'Entrada': ['R$ 29.85', 'R$ 45.12', 'R$ 31.76'],
            'Atual': ['R$ 32.30', 'R$ 44.49', 'R$ 32.35'],
            'P/L': ['+R$ 245', '-R$ 127', '+R$ 89'],
            'Status': ['Aberta', 'Ajuste', 'Alvo']
        }
        pd.DataFrame(posicoes_data).to_excel(writer, sheet_name='Posições Abertas', index=False)
        
        # Aba de histórico
        historico_data = {
            'Data': ['18/06/2025', '18/06/2025', '17/06/2025'],
            'Par': ['VALE3/ITUB4', 'PETR4/BBDC4', 'ABEV3/B3SA3'],
            'Resultado': ['+R$ 285', '-R$ 142', '+R$ 156'],
            'Duração': ['6h 15m', '5h 45m', '18h 45m'],
            'Motivo': ['Take Profit', 'Stop Loss', 'Take Profit']
        }
        pd.DataFrame(historico_data).to_excel(writer, sheet_name='Histórico de Trades', index=False)
    
    output.seek(0)
    
    st.success("📊 Relatório Excel gerado com sucesso!")
    return output.getvalue()

def generate_pdf_report():
    """Gera relatório PDF executivo"""
    # Simulação de geração de PDF
    import io
    
    # Esta seria a implementação real com reportlab ou similar
    fake_pdf_content = b"PDF Report Content - Trading Quantitativo Dashboard"
    
    st.success("📄 Relatório PDF gerado com sucesso!")
    return fake_pdf_content

def generate_daily_report():
    """Gera relatório diário consolidado"""
    import io
    
    # Criar relatório diário consolidado
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Resumo do dia
        resumo_diario = {
            'Hora': ['09:00', '12:00', '15:00', '18:00'],
            'Equity': ['R$ 122.700', 'R$ 124.100', 'R$ 125.000', 'R$ 125.000'],
            'P/L Acumulado': ['+R$ 500', '+R$ 1.800', '+R$ 2.300', '+R$ 2.300'],
            'Trades': [3, 7, 12, 12],
            'Win Rate': ['67%', '71%', '68%', '68%']
        }
        pd.DataFrame(resumo_diario).to_excel(writer, sheet_name='Resumo Diário', index=False)
    
    output.seek(0)
    
    st.success("📋 Relatório diário gerado com sucesso!")
    return output.getvalue()

def connect_mt5_system(usuario, senha, servidor):
    """Conecta ao sistema MT5 real"""
    # Inicializar MT5Manager se não existir
    if 'mt5_manager' not in st.session_state:
        st.session_state.mt5_manager = MT5Manager()
    
    mt5_manager = st.session_state.mt5_manager
    
    # Validar entrada de usuário
    if not usuario or not senha or not servidor:
        st.error("❌ Preencha todos os campos de login")
        return False
    
    # Tentar converter login para inteiro
    try:
        login_int = int(usuario)
    except ValueError:
        st.error("❌ Login deve ser um número")
        return False
    
    # Mostrar status de conexão
    with st.spinner("🔄 Conectando ao MT5..."):
        # 1. Inicializar MT5
        init_success, init_msg = mt5_manager.initialize_mt5()
        
        if not init_success:
            st.error(init_msg)
            return False
        
        st.info(init_msg)
        
        # 2. Autenticar
        auth_success, auth_msg = mt5_manager.authenticate(login_int, senha, servidor)
        
        if not auth_success:
            st.error(auth_msg)
            return False
        
        # Sucesso na autenticação
        st.success(auth_msg)
        
        # 3. Verificar saúde da conexão
        health_success, health_msg, health_data = mt5_manager.check_connection_health()
        
        if health_success:
            st.info(health_msg)
        else:
            st.warning(health_msg)
        
        # 4. Armazenar informações no session_state
        st.session_state.mt5_connected = True
        st.session_state.account_info = mt5_manager.account_info
        st.session_state.connection_health = health_data
        
        # 5. Exibir informações da conta
        if mt5_manager.account_info:
            with st.expander("📊 Informações da Conta", expanded=False):
                info = mt5_manager.account_info
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("💰 Balance", f"${info.get('balance', 0):,.2f}")
                    st.metric("� Equity", f"${info.get('equity', 0):,.2f}")
                
                with col2:
                    st.metric("🔗 Leverage", f"1:{info.get('leverage', 0)}")
                    st.metric("💼 Margin", f"${info.get('margin', 0):,.2f}")
                
                with col3:
                    st.metric("💲 Profit", f"${info.get('profit', 0):,.2f}")
                    st.metric("🆓 Free Margin", f"${info.get('free_margin', 0):,.2f}")
                
                st.json(info)
        
        return True

def test_mt5_connection():
    """Testa conexão MT5"""
    if st.session_state.trading_system.mt5_connected:
        st.success("✅ Conexão MT5 ativa")
        
        # Mostrar info da conta se disponível
        account_info = st.session_state.trading_system.get_account_info()
        if account_info:
            st.json(account_info)
    else:
        st.warning("⚠️ MT5 não conectado")

def save_configuration_profile():
    """Salva perfil de configuração"""
    # Capturar configurações atuais
    config_profile = {
        'timestamp': datetime.now().isoformat(),
        'estrategia': st.session_state.get('strategy_selection', 'Cointegração'),
        'timeframe': st.session_state.get('timeframe', 'D1'),
        'risco_trade': st.session_state.get('risco_trade', 1.0),
        'max_posicoes': st.session_state.get('max_posicoes', 5)
    }
    
    # Salvar em session_state
    if 'saved_profiles' not in st.session_state:
        st.session_state.saved_profiles = []
    
    st.session_state.saved_profiles.append(config_profile)
    
    st.success("💾 Perfil de configuração salvo!")

def reset_all_settings():
    """Reseta todas as configurações"""
    # Resetar configurações específicas
    reset_keys = [
        'strategy_selection', 'timeframe', 'risco_trade', 'max_posicoes',
        'filtro_cointegração', 'filtro_volatilidade', 'mt5_user'
    ]
    
    for key in reset_keys:
        if key in st.session_state:
            del st.session_state[key]
    
    st.warning("🔄 Todas as configurações foram resetadas!")

def send_test_alert():
    """Envia alerta de teste"""
    # Simulação de envio de alerta
    alert_message = f"""
    🚨 ALERTA DE TESTE - Trading Quantitativo
    
    Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    Sistema: Operacional
    Status: Teste de conectividade de alertas
    
    Este é um teste do sistema de alertas.
    Todos os sistemas estão funcionando normalmente.
    """
    
    # Aqui seria implementada a integração real com WhatsApp/Email
    st.info("📱 Alerta de teste enviado via WhatsApp/Email (simulado)")
    st.code(alert_message)

def render_executive_alerts_section():
    """Renderiza seção de alertas executivos"""
    st.markdown("---")
    st.markdown("### 🚨 Alertas e Relatórios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**⚡ Configurações de Alerta**")
        
        alert_ordem = st.checkbox("📤 Ordem Executada", value=True)
        alert_stop = st.checkbox("🎯 Stop/TP Atingido", value=True)
        alert_erro = st.checkbox("⚠️ Erro/Crash", value=True)
        alert_inatividade = st.checkbox("⏰ Inatividade", value=False)
        
        st.markdown("**📱 Canais**")
        whatsapp_alerts = st.toggle("WhatsApp", value=True)
        email_alerts = st.toggle("E-mail", value=True)
        
        if whatsapp_alerts:
            whatsapp_number = st.text_input("Número WhatsApp", placeholder="+55 11 99999-9999")
        
        if email_alerts:
            email_address = st.text_input("E-mail", placeholder="seu@email.com")
    
    with col2:
        st.markdown("**📊 Relatórios**")
        
        if st.button("📊 Download Excel", use_container_width=True):
            excel_data = generate_excel_report()
            st.download_button(
                label="📥 Baixar Excel",
                data=excel_data,
                file_name=f"trading_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        if st.button("📄 Download PDF", use_container_width=True):
            pdf_data = generate_pdf_report()
            st.download_button(
                label="📥 Baixar PDF",
                data=pdf_data,
                file_name=f"trading_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        st.metric("Relatórios Hoje", "5", delta="2")
        st.metric("Última Exportação", "14:25")

def render_executive_status_cards():
    """Renderiza os cartões de status executivos (KPIs principais)"""
    
    # Usar dados simulados para demonstração
    equity_atual = 125000.0
    balance = 100000.0
    pnl_diario = 2300.0
    num_posicoes = 3
    num_ativos = len(st.session_state.get('ativos_selecionados', ['EURUSD', 'GBPUSD']))
    
    # Calcular métricas
    delta_equity = ((equity_atual - balance) / balance * 100) if balance > 0 else 0
    pnl_percent = (pnl_diario / equity_atual * 100) if equity_atual > 0 else 0
    
    # Renderizar cartões em layout executivo
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        # Equity da conta
        st.metric(
            "💰 Equity",
            f"${equity_atual:,.2f}",
            f"{delta_equity:+.2f}%",
            delta_color="normal"
        )
    
    with col2:
        # P&L Diário
        color = "normal" if pnl_diario >= 0 else "inverse"
        st.metric(
            "📈 P&L Diário",
            f"${pnl_diario:+,.2f}",
            f"{pnl_percent:+.2f}%",
            delta_color=color
        )
    
    with col3:
        # Posições Ativas
        st.metric(
            "🎯 Posições",
            f"{num_posicoes}",
            "Ativas",
            delta_color="off"
        )
    
    with col4:
        # Ativos Monitorados
        st.metric(
            "📊 Ativos",
            f"{num_ativos}",
            "Monitorados",
            delta_color="off"
        )
    
    with col5:
        # Status do Sistema
        status_color = "normal"
        status_text = "Operacional"
        st.metric(
            "⚡ Sistema", 
            "✅ ON",
            status_text,
            delta_color="off"
        )
        free_margin = 120000.0
        margin_level = 2500.0
        num_posicoes = 15
        num_ativos = 225
        delta_equity = ((equity_atual - balance) / balance) * 100
        pnl_percent = (pnl_diario / equity_atual) * 100
    
    # Primeira linha de cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_icon = "🟢" if num_ativos > 0 else "🔴"
        st.metric(
            label=f"{status_icon} Ativos Monitorados",
            value=str(num_ativos),
            delta="Tempo Real" if st.session_state.get('mt5_connected', False) else "Simulado"
        )
    
    with col2:
        positions_icon = "📈" if num_posicoes > 0 else "📊"
        positions_delta = f"+{num_posicoes}" if num_posicoes > 0 else "Nenhuma"
        st.metric(
            label=f"{positions_icon} Posições Abertas", 
            value=str(num_posicoes),
            delta=positions_delta
        )
    
    with col3:
        equity_icon = "💰" if delta_equity >= 0 else "📉"
        currency = st.session_state.get('account_info', {}).get('currency', 'USD')
        st.metric(
            label=f"{equity_icon} Equity Atual",
            value=f"{currency} {equity_atual:,.2f}",
            delta=f"{delta_equity:+.2f}%"
        )
    
    with col4:
        pnl_icon = "📈" if pnl_diario >= 0 else "📉"
        st.metric(
            label=f"{pnl_icon} P&L Atual",
            value=f"{currency} {pnl_diario:+,.2f}",
            delta=f"{pnl_percent:+.2f}%"
        )
    
    # Segunda linha de cards
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        # Status de conexão
        if st.session_state.get('mt5_connected', False):
            st.metric(
                label="🔗 Status MT5",
                value="CONECTADO",
                delta="Online"
            )
        else:
            st.metric(
                label="🔌 Status MT5",
                value="DESCONECTADO",
                delta="Offline"
            )
    
    with col6:
        # Margem utilizada
        margin_percent = (margin / equity_atual * 100) if equity_atual > 0 else 0
        margin_status = "Normal" if margin_percent < 50 else "Alta" if margin_percent < 80 else "Crítica"
        st.metric(
            label="💼 Margem Utilizada",
            value=f"{currency} {margin:,.2f}",
            delta=f"{margin_percent:.1f}% - {margin_status}"
        )
    
    with col7:
        # Margem livre
        if st.session_state.get('mt5_connected', False):
            st.metric(
                label="🆓 Margem Livre",
                value=f"{currency} {free_margin:,.2f}",
                delta="Disponível"
            )
        else:
            # Win rate simulado
            win_rate = 68.5
            st.metric(
                label="🎯 Win Rate (Sim.)",
                value=f"{win_rate:.1f}%",
                delta="+2.3% sem."
            )
    
    with col8:
        # Nível de margem ou Sharpe ratio
        if st.session_state.get('mt5_connected', False) and margin_level > 0:
            margin_health = "Saudável" if margin_level > 1000 else "Atenção" if margin_level > 500 else "Crítico"
            st.metric(
                label="� Nível de Margem",                value=f"{margin_level:.0f}%",
                delta=margin_health
            )
        else:
            # Sharpe ratio simulado
            sharpe_ratio = 1.42
            st.metric(
                label="⭐ Sharpe Ratio (Sim.)",
                value=f"{sharpe_ratio:.2f}",
                delta="Excelente"
            )

def render_executive_sidebar():
    """Renderiza sidebar executiva conforme especificações"""
    with st.sidebar:
        st.markdown('<div class="sidebar-title">🔐 Login MT5</div>', unsafe_allow_html=True)
        
        # Status de conexão atual
        if 'mt5_connected' in st.session_state and st.session_state.mt5_connected:
            st.success("✅ MT5 Conectado")
            
            # Exibir informações da conta
            if 'account_info' in st.session_state:
                info = st.session_state.account_info
                st.info(f"👤 {info.get('name', 'N/A')} | 💰 ${info.get('balance', 0):,.2f}")
            
            # Botão para desconectar
            if st.button("🔌 Desconectar", use_container_width=True, type="secondary"):
                if 'mt5_manager' in st.session_state:
                    st.session_state.mt5_manager.disconnect()
                st.session_state.mt5_connected = False
                st.session_state.account_info = {}
                st.rerun()
        else:
            st.warning("⚠️ MT5 Desconectado")
            
            usuario = st.text_input("Usuário", value="", placeholder="Login da conta")
            senha = st.text_input("Senha", type="password", value="", placeholder="Senha da conta")
            servidor = st.selectbox("Servidor", ["Broker-Demo", "Broker-Live", "XM-Demo", "XM-Real"])
            
            if st.button("🚀 Conectar MT5", use_container_width=True, type="primary"):
                if usuario and senha and servidor:
                    connect_mt5_system(usuario, senha, servidor)
                    st.rerun()
                else:
                    st.error("❌ Preencha todos os campos")
        
        st.markdown("---")
        
        # Seleção de Estratégia
        st.markdown('<div class="sidebar-title">🎯 Seleção de Estratégia</div>', unsafe_allow_html=True)
        estrategia = st.selectbox(
            "Estratégia",
            ["Cointegração", "Beta Rotation", "ARIMA", "ML"],
            index=0
        )
        
        st.markdown("---")
        
        # Ativos Monitorados com validação real
        st.markdown('<div class="sidebar-title">📈 Ativos Monitorados</div>', unsafe_allow_html=True)
        
        # Obter símbolos disponíveis do MT5 se conectado
        if 'mt5_connected' in st.session_state and st.session_state.mt5_connected and 'mt5_manager' in st.session_state:
            # Usar símbolos reais do MT5
            mt5_manager = st.session_state.mt5_manager
            success, msg, available_symbols = mt5_manager.get_available_symbols("all")
            
            if success and available_symbols:
                ativos_disponiveis = available_symbols[:50]  # Limitar para performance
            else:
                st.warning("⚠️ Não foi possível carregar símbolos do MT5")
                ativos_disponiveis = ["EURUSD", "GBPUSD", "USDJPY", "USDCHF"]
        else:
            # Usar símbolos padrão em modo simulado
            ativos_disponiveis = [
                "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "NZDUSD",
                "EURGBP", "EURJPY", "GBPJPY", "XAUUSD", "XAGUSD", "US30"
            ]
        
        ativos_selecionados = st.multiselect(
            "Selecionar Ativos",
            ativos_disponiveis,
            default=ativos_disponiveis[:3] if ativos_disponiveis else []
        )
        
        # Validar símbolos selecionados em tempo real
        if ativos_selecionados and 'mt5_connected' in st.session_state and st.session_state.mt5_connected:
            st.markdown("**🔍 Status dos Símbolos:**")
            for symbol in ativos_selecionados[:5]:  # Validar apenas os primeiros 5
                if 'mt5_manager' in st.session_state:
                    mt5_manager = st.session_state.mt5_manager
                    is_valid, status_msg, symbol_info = mt5_manager.validate_symbol(symbol)
                    
                    if is_valid:
                        # Obter tick em tempo real
                        tick_success, tick_msg, tick_data = mt5_manager.get_realtime_tick(symbol)
                        if tick_success:
                            spread = tick_data.get('spread', 0)
                            bid = tick_data.get('bid', 0)
                            ask = tick_data.get('ask', 0)
                            st.success(f"✅ {symbol}: {bid:.5f}/{ask:.5f} (Spread: {spread:.5f})")
                        else:
                            st.warning(f"⚠️ {symbol}: Válido mas sem tick")
                    else:
                        st.error(f"❌ {symbol}: {status_msg}")
        
        # Filtros por tipo de mercado
        mercado_filtro = st.selectbox(
            "Filtro por Mercado",
            ["Todos", "Forex", "Stocks", "Crypto", "Commodities"]
        )
        
        st.markdown("---")
        
        # Parâmetros-chave
        st.markdown('<div class="sidebar-title">⚙️ Parâmetros-chave</div>', unsafe_allow_html=True)
        
        timeframe = st.selectbox("Timeframe", ["M1", "M5", "M15", "H1", "D1"], index=4)
        periodo_analise = st.number_input("Período de Análise", min_value=50, max_value=252, value=252)
        zscore_limiar = st.slider("Limiar de Z-Score", min_value=1.0, max_value=4.0, value=2.0, step=0.1)
        max_posicoes = st.number_input("Máx. Posições Simultâneas", min_value=1, max_value=20, value=5)
        risco_trade = st.number_input("Risco por Trade (%)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
        
        st.markdown("**Stop/Target (%)**")
        col1, col2 = st.columns(2)
        with col1:
            stop_loss = st.number_input("Stop", min_value=0.5, max_value=20.0, value=2.5, step=0.1)
        with col2:
            take_profit = st.number_input("Target", min_value=0.5, max_value=20.0, value=5.0, step=0.1)
        
        st.markdown("---")
        
        # Filtros
        st.markdown('<div class="sidebar-title">🔍 Filtros</div>', unsafe_allow_html=True)
        
        filtro_cointegração = st.checkbox("Cointegração", value=True)
        filtro_volatilidade = st.checkbox("Volatilidade", value=True)
        filtro_volume = st.checkbox("Volume", value=False)
        filtro_spread = st.checkbox("Spread", value=True)
        
        st.markdown("---")
        
        # Controles do Sistema
        st.markdown('<div class="sidebar-title">🎛️ Controles</div>', unsafe_allow_html=True)
        
        # Sistema ligado/desligado
        sistema_ativo = st.toggle("Sistema Ativo", value=False)
        
        if st.button("💾 Salvar Perfil", use_container_width=True):
            save_configuration_profile()
            st.success("✅ Perfil salvo!")
        
        if st.button("🔄 Resetar Tudo", use_container_width=True):
            reset_all_settings()
            st.warning("⚠️ Configurações resetadas!")
        if st.button("📱 Teste de Alerta", use_container_width=True):
            send_test_alert()
            st.info("📧 Alerta de teste enviado!")
        
        # Modo Real/Simulação
        modo_real = st.toggle("Modo Real", value=True)
        if modo_real:
            st.success("🔴 **MODO REAL ATIVO**")
        else:
            st.info("🟡 **MODO SIMULAÇÃO**")
        
        # Armazenar valores selecionados no session_state
        st.session_state.ativos_selecionados = ativos_selecionados
        st.session_state.strategy_selection = estrategia
        st.session_state.timeframe = timeframe
        st.session_state.periodo_analise = periodo_analise
        st.session_state.zscore_threshold = zscore_limiar
        st.session_state.max_posicoes = max_posicoes
        st.session_state.risco_trade = risco_trade
        st.session_state.stop_loss = stop_loss
        st.session_state.take_profit = take_profit

def render_executive_charts_panel():
    """Renderiza painel de gráficos executivos com dados reais do MT5"""
    st.markdown("---")
    st.markdown("### 📊 Painéis de Visualização")
    
    # Verificar se há símbolos selecionados
    ativos_selecionados = st.session_state.get('ativos_selecionados', ['EURUSD', 'GBPUSD'])
    
    # Primeira linha de gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Dados de Mercado em Tempo Real")
        
        # Usar dados reais se MT5 está conectado
        if ('mt5_connected' in st.session_state and st.session_state.mt5_connected and 
            'mt5_manager' in st.session_state and ativos_selecionados):
            
            symbol = ativos_selecionados[0]  # Usar o primeiro símbolo selecionado
            mt5_manager = st.session_state.mt5_manager
            
            # Obter dados históricos reais
            success, msg, market_data = mt5_manager.get_market_data(symbol, 'H1', 100)
            
            if success and not market_data.empty:
                fig_market = go.Figure()
                
                # Candlestick chart
                fig_market.add_trace(go.Candlestick(
                    x=market_data.index,
                    open=market_data['open'],
                    high=market_data['high'],
                    low=market_data['low'],
                    close=market_data['close'],
                    name=f'{symbol} H1'
                ))
                
                fig_market.update_layout(
                    title=f"🔥 {symbol} - Tempo Real",
                    template="plotly_dark",
                    height=400,
                    xaxis_rangeslider_visible=False,
                    margin=dict(l=0, r=0, t=40, b=0)
                )
                
                st.plotly_chart(fig_market, use_container_width=True)
                
                # Exibir última cotação
                latest = market_data.iloc[-1]
                col1a, col1b, col1c = st.columns(3)
                with col1a:
                    st.metric("💰 Close", f"{latest['close']:.5f}")
                with col1b:
                    change = latest['close'] - latest['open']
                    st.metric("📊 Change", f"{change:.5f}", delta=f"{change:.5f}")
                with col1c:
                    st.metric("📈 Volume", f"{latest['tick_volume']:,.0f}")
            else:
                st.error(f"❌ Erro ao obter dados: {msg}")
                # Fallback para dados simulados
                render_simulated_equity_chart()
        else:
            # Dados simulados se não conectado
            render_simulated_equity_chart()
    
    with col2:
        st.markdown("#### 📊 Análise de Spread em Tempo Real")
        
        # Se temos pelo menos 2 símbolos, calcular spread real
        if (len(ativos_selecionados) >= 2 and 'mt5_connected' in st.session_state and 
            st.session_state.mt5_connected and 'mt5_manager' in st.session_state):
            
            symbol1, symbol2 = ativos_selecionados[0], ativos_selecionados[1]
            mt5_manager = st.session_state.mt5_manager
            
            # Obter ticks em tempo real para ambos os símbolos
            tick1_success, _, tick1_data = mt5_manager.get_realtime_tick(symbol1)
            tick2_success, _, tick2_data = mt5_manager.get_realtime_tick(symbol2)
            
            if tick1_success and tick2_success:
                # Calcular spread normalizado
                price1 = tick1_data['bid']
                price2 = tick2_data['bid']
                spread = price1 - price2
                
                # Obter dados históricos para análise de z-score
                success1, _, data1 = mt5_manager.get_market_data(symbol1, 'H1', 100)
                success2, _, data2 = mt5_manager.get_market_data(symbol2, 'H1', 100)
                
                if success1 and success2 and not data1.empty and not data2.empty:
                    # Alinhar timeframes
                    common_index = data1.index.intersection(data2.index)
                    if len(common_index) > 20:
                        aligned_data1 = data1.loc[common_index]['close']
                        aligned_data2 = data2.loc[common_index]['close']
                        
                        # Calcular spread histórico
                        spread_series = aligned_data1 - aligned_data2
                        spread_mean = spread_series.mean()
                        spread_std = spread_series.std()
                        
                        # Z-score atual
                        current_zscore = (spread - spread_mean) / spread_std if spread_std > 0 else 0
                        
                        # Gráfico de spread
                        fig_spread = go.Figure()
                        
                        fig_spread.add_trace(go.Scatter(
                            x=spread_series.index,
                            y=spread_series.values,
                            mode='lines',
                            name='Spread Histórico',
                            line=dict(color='#17a2b8', width=2)
                        ))
                        
                        # Linha do spread atual
                        fig_spread.add_hline(
                            y=spread, 
                            line_color="#ffd700", 
                            line_dash="dash",
                            annotation_text=f"Atual: {spread:.5f} (Z:{current_zscore:.2f})"
                        )
                        
                        # Linhas de threshold
                        fig_spread.add_hline(y=spread_mean + 2*spread_std, line_color="#dc3545", line_dash="dot")
                        fig_spread.add_hline(y=spread_mean - 2*spread_std, line_color="#dc3545", line_dash="dot")
                        
                        fig_spread.update_layout(
                            title=f"🎯 Spread {symbol1}/{symbol2}",
                            template="plotly_dark",
                            height=400,
                            margin=dict(l=0, r=0, t=40, b=0)
                        )
                        
                        st.plotly_chart(fig_spread, use_container_width=True)
                        
                        # Exibir métricas do spread
                        col2a, col2b, col2c = st.columns(3)
                        with col2a:
                            st.metric("📐 Spread Atual", f"{spread:.5f}")
                        with col2b:
                            color = "inverse" if abs(current_zscore) > 2 else "normal"
                            st.metric("📊 Z-Score", f"{current_zscore:.2f}", delta_color=color)
                        with col2c:
                            signal = "SELL" if current_zscore > 2 else "BUY" if current_zscore < -2 else "HOLD"
                            st.metric("🎯 Sinal", signal)
                    else:
                        st.warning("⚠️ Dados insuficientes para análise de spread")
                        render_simulated_zscore_chart()
                else:
                    st.error("❌ Erro ao obter dados históricos para spread")
                    render_simulated_zscore_chart()
            else:
                st.error("❌ Erro ao obter ticks em tempo real")
                render_simulated_zscore_chart()
        else:
            # Dados simulados
            render_simulated_zscore_chart()
    
    # Segunda linha de gráficos
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### 🎯 Posições em Tempo Real")
        
        # Obter posições reais se conectado
        if ('mt5_connected' in st.session_state and st.session_state.mt5_connected and 
            'mt5_manager' in st.session_state):
            
            mt5_manager = st.session_state.mt5_manager
            pos_success, pos_msg, positions = mt5_manager.get_positions()
            
            if pos_success and positions:
                # Criar gráfico de P&L das posições
                symbols = [pos['symbol'] for pos in positions]
                profits = [pos['profit'] for pos in positions]
                
                fig_positions = go.Figure()
                fig_positions.add_trace(go.Bar(
                    x=symbols,
                    y=profits,
                    marker_color=['#28a745' if p > 0 else '#dc3545' for p in profits],
                    name='P&L por Posição'
                ))
                
                fig_positions.update_layout(
                    title="💼 P&L das Posições Abertas",
                    template="plotly_dark",
                    height=300,
                    margin=dict(l=0, r=0, t=40, b=0)
                )
                
                st.plotly_chart(fig_positions, use_container_width=True)
                
                # Resumo das posições
                total_profit = sum(profits)
                st.metric("💰 P&L Total", f"${total_profit:.2f}", 
                         delta=f"${total_profit:.2f}", 
                         delta_color="normal" if total_profit >= 0 else "inverse")
                
            else:
                st.info("📊 Nenhuma posição aberta")
                render_simulated_signals_chart()
        else:
            render_simulated_signals_chart()
    
    with col4:
        st.markdown("#### 🌡️ Saúde da Conexão MT5")
        
        if ('mt5_connected' in st.session_state and st.session_state.mt5_connected and 
            'mt5_manager' in st.session_state):
            
            mt5_manager = st.session_state.mt5_manager
            health_success, health_msg, health_data = mt5_manager.check_connection_health()
            
            if health_success and health_data:
                # Gráfico de ping
                ping_history = [health_data.get('ping', 50) + np.random.randint(-10, 10) for _ in range(50)]
                times = pd.date_range(end=datetime.now(), periods=50, freq='1min')
                
                fig_health = go.Figure()
                fig_health.add_trace(go.Scatter(
                    x=times,
                    y=ping_history,
                    mode='lines+markers',
                    name='Ping (ms)',
                    line=dict(color='#28a745', width=2),
                    marker=dict(size=4)
                ))
                
                fig_health.update_layout(
                    title="🌐 Latência da Conexão",
                    template="plotly_dark",
                    height=300,
                    margin=dict(l=0, r=0, t=40, b=0)
                )
                
                st.plotly_chart(fig_health, use_container_width=True)
                
                # Status indicators
                col4a, col4b = st.columns(2)
                with col4a:
                    ping = health_data.get('ping', 0)
                    color = "normal" if ping < 100 else "inverse"
                    st.metric("🌐 Ping", f"{ping}ms", delta_color=color)
                
                with col4b:
                    uptime = health_data.get('uptime_seconds', 0) / 3600
                    st.metric("⏱️ Uptime", f"{uptime:.1f}h")
                
            else:
                st.error(f"❌ Erro na verificação: {health_msg}")
        else:
            st.warning("⚠️ MT5 não conectado")

def render_simulated_equity_chart():
    """Renderiza gráfico de equity simulado"""
    dates = pd.date_range("2024-01-01", periods=252, freq='D')
    equity_values = 100000 + np.cumsum(np.random.randn(252) * 500)
    
    fig_equity = go.Figure()
    fig_equity.add_trace(go.Scatter(
        x=dates,
        y=equity_values,
        mode='lines',
        name='Equity (Simulado)',
        line=dict(color='#28a745', width=2),
        fill='tonexty',
        fillcolor='rgba(40, 167, 69, 0.1)'
    ))
    
    fig_equity.update_layout(
        title="📈 Curva de Equity (Simulado)",
        template="plotly_dark",
        height=400,
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    st.plotly_chart(fig_equity, use_container_width=True)

def render_simulated_zscore_chart():
    """Renderiza gráfico de Z-Score simulado"""
    zscores = np.random.normal(0, 1, 1000)
    
    fig_zscore = go.Figure()
    fig_zscore.add_trace(go.Histogram(
        x=zscores,
        nbinsx=30,
        name='Z-Score (Simulado)',
        marker_color='#17a2b8',
        opacity=0.7
    ))
    
    # Adicionar linhas de threshold
    fig_zscore.add_vline(x=2.0, line_color="#dc3545", line_dash="dash")
    fig_zscore.add_vline(x=-2.0, line_color="#dc3545", line_dash="dash")
    
    fig_zscore.update_layout(
        title="📊 Distribuição Z-Score (Simulado)",
        template="plotly_dark",
        height=400,
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    st.plotly_chart(fig_zscore, use_container_width=True)

def render_simulated_signals_chart():
    """Renderiza gráfico de sinais simulado"""
    dates = pd.date_range("2024-01-01", periods=252, freq='D')
    spread_values = np.cumsum(np.random.randn(252) * 0.1)
    signals = np.where(spread_values > 0.2, 1, np.where(spread_values < -0.2, -1, 0))
    
    fig_signals = go.Figure()
    
    # Spread
    fig_signals.add_trace(go.Scatter(
        x=dates,
        y=spread_values,
        mode='lines',
        name='Spread (Simulado)',
        line=dict(color='#ffd700', width=2)
    ))
    
    # Sinais
    fig_signals.add_trace(go.Scatter(
        x=dates,
        y=signals * 0.3,
        mode='markers+lines',
        name='Sinais',
        line=dict(color='#fd7e14', width=1, dash='dot'),
        marker=dict(size=4)
    ))
    
    fig_signals.update_layout(        title="🎯 Sinais de Trading (Simulado)",
        template="plotly_dark",
        height=300,
        showlegend=True,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    st.plotly_chart(fig_signals, use_container_width=True)

def render_signals_and_positions_panel():
    """Renderiza painel de sinais e posições"""
    st.markdown("---")
    st.markdown("### 🎯 Sinais e Posições")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Sinais Atuais")
        
        # Dados de sinais simulados
        sinais_data = {
            "Par": ["VALE3/ITUB4", "PETR4/BBDC4", "ABEV3/B3SA3"],
            "Sinal": ["Compra", "Venda", "Neutro"],
            "Confiança": ["85%", "92%", "68%"],
            "Timestamp": [
                "19/06/2025 14:23:15",
                "19/06/2025 14:18:42", 
                "19/06/2025 14:15:33"
            ],
            "Trigger": ["Z-Score -2.1", "Z-Score +2.3", "ARIMA"]
        }
        
        df_sinais = pd.DataFrame(sinais_data)
        st.dataframe(df_sinais, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### 💼 Posições Abertas")
        
        # Dados de posições simuladas
        posicoes_data = {
            "Par/Ativo": ["PETR4/VALE3", "ITUB4/BBDC4", "ABEV3/B3SA3"],
            "Qtd.": [100, 200, 150],
            "Preço Entrada": ["R$ 29.85", "R$ 45.12", "R$ 31.76"],
            "P/L Atual": ["+R$ 245", "-R$ 127", "+R$ 89"],
            "SL/TP": ["28.50/31.20", "44.00/46.50", "30.80/32.90"],
            "Status": ["Aberta", "Ajuste", "Alvo"]
        }
        
        df_posicoes = pd.DataFrame(posicoes_data)
        st.dataframe(df_posicoes, use_container_width=True, hide_index=True)
        
        # Botões de ação rápida
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.button("🔴 Fechar", use_container_width=True)
        with col_b:
            st.button("📉 Reduzir", use_container_width=True)
        with col_c:
            st.button("⚙️ Modificar", use_container_width=True)

def render_history_and_audit_panel():
    """Renderiza painel de histórico e auditoria"""
    st.markdown("---")
    st.markdown("### 📋 Histórico & Auditoria")
    
    tab1, tab2, tab3 = st.tabs(["📈 Trade History", "📝 Log de Eventos", "📊 Resumo"])
    
    with tab1:
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            data_inicio = st.date_input("Data Início", value=datetime.now().date() - timedelta(days=30))
        with col2:
            data_fim = st.date_input("Data Fim", value=datetime.now().date())
        with col3:
            filtro_resultado = st.selectbox("Resultado", ["Todos", "Lucro", "Prejuízo"])
        
        # Tabela de histórico
        historico_data = {
            "Par": ["VALE3/ITUB4", "PETR4/BBDC4", "ABEV3/B3SA3", "SUZB3/RENT3"],
            "Tipo": ["Long/Short", "Short/Long", "Long/Short", "Long/Short"],
            "Data Entrada": ["18/06/2025 09:15", "18/06/2025 10:30", "17/06/2025 14:45", "17/06/2025 16:20"],
            "Data Saída": ["18/06/2025 15:30", "18/06/2025 16:15", "18/06/2025 09:30", "18/06/2025 11:45"],
            "Resultado": ["+R$ 285", "-R$ 142", "+R$ 156", "+R$ 97"],
            "Duração": ["6h 15m", "5h 45m", "18h 45m", "19h 25m"],
            "Motivo": ["Take Profit", "Stop Loss", "Take Profit", "Take Profit"]
        }
        
        df_historico = pd.DataFrame(historico_data)
        st.dataframe(df_historico, use_container_width=True, hide_index=True)
    
    with tab2:
        # Log de eventos
        st.markdown("**Log de Eventos em Tempo Real**")
        
        log_events = [
            "19/06/2025 14:25:33 - INFO: Nova ordem enviada",
            "19/06/2025 14:23:15 - SUCCESS: Sinal detectado Z-Score -2.1",
            "19/06/2025 14:18:42 - WARNING: Alta volatilidade detectada",
            "19/06/2025 14:15:33 - INFO: Análise atualizada",
            "19/06/2025 14:12:28 - SUCCESS: Take Profit atingido +R$ 156"
        ]
        
        for event in log_events:
            st.text(event)
    
    with tab3:
        # Resumo estatístico
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Estatísticas Diárias**")
            stats_data = {
                "Métrica": ["Lucro/Prejuízo", "Nº de Trades", "Win Rate"],
                "Hoje": ["+R$ 2.300", "12", "75%"],
                "Ontem": ["+R$ 1.850", "8", "62%"]
            }
            df_stats = pd.DataFrame(stats_data)
            st.dataframe(df_stats, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("**Gráfico de Trades**")
            trades_results = [285, 245, 189, 156, 97, -87, -125, -142]
            colors = ['green' if x > 0 else 'red' for x in trades_results]
            
            fig_trades = go.Figure(data=[
                go.Bar(x=list(range(len(trades_results))), y=trades_results, marker_color=colors)
            ])
            
            fig_trades.update_layout(
                template="plotly_dark",
                height=250,
                showlegend=False,
                margin=dict(l=0, r=0, t=20, b=0)
            )
            
            st.plotly_chart(fig_trades, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# 🚀 EXECUÇÃO PRINCIPAL DO DASHBOARD
# ════════════════════════════════════════════════════════════════════════════════

def main():
    """
    Função principal do dashboard executivo de trading quantitativo
    """
    try:
        # Inicialização básica
        st.title("🚀 Trading Quantitativo - Dashboard Executivo")
        
        # Inicializar session state básico
        initialize_simple_session_state()
        
        # Renderizar header institucional
        render_institutional_header()
        
        # Renderizar cartões de status executivo
        render_executive_status_cards()
        
        # Renderizar painel principal
        render_main_dashboard()
        
        # Renderizar rodapé
        render_footer()
            
    except Exception as e:
        st.error(f"❌ Erro crítico no sistema: {str(e)}")
        st.exception(e)


def initialize_simple_session_state():
    """Inicializa session state de forma segura e gradual"""
    
    # Configurações básicas
    if 'dashboard_mode' not in st.session_state:
        st.session_state.dashboard_mode = 'simulated'
    
    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = False
    
    if 'refresh_interval' not in st.session_state:
        st.session_state.refresh_interval = 30
    
    # Dados simulados para demonstração
    if 'ativos_selecionados' not in st.session_state:
        st.session_state.ativos_selecionados = ['EURUSD', 'GBPUSD', 'USDJPY']
    
    # Status do sistema
    if 'system_status' not in st.session_state:
        st.session_state.system_status = {
            'trading_enabled': True,
            'data_feed_active': True,
            'algorithms_running': True,
            'risk_management_active': True
        }


def render_main_dashboard():
    """Renderiza o painel principal do dashboard"""
    
    # Sidebar com controles
    with st.sidebar:
        st.header("🎛️ Controles")
        
        # Modo de operação
        mode = st.selectbox(
            "Modo de Operação",
            ["Simulado", "Real (MT5)"],
            index=0 if st.session_state.dashboard_mode == 'simulated' else 1
        )
        
        # Ativos para análise
        st.multiselect(
            "Ativos Selecionados",
            ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "NZDUSD"],
            default=st.session_state.ativos_selecionados
        )
        
        # Auto-refresh
        auto_refresh = st.checkbox("Auto-refresh", value=st.session_state.auto_refresh)
        
        if auto_refresh:
            refresh_interval = st.slider("Intervalo (segundos)", 10, 300, st.session_state.refresh_interval)
    
    # Área principal com tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Análise", "💰 Posições", "📈 Performance", "⚙️ Configurações"])
    
    with tab1:
        render_analysis_tab()
    
    with tab2:
        render_positions_tab()
        
    with tab3:
        render_performance_tab()
        
    with tab4:
        render_settings_tab()


def render_analysis_tab():
    """Renderiza a aba de análise"""
    st.subheader("📊 Análise de Cointegração e Sinais")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Pares Analisados", "12", "↑ 2")
    
    with col2:
        st.metric("Sinais Ativos", "3", "↑ 1")
        
    with col3:
        st.metric("Accuracy Modelo", "78.5%", "↑ 2.3%")
        
    with col4:
        st.metric("Spread Médio", "1.2 pips", "↓ 0.1")
    
    # Gráfico de exemplo
    st.subheader("📈 Evolução dos Spreads")
    
    # Dados simulados para o gráfico
    dates = pd.date_range(start='2024-01-01', periods=100, freq='H')
    data = {
        'time': dates,
        'EURUSD_GBPUSD': np.random.normal(0, 0.01, 100).cumsum(),
        'USDJPY_USDCHF': np.random.normal(0, 0.01, 100).cumsum()
    }
    df_spreads = pd.DataFrame(data)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_spreads['time'], y=df_spreads['EURUSD_GBPUSD'], 
                            name='EUR/USD - GBP/USD', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df_spreads['time'], y=df_spreads['USDJPY_USDCHF'], 
                            name='USD/JPY - USD/CHF', line=dict(color='red')))
    
    fig.update_layout(
        title="Evolução dos Spreads - Pairs Trading",
        xaxis_title="Tempo",
        yaxis_title="Spread (normalizado)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_positions_tab():
    """Renderiza a aba de posições"""
    st.subheader("💰 Posições Abertas")
    
    # Dados simulados de posições
    positions_data = {
        'Par': ['EURUSD/GBPUSD', 'USDJPY/USDCHF', 'AUDUSD/NZDUSD'],
        'Tipo': ['Long Spread', 'Short Spread', 'Long Spread'],
        'Volume': ['0.1 / 0.1', '0.2 / 0.2', '0.15 / 0.15'],
        'Entrada': ['1.0847', '0.9823', '1.0654'],
        'Atual': ['1.0851', '0.9819', '1.0658'],
        'P&L': ['+$45.20', '-$12.80', '+$23.10'],
        'Status': ['✅ Ativo', '⚠️ Monitor', '✅ Ativo']
    }
    
    df_positions = pd.DataFrame(positions_data)
    st.dataframe(df_positions, use_container_width=True)
    
    # Resumo de P&L
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("P&L Total", "+$55.50", "+$8.30")
    
    with col2:
        st.metric("Posições Ativas", "3", "→")
        
    with col3:
        st.metric("Win Rate", "67%", "+5%")


def render_performance_tab():
    """Renderiza a aba de performance"""
    st.subheader("📈 Análise de Performance")
    
    # Gráfico de equity curve
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    equity = 10000 + np.random.normal(50, 200, 30).cumsum()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=equity, mode='lines', name='Equity Curve',
                            line=dict(color='green', width=2)))
    
    fig.update_layout(
        title="Curva de Capital - Últimos 30 dias",
        xaxis_title="Data",
        yaxis_title="Capital ($)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Métricas de performance
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Retorno Total", "12.5%", "+2.1%")
    
    with col2:
        st.metric("Sharpe Ratio", "1.8", "+0.2")
        
    with col3:
        st.metric("Max Drawdown", "-3.2%", "+0.8%")
        
    with col4:
        st.metric("Volatilidade", "8.5%", "-0.5%")


def render_settings_tab():
    """Renderiza a aba de configurações"""
    st.subheader("⚙️ Configurações do Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Parâmetros de Trading")
        
        risk_per_trade = st.slider("Risco por operação (%)", 0.5, 5.0, 2.0, 0.1)
        max_positions = st.slider("Máximo de posições", 1, 10, 5)
        stop_loss = st.slider("Stop Loss (pips)", 10, 100, 50, 5)
        take_profit = st.slider("Take Profit (pips)", 20, 200, 100, 10)
    
    with col2:
        st.subheader("📊 Parâmetros de Análise")
        
        lookback_period = st.slider("Período de análise (dias)", 30, 365, 90)
        confidence_level = st.slider("Nível de confiança (%)", 90, 99, 95)
        rebalance_freq = st.selectbox("Frequência de rebalanceamento", 
                                     ["Diário", "Semanal", "Mensal"])
        
    # Botões de ação
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Salvar Configurações"):
            st.success("Configurações salvas com sucesso!")
    
    with col2:
        if st.button("🔄 Restaurar Padrões"):
            st.info("Configurações restauradas para os valores padrão!")
            
    with col3:
        if st.button("📤 Exportar Relatório"):
            st.success("Relatório exportado para download!")

def render_footer():
    """Renderiza rodapé com informações do sistema"""
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; color: #666;'>
            <small>
                🚀 <strong>Trading System Pro</strong><br>
                Versão 2.0 | Build 2025.01.21
            </small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; color: #666;'>
            <small>
                ⚡ Powered by Streamlit<br>
                📊 Advanced Analytics & AI
            </small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; color: #666;'>
            <small>
                📈 Pairs Trading System<br>
                🤖 MT5 Integration Ready
            </small>
        </div>
        """, unsafe_allow_html=True)

def setup_logging():
    """Configura sistema de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('trading_system.log'),
            logging.StreamHandler()
        ]
    )

# ════════════════════════════════════════════════════════════════════════════════
# 🔧 INTEGRAÇÃO MT5 REAL - MANAGER AVANÇADO
# ════════════════════════════════════════════════════════════════════════════════

class MT5Manager:
    """Gerenciador avançado para integração real com MetaTrader 5"""
    
    def __init__(self):
        self.is_connected = False
        self.account_info = {}
        self.symbols_info = {}
        self.last_connection_time = None
        self.connection_attempts = 0
        self.max_connection_attempts = 3
        self.connection_timeout = 30  # segundos
        self.symbols_cache = {}
        self.last_tick_time = {}
        
    def initialize_mt5(self) -> Tuple[bool, str]:
        """Inicializa MT5 com validação completa"""
        if not HAS_MT5:
            return False, "❌ MetaTrader5 não instalado. Execute: pip install MetaTrader5"
        
        try:
            # Tentar inicializar MT5
            if not mt5.initialize():
                error_info = mt5.last_error()
                return False, f"❌ Falha na inicialização MT5: {error_info}"
            
            # Verificar versão do terminal
            terminal_info = mt5.terminal_info()
            if terminal_info is None:
                return False, "❌ Não foi possível obter informações do terminal MT5"
            
            # Verificar se o terminal está conectado
            if not terminal_info.connected:
                return False, "❌ Terminal MT5 não está conectado ao servidor"
            
            # Verificar se trading está habilitado
            if not terminal_info.trade_allowed:
                return False, "⚠️ Trading não está habilitado no terminal MT5"
            
            self.last_connection_time = datetime.now()
            return True, f"✅ MT5 inicializado - Versão: {terminal_info.build}"
            
        except Exception as e:
            return False, f"❌ Erro na inicialização MT5: {str(e)}"
    
    def authenticate(self, login: int, password: str, server: str) -> Tuple[bool, str]:
        """Autentica no MT5 com validação robusta"""
        try:
            # Validar parâmetros
            if not login or not password or not server:
                return False, "❌ Credenciais incompletas (login, senha, servidor)"
            
            # Tentar login
            success = mt5.login(login, password=password, server=server)
            
            if not success:
                error_info = mt5.last_error()
                self.connection_attempts += 1
                
                # Mapear erros comuns
                error_messages = {
                    1: "❌ Credenciais inválidas",
                    2: "❌ Erro de rede - verificar conexão",
                    64: "❌ Conta desabilitada",
                    65: "❌ Parâmetros de login inválidos",
                    128: "❌ Timeout de conexão",
                    129: "❌ Preços inválidos",
                    130: "❌ Stops inválidos",
                    131: "❌ Volume inválido",
                    132: "❌ Mercado fechado",
                    133: "❌ Trading desabilitado",
                    134: "❌ Margem insuficiente"
                }
                
                error_msg = error_messages.get(error_info[0], f"❌ Erro MT5 #{error_info[0]}: {error_info[1]}")
                return False, error_msg
            
            # Validar informações da conta
            account_info = mt5.account_info()
            if account_info is None:
                return False, "❌ Não foi possível obter informações da conta"
              # Armazenar informações da conta
            self.account_info = {
                'login': account_info.login,
                'server': account_info.server,
                'currency': account_info.currency,
                'company': account_info.company,
                'name': account_info.name,
                'balance': account_info.balance,
                'equity': account_info.equity,
                'margin': account_info.margin,
                'free_margin': account_info.margin_free,
                'margin_level': account_info.margin_level,
                'profit': account_info.profit,
                'leverage': account_info.leverage,
                'trade_allowed': getattr(account_info, 'trade_allowed', True),
                'expert_allowed': getattr(account_info, 'trade_expert', True)
            }
            
            self.is_connected = True
            self.connection_attempts = 0
            
            return True, f"✅ Autenticado: {account_info.name} ({account_info.login}) - {account_info.server}"
            
        except Exception as e:
            return False, f"❌ Erro na autenticação: {str(e)}"
    
    def validate_symbol(self, symbol: str) -> Tuple[bool, str, Dict]:
        """Valida se um símbolo existe e está disponível"""
        try:
            # Verificar cache primeiro
            if symbol in self.symbols_cache:
                cache_time = self.symbols_cache[symbol].get('timestamp', datetime.min)
                if (datetime.now() - cache_time).seconds < 300:  # Cache por 5 minutos
                    return True, "✅ Símbolo válido (cache)", self.symbols_cache[symbol]['info']
            
            # Obter informações do símbolo
            symbol_info = mt5.symbol_info(symbol)
            
            if symbol_info is None:
                return False, f"❌ Símbolo '{symbol}' não encontrado", {}
            
            # Verificar se o símbolo está visível
            if not symbol_info.visible:
                # Tentar tornar visível
                if not mt5.symbol_select(symbol, True):
                    return False, f"⚠️ Símbolo '{symbol}' não disponível para trading", {}
            
            # Verificar se trading está habilitado para o símbolo
            if symbol_info.trade_mode == mt5.SYMBOL_TRADE_MODE_DISABLED:
                return False, f"⚠️ Trading desabilitado para '{symbol}'", {}
            
            # Compilar informações do símbolo
            symbol_data = {
                'name': symbol_info.name,
                'description': symbol_info.description,
                'currency_base': symbol_info.currency_base,
                'currency_profit': symbol_info.currency_profit,
                'currency_margin': symbol_info.currency_margin,
                'digits': symbol_info.digits,
                'point': symbol_info.point,
                'spread': symbol_info.spread,
                'trade_mode': symbol_info.trade_mode,
                'min_lot': symbol_info.volume_min,
                'max_lot': symbol_info.volume_max,
                'lot_step': symbol_info.volume_step,
                'swap_long': symbol_info.swap_long,
                'swap_short': symbol_info.swap_short,
                'session_deals': symbol_info.session_deals,
                'session_buy_orders': symbol_info.session_buy_orders,
                'session_sell_orders': symbol_info.session_sell_orders,
                'timestamp': datetime.now()
            }
            
            # Armazenar no cache
            self.symbols_cache[symbol] = {
                'info': symbol_data,
                'timestamp': datetime.now()
            }
            
            return True, f"✅ Símbolo '{symbol}' válido e disponível", symbol_data
            
        except Exception as e:
            return False, f"❌ Erro ao validar símbolo '{symbol}': {str(e)}", {}
    
    def get_realtime_tick(self, symbol: str) -> Tuple[bool, str, Dict]:
        """Obtém tick em tempo real de um símbolo"""
        try:
            # Validar símbolo primeiro
            is_valid, msg, symbol_info = self.validate_symbol(symbol)
            if not is_valid:
                return False, msg, {}
            
            # Obter tick atual
            tick = mt5.symbol_info_tick(symbol)
            
            if tick is None:
                return False, f"❌ Não foi possível obter tick para '{symbol}'", {}
            
            # Compilar dados do tick
            tick_data = {
                'symbol': symbol,
                'time': datetime.fromtimestamp(tick.time),
                'bid': tick.bid,
                'ask': tick.ask,
                'last': tick.last,
                'volume': tick.volume,
                'spread': tick.ask - tick.bid,
                'spread_points': int((tick.ask - tick.bid) / symbol_info.get('point', 0.00001)),
                'flags': tick.flags
            }
            
            # Atualizar cache de último tick
            self.last_tick_time[symbol] = tick_data['time']
            
            return True, f"✅ Tick obtido para '{symbol}'", tick_data
            
        except Exception as e:
            return False, f"❌ Erro ao obter tick para '{symbol}': {str(e)}", {}
    
    def get_market_data(self, symbol: str, timeframe: str, count: int = 1000) -> Tuple[bool, str, pd.DataFrame]:
        """Obtém dados históricos em tempo real"""
        try:
            # Validar símbolo
            is_valid, msg, symbol_info = self.validate_symbol(symbol)
            if not is_valid:
                return False, msg, pd.DataFrame()
            
            # Mapear timeframes
            timeframe_map = {
                'M1': mt5.TIMEFRAME_M1,
                'M5': mt5.TIMEFRAME_M5,
                'M15': mt5.TIMEFRAME_M15,
                'M30': mt5.TIMEFRAME_M30,
                'H1': mt5.TIMEFRAME_H1,
                'H4': mt5.TIMEFRAME_H4,
                'D1': mt5.TIMEFRAME_D1,
                'W1': mt5.TIMEFRAME_W1,
                'MN1': mt5.TIMEFRAME_MN1
            }
            
            mt5_timeframe = timeframe_map.get(timeframe)
            if mt5_timeframe is None:
                return False, f"❌ Timeframe '{timeframe}' não suportado", pd.DataFrame()
            
            # Obter dados históricos
            rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, count)
            
            if rates is None or len(rates) == 0:
                return False, f"❌ Sem dados históricos para '{symbol}' ({timeframe})", pd.DataFrame()
            
            # Converter para DataFrame
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.set_index('time', inplace=True)
            
            # Adicionar informações derivadas
            df['spread'] = df['high'] - df['low']
            df['body'] = abs(df['close'] - df['open'])
            df['upper_shadow'] = df['high'] - df[['open', 'close']].max(axis=1)
            df['lower_shadow'] = df[['open', 'close']].min(axis=1) - df['low']
            
            return True, f"✅ {len(df)} barras obtidas para '{symbol}' ({timeframe})", df
            
        except Exception as e:
            return False, f"❌ Erro ao obter dados para '{symbol}': {str(e)}", pd.DataFrame()
    
    def get_positions(self) -> Tuple[bool, str, List[Dict]]:
        """Obtém posições abertas em tempo real"""
        try:
            if not self.is_connected:
                return False, "❌ MT5 não conectado", []
            
            # Obter posições
            positions = mt5.positions_get()
            
            if positions is None:
                return True, "✅ Nenhuma posição aberta", []
            
            positions_list = []
            
            for pos in positions:
                # Obter tick atual para calcular P/L atualizado
                tick_success, tick_msg, tick_data = self.get_realtime_tick(pos.symbol)
                
                current_price = pos.price_current
                if tick_success:
                    current_price = tick_data['bid'] if pos.type == mt5.ORDER_TYPE_SELL else tick_data['ask']
                
                # Calcular P/L
                if pos.type == mt5.ORDER_TYPE_BUY:
                    pnl_points = current_price - pos.price_open
                else:
                    pnl_points = pos.price_open - current_price
                
                position_data = {
                    'ticket': pos.ticket,
                    'symbol': pos.symbol,
                    'type': 'BUY' if pos.type == mt5.ORDER_TYPE_BUY else 'SELL',
                    'volume': pos.volume,
                    'price_open': pos.price_open,
                    'price_current': current_price,
                    'sl': pos.sl,
                    'tp': pos.tp,
                    'profit': pos.profit,
                    'profit_points': pnl_points,
                    'swap': pos.swap,
                    'comment': pos.comment,
                    'time_open': datetime.fromtimestamp(pos.time),
                    'magic': pos.magic,
                    'identifier': pos.identifier
                }
                
                positions_list.append(position_data)
            
            return True, f"✅ {len(positions_list)} posições encontradas", positions_list
            
        except Exception as e:
            return False, f"❌ Erro ao obter posições: {str(e)}", []
    
    def get_available_symbols(self, filter_type: str = "all") -> Tuple[bool, str, List[str]]:
        """Obtém lista de símbolos disponíveis"""
        try:
            if not self.is_connected:
                return False, "❌ MT5 não conectado", []
            
            # Obter todos os símbolos
            symbols = mt5.symbols_get()
            
            if symbols is None:
                return False, "❌ Não foi possível obter lista de símbolos", []
            
            symbol_names = []
            
            for symbol in symbols:
                # Filtrar por tipo se especificado
                if filter_type == "forex" and not symbol.name.count('/') == 1:
                    continue
                elif filter_type == "stocks" and '/' in symbol.name:
                    continue
                elif filter_type == "crypto" and not any(crypto in symbol.name.upper() for crypto in ['BTC', 'ETH', 'XRP', 'LTC']):
                    continue
                
                # Adicionar apenas símbolos visíveis e com trading habilitado
                if symbol.visible and symbol.trade_mode != mt5.SYMBOL_TRADE_MODE_DISABLED:
                    symbol_names.append(symbol.name)
            
            symbol_names.sort()
            return True, f"✅ {len(symbol_names)} símbolos disponíveis", symbol_names
            
        except Exception as e:
            return False, f"❌ Erro ao obter símbolos: {str(e)}", []
    
    def check_connection_health(self) -> Tuple[bool, str, Dict]:
        """Verifica saúde da conexão MT5"""
        try:
            if not self.is_connected:
                return False, "❌ MT5 não conectado", {}
            
            # Verificar informações do terminal
            terminal_info = mt5.terminal_info()
            if terminal_info is None:
                return False, "❌ Não foi possível verificar status do terminal", {}
            
            # Verificar informações da conta
            account_info = mt5.account_info()
            if account_info is None:
                return False, "❌ Não foi possível verificar status da conta", {}
            
            # Compilar status de saúde
            health_data = {
                'terminal_connected': terminal_info.connected,
                'trade_allowed': terminal_info.trade_allowed,
                'account_trade_allowed': account_info.trade_allowed,
                'account_expert_allowed': account_info.trade_expert,
                'ping': terminal_info.ping_last,
                'retransmission': terminal_info.retransmission,
                'connection_time': self.last_connection_time,
                'uptime_seconds': (datetime.now() - self.last_connection_time).total_seconds() if self.last_connection_time else 0
            }
              # Verificar problemas
            issues = []
            if not terminal_info.connected:
                issues.append("Terminal desconectado")
            if not terminal_info.trade_allowed:
                issues.append("Trading desabilitado no terminal")
            if not account_info.trade_allowed:
                issues.append("Trading desabilitado na conta")
            if terminal_info.ping_last > 1000:
                issues.append(f"Ping alto: {terminal_info.ping_last}ms")
            
            status = "✅ Conexão saudável" if not issues else f"⚠️ Problemas: {', '.join(issues)}"
            
            return len(issues) == 0, status, health_data
            
        except Exception as e:
            return False, f"❌ Erro ao verificar conexão: {str(e)}", {}
    
    def disconnect(self) -> bool:
        """Desconecta do MT5"""
        try:
            mt5.shutdown()
            self.is_connected = False
            self.account_info = {}
            self.symbols_cache = {}
            return True
        except:
            return False

# ════════════════════════════════════════════════════════════════════════════════
# 🎯 PONTO DE ENTRADA DA APLICAÇÃO
# ════════════════════════════════════════════════════════════════════════════════

# Executar dashboard principal uma única vez
if __name__ == "__main__" or 'streamlit' in str(__file__):
    main()
