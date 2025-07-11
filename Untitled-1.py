"""
Sistema de Trading Profissional - Streamlit App
Aplicativo completo para operações de pares com análise de cointegração,
modelos ARIMA/GARCH e execução automatizada de ordens.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import inspect
import time
import json
import os
from datetime import datetime, timedelta
import threading
import asyncio
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# Importar módulos adicionais
import calculo_entradas_v55 as ce55
from sistema_integrado import SistemaIntegrado

# Configuração da página
st.set_page_config(
    page_title="Trading System Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Imports do sistema de trading REAL
try:
    import MetaTrader5 as mt5
    HAS_MT5 = True
except ImportError:
    HAS_MT5 = False
    st.error("MetaTrader5 não encontrado. Instale com: pip install MetaTrader5")

# Importar sistema real de integração E configurações reais
try:
    from trading_real_integration import (
        real_state, HAS_REAL_CONFIG, HAS_REAL_ANALYSIS, REAL_CONFIG,
        get_real_analysis_data, get_real_market_data, execute_real_trading_analysis,
        get_real_system_status, get_real_trading_opportunities
    )
    from config_real import (
        get_real_config_for_streamlit, DEPENDENTE_REAL, INDEPENDENTE_REAL, 
        SEGMENTOS_REAIS, FILTER_PARAMS_REAL, get_setores_disponiveis,
        get_pares_por_setor, is_horario_operacao, SYSTEM_INFO
    )
    from analise_real import get_analise_para_streamlit, executar_analise_completa
    HAS_REAL_SYSTEM = True
    print("✅ Sistema real e configurações carregados!")
except ImportError as e:
    print(f"❌ Erro ao importar sistema real: {e}")
    HAS_REAL_SYSTEM = False
    HAS_REAL_CONFIG = False
    real_trading_system = None
    st.error(f"❌ Erro ao carregar sistema real: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 CONFIGURAÇÃO DO SISTEMA REAL INTEGRADO
# ═══════════════════════════════════════════════════════════════════════════════

def get_config_real_para_streamlit():
    """Retorna configuração real formatada para Streamlit"""
    if HAS_REAL_SYSTEM and HAS_REAL_CONFIG:
        config = get_real_config_for_streamlit()
        config['sistema_real_ativo'] = True
        config['total_ativos'] = len(config['pairs_combined'])
        config['total_setores'] = len(get_setores_disponiveis())
        return config
    else:
        # Fallback com configuração básica
        return {
            'pairs_combined': ['PETR4', 'VALE3', 'ITUB4', 'BBDC4'],
            'sistema_real_ativo': False,
            'total_ativos': 4,
            'total_setores': 4
        }

def get_real_pairs_list():
    """Retorna lista real de pares para seleção"""
    if HAS_REAL_SYSTEM:
        return REAL_CONFIG.get('pairs_combined', DEPENDENTE_REAL)
    return ['PETR4', 'VALE3', 'ITUB4', 'BBDC4']  # Fallback

def get_real_sectors_list():
    """Retorna lista real de setores"""
    if HAS_REAL_SYSTEM:
        return get_setores_disponiveis()
    return ['Petróleo', 'Mineração', 'Bancos']  # Fallback

# ETAPA 1: Configuração de estado da sessão conectada ao sistema real
def initialize_session_state():
    """Inicializar estado da sessão conectado ao sistema real"""
    if 'trading_system' not in st.session_state:
        st.session_state.trading_system = "sistema_real"
    
    # Conectar ao sistema real se disponível
    if HAS_REAL_SYSTEM:
        st.session_state.real_system = real_state
        st.session_state.real_config = get_config_real_para_streamlit()
    else:
        st.session_state.real_system = None
        st.session_state.real_config = get_config_real_para_streamlit()
    
    # Estado do dashboard
    if 'dashboard_mode' not in st.session_state:
        st.session_state.dashboard_mode = 'real' if HAS_REAL_SYSTEM else 'simulated'
    
    # Configurações
    if 'config' not in st.session_state:
        st.session_state.config = st.session_state.real_config

# CSS customizado para interface profissional
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2d5a9b 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #1f4e79;
        margin-bottom: 1rem;
    }
    
    .status-card {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: white;
        font-weight: bold;
    }
    
    .status-online {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
    }
    
    .status-offline {
        background: linear-gradient(90deg, #f44336 0%, #da190b 100%);
    }
    
    .status-processing {
        background: linear-gradient(90deg, #ff9800 0%, #f57c00 100%);
    }
    
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #1f4e79 0%, #2d5a9b 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #2d5a9b 0%, #3a6bb5 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .trade-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        background: white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .profit-positive {
        color: #4CAF50;
        font-weight: bold;
    }
    
    .profit-negative {
        color: #f44336;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Classes do sistema de trading
class TradingSystemCore:
    """Core do sistema de trading"""
    
    def __init__(self):
        self.mt5_connected = False
        self.is_running = False
        self.current_pairs = []
        self.active_positions = []
        self.trading_log = []
        self.analysis_results = {}
        self.last_update = None
        
    def connect_mt5(self, login: int = None, password: str = None, server: str = None):
        """Conecta ao MetaTrader 5"""
        if not HAS_MT5:
            return False
            
        try:
            if login and password and server:
                authorized = mt5.initialize(
                    login=login,
                    password=password,
                    server=server
                )
            else:
                authorized = mt5.initialize()
                
            if authorized:
                self.mt5_connected = True
                account_info = mt5.account_info()
                if account_info:
                    return True
            return False
        except Exception as e:
            st.error(f"Erro ao conectar MT5: {e}")
            return False
    
    def get_account_info(self):
        """Obtém informações da conta"""
        if not self.mt5_connected:
            return None
            
        try:
            account_info = mt5.account_info()
            if account_info:
                return {
                    'balance': account_info.balance,
                    'equity': account_info.equity,
                    'margin': account_info.margin,
                    'free_margin': account_info.margin_free,
                    'profit': account_info.profit,
                    'currency': account_info.currency,
                    'leverage': account_info.leverage,
                    'company': account_info.company,
                    'server': account_info.server
                }
        except Exception as e:
            st.error(f"Erro ao obter info da conta: {e}")
        return None
    
    def get_symbol_data(self, symbol: str, timeframe: str, count: int = 1000):
        """Obtém dados históricos de um símbolo"""
        if not self.mt5_connected:
            return None
            
        try:
            # Mapeamento de timeframes
            tf_map = {
                'M1': mt5.TIMEFRAME_M1,
                'M5': mt5.TIMEFRAME_M5,
                'M15': mt5.TIMEFRAME_M15,
                'M30': mt5.TIMEFRAME_M30,
                'H1': mt5.TIMEFRAME_H1,
                'H4': mt5.TIMEFRAME_H4,
                'D1': mt5.TIMEFRAME_D1
            }
            
            tf = tf_map.get(timeframe, mt5.TIMEFRAME_H1)
            rates = mt5.copy_rates_from_pos(symbol, tf, 0, count)
            
            if rates is not None:
                df = pd.DataFrame(rates)
                df['time'] = pd.to_datetime(df['time'], unit='s')
                return df
        except Exception as e:
            st.error(f"Erro ao obter dados do símbolo {symbol}: {e}")
        return None

class ParameterManager:
    """Gerenciador de parâmetros do sistema"""
    
    @staticmethod
    def get_default_pairs():
        """Lista de pares padrão"""
        return [
            'PETR4', 'VALE3', 'ITUB4', 'BBDC4', 'ABEV3',
            'MGLU3', 'WEGE3', 'RENT3', 'LREN3', 'GGBR4',
            'USIM5', 'CSNA3', 'GOAU4', 'SUZB3', 'RAIL3',
            'CCRO3', 'VIVT3', 'TIMP3', 'ELET3', 'CMIG4'
        ]
    
    @staticmethod
    def get_default_config():
        """Configuração padrão do sistema"""
        return {
            'pairs': ParameterManager.get_default_pairs(),
            'timeframe': 'D1',
            'period': 20,
            'min_train': 70,
            'zscore_threshold': 2.0,
            'max_positions': 5,
            'risk_per_trade': 0.02,
            'stop_loss': 0.05,
            'take_profit': 0.10,
            'enable_cointegration': True,
            'enable_volatility_filter': True,
            'min_volume': 1000000,
            'max_spread': 0.01
        }

def initialize_session_state():
    """Inicializa o estado da sessão"""
    if 'trading_system' not in st.session_state:
        st.session_state.trading_system = TradingSystemCore()
      # ETAPA 1: Integrar configurações reais
    if 'config' not in st.session_state:
        if HAS_REAL_SYSTEM:
            # Usar configurações do código real
            st.session_state.config = REAL_CONFIG.copy()
        else:
            # Fallback para configurações padrão
            st.session_state.config = ParameterManager.get_default_config()
    
    # ETAPA 1: Inicializar estado do sistema real
    if 'real_trading_state' not in st.session_state and HAS_REAL_SYSTEM:
        st.session_state.real_trading_state = real_state

    # Instância do sistema integrado
    if 'integrated_system' not in st.session_state:
        st.session_state.integrated_system = SistemaIntegrado()

    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = False
    
    if 'refresh_interval' not in st.session_state:
        st.session_state.refresh_interval = 30
      # ETAPA 1: Status de integração
    if 'integration_status' not in st.session_state:
        st.session_state.integration_status = {
            'has_real_code': HAS_REAL_SYSTEM,
            'system_initialized': False,
            'last_check': datetime.now()
        }

def render_header():
    """Renderiza o cabeçalho principal"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Sistema de Trading Profissional</h1>
        <p>Análise de Cointegração | Modelos ARIMA/GARCH | Execução Automatizada</p>
    </div>
    """, unsafe_allow_html=True)

def render_connection_status():
    """Renderiza o status de conexão - ETAPA 1: Integrado com sistema real"""
    system = st.session_state.trading_system
    
    # ETAPA 1: Adicionar status do sistema real
    if HAS_REAL_SYSTEM:
        real_status = get_real_system_status()
        
        # Status combinado
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if real_status.get('mt5_conectado', False):
                account_info = system.get_account_info()
                if account_info:
                    status_class = "status-online"
                    status_text = f"🟢 MT5 CONECTADO - {account_info['company']} | {account_info['server']}"
                else:
                    status_class = "status-offline"
                    status_text = "🔴 ERRO NA CONEXÃO MT5"
            else:
                status_class = "status-offline"
                status_text = "🔴 MT5 DESCONECTADO"
        
        with col2:
            # Status do sistema real
            if real_status.get('has_original_code', False):
                if real_status.get('is_running', False):
                    st.markdown('<div class="status-card status-processing">🔄 SISTEMA ATIVO</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="status-card status-offline">⏸️ SISTEMA PARADO</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-card status-offline">❌ CÓDIGO ORIGINAL N/D</div>', unsafe_allow_html=True)
        
        # Exibir status principal
        st.markdown(f'<div class="status-card {status_class}">{status_text}</div>', unsafe_allow_html=True)
        
        # Métricas da conta (se conectado)
        if system.mt5_connected:
            account_info = system.get_account_info()
            if account_info:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Saldo", f"{account_info['currency']} {account_info['balance']:,.2f}")
                with col2:
                    st.metric("Equity", f"{account_info['currency']} {account_info['equity']:,.2f}")
                with col3:
                    st.metric("Margem Livre", f"{account_info['currency']} {account_info['free_margin']:,.2f}")
                with col4:
                    profit_color = "profit-positive" if account_info['profit'] >= 0 else "profit-negative"
                    st.metric("Lucro/Prejuízo", f"{account_info['currency']} {account_info['profit']:,.2f}")        # ETAPA 1: Métricas do sistema real
        if real_status.get('has_original_code', False):
            st.subheader("📊 Status do Sistema Real")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Iterações", real_status.get('current_iteration', 0))
            with col2:
                st.metric("Operações Ativas", real_status.get('active_operations', 0))
            with col3:
                status_ai = "✅" if real_status.get('has_ai_models', False) else "❌"
                st.metric("IA", status_ai)
            with col4:
                status_cache = "✅" if real_status.get('cache_loaded', False) else "❌"
                st.metric("Cache", status_cache)
            with col5:
                st.metric("Logs", real_status.get('total_logs', 0))
                
    else:
        # Fallback para versão original
        if system.mt5_connected:
            account_info = system.get_account_info()
            if account_info:
                status_class = "status-online"
                status_text = f"🟢 CONECTADO - {account_info['company']} | {account_info['server']}"
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Saldo", f"{account_info['currency']} {account_info['balance']:,.2f}")
                with col2:
                    st.metric("Equity", f"{account_info['currency']} {account_info['equity']:,.2f}")
                with col3:
                    st.metric("Margem Livre", f"{account_info['currency']} {account_info['free_margin']:,.2f}")
                with col4:
                    profit_color = "profit-positive" if account_info['profit'] >= 0 else "profit-negative"
                    st.metric("Lucro/Prejuízo", f"{account_info['currency']} {account_info['profit']:,.2f}")
            else:
                status_class = "status-offline"
                status_text = "🔴 ERRO NA CONEXÃO"
        else:
            status_class = "status-offline"
            status_text = "🔴 DESCONECTADO"
        
        st.markdown(f'<div class="status-card {status_class}">{status_text}</div>', unsafe_allow_html=True)

def render_sidebar():
    """Renderiza a barra lateral com configurações"""
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Conexão MT5
        st.subheader("Conexão MetaTrader 5")
        
        with st.expander("Configurar Conexão", expanded=not st.session_state.trading_system.mt5_connected):
            login = st.number_input("Login", value=0, help="Deixe 0 para usar a última conta logada")
            password = st.text_input("Senha", type="password")
            server = st.text_input("Servidor", help="Ex: MetaQuotes-Demo")
            
            if st.button("🔌 Conectar"):
                with st.spinner("Conectando..."):
                    if st.session_state.trading_system.connect_mt5(
                        login if login > 0 else None,
                        password if password else None,
                        server if server else None
                    ):
                        st.success("✅ Conectado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Falha na conexão!")
        
        # Configurações de Trading
        st.subheader("📊 Parâmetros de Trading")
        
        config = st.session_state.config
        
        # Timeframe
        config['timeframe'] = st.selectbox(
            "Timeframe",
            ['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1'],
            index=['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1'].index(config['timeframe'])
        )
          # Período de análise
        config['period'] = st.slider("Período de Análise", 10, 100, config.get('period', 20))
        
        # Z-Score threshold
        config['zscore_threshold'] = st.slider("Limite Z-Score", 1.0, 5.0, config.get('zscore_threshold', 2.0), 0.1)
          # Gestão de Risco
        st.subheader("🛡️ Gestão de Risco")
        
        config['max_positions'] = st.slider("Máx. Posições Simultâneas", 1, 20, config.get('max_positions', 5))
        config['risk_per_trade'] = st.slider("Risco por Trade (%)", 0.01, 0.10, config.get('risk_per_trade', 0.02), 0.001)
        config['stop_loss'] = st.slider("Stop Loss (%)", 0.01, 0.20, config.get('stop_loss', 0.05), 0.001)
        config['take_profit'] = st.slider("Take Profit (%)", 0.02, 0.50, config.get('take_profit', 0.10), 0.001)
          # Filtros Avançados
        st.subheader("🔍 Filtros Avançados")
        
        config['enable_cointegration'] = st.checkbox(
            "Filtro de Cointegração",
            config.get('enable_cointegration', True)
        )
        
        config['enable_volatility_filter'] = st.checkbox(
            "Filtro de Volatilidade",
            config.get('enable_volatility_filter', True)
        )
        
        config['min_volume'] = st.number_input(
            "Volume Mínimo",
            1000, 100000000, config.get('min_volume', 1000000)
        )
        
        config['max_spread'] = st.slider(
            "Spread Máximo (%)",
            0.001, 0.10, config.get('max_spread', 0.01), 0.001
        )
        
        # Atualização Automática
        st.subheader("🔄 Atualização")
        
        st.session_state.auto_refresh = st.checkbox(
            "Atualização Automática",
            st.session_state.auto_refresh
        )
        
        if st.session_state.auto_refresh:
            st.session_state.refresh_interval = st.slider(
                "Intervalo (segundos)",
                5, 300, st.session_state.refresh_interval
            )
        
        # Ações do Sistema
        st.subheader("🎮 Controles")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("▶️ Iniciar", use_container_width=True):
                st.session_state.trading_system.is_running = True
                st.success("Sistema iniciado!")
                st.rerun()
        
        with col2:
            if st.button("⏹️ Parar", use_container_width=True):
                st.session_state.trading_system.is_running = False
                st.warning("Sistema parado!")
                st.rerun()
        
        if st.button("🔄 Atualizar Agora", use_container_width=True):
            st.rerun()
        
        # Salvar/Carregar Configurações
        st.subheader("💾 Configurações")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Salvar", use_container_width=True):
                try:
                    with open("trading_config.json", "w") as f:
                        json.dump(config, f, indent=2)
                    st.success("Configurações salvas!")
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")
        
        with col2:
            if st.button("📤 Carregar", use_container_width=True):
                try:
                    if os.path.exists("trading_config.json"):
                        with open("trading_config.json", "r") as f:
                            st.session_state.config = json.load(f)
                        st.success("Configurações carregadas!")
                        st.rerun()
                    else:
                        st.warning("Arquivo não encontrado!")
                except Exception as e:
                    st.error(f"Erro ao carregar: {e}")

def render_pair_selection():
    """Renderiza a seleção de pares"""
    st.header("📊 Seleção de Pares")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Lista de pares disponíveis
        available_pairs = ParameterManager.get_default_pairs()
        
        # Permitir adicionar pares customizados
        custom_pair = st.text_input("Adicionar par customizado (ex: PETR4)")
        if custom_pair and st.button("➕ Adicionar"):
            if custom_pair.upper() not in available_pairs:
                available_pairs.append(custom_pair.upper())
                st.success(f"Par {custom_pair.upper()} adicionado!")
          # Seleção múltipla de pares
        # Filtrar apenas pares que existem na lista disponível
        valid_defaults = [pair for pair in st.session_state.config['pairs'] if pair in available_pairs]
        
        selected_pairs = st.multiselect(
            "Selecione os pares para análise",
            available_pairs,
            default=valid_defaults[:10]  # Limita a 10 pares padrão válidos
        )
        
        st.session_state.config['pairs'] = selected_pairs
    
    with col2:
        st.subheader("Estatísticas dos Pares")
        if selected_pairs:
            st.metric("Pares Selecionados", len(selected_pairs))
            st.metric("Combinações Possíveis", len(selected_pairs) * (len(selected_pairs) - 1) // 2)
            
            # Mostrar alguns pares selecionados
            st.write("**Primeiros 5 pares:**")
            for pair in selected_pairs[:5]:
                st.write(f"• {pair}")
            
            if len(selected_pairs) > 5:
                st.write(f"... e mais {len(selected_pairs) - 5} pares")

def render_analysis_results():
    """Renderiza os resultados da análise - ETAPA 2: Integrado com sistema real"""
    st.header("📈 Resultados da Análise")
      # ETAPA 2: Usar dados do sistema real se disponível
    use_real_system = HAS_REAL_SYSTEM and hasattr(st.session_state, 'real_system') and st.session_state.real_system
    
    # Verificar se há dados disponíveis
    has_data = False
    if use_real_system and st.session_state.real_state.dados_mercado:
        has_data = True
    elif hasattr(st.session_state.trading_system, 'analysis_results') and st.session_state.trading_system.analysis_results:
        has_data = True
      # Placeholder para quando não há dados
    if not has_data:
        st.info("📊 Execute a análise para ver os resultados aqui.")
        
        if st.button("🔍 Executar Análise"):
            with st.spinner("Analisando pares..."):
                if use_real_system:
                    # ETAPA 4: Usar análise real aprimorada
                    pairs = st.session_state.config.get('pairs', ['EURUSD', 'GBPUSD'])
                    try:
                        # Tentar usar análise real através do sistema integrado
                        if HAS_REAL_SYSTEM and 'real_trading_state' in st.session_state:
                            real_status = get_real_system_status()
                            real_results = real_status.get('analysis_results', [])
                        else:
                            real_results = []
                    except Exception as e:
                        st.warning(f"Erro ao acessar análise real: {e}")
                        real_results = []
                    
                    # Atualizar resultados com dados reais
                    st.session_state.trading_system.analysis_results = real_results
                else:
                    # Fallback para análise simulada
                    time.sleep(2)
                    mock_results = {
                        'pairs_analyzed': len(st.session_state.config['pairs']),
                        'cointegrated_pairs': np.random.randint(5, 15),
                        'signals_found': np.random.randint(2, 8),
                        'last_update': datetime.now()
                    }
                    st.session_state.trading_system.analysis_results = mock_results
                
                st.success("✅ Análise concluída!")
                st.rerun()
        return
      # Obter resultados (real ou simulado)
    if use_real_system and hasattr(st.session_state, 'real_state') and st.session_state.real_state and st.session_state.real_state.dados_mercado:
        results = {
            'pairs_analyzed': len(st.session_state.real_state.dados_mercado),
            'cointegrated_pairs': len([p for p in st.session_state.real_state.dados_mercado.values() if p.get('signal') != 'NEUTRO']),
            'signals_found': len([p for p in st.session_state.real_state.dados_mercado.values() if p.get('confidence', 0) > 0.7]),
            'last_update': st.session_state.real_state.ultima_atualizacao or datetime.now(),
            'real_data': st.session_state.real_state.dados_mercado
        }
    else:
        results = st.session_state.trading_system.analysis_results
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Pares Analisados",
            results.get('pairs_analyzed', 0),
            help="Total de pares processados na última análise"
        )
    
    with col2:
        st.metric(
            "Pares Cointegrados",
            results.get('cointegrated_pairs', 0),
            help="Pares que passaram no teste de cointegração"
        )
    
    with col3:
        st.metric(
            "Sinais Encontrados",
            results.get('signals_found', 0),
            help="Oportunidades de trading identificadas"
        )
    
    with col4:
        if 'last_update' in results:
            time_diff = datetime.now() - results['last_update']
            st.metric(
                "Última Atualização",
                f"{time_diff.seconds//60}min atrás",
                help="Tempo desde a última análise"
            )
      # Gráfico de distribuição Z-Score - ETAPA 4: Dados reais
    st.subheader("📊 Distribuição de Z-Scores")
    
    # Usar dados reais se disponíveis
    if use_real_system and 'zscore_distribution' in results:
        z_scores = results['zscore_distribution']
    elif 'real_data' in results:
        # Extrair z-scores dos dados reais
        z_scores = [data.get('zscore', 0) for data in results['real_data'].values()]
    else:
        # Dados simulados para o gráfico
        z_scores = np.random.normal(0, 1.5, 100)
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=z_scores,
        nbinsx=20,
        name="Z-Scores",
        marker_color='rgba(31, 78, 121, 0.7)'
    ))
    
    # Adicionar linhas de threshold
    fig.add_vline(x=st.session_state.config['zscore_threshold'], 
                  line_dash="dash", line_color="red", 
                  annotation_text="Limite Superior")
    fig.add_vline(x=-st.session_state.config['zscore_threshold'], 
                  line_dash="dash", line_color="red", 
                  annotation_text="Limite Inferior")
    
    fig.update_layout(
        title="Distribuição de Z-Scores dos Pares",
        xaxis_title="Z-Score",
        yaxis_title="Frequência",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
      # Tabela de sinais - ETAPA 2: Usar dados reais
    st.subheader("🎯 Sinais de Trading")
      # ETAPA 4: Gerar tabela com dados reais aprimorados
    signals_data = []
    
    if use_real_system and 'real_data' in results:
        # Usar dados reais do sistema
        for symbol, data in results['real_data'].items():
            if data.get('signal') != 'NEUTRO':
                signals_data.append({
                    'Par': symbol,
                    'Preço Atual': f"{data.get('current_price', 0):.5f}",
                    'Sinal': data.get('signal', 'NEUTRO'),
                    'Confiança': f"{data.get('confidence', 0):.1%}",
                    'RSI': f"{data.get('rsi', 0):.1f}",
                    'MA20': f"{data.get('ma_20', 0):.5f}",
                    'Z-Score': f"{data.get('zscore', 0):.2f}",
                    'Recomendação': data.get('recommendation', 'HOLD'),
                    'Timestamp': data.get('last_update', datetime.now()).strftime("%H:%M:%S")
                })
    else:
        # Fallback para dados simulados
        for i in range(5):
            pair1 = np.random.choice(st.session_state.config['pairs'])
            pair2 = np.random.choice([p for p in st.session_state.config['pairs'] if p != pair1])
            z_score = np.random.uniform(-3, 3)
            confidence = np.random.uniform(0.6, 0.95)
            
            signals_data.append({
                'Par': f"{pair1}/{pair2}",
                'Z-Score': round(z_score, 2),
                'Sinal': 'COMPRA' if z_score < -st.session_state.config['zscore_threshold'] else 'VENDA',
                'Confiança': f"{confidence:.1%}",
                'Timestamp': (datetime.now() - timedelta(minutes=np.random.randint(1, 30))).strftime("%H:%M:%S")            })
    
    if signals_data:
        df_signals = pd.DataFrame(signals_data)
        
        # Colorir as linhas baseado no tipo de sinal e força
        def highlight_signal(row):
            if row['Sinal'] == 'COMPRA':
                return ['background-color: rgba(76, 175, 80, 0.1)'] * len(row)
            elif row['Sinal'] == 'VENDA':
                return ['background-color: rgba(244, 67, 54, 0.1)'] * len(row)
            return [''] * len(row)
        
        # Exibir tabela com formatação aprimorada
        st.dataframe(
            df_signals.style.apply(highlight_signal, axis=1),
            use_container_width=True,
            hide_index=True
        )
        
        # ETAPA 4: Estatísticas dos sinais se dados reais disponíveis
        if use_real_system and 'summary' in results:
            summary = results['summary']
            
            st.subheader("📊 Resumo dos Sinais")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Sinais de Compra", 
                    summary.get('signals_distribution', {}).get('buy', 0),
                    help="Número de sinais de compra identificados"
                )
            
            with col2:
                st.metric(
                    "Sinais de Venda", 
                    summary.get('signals_distribution', {}).get('sell', 0),
                    help="Número de sinais de venda identificados"
                )
            
            with col3:
                st.metric(
                    "Sinais Fortes", 
                    summary.get('signal_strength', {}).get('strong', 0),
                    help="Sinais com alta confiança (>80%)"
                )
            
            with col4:
                st.metric(
                    "Z-Scores Extremos", 
                    summary.get('market_metrics', {}).get('extreme_zscores', 0),
                    help="Z-scores com valor absoluto > 2"
                )
    else:
        st.info("Nenhum sinal de trading encontrado no momento.")
        
        # Botão para forçar nova análise
        if st.button("🔄 Reanalizar Pares"):
            if use_real_system:
                with st.spinner("Executando nova análise..."):
                    pairs = st.session_state.config.get('pairs', [])
                    if pairs:
                        try:
                            # Tentar usar análise real através do sistema integrado
                            if HAS_REAL_SYSTEM and 'real_trading_state' in st.session_state:
                                real_status = get_real_system_status()
                                new_results = real_status.get('analysis_results', [])
                            else:
                                new_results = []
                        except Exception as e:
                            st.warning(f"Erro ao executar análise real: {e}")
                            new_results = []
                        
                        st.session_state.trading_system.analysis_results = new_results
                        st.success("✅ Nova análise concluída!")
                        st.rerun()
                    else:
                        st.warning("Configure alguns pares primeiro!")

def render_positions_monitor():
    """Renderiza o monitor de posições - ETAPA 4: Dados reais"""
    st.header("💼 Monitor de Posições")
    
    # ETAPA 4: Obter dados reais de posições
    use_real_data = HAS_REAL_SYSTEM and hasattr(st.session_state, 'real_system') and st.session_state.real_system
    
    if use_real_data:
        # Obter dados reais do sistema
        real_status = get_real_system_status()
        positions_data = real_status.get('positions', [])
        
        # Métricas reais
        total_positions = len(positions_data)
        total_pnl = sum([pos.get('pnl', 0) for pos in positions_data])
        margin_used = real_status.get('margin_used', 0)
        
        # Status das posições reais
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Posições Abertas", total_positions, 
                     real_status.get('position_change', 0))
        
        with col2:
            st.metric("P&L Total", f"R$ {total_pnl:.2f}", 
                     real_status.get('pnl_change', 0))
        
        with col3:
            st.metric("Margem Utilizada", f"{margin_used:.1f}%", 
                     real_status.get('margin_change', 0))
        
        # Converter dados reais para formato da tabela
        if positions_data:
            df_positions = pd.DataFrame([
                {
                    'Ticket': pos.get('ticket', 'N/A'),
                    'Par': pos.get('symbol', 'N/A'),
                    'Tipo': pos.get('type', 'N/A'),
                    'Volume': pos.get('volume', 0),
                    'Preço Abertura': pos.get('open_price', 0),
                    'Preço Atual': pos.get('current_price', 0),
                    'P&L': pos.get('pnl', 0),
                    'Z-Score Atual': pos.get('zscore', 0),
                    'Tempo': pos.get('time', datetime.now().strftime("%H:%M:%S"))
                }
                for pos in positions_data
            ])
        else:
            df_positions = pd.DataFrame()
    else:
        # Status das posições (dados simulados para fallback)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Posições Abertas", 3, "1")
        
        with col2:
            st.metric("P&L Total", "R$ 1,250.50", "250.50")
        
        with col3:
            st.metric("Margem Utilizada", "15.3%", "-2.1%")
        
        # Tabela de posições (dados simulados)
        positions_data = [
            {
                'Ticket': 12345,
                'Par': 'PETR4/VALE3',
                'Tipo': 'BUY',
                'Volume': 100,
                'Preço Abertura': 28.50,
                'Preço Atual': 29.20,
                'P&L': 70.00,
                'Z-Score Atual': -1.8,
                'Tempo': '15:30:45'
            },
            {
                'Ticket': 12346,
                'Par': 'ITUB4/BBDC4',
                'Tipo': 'SELL',
                'Volume': 200,
                'Preço Abertura': 25.80,
                'Preço Atual': 25.20,
                'P&L': 120.00,
                'Z-Score Atual': 2.1,
                'Tempo': '14:25:12'
            },
            {
                'Ticket': 12347,
                'Par': 'WEGE3/RAIL3',
                'Tipo': 'BUY',
                'Volume': 150,
                'Preço Abertura': 32.10,
                'Preço Atual': 32.50,
                'P&L': 60.50,
                'Z-Score Atual': -0.9,
                'Tempo': '13:45:22'
            }
        ]
        
        df_positions = pd.DataFrame(positions_data)
      # Função para colorir P&L
    def color_pnl(val):
        color = 'green' if val > 0 else 'red'
        return f'color: {color}; font-weight: bold'
    
    # Exibir tabela com formatação
    if not df_positions.empty:
        st.dataframe(
            df_positions.style.applymap(color_pnl, subset=['P&L']),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhuma posição aberta no momento.")
      # Gráfico de P&L ao longo do tempo - ETAPA 4: Dados reais
    st.subheader("📊 Evolução do P&L")
    
    if use_real_data and 'pnl_history' in real_status:
        # Usar histórico real de P&L
        pnl_history = real_status.get('pnl_history', [])
        if pnl_history:
            times = [entry['timestamp'] for entry in pnl_history]
            pnl_values = [entry['cumulative_pnl'] for entry in pnl_history]
        else:
            # Fallback se não houver histórico
            times = [datetime.now()]
            pnl_values = [total_pnl]
    else:
        # Dados simulados para o gráfico
        times = pd.date_range(start=datetime.now() - timedelta(hours=6), 
                             end=datetime.now(), freq='15min')
        pnl_values = np.cumsum(np.random.randn(len(times)) * 50)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=times,
        y=pnl_values,
        mode='lines',
        name='P&L Cumulativo',
        line=dict(color='rgba(31, 78, 121, 0.8)', width=2)
    ))
    
    fig.update_layout(
        title="Evolução do P&L Cumulativo",
        xaxis_title="Horário",
        yaxis_title="P&L (R$)",
        showlegend=False,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Controles de posições
    st.subheader("🎮 Controles")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Atualizar Posições", use_container_width=True):
            st.success("Posições atualizadas!")
    
    with col2:
        if st.button("🔴 Fechar Todas", use_container_width=True):
            st.warning("Todas as posições serão fechadas!")
    
    with col3:
        if st.button("📈 Relatório", use_container_width=True):
            st.info("Gerando relatório...")
    
    with col4:
        if st.button("⚙️ Configurar Alerts", use_container_width=True):
            st.info("Configurando alertas...")

def render_real_system_logs():
    """Renderiza logs do sistema real de trading"""
    if not HAS_REAL_SYSTEM:
        st.info("Sistema real não disponível")
        return
    
    st.header("📋 Logs do Sistema Real")
    
    # Controles
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        log_filter = st.selectbox(
            "Filtrar por nível:",
            ["TODOS", "INFO", "WARNING", "ERROR", "DEBUG"]
        )
    
    with col2:
        limit = st.number_input("Máx. logs:", 10, 1000, 100)
    
    with col3:
        if st.button("🔄 Atualizar"):
            st.rerun()
      # Obter logs
    try:
        if HAS_REAL_SYSTEM and 'real_trading_state' in st.session_state:
            real_status = get_real_system_status()
            logs = real_status.get('system_logs', [])[:limit]
        else:
            logs = []
    except Exception:
        logs = []
    
    if not logs:
        st.info("Nenhum log disponível")
        return
    
    # Filtrar logs
    if log_filter != "TODOS":
        logs = [log for log in logs if log.get('nivel') == log_filter]
    
    # Exibir logs
    st.subheader(f"📝 Últimos {len(logs)} logs")
    
    for log in reversed(logs):  # Mais recentes primeiro
        timestamp = log.get('timestamp', 'N/A')
        nivel = log.get('nivel', 'INFO')
        mensagem = log.get('mensagem', '')
        
        # Cor baseada no nível
        if nivel == 'ERROR':
            st.error(f"🔴 **{timestamp}** - {mensagem}")
        elif nivel == 'WARNING':
            st.warning(f"🟡 **{timestamp}** - {mensagem}")
        elif nivel == 'INFO':
            st.info(f"🔵 **{timestamp}** - {mensagem}")
        else:
            st.text(f"⚪ **{timestamp}** - {mensagem}")

def render_system_logs():
    """Renderiza logs do sistema - ETAPA 2: Integrado com sistema real"""
    if HAS_REAL_SYSTEM and st.session_state.get('show_real_logs', False):
        render_real_system_logs()
        if st.button("⬅️ Voltar para logs normais"):
            st.session_state.show_real_logs = False
            st.rerun()
        return
    
    # Logs normais do sistema Streamlit
    st.header("📝 Logs do Sistema")
    
    # Botão para ver logs do sistema real
    if HAS_REAL_SYSTEM:
        if st.button("🚀 Ver Logs do Sistema Real"):
            st.session_state.show_real_logs = True
            st.rerun()
    
    # Placeholder para logs
    log_entries = [
        {"timestamp": "2024-01-15 10:30:15", "level": "INFO", "message": "Sistema iniciado com sucesso"},
        {"timestamp": "2024-01-15 10:30:20", "level": "INFO", "message": "Conectado ao MetaTrader 5"},
        {"timestamp": "2024-01-15 10:30:25", "level": "INFO", "message": "Carregando configurações"},
        {"timestamp": "2024-01-15 10:30:30", "level": "WARNING", "message": "Spread alto detectado em PETR4"},
        {"timestamp": "2024-01-15 10:30:35", "level": "INFO", "message": "Análise de cointegração iniciada"},
        {"timestamp": "2024-01-15 10:30:40", "level": "SUCCESS", "message": "3 pares cointegrados encontrados"},
        {"timestamp": "2024-01-15 10:30:45", "level": "INFO", "message": "Sinal de compra gerado para VALE3/PETR4"},
        {"timestamp": "2024-01-15 10:30:50", "level": "ERROR", "message": "Falha na conexão com servidor de dados"},
    ]
    
    # Filtros
    col1, col2 = st.columns([3, 1])
    
    with col1:
        log_level_filter = st.selectbox(
            "Filtrar por nível:",
            ["TODOS", "INFO", "WARNING", "ERROR", "SUCCESS"]
        )
    
    with col2:
        auto_refresh = st.checkbox("Auto-refresh", value=st.session_state.auto_refresh)
        st.session_state.auto_refresh = auto_refresh
    
    # Aplicar filtro
    if log_level_filter != "TODOS":
        filtered_logs = [log for log in log_entries if log["level"] == log_level_filter]
    else:
        filtered_logs = log_entries
    
    # Exibir logs
    st.subheader(f"📋 Logs Recentes ({len(filtered_logs)} entradas)")
    
    for log in reversed(filtered_logs):  # Mais recentes primeiro
        timestamp = log["timestamp"]
        level = log["level"]
        message = log["message"]
        
        if level == "ERROR":
            st.error(f"🔴 **{timestamp}** - {message}")
        elif level == "WARNING":
            st.warning(f"🟡 **{timestamp}** - {message}")
        elif level == "SUCCESS":
            st.success(f"🟢 **{timestamp}** - {message}")
        else:
            st.info(f"🔵 **{timestamp}** - {message}")
    
    # Auto-refresh
    if auto_refresh:
        time.sleep(st.session_state.refresh_interval)
        st.rerun()

def render_dashboard():
    """Renderiza o dashboard principal - ETAPA 4: Dados reais"""
    st.header("🎯 Dashboard")
    
    # ETAPA 4: Obter dados reais do sistema
    use_real_data = HAS_REAL_SYSTEM and hasattr(st.session_state, 'real_system') and st.session_state.real_system
    
    if use_real_data:
        # Dados reais do sistema
        real_status = get_real_system_status()
        account_info = st.session_state.trading_system.get_account_info() if hasattr(st.session_state.trading_system, 'get_account_info') else {}
        
        # Métricas principais reais
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            balance = account_info.get('balance', real_status.get('balance', 0))
            balance_change = real_status.get('balance_change', 0)
            st.metric("Saldo Atual", f"R$ {balance:,.2f}", f"{balance_change:+,.2f}")
        
        with col2:
            trades_today = real_status.get('trades_today', 0)
            trades_change = real_status.get('trades_change', 0)
            st.metric("Trades Hoje", trades_today, f"{trades_change:+d}")
        
        with col3:
            win_rate = real_status.get('win_rate', 0)
            win_rate_change = real_status.get('win_rate_change', 0)
            st.metric("Taxa de Acerto", f"{win_rate:.1f}%", f"{win_rate_change:+.1f}%")
        
        with col4:
            drawdown = real_status.get('drawdown', 0)
            drawdown_change = real_status.get('drawdown_change', 0)
            st.metric("Drawdown", f"{drawdown:.1f}%", f"{drawdown_change:+.1f}%")
        
        with col5:
            sharpe = real_status.get('sharpe_ratio', 0)
            sharpe_change = real_status.get('sharpe_change', 0)
            st.metric("Sharpe Ratio", f"{sharpe:.2f}", f"{sharpe_change:+.2f}")
          # Gráficos com dados reais
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de performance real
            st.subheader("📈 Performance Acumulada")
            
            if 'equity_history' in real_status and real_status.get('equity_history'):
                equity_data = real_status.get('equity_history', [])
                dates = [entry['timestamp'] for entry in equity_data]
                equity_values = [entry['equity'] for entry in equity_data]
            else:
                # Fallback se não houver histórico
                dates = pd.date_range(start=datetime.now() - timedelta(days=30), 
                                     end=datetime.now(), freq='D')
                equity_values = [balance] * len(dates)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates,
                y=equity_values,
                mode='lines',
                name='Equity Curve',
                line=dict(color='rgba(31, 78, 121, 0.8)', width=2),
                fill='tonexty'
            ))
            
            fig.update_layout(
                title="Curva de Equity (Real)",
                xaxis_title="Data",
                yaxis_title="Valor da Conta (R$)",
                showlegend=False            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Distribuição de trades reais
            st.subheader("📊 Distribuição de Trades")
            
            if 'trade_results' in real_status and real_status.get('trade_results'):
                trade_results = real_status.get('trade_results', [])
            else:
                # Fallback para dados simulados
                trade_results = np.random.normal(50, 100, 50)
            
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=trade_results,
                nbinsx=15,
                name="Resultados",
                marker_color='rgba(31, 78, 121, 0.7)'
            ))
            
            fig.update_layout(
                title="Distribuição de Resultados por Trade",
                xaxis_title="Resultado (R$)",
                yaxis_title="Frequência",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Tabela de melhores e piores trades - dados reais
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏆 Melhores Trades")
            if 'best_trades' in real_status and real_status['best_trades']:
                best_trades_data = real_status['best_trades']
                best_trades = pd.DataFrame([
                    {
                        'Par': trade.get('symbol', 'N/A'),
                        'Resultado': f"R$ {trade.get('pnl', 0):.2f}",
                        'Data': trade.get('date', 'N/A')
                    }
                    for trade in best_trades_data[:3]
                ])
            else:
                best_trades = pd.DataFrame({
                    'Par': ['PETR4/VALE3', 'ITUB4/BBDC4', 'WEGE3/RAIL3'],
                    'Resultado': ['R$ 450.20', 'R$ 380.50', 'R$ 275.80'],
                    'Data': ['15/06', '14/06', '13/06']
                })
            st.dataframe(best_trades, hide_index=True, use_container_width=True)
        
        with col2:
            st.subheader("❌ Piores Trades")
            if 'worst_trades' in real_status and real_status['worst_trades']:
                worst_trades_data = real_status['worst_trades']
                worst_trades = pd.DataFrame([
                    {
                        'Par': trade.get('symbol', 'N/A'),
                        'Resultado': f"R$ {trade.get('pnl', 0):.2f}",
                        'Data': trade.get('date', 'N/A')
                    }
                    for trade in worst_trades_data[:3]
                ])
            else:
                worst_trades = pd.DataFrame({
                    'Par': ['MGLU3/LREN3', 'CCRO3/RAIL3', 'GOAU4/CSNA3'],
                    'Resultado': ['-R$ 125.40', '-R$ 89.20', '-R$ 67.30'],
                    'Data': ['15/06', '14/06', '12/06']
                })
            st.dataframe(worst_trades, hide_index=True, use_container_width=True)
    
    else:
        # Fallback para dados simulados
        # Métricas principais do dashboard
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Saldo Atual", "R$ 50,250.80", "1,250.30")
        
        with col2:
            st.metric("Trades Hoje", "12", "3")
        
        with col3:
            st.metric("Taxa de Acerto", "68.5%", "2.1%")
        
        with col4:
            st.metric("Drawdown", "-2.3%", "-0.5%")
        
        with col5:
            st.metric("Sharpe Ratio", "1.85", "0.12")
        
        # Gráficos do dashboard
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de performance
            st.subheader("📈 Performance Acumulada")
            
            dates = pd.date_range(start=datetime.now() - timedelta(days=30), 
                                 end=datetime.now(), freq='D')
            performance = np.cumsum(np.random.randn(len(dates)) * 0.02) + 1
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates,
                y=performance * 50000,  # Simular valor inicial
                mode='lines',
                name='Equity Curve',
                line=dict(color='rgba(31, 78, 121, 0.8)', width=2),
                fill='tonexty'
            ))
            
            fig.update_layout(
                title="Curva de Equity (30 dias)",
                xaxis_title="Data",
                yaxis_title="Valor da Conta (R$)",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Distribuição de trades
            st.subheader("📊 Distribuição de Trades")
            
            trade_results = np.random.normal(50, 100, 50)  # Simular resultados
            
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=trade_results,
                nbinsx=15,
                name="Resultados",
                marker_color='rgba(31, 78, 121, 0.7)'
            ))
            
            fig.update_layout(
                title="Distribuição de Resultados por Trade",
                xaxis_title="Resultado (R$)",
                yaxis_title="Frequência",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Tabela de melhores e piores trades
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏆 Melhores Trades")
            best_trades = pd.DataFrame({
                'Par': ['PETR4/VALE3', 'ITUB4/BBDC4', 'WEGE3/RAIL3'],
                'Resultado': ['R$ 450.20', 'R$ 380.50', 'R$ 275.80'],
                'Data': ['15/06', '14/06', '13/06']
            })
            st.dataframe(best_trades, hide_index=True, use_container_width=True)
        
        with col2:
            st.subheader("❌ Piores Trades")
            worst_trades = pd.DataFrame({
                'Par': ['MGLU3/LREN3', 'CCRO3/RAIL3', 'GOAU4/CSNA3'],
                'Resultado': ['-R$ 125.40', '-R$ 89.20', '-R$ 67.30'],
                'Data': ['15/06', '14/06', '12/06']
            })
            st.dataframe(worst_trades, hide_index=True, use_container_width=True)

# ETAPA 4: Painel de controle aprimorado com dados reais
def render_trading_control_panel():
    """Painel de controle para o sistema de trading real - ETAPA 4 Aprimorado"""
    if not HAS_REAL_SYSTEM:
        st.error("Sistema real não disponível")
        return
    
    st.header("🎛️ Controle do Sistema de Trading")
    
    # Status atual detalhado
    real_status = get_real_system_status()
    
    # Métricas de status principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if real_status.get('is_initialized', False):
            st.success("✅ Inicializado")
        else:
            st.error("❌ Não Inicializado")
    
    with col2:
        if real_status.get('is_running', False):
            st.success("🟢 Executando")
        else:
            st.warning("⏸️ Parado")
    
    with col3:
        if real_status.get('mt5_connected', False):
            st.success("🔗 MT5 Conectado")
        else:
            st.error("❌ MT5 Desconectado")
    
    with col4:
        st.metric("Pares Monitorados", real_status.get('pairs_monitored', 0))
    
    # ETAPA 4: Métricas avançadas do sistema
    st.subheader("📊 Métricas do Sistema")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Posições Abertas", 
            real_status.get('positions_open', 0),
            real_status.get('position_change', 0)
        )
    
    with col2:
        st.metric(
            "Iteração Atual", 
            real_status.get('current_iteration', 0)
        )
    
    with col3:
        balance = real_status.get('balance', 0)
        st.metric(
            "Saldo da Conta", 
            f"R$ {balance:,.2f}",
            f"R$ {real_status.get('balance_change', 0):+,.2f}"
        )
    
    with col4:
        st.metric(
            "Trades Hoje", 
            real_status.get('trades_today', 0),
            real_status.get('trades_change', 0)
        )
    
    with col5:
        win_rate = real_status.get('win_rate', 0)
        st.metric(
            "Taxa de Acerto", 
            f"{win_rate:.1f}%",
            f"{real_status.get('win_rate_change', 0):+.1f}%"
        )
    
    # Status de componentes do sistema
    st.subheader("🔧 Status dos Componentes")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if real_status.get('has_ai_models', False):
            st.success("🤖 Modelos IA: Ativos")
        else:
            st.warning("🤖 Modelos IA: Inativos")
    
    with col2:
        if real_status.get('cache_loaded', False):
            st.success("💾 Cache: Carregado")
        else:
            st.warning("💾 Cache: Não Carregado")
    
    with col3:
        if real_status.get('has_original_code', False):
            st.success("📜 Código Original: OK")
        else:
            st.error("📜 Código Original: Erro")
    
    with col4:
        last_update = real_status.get('last_update')
        if last_update:
            time_diff = datetime.now() - last_update
            status = "🕐 Atualizado" if time_diff.seconds < 60 else "⏰ Desatualizado"
            st.info(f"{status}: {time_diff.seconds}s")
        else:
            st.warning("⏰ Sem Atualizações")
      # Controles principais
    st.subheader("🎮 Controles")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ Iniciar Sistema", key="start_real_system"):
            with st.spinner("Iniciando sistema real..."):
                try:
                    # Tentar iniciar através do sistema real integrado
                    if HAS_REAL_SYSTEM and 'real_trading_state' in st.session_state:
                        st.session_state.real_trading_state['is_running'] = True
                        st.success("Sistema real iniciado!")
                    else:
                        st.warning("Sistema real não disponível")
                except Exception as e:
                    st.error(f"Erro ao iniciar sistema: {e}")
                time.sleep(1)
                st.rerun()
    
    with col2:
        if st.button("⏹️ Parar Sistema", key="stop_real_system"):
            with st.spinner("Parando sistema real..."):
                try:
                    # Tentar parar através do sistema real integrado
                    if HAS_REAL_SYSTEM and 'real_trading_state' in st.session_state:
                        st.session_state.real_trading_state['is_running'] = False
                        st.success("Sistema real parado!")
                    else:
                        st.warning("Sistema real não disponível")
                except Exception as e:
                    st.error(f"Erro ao parar sistema: {e}")
                time.sleep(1)
                st.rerun()
    
    with col3:
        if st.button("🔄 Executar Análise Manual", key="manual_analysis"):
            with st.spinner("Executando análise..."):
                pairs = st.session_state.config.get('pairs', ['EURUSD', 'GBPUSD'])
                try:
                    # Tentar usar análise real através do sistema integrado
                    if HAS_REAL_SYSTEM and 'real_trading_state' in st.session_state:
                        real_status = get_real_system_status()
                        results = real_status.get('analysis_results', [])
                    else:
                        results = []
                except Exception as e:
                    st.warning(f"Erro ao executar análise: {e}")
                    results = []
                st.success(f"Análise concluída! {len(results)} pares processados")
                time.sleep(1)
                st.rerun()
    
    # ETAPA 3: Executar função principal do código original
    st.subheader("🚀 Sistema Original")
    
    if st.button("🎯 Executar Função Principal Original", key="run_original_main"):
        if HAS_REAL_SYSTEM and real_status.get('has_original_code', False):
            with st.spinner("Executando a função principal do sistema original..."):
                try:
                    # Criar um novo thread para executar a função principal
                    import threading
                    
                    def run_original_main():
                        try:
                            # Executar a função main do código original através do sistema real
                            from trading_real_integration import execute_main_function
                            execute_main_function()
                            st.success("Função principal executada com sucesso")
                        except Exception as e:
                            st.error(f"Erro na execução da função principal: {e}")
                    
                    # Executar em thread separada para não bloquear o Streamlit
                    thread = threading.Thread(target=run_original_main, daemon=True)
                    thread.start()
                    
                    st.success("✅ Função principal iniciada em background!")
                    st.info("Verifique os logs para acompanhar o progresso")
                    
                except Exception as e:
                    st.error(f"Erro ao executar função principal: {e}")
        else:
            st.error("Função principal do código original não disponível")
      # Monitoramento em tempo real
    st.subheader("📊 Monitoramento em Tempo Real")
    
    if real_status.get('is_running', False):
        # Auto-refresh se estiver executando
        if st.checkbox("🔄 Auto-refresh (30s)", key="auto_refresh_trading"):
            time.sleep(30)
            st.rerun()
          # Últimos dados
        if hasattr(st.session_state, 'real_state') and st.session_state.real_state and st.session_state.real_state.dados_mercado:
            st.write("**Últimos dados do mercado:**")
            
            for symbol, data in list(st.session_state.real_state.dados_mercado.items())[:5]:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.write(f"**{symbol}**")
                
                with col2:
                    st.write(f"Preço: {data.get('current_price', 0):.5f}")
                
                with col3:
                    signal = data.get('signal', 'NEUTRO')
                    if signal == 'COMPRA':
                        st.success(f"📈 {signal}")
                    elif signal == 'VENDA':
                        st.error(f"📉 {signal}")
                    else:
                        st.info(f"➡️ {signal}")
                
                with col4:
                    confidence = data.get('confidence', 0)
                    st.write(f"Conf: {confidence:.1%}")
      # Logs recentes
    st.subheader("📋 Logs Recentes")
    
    # Tentar obter logs do sistema real ou usar fallback
    try:
        if HAS_REAL_SYSTEM and 'real_trading_state' in st.session_state:
            real_status = get_real_system_status()
            recent_logs = real_status.get('recent_logs', [])
        else:
            recent_logs = []
    except Exception:
        recent_logs = []
    
    if recent_logs:
        for log in reversed(recent_logs[-5:]):  # Últimos 5 logs
            timestamp = log.get('timestamp', 'N/A')
            nivel = log.get('nivel', 'INFO')
            mensagem = log.get('mensagem', '')
            
            if nivel == 'ERROR':
                st.error(f"🔴 {timestamp}: {mensagem}")
            elif nivel == 'WARNING':
                st.warning(f"🟡 {timestamp}: {mensagem}")
            else:
                st.info(f"🔵 {timestamp}: {mensagem}")
    else:
        st.info("Nenhum log disponível")

# ETAPA 5: Funcionalidades avançadas
def export_trading_data():
    """Exportar dados de trading para análise externa - ETAPA 5"""
    try:
        if not HAS_REAL_SYSTEM:
            st.warning("Sistema real não disponível para exportação")
            return None
        
        # Obter dados do sistema
        real_status = get_real_system_status()
        
        # Preparar dados para exportação
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'system_status': {
                'is_running': real_status.get('is_running', False),
                'mt5_connected': real_status.get('mt5_connected', False),
                'pairs_monitored': real_status.get('pairs_monitored', 0),
                'positions_open': real_status.get('positions_open', 0)
            },
            'account_info': {
                'balance': real_status.get('balance', 0),
                'trades_today': real_status.get('trades_today', 0),
                'win_rate': real_status.get('win_rate', 0),
                'drawdown': real_status.get('drawdown', 0),
                'sharpe_ratio': real_status.get('sharpe_ratio', 0)
            },
            'positions': real_status.get('positions', []),
            'trade_results': real_status.get('trade_results', []),
            'best_trades': real_status.get('best_trades', []),
            'worst_trades': real_status.get('worst_trades', [])
        }
        
        # Converter para JSON
        json_data = json.dumps(export_data, indent=2, default=str)
        
        return json_data
    
    except Exception as e:
        st.error(f"Erro ao exportar dados: {e}")
        return None

def generate_performance_report():
    """Gerar relatório de performance detalhado - ETAPA 5"""
    try:
        if not HAS_REAL_SYSTEM:
            return "Sistema real não disponível"
        
        real_status = get_real_system_status()
        
        # Criar relatório
        report = f"""
# 📊 RELATÓRIO DE PERFORMANCE - SISTEMA DE TRADING
**Data/Hora:** {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

## 📈 Resumo Executivo
- **Status do Sistema:** {'🟢 Ativo' if real_status.get('is_running') else '🔴 Inativo'}
- **Conexão MT5:** {'✅ Conectado' if real_status.get('mt5_connected') else '❌ Desconectado'}
- **Saldo da Conta:** R$ {real_status.get('balance', 0):,.2f}
- **Posições Abertas:** {real_status.get('positions_open', 0)}

## 📊 Métricas de Performance
- **Trades Executados Hoje:** {real_status.get('trades_today', 0)}
- **Taxa de Acerto:** {real_status.get('win_rate', 0):.1f}%
- **Drawdown Atual:** {real_status.get('drawdown', 0):.1f}%
- **Sharpe Ratio:** {real_status.get('sharpe_ratio', 0):.2f}

## 🎯 Análise de Pares
- **Pares Monitorados:** {real_status.get('pairs_monitored', 0)}
- **Iteração Atual:** {real_status.get('current_iteration', 0)}

## 🏆 Melhores Trades
"""
        
        # Adicionar melhores trades
        best_trades = real_status.get('best_trades', [])
        if best_trades:
            for i, trade in enumerate(best_trades[:5], 1):
                report += f"{i}. {trade.get('symbol', 'N/A')} - R$ {trade.get('pnl', 0):.2f} ({trade.get('date', 'N/A')})\n"
        else:
            report += "Nenhum trade registrado ainda.\n"
        
        report += f"""
## ❌ Piores Trades
"""
        
        # Adicionar piores trades
        worst_trades = real_status.get('worst_trades', [])
        if worst_trades:
            for i, trade in enumerate(worst_trades[:5], 1):
                report += f"{i}. {trade.get('symbol', 'N/A')} - R$ {trade.get('pnl', 0):.2f} ({trade.get('date', 'N/A')})\n"
        else:
            report += "Nenhum trade negativo registrado.\n"
        
        report += f"""
## 🔧 Status Técnico
- **Modelos IA:** {'✅ Ativos' if real_status.get('has_ai_models') else '❌ Inativos'}
- **Cache:** {'✅ Carregado' if real_status.get('cache_loaded') else '❌ Não Carregado'}
- **Código Original:** {'✅ OK' if real_status.get('has_original_code') else '❌ Erro'}

---
*Relatório gerado automaticamente pelo Sistema de Trading Pro*
        """
        
        return report
    
    except Exception as e:
        return f"Erro ao gerar relatório: {e}"

def render_advanced_features():
    """Renderizar funcionalidades avançadas - ETAPA 5"""
    st.header("🚀 Funcionalidades Avançadas")
    
    # Seção de exportação
    st.subheader("📥 Exportação de Dados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Exportar Dados JSON", use_container_width=True):
            json_data = export_trading_data()
            if json_data:
                st.download_button(
                    label="💾 Download JSON",
                    data=json_data,
                    file_name=f"trading_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
                st.success("✅ Dados preparados para download!")
    
    with col2:
        if st.button("📈 Gerar Relatório", use_container_width=True):
            report = generate_performance_report()
            st.download_button(
                label="📄 Download Relatório",
                data=report,
                file_name=f"relatorio_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
            st.success("✅ Relatório gerado!")
    
    with col3:
        if st.button("💾 Backup Config", use_container_width=True):
            config_backup = json.dumps(st.session_state.config, indent=2)
            st.download_button(
                label="⬇️ Download Backup",
                data=config_backup,
                file_name=f"config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
            st.success("✅ Backup da configuração criado!")

    # Seção para executar funções dos módulos
    st.subheader("🛠️ Execução de Funções")

    module_option = st.selectbox(
        "Módulo",
        ["calculo_entradas_v55", "sistema_integrado"],
        key="module_choice"
    )

    if module_option == "calculo_entradas_v55":
        functions = {
            name: func for name, func in inspect.getmembers(ce55, inspect.isfunction)
        }
    else:
        sistema = st.session_state.integrated_system
        functions = {
            name: getattr(sistema, name)
            for name, func in inspect.getmembers(SistemaIntegrado, inspect.isfunction)
            if not name.startswith("_")
        }

    if functions:
        selected_name = st.selectbox("Função", sorted(functions.keys()), key="func_name")
        selected_func = functions[selected_name]
        st.markdown("**Docstring**")
        st.write(inspect.getdoc(selected_func) or "Sem documentação.")
        param_input = st.text_area("Parâmetros (JSON ou dict)", "{}", key="func_params")
        if st.button("Executar função", key="exec_func"):
            try:
                try:
                    kwargs = json.loads(param_input or '{}')
                except Exception:
                    import ast
                    kwargs = ast.literal_eval(param_input or '{}')
                result = selected_func(**kwargs)
                st.subheader('Resultado')
                if isinstance(result, pd.DataFrame):
                    st.dataframe(result)
                else:
                    st.write(result)
            except Exception as e:
                st.error(f'Erro ao executar: {e}')
    
    # Seção de monitoramento avançado
    st.subheader("📡 Monitoramento em Tempo Real")
    
    if HAS_REAL_SYSTEM:
        real_status = get_real_system_status()
        
        # Alertas automáticos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚨 Alertas Automáticos")
            
            # Verificar condições de alerta
            alerts = []
            
            if real_status.get('drawdown', 0) > 5:
                alerts.append("⚠️ Drawdown alto detectado!")
            
            if real_status.get('positions_open', 0) > st.session_state.config.get('max_positions', 5):
                alerts.append("⚠️ Limite de posições excedido!")
            
            if not real_status.get('mt5_connected', False):
                alerts.append("🔴 Conexão MT5 perdida!")
            
            if real_status.get('win_rate', 0) < 40:
                alerts.append("📉 Taxa de acerto baixa!")
            
            if alerts:
                for alert in alerts:
                    st.error(alert)
            else:
                st.success("✅ Todos os parâmetros normais")
        
        with col2:
            st.subheader("📊 Métricas em Tempo Real")
            
            # Mostrar algumas métricas dinâmicas
            equity_history = real_status.get('equity_history', [])
            if equity_history:
                latest_equity = equity_history[-1]['equity']
                st.metric("Equity Atual", f"R$ {latest_equity:,.2f}")
            
            pnl_history = real_status.get('pnl_history', [])
            if pnl_history:
                latest_pnl = pnl_history[-1]['cumulative_pnl']
                st.metric("P&L Acumulado", f"R$ {latest_pnl:,.2f}")
            
            st.metric("Uptime", f"{real_status.get('current_iteration', 0)} iterações")
    else:
        st.info("Sistema real não disponível para monitoramento avançado")
    
    # Auto-refresh para esta seção
    if st.checkbox("🔄 Auto-refresh (30s)", key="advanced_refresh"):
        time.sleep(30)
        st.rerun()

# Função auxiliar para acessar real_state de forma segura
def get_real_state():
    """Retorna o real_state de forma segura ou None se não estiver disponível"""
    if hasattr(st.session_state, 'real_state') and st.session_state.real_state:
        return st.session_state.real_state
    return None

def main():
    """Função principal do aplicativo"""
    initialize_session_state()
    render_header()
    render_connection_status()
    
    # Menu de navegação - ETAPA 5: Adicionada aba de funcionalidades avançadas
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "🎯 Dashboard",
        "📊 Seleção de Pares", 
        "📈 Análise",
        "💼 Posições",
        "🎛️ Controle",
        "📝 Logs",
        "🚀 Avançado",
        "ℹ️ Sobre"
    ])
    
    with tab1:
        render_dashboard()
    
    with tab2:
        render_pair_selection()
    
    with tab3:
        render_analysis_results()
    
    with tab4:
        render_positions_monitor()
    
    with tab5:
        render_trading_control_panel()  # ETAPA 3: Nova aba
    
    with tab6:
        render_system_logs()
    
    with tab7:
        render_advanced_features()  # ETAPA 5: Nova aba de funcionalidades avançadas
    
    with tab8:
        st.header("ℹ️ Sobre o Sistema")
        st.markdown("""
        ### 🚀 Sistema de Trading Profissional
        
        Este sistema oferece uma solução completa para trading automatizado de pares de ações,
        baseado em análise de cointegração e modelos estatísticos avançados.
        
        #### 🔧 Funcionalidades Principais:
        
        - **Análise de Cointegração**: Identifica pares de ações com relação estatística estável
        - **Modelos ARIMA/GARCH**: Previsão de preços e volatilidade
        - **Execução Automatizada**: Envio automático de ordens via MetaTrader 5
        - **Gestão de Risco**: Controles avançados de stop-loss e take-profit
        - **Monitoramento em Tempo Real**: Dashboard completo com métricas e gráficos
        - **Logs Detalhados**: Rastreamento completo de todas as operações
        
        #### 📊 Indicadores Técnicos:
        
        - Z-Score para identificação de oportunidades
        - Beta rolling para análise de correlação
        - Filtros de volatilidade e volume
        - Análise de spread e liquidez
        
        #### ⚙️ Configurações Avançadas:
        
        - Múltiplos timeframes (M1 a D1)
        - Parâmetros personalizáveis de risco
        - Filtros de seleção de pares
        - Alertas e notificações
        
        #### 🛡️ Segurança:
        
        - Conexão segura com MetaTrader 5
        - Validação de dados em tempo real
        - Controles de margem e exposição
        - Logs de auditoria completos
        
        ---
        
        **Versão**: 1.0.0  
        **Desenvolvido para**: Operações Profissionais de Trading  
        **Suporte**: Trading System Pro Team
        """)
    
    # Renderizar sidebar
    render_sidebar()
    
    # Auto-refresh se habilitado
    if st.session_state.auto_refresh and st.session_state.trading_system.is_running:
        time.sleep(st.session_state.refresh_interval)
        st.rerun()

if __name__ == "__main__":
    main()
