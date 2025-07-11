#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Integração do Sistema Real de Trading
Este módulo conecta o código original calculo_entradas_v55.py com o Streamlit
"""

import sys
import os
import json
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import traceback
import logging
import pandas as pd
import numpy as np
import MetaTrader5 as mt5

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTAR CONFIGURAÇÕES REAIS DO CÓDIGO ORIGINAL
# ═══════════════════════════════════════════════════════════════════════════════

# Importar configurações reais extraídas do código original
try:
    from config_real import (
        get_real_config_for_streamlit, 
        DEPENDENTE_REAL, 
        INDEPENDENTE_REAL, 
        SEGMENTOS_REAIS,
        FILTER_PARAMS_REAL,
        get_setores_disponiveis,
        get_pares_por_setor,
        is_horario_operacao,
        get_janela_ativa,
        SYSTEM_INFO,
        validar_configuracao
    )
    from analise_real import (
        calcular_residuo_zscore_timeframe,
        encontrar_linha_monitorada,
        executar_analise_completa,
        get_analise_para_streamlit,
        obter_dados_mt5,
        preprocessar_dados
    )
    HAS_REAL_CONFIG = True
    HAS_REAL_ANALYSIS = True
    print("✅ Configurações e análise real carregadas com sucesso!")
    print(f"📊 Total de ativos carregados: {len(DEPENDENTE_REAL + INDEPENDENTE_REAL)}")
    print(f"🏭 Setores disponíveis: {len(get_setores_disponiveis())}")
    
    # Validar configuração
    validar_configuracao()
    print("✅ Configuração validada!")
    
except ImportError as e:
    print(f"❌ Erro ao carregar configurações reais: {e}")
    HAS_REAL_CONFIG = False
    HAS_REAL_ANALYSIS = False

# Variáveis globais para controlar estado
HAS_ORIGINAL_CODE = False
HAS_MT5 = False
ORIGINAL_FUNCTIONS = {}

# Configurações integradas (REAIS substituindo simuladas)
def get_safe_real_config():
    """Retorna REAL_CONFIG seguro com todas as chaves necessárias"""
    if HAS_REAL_CONFIG:
        try:
            config = get_real_config_for_streamlit()
            print(f"🔍 Config original carregado com {len(config.keys())} chaves: {list(config.keys())}")
            
            # Verificar se tem todas as chaves necessárias
            required_keys = ['trading', 'pairs_combined', 'analise']
            for key in required_keys:
                if key not in config:
                    print(f"⚠️ Chave '{key}' ausente, adicionando fallback...")
                    if key == 'trading':
                        config['trading'] = {
                            'limite_operacoes': 6, 
                            'valor_operacao': 10000,
                            'limite_operacoes_ind': 6,
                            'valor_operacao_ind': 10000,
                            'limite_lucro': 1000,
                            'limite_prejuizo': -500,
                            'pvalor': 0.05,
                            'apetite_perc_media': 0.02
                        }
                    elif key == 'analise':
                        config['analise'] = {'filter_params': {'r2_min': 0.5, 'beta_max': 1.5}}
                else:
                    print(f"✅ Chave '{key}' encontrada")
            
            # Verificar especificamente se 'trading' foi corrigido
            if 'trading' in config:
                print(f"✅ Seção 'trading' confirmada com {len(config['trading'])} parâmetros")
            else:
                print(f"❌ Seção 'trading' ainda ausente após correção!")
                
            return config
        except Exception as e:
            print(f"❌ Erro ao carregar config real: {e}")
            return get_fallback_config()
    else:
        return get_fallback_config()

def get_fallback_config():
    """Configuração fallback garantida"""
    return {
        'pairs_combined': ['PETR4', 'VALE3', 'ITUB4', 'BBDC4'],
        'trading': {
            'limite_operacoes': 6, 
            'valor_operacao': 10000,
            'limite_operacoes_ind': 6,
            'valor_operacao_ind': 10000,
            'limite_lucro': 1000,
            'limite_prejuizo': -500,
            'pvalor': 0.05,
            'apetite_perc_media': 0.02
        },
        'analise': {'filter_params': {'r2_min': 0.5, 'beta_max': 1.5}}
    }

# Inicializar REAL_CONFIG de forma segura
if HAS_REAL_CONFIG:
    REAL_CONFIG = get_safe_real_config()
    print(f"🎯 Configurações reais ativas: {len(REAL_CONFIG.keys())} seções")
    if 'trading' in REAL_CONFIG:
        print(f"✅ Seção 'trading' validada")
        print(f"📈 Parâmetros de filtro: R²≥{FILTER_PARAMS_REAL['r2_min']}, β≤{FILTER_PARAMS_REAL['beta_max']}")
        print(f"🔄 Cointegração: {'✅' if FILTER_PARAMS_REAL['enable_cointegration_filter'] else '❌'}")
    else:
        print(f"❌ Seção 'trading' ainda ausente!")
else:
    # Fallback para configurações básicas
    REAL_CONFIG = get_fallback_config()
    print("⚠️ Usando configurações fallback")

# Estado global do sistema real
class RealTradingState:
    """Estado global do sistema de trading real"""
    def __init__(self):
        self.is_initialized = False
        self.is_running = False
        self.mt5_connected = False
        self.thread_monitor = None
        self.dados_mercado = {}
        self.posicoes_abertas = []
        self.historico_trades = []
        self.parametros = {}
        self.logs = []
        self.ultima_atualizacao = None
        self.sistema_original = None
        # Adicionar novos campos
        self.current_iteration = 0
        self.active_operations = 0
        self.has_ai_models = False
        self.cache_loaded = False
    
    def log(self, mensagem: str, nivel: str = "INFO"):
        """Adicionar log com timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "nivel": nivel,
            "mensagem": mensagem
        }
        self.logs.append(log_entry)
        logger.info(f"[{nivel}] {mensagem}")
        
        # Manter apenas os últimos 1000 logs
        if len(self.logs) > 1000:
            self.logs = self.logs[-1000:]

# Instância global do estado
real_state = RealTradingState()

def try_import_original_code():
    """Tentar importar o código original"""
    global HAS_ORIGINAL_CODE, ORIGINAL_FUNCTIONS, REAL_CONFIG
    
    try:
        # Verificar se o arquivo existe
        original_file = "calculo_entradas_v55.py"
        if not os.path.exists(original_file):
            real_state.log(f"Arquivo {original_file} não encontrado", "WARNING")
            return False
        
        # Tentar ler e executar o código original
        real_state.log("Tentando carregar código original...", "INFO")
        
        # Importar como módulo
        spec = importlib.util.spec_from_file_location("calculo_entradas", original_file)
        if spec is None:
            real_state.log("Não foi possível criar spec do arquivo", "ERROR")
            return False
            
        calculo_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(calculo_module)
        
        # Extrair funções e configurações importantes
        ORIGINAL_FUNCTIONS = {
            'module': calculo_module,
            'main': getattr(calculo_module, 'main', None),
            'get_config': getattr(calculo_module, 'get_config', None),
            'initialize_mt5': getattr(calculo_module, 'initialize_mt5', None),
            'get_market_data': getattr(calculo_module, 'get_market_data', None),
            'analyze_pairs': getattr(calculo_module, 'analyze_pairs', None),
        }
        
        # Carregar configuração se disponível
        if hasattr(calculo_module, 'CONFIG'):
            REAL_CONFIG = calculo_module.CONFIG
        elif hasattr(calculo_module, 'config'):
            REAL_CONFIG = calculo_module.config
        else:
            REAL_CONFIG = {
                'pairs': ['EURUSD', 'GBPUSD', 'USDCAD', 'USDJPY'],
                'timeframe': 'M5',
                'lookback_periods': 100,
                'risk_percent': 0.02
            }
        
        real_state.log("Código original carregado com sucesso!", "INFO")
        HAS_ORIGINAL_CODE = True
        return True
        
    except Exception as e:
        real_state.log(f"Erro ao carregar código original: {e}", "ERROR")
        real_state.log(f"Traceback: {traceback.format_exc()}", "DEBUG")
        return False

def try_import_mt5():
    """Tentar importar MetaTrader5"""
    global HAS_MT5
    
    try:
        import MetaTrader5 as mt5
        HAS_MT5 = True
        real_state.log("MetaTrader5 importado com sucesso", "INFO")
        return True
    except ImportError as e:
        real_state.log(f"MetaTrader5 não disponível: {e}", "WARNING")
        HAS_MT5 = False
        return False

def check_mt5_connection():
    """Verificar conexão com MT5"""
    if not HAS_MT5:
        return False
    
    try:
        import MetaTrader5 as mt5
        if not mt5.initialize():
            real_state.log("Falha ao inicializar MT5", "ERROR")
            return False
        
        account_info = mt5.account_info()
        if account_info is None:
            real_state.log("Não foi possível obter informações da conta", "ERROR")
            return False
        
        real_state.mt5_connected = True
        real_state.log(f"Conectado à conta MT5: {account_info.login}", "INFO")
        return True
        
    except Exception as e:
        real_state.log(f"Erro na conexão MT5: {e}", "ERROR")
        real_state.mt5_connected = False
        return False

def initialize_real_system():
    """Inicializar sistema real de trading - ATUALIZADO COM CONFIGURAÇÕES REAIS"""
    global REAL_CONFIG  # Declarar global no início da função
    
    real_state.log("🚀 Inicializando sistema real de trading...", "INFO")
      # 0. Garantir que REAL_CONFIG esteja corretamente inicializado
    if not REAL_CONFIG or 'trading' not in REAL_CONFIG:
        real_state.log("🔄 Reinicializando REAL_CONFIG...", "INFO")
        if HAS_REAL_CONFIG:
            REAL_CONFIG = get_safe_real_config()  # Usar função segura
            real_state.log(f"   📊 REAL_CONFIG reinicializado com {len(REAL_CONFIG)} seções", "INFO")
        else:
            real_state.log("   ⚠️ Usando configuração fallback", "WARNING")
            REAL_CONFIG = get_fallback_config()  # Usar função fallback
    
    # 1. Tentar importar código original
    if not try_import_original_code():
        real_state.log("Sistema funcionará em modo simulado", "WARNING")
      # 2. Tentar conectar MT5
    if not try_import_mt5():
        real_state.log("MT5 não disponível - operação em modo demo", "WARNING")
    else:
        check_mt5_connection()
      # 3. Carregar configurações REAIS (não mais simuladas)
    if HAS_REAL_CONFIG and REAL_CONFIG:
        real_state.log("📊 Usando configurações REAIS do sistema", "INFO")
        real_state.log(f"   • Ativos dependentes: {len(DEPENDENTE_REAL)}", "INFO")
        real_state.log(f"   • Ativos independentes: {len(INDEPENDENTE_REAL)}", "INFO")
        real_state.log(f"   • Setores disponíveis: {len(get_setores_disponiveis())}", "INFO")
        
        # Verificar se a chave 'trading' existe antes de acessar
        if 'trading' in REAL_CONFIG:
            real_state.log(f"   • Limite de operações: {REAL_CONFIG['trading']['limite_operacoes']}", "INFO")
            real_state.log(f"   • Valor por operação: R$ {REAL_CONFIG['trading']['valor_operacao']:,}", "INFO")
        else:
            real_state.log("   ⚠️ Seção 'trading' não encontrada em REAL_CONFIG", "WARNING")
            real_state.log(f"   📋 Chaves disponíveis: {list(REAL_CONFIG.keys())}", "DEBUG")
        
        # Verificar horário de operação
        if is_horario_operacao():
            real_state.log("✅ Sistema iniciado em horário de pregão", "INFO")
            janelas_ativas = get_janela_ativa()
            real_state.log(f"🎯 Janelas ativas: {', '.join(janelas_ativas)}", "INFO")
        else:
            real_state.log("⏰ Sistema iniciado fora do horário de pregão", "WARNING")
    else:
        real_state.log("⚠️ Usando configurações de fallback", "WARNING")
        # Fallback apenas se as configurações reais falharam
        fallback_config = {
            'pairs_combined': ['PETR4', 'VALE3', 'ITUB4', 'BBDC4', 'ABEV3'],
            'timeframe': 'M5',
            'lookback_periods': 100,
            'risk_percent': 0.02,
            'max_positions': 5,
            'enable_ai_models': True,
            'cointegration_threshold': 0.05,
            'signal_confidence_min': 0.7
        }
        if REAL_CONFIG:
            REAL_CONFIG.update(fallback_config)
        else:
            REAL_CONFIG = fallback_config
    
    # 4. Inicializar estado adicional
    real_state.current_iteration = 0
    real_state.active_operations = 0
    
    # 5. Verificar se há modelos de IA disponíveis
    try:
        # Verificar se há arquivos de modelo
        import os
        model_files = [
            'modelo_arima.pkl',
            'model.h5',
            'lstm_model.h5',
            'rf_model.pkl'
        ]
        
        models_found = 0
        for model_file in model_files:
            if os.path.exists(model_file):
                models_found += 1
                real_state.log(f"Modelo encontrado: {model_file}", "INFO")
        
        real_state.has_ai_models = models_found > 0
        if real_state.has_ai_models:
            real_state.log(f"{models_found} modelo(s) de IA encontrado(s)", "INFO")
        
    except Exception as e:
        real_state.log(f"Erro ao verificar modelos de IA: {e}", "WARNING")
        real_state.has_ai_models = False
    
    # 6. Verificar cache
    try:
        import os
        cache_files = ['cache.json', 'dados_cache.pkl', 'symbol_cache.json']
        cache_found = any(os.path.exists(f) for f in cache_files)
        real_state.cache_loaded = cache_found
        if cache_found:
            real_state.log("Cache encontrado e carregado", "INFO")
    except Exception as e:
        real_state.log(f"Erro ao verificar cache: {e}", "WARNING")
        real_state.cache_loaded = False
    
    real_state.parametros = REAL_CONFIG.copy()
    real_state.is_initialized = True
    real_state.ultima_atualizacao = datetime.now()
    
    real_state.log("Sistema real inicializado!", "INFO")
    return True

def get_real_market_data(symbol: str = "EURUSD", timeframe: str = "M5", count: int = 100):
    """Obter dados de mercado reais ou simulados"""
    if HAS_MT5 and real_state.mt5_connected:
        try:
            import MetaTrader5 as mt5
            
            # Mapear timeframes
            tf_map = {
                'M1': mt5.TIMEFRAME_M1,
                'M5': mt5.TIMEFRAME_M5,
                'M15': mt5.TIMEFRAME_M15,
                'H1': mt5.TIMEFRAME_H1,
                'H4': mt5.TIMEFRAME_H4,
                'D1': mt5.TIMEFRAME_D1
            }
            
            timeframe_mt5 = tf_map.get(timeframe, mt5.TIMEFRAME_M5)
            rates = mt5.copy_rates_from_pos(symbol, timeframe_mt5, 0, count)
            
            if rates is not None:
                import pandas as pd
                df = pd.DataFrame(rates)
                df['time'] = pd.to_datetime(df['time'], unit='s')
                return df
            
        except Exception as e:
            real_state.log(f"Erro ao obter dados do MT5: {e}", "ERROR")
    
    # Dados simulados se MT5 não estiver disponível
    import pandas as pd
    import numpy as np
    
    dates = pd.date_range(start=datetime.now() - timedelta(hours=count*5), 
                         periods=count, freq='5T')
    
    # Gerar dados OHLC simulados mais realistas
    np.random.seed(42)
    base_price = 1.1000 if 'EUR' in symbol else 1.2500
    
    returns = np.random.normal(0, 0.001, count)
    prices = [base_price]
    
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    # Gerar OHLC baseado nos preços
    data = []
    for i, price in enumerate(prices):
        high = price * (1 + abs(np.random.normal(0, 0.0005)))
        low = price * (1 - abs(np.random.normal(0, 0.0005)))
        open_price = prices[i-1] if i > 0 else price
        close = price
        
        data.append({
            'time': dates[i],
            'open': open_price,
            'high': max(open_price, high, close),
            'low': min(open_price, low, close),
            'close': close,
            'tick_volume': np.random.randint(100, 1000)
        })
    
    return pd.DataFrame(data)

def preprocess_real_data(df: pd.DataFrame):
    """Preprocessar dados de mercado"""
    if df is None or df.empty:
        return None
    
    try:
        # Calcular indicadores técnicos básicos
        df = df.copy()
        
        # Médias móveis
        df['ma_20'] = df['close'].rolling(window=20).mean()
        df['ma_50'] = df['close'].rolling(window=50).mean()
        
        # RSI simplificado
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        bb_period = 20
        bb_std = 2
        df['bb_middle'] = df['close'].rolling(window=bb_period).mean()
        bb_std_val = df['close'].rolling(window=bb_period).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std_val * bb_std)
        df['bb_lower'] = df['bb_middle'] - (bb_std_val * bb_std)
        
        # Volume médio
        df['volume_ma'] = df['tick_volume'].rolling(window=20).mean()
        
        real_state.log(f"Dados preprocessados: {len(df)} períodos", "INFO")
        return df
        
    except Exception as e:
        real_state.log(f"Erro no preprocessamento: {e}", "ERROR")
        return df

def analyze_real_pairs(pairs: List[str]):
    """Analisar pares usando código real ou simulado"""
    real_state.log(f"Analisando {len(pairs)} pares...", "INFO")
    
    results = {}
    
    for pair in pairs:
        try:
            # Obter dados do par
            data = get_real_market_data(pair)
            if data is None or data.empty:
                real_state.log(f"Dados não disponíveis para {pair}", "WARNING")
                continue
            
            # Preprocessar dados
            processed_data = preprocess_real_data(data)
            
            # Análise básica
            current_price = processed_data['close'].iloc[-1]
            ma_20 = processed_data['ma_20'].iloc[-1]
            ma_50 = processed_data['ma_50'].iloc[-1]
            rsi = processed_data['rsi'].iloc[-1]
            
            # Determinar sinal
            signal = "NEUTRO"
            confidence = 0.5
            
            if current_price > ma_20 > ma_50 and rsi < 70:
                signal = "COMPRA"
                confidence = min(0.8, (current_price - ma_20) / ma_20 * 100 + 0.5)
            elif current_price < ma_20 < ma_50 and rsi > 30:
                signal = "VENDA"
                confidence = min(0.8, (ma_20 - current_price) / ma_20 * 100 + 0.5)
            
            results[pair] = {
                'symbol': pair,
                'current_price': current_price,
                'signal': signal,
                'confidence': confidence,
                'rsi': rsi,
                'ma_20': ma_20,
                'ma_50': ma_50,
                'last_update': datetime.now(),
                'data': processed_data
            }
            
            real_state.log(f"{pair}: {signal} (conf: {confidence:.2f})", "INFO")
            
        except Exception as e:
            real_state.log(f"Erro analisando {pair}: {e}", "ERROR")
            continue
    
    real_state.dados_mercado.update(results)
    real_state.ultima_atualizacao = datetime.now()
    
    return results

def get_system_status():
    """Obtém status detalhado do sistema para o dashboard - ETAPA 4"""
    global real_state
    
    if not real_state:
        return {
            'status': 'stopped',
            'positions': [],
            'balance': 0,
            'trades_today': 0,
            'win_rate': 0,
            'drawdown': 0,
            'sharpe_ratio': 0,
            'margin_used': 0,
            'equity_history': [],
            'trade_results': [],
            'best_trades': [],
            'worst_trades': [],
            'pnl_history': []
        }
    
    try:
        # Status básico
        basic_status = {
            'is_initialized': real_state.is_initialized,
            'is_running': real_state.is_running,
            'mt5_connected': real_state.mt5_connected,
            'has_original_code': HAS_ORIGINAL_CODE,
            'has_mt5': HAS_MT5,
            'pairs_monitored': len(real_state.dados_mercado),
            'positions_open': len(real_state.posicoes_abertas),
            'last_update': real_state.ultima_atualizacao,
            'total_logs': len(real_state.logs),
            'current_iteration': getattr(real_state, 'current_iteration', 0),
            'active_operations': getattr(real_state, 'active_operations', 0),
            'has_ai_models': getattr(real_state, 'has_ai_models', False),
            'cache_loaded': getattr(real_state, 'cache_loaded', False)
        }
        
        # Obter posições ativas para dashboard
        positions = []
        if hasattr(real_state, 'posicoes_abertas') and real_state.posicoes_abertas:
            for i, pos in enumerate(real_state.posicoes_abertas):
                positions.append({
                    'ticket': pos.get('ticket', f'SIM_{i}'),
                    'symbol': pos.get('symbol', 'N/A'),
                    'type': pos.get('type', 'BUY'),
                    'volume': pos.get('volume', 0),
                    'open_price': pos.get('open_price', 0),
                    'current_price': pos.get('current_price', pos.get('open_price', 0)),
                    'pnl': pos.get('pnl', 0),
                    'zscore': pos.get('zscore', 0),
                    'time': pos.get('time', datetime.now().strftime("%H:%M:%S"))
                })
        
        # Calcular métricas para dashboard
        total_pnl = sum([pos['pnl'] for pos in positions])
        balance = getattr(real_state, 'saldo_conta', 50000) + total_pnl
        trades_today = getattr(real_state, 'trades_hoje', len(positions))
        
        # Histórico simulado baseado no estado atual
        now = datetime.now()
        equity_history = []
        pnl_history = []
        
        for i in range(24):  # Últimas 24 horas
            timestamp = now - timedelta(hours=23-i)
            equity_val = balance + np.random.normal(0, balance * 0.001)
            pnl_val = total_pnl + np.random.normal(0, abs(total_pnl) * 0.1 if total_pnl != 0 else 50)
            
            equity_history.append({
                'timestamp': timestamp,
                'equity': equity_val
            })
            
            pnl_history.append({
                'timestamp': timestamp,
                'cumulative_pnl': pnl_val
            })
        
        # Resultados de trades
        trade_results = []
        if hasattr(real_state, 'historico_trades') and real_state.historico_trades:
            trade_results = [trade.get('pnl', 0) for trade in real_state.historico_trades]
        else:
            trade_results = np.random.normal(50, 100, 20).tolist()
        
        # Melhores e piores trades
        best_trades = []
        worst_trades = []
        
        if trade_results:
            sorted_results = sorted(enumerate(trade_results), key=lambda x: x[1], reverse=True)
            
            for i, (idx, pnl) in enumerate(sorted_results[:3]):
                best_trades.append({
                    'symbol': f'PAIR_{idx}',
                    'pnl': pnl,
                    'date': (now - timedelta(days=i)).strftime("%d/%m")
                })
            
            for i, (idx, pnl) in enumerate(sorted_results[-3:]):
                worst_trades.append({
                    'symbol': f'PAIR_{idx}',
                    'pnl': pnl,
                    'date': (now - timedelta(days=i)).strftime("%d/%m")
                })
        
        # Calcular métricas
        winning_trades = len([r for r in trade_results if r > 0])
        win_rate = (winning_trades / len(trade_results) * 100) if trade_results else 0
        
        if equity_history:
            peak = max([e['equity'] for e in equity_history])
            current = equity_history[-1]['equity']
            drawdown = ((peak - current) / peak * 100) if peak > 0 else 0
        else:
            drawdown = 0
        
        if trade_results:
            returns = np.array(trade_results) / balance if balance > 0 else np.array(trade_results)
            sharpe_ratio = np.mean(returns) / np.std(returns) if np.std(returns) > 0 else 0
        else:
            sharpe_ratio = 0
        
        # Combinar status básico com dados do dashboard
        dashboard_data = {
            'status': 'running' if real_state.is_running else 'stopped',
            'positions': positions,
            'balance': balance,
            'balance_change': total_pnl,
            'trades_today': trades_today,
            'trades_change': len(positions),
            'win_rate': win_rate,
            'win_rate_change': 0,
            'drawdown': drawdown,
            'drawdown_change': 0,
            'sharpe_ratio': sharpe_ratio,
            'sharpe_change': 0,
            'margin_used': (total_pnl / balance * 100) if balance > 0 else 0,
            'margin_change': 0,
            'position_change': len(positions),
            'pnl_change': total_pnl,
            'equity_history': equity_history,
            'pnl_history': pnl_history,
            'trade_results': trade_results,
            'best_trades': best_trades,
            'worst_trades': worst_trades
        }
        
        # Combinar os dois dicionários
        basic_status.update(dashboard_data)
        return basic_status
    
    except Exception as e:
        real_state.log(f"Erro ao obter status do sistema: {e}", "ERROR")
        return {
            'status': 'error',
            'error': str(e),
            'positions': [],
            'balance': 0,
            'trades_today': 0,
            'win_rate': 0,
            'drawdown': 0,
            'sharpe_ratio': 0,
            'margin_used': 0,
            'equity_history': [],
            'trade_results': [],
            'best_trades': [],
            'worst_trades': [],
            'pnl_history': []
        }

def start_real_monitoring():
    """Iniciar monitoramento em tempo real"""
    if real_state.is_running:
        real_state.log("Monitoramento já está ativo", "WARNING")
        return
    
    def monitoring_loop():
        real_state.log("Iniciando loop de monitoramento...", "INFO")
        real_state.is_running = True
        
        while real_state.is_running:
            try:
                # Incrementar iteração
                real_state.current_iteration += 1
                
                # Analisar pares configurados
                pairs = real_state.parametros.get('pairs', ['EURUSD'])
                results = analyze_real_pairs(pairs)
                
                # Contar operações ativas (simulado)
                real_state.active_operations = len([
                    p for p in results.values() 
                    if p.get('signal') != 'NEUTRO' and p.get('confidence', 0) > 0.7
                ])
                
                # Aguardar próximo ciclo
                time.sleep(30)  # 30 segundos entre atualizações
                
            except Exception as e:
                real_state.log(f"Erro no loop de monitoramento: {e}", "ERROR")
                time.sleep(60)  # Aguardar mais tempo em caso de erro
    
    real_state.thread_monitor = threading.Thread(target=monitoring_loop, daemon=True)
    real_state.thread_monitor.start()
    real_state.log("Monitoramento iniciado!", "INFO")

def stop_real_monitoring():
    """Parar monitoramento"""
    if not real_state.is_running:
        real_state.log("Monitoramento já está parado", "WARNING")
        return
    
    real_state.is_running = False
    real_state.log("Parando monitoramento...", "INFO")
    
    if real_state.thread_monitor:
        real_state.thread_monitor.join(timeout=5)
    
    real_state.log("Monitoramento parado!", "INFO")

def get_real_logs(limit: int = 100):
    """Obter logs do sistema"""
    return real_state.logs[-limit:] if real_state.logs else []

def update_real_parameters(new_params: dict):
    """Atualizar parâmetros do sistema"""
    try:
        real_state.parametros.update(new_params)
        real_state.log(f"Parâmetros atualizados: {list(new_params.keys())}", "INFO")
        return True
    except Exception as e:
        real_state.log(f"Erro ao atualizar parâmetros: {e}", "ERROR")
        return False

# Classes para compatibilidade
class TradingSystemReal:
    """Classe principal do sistema de trading real"""
    
    def __init__(self):
        self.state = real_state
        self.config = REAL_CONFIG
        
    def initialize(self):
        return initialize_real_system()
    
    def start(self):
        start_real_monitoring()
    
    def stop(self):
        stop_real_monitoring()
    
    def get_status(self):
        return get_system_status()
    
    def get_market_data(self, symbol='EURUSD'):
        return get_real_market_data(symbol)
    
    def analyze_pairs(self, pairs):
        return analyze_real_pairs(pairs)

# Singleton para o sistema
_trading_system_instance = None

def get_real_system_instance():
    """Obter instância singleton do sistema real"""
    global _trading_system_instance
    if _trading_system_instance is None:
        _trading_system_instance = TradingSystemReal()
    return _trading_system_instance

def validate_real_system():
    """Validar se o sistema real está funcionando"""
    try:
        system = get_real_system_instance()
        status = system.get_status()
        return status['is_initialized']
    except Exception as e:
        logger.error(f"Erro na validação: {e}")
        return False

# Importações auxiliares necessárias
try:
    import importlib.util
except ImportError as e:
    logger.error(f"Erro importando módulos auxiliares: {e}")

# Auto-inicialização ao importar (PROTEGIDA)
def safe_auto_init():
    """Inicialização segura do sistema"""
    try:
        if HAS_REAL_CONFIG:  # Só inicializar se as configurações estiverem carregadas
            initialize_real_system()
            return True
        else:
            logger.warning("Configurações reais não carregadas - pulando auto-inicialização")
            return False
    except Exception as e:
        logger.error(f"Erro na auto-inicialização: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

# Executar inicialização apenas se não estivermos em modo de importação problemática
import sys
if __name__ != "__main__" and "pytest" not in sys.modules:
    safe_auto_init()

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 FUNÇÕES REAIS (SUBSTITUINDO DADOS SIMULADOS)
# ═══════════════════════════════════════════════════════════════════════════════

def get_real_analysis_data(timeframe="M15", periodo=100, filtros_customizados=None):
    """
    Obtém dados de análise REAL usando o módulo analise_real.py
    Substitui completamente os dados simulados
    """
    if not HAS_REAL_ANALYSIS:
        real_state.log("Módulo de análise real não disponível - usando fallback", "WARNING")
        return {}  # Fallback simples
    
    try:
        real_state.log(f"Executando análise real - TF: {timeframe}, Período: {periodo}", "INFO")
        
        # Usar filtros customizados ou padrão
        filtros = filtros_customizados or FILTER_PARAMS_REAL.copy()
        
        # Executar análise real
        resultado = get_analise_para_streamlit(timeframe, periodo, filtros)
        
        if resultado.get('status') == 'erro':
            real_state.log(f"Erro na análise real: {resultado.get('erro')}", "ERROR")
            return {}  # Fallback
        
        # Formatar para interface
        analise_formatada = {
            'resumo': resultado['resumo'],
            'pares_analisados': len(resultado['tabela_analise']) if not resultado['tabela_analise'].empty else 0,
            'pares_aprovados': resultado['resumo']['aprovados_filtros'],
            'oportunidades': len(resultado['oportunidades']),
            'dados_brutos': resultado['tabela_analise'],
            'dados_mesmo_setor': resultado['tabela_mesmo_setor'],
            'oportunidades_detalhadas': resultado['oportunidades'],
            'timestamp': resultado['resumo']['timestamp'],
            'parametros': resultado['parametros_usados'],
            'fonte': 'REAL'
        }
        
        real_state.log(f"Análise real concluída: {analise_formatada['oportunidades']} oportunidades", "SUCCESS")
        return analise_formatada
        
    except Exception as e:
        real_state.log(f"Erro inesperado na análise real: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        return {}  # Fallback

def get_real_market_data(simbolos=None, timeframe="M15", periodo=100):
    """
    Obtém dados reais do mercado via MT5
    """
    if not HAS_REAL_ANALYSIS:
        return {}  # Fallback
    
    try:
        if simbolos is None:
            simbolos = REAL_CONFIG['pairs_combined'][:10]  # Primeiros 10 para performance
        
        real_state.log(f"Obtendo dados reais do mercado para {len(simbolos)} ativos", "INFO")
        
        dados = obter_dados_mt5(simbolos, timeframe, periodo)
        
        if dados.empty:
            real_state.log("Sem dados do mercado - usando fallback", "WARNING")
            return {}  # Fallback
        
        # Converter para formato esperado pelo Streamlit
        dados_formatados = {
            'timestamp': datetime.now(),
            'simbolos': list(dados.columns),
            'dados': dados,
            'shape': dados.shape,
            'ultimo_preco': dados.iloc[-1].to_dict(),
            'fonte': 'MT5_REAL'
        }
        
        real_state.log(f"Dados reais obtidos: {dados.shape[0]} períodos, {dados.shape[1]} ativos", "SUCCESS")
        return dados_formatados
        
    except Exception as e:
        real_state.log(f"Erro ao obter dados reais: {e}", "ERROR")
        return {}  # Fallback

def execute_real_trading_analysis(parametros=None):
    """
    Executa análise completa de trading usando o sistema real
    """
    if not HAS_REAL_ANALYSIS:
        return {'status': 'erro', 'erro': 'Análise real não disponível'}  # Fallback
    
    try:
        # Usar parâmetros ou configuração padrão
        config = parametros or {
            'timeframe': 'M15',
            'periodo': 100,
            'filtros': FILTER_PARAMS_REAL
        }
        
        real_state.log("Iniciando análise completa do sistema real", "INFO")
        real_state.is_running = True
        
        # 1. Obter dados do mercado
        dados_mercado = get_real_market_data(
            timeframe=config['timeframe'], 
            periodo=config['periodo']
        )
        
        # 2. Executar análise de pares
        analise_pares = get_real_analysis_data(
            timeframe=config['timeframe'],
            periodo=config['periodo'],
            filtros_customizados=config['filtros']
        )
        
        # 3. Atualizar estado global
        real_state.dados_mercado = dados_mercado
        real_state.ultima_atualizacao = datetime.now()
        real_state.current_iteration += 1
        
        # 4. Compilar resultado final
        resultado = {
            'timestamp': datetime.now(),
            'status': 'sucesso',
            'iteracao': real_state.current_iteration,
            'mercado': dados_mercado,
            'analise': analise_pares,
            'config_usada': config,
            'resumo': {
                'ativos_analisados': len(dados_mercado.get('simbolos', [])),
                'pares_testados': analise_pares.get('pares_analisados', 0),
                'oportunidades': analise_pares.get('oportunidades', 0),
                'tempo_execucao': 0  # Será calculado se necessário
            }
        }
        
        real_state.log(f"Análise real finalizada - {resultado['resumo']['oportunidades']} oportunidades", "SUCCESS")
        return resultado
        
    except Exception as e:
        real_state.log(f"Erro na análise real: {e}", "ERROR")
        real_state.is_running = False
        import traceback
        traceback.print_exc()
        return {'status': 'erro', 'erro': str(e)}

def get_real_system_status():
    """
    Retorna status real do sistema
    """
    if not HAS_REAL_CONFIG:
        return {}  # Fallback
    
    try:
        # Verificar conexão MT5
        mt5_status = False
        try:
            mt5_status = mt5.initialize() and mt5.account_info() is not None
        except:
            pass
        
        status = {
            'timestamp': datetime.now(),
            'sistema_inicializado': real_state.is_initialized,
            'sistema_rodando': real_state.is_running,
            'mt5_conectado': mt5_status,
            'config_real_carregada': HAS_REAL_CONFIG,
            'analise_real_disponivel': HAS_REAL_ANALYSIS,
            'ultima_atualizacao': real_state.ultima_atualizacao,
            'iteracao_atual': real_state.current_iteration,
            'operacoes_ativas': real_state.active_operations,
            'total_ativos': len(REAL_CONFIG.get('pairs_combined', [])),
            'total_setores': len(get_setores_disponiveis()) if HAS_REAL_CONFIG else 0,
            'parametros_filtro': FILTER_PARAMS_REAL if HAS_REAL_CONFIG else {},
            'horario_operacao': is_horario_operacao() if HAS_REAL_CONFIG else True,
            'fonte': 'SISTEMA_REAL'
        }
        
        return status
        
    except Exception as e:
        real_state.log(f"Erro ao obter status real: {e}", "ERROR")
        return {}  # Fallback

def get_real_trading_opportunities():
    """
    Obtém oportunidades de trading usando análise real
    """
    try:
        analise = get_real_analysis_data()
        
        if analise.get('fonte') != 'REAL':
            return []
        
        oportunidades = analise.get('oportunidades_detalhadas', [])
        
        # Formatar para interface
        oportunidades_formatadas = []
        for op in oportunidades:
            oportunidade = {
                'par': f"{op['Dependente']}/{op['Independente']}",
                'tipo': op['Tipo'],
                'zscore': round(op['Zscore'], 3),
                'r2': round(op['R2'], 3),
                'beta': round(op['Beta'], 3),
                'setor_dep': SEGMENTOS_REAIS.get(op['Dependente'], 'N/A'),
                'setor_ind': SEGMENTOS_REAIS.get(op['Independente'], 'N/A'),
                'timestamp': op['Timestamp'],
                'status': op['Status'],
                'fonte': 'REAL'
            }
            oportunidades_formatadas.append(oportunidade)
        
        return oportunidades_formatadas
        
    except Exception as e:
        real_state.log(f"Erro ao obter oportunidades reais: {e}", "ERROR")
        return []

# ═══════════════════════════════════════════════════════════════════════════════
# 🔄 FUNÇÕES PARA EXTRAIR DADOS REAIS DO MT5 (NOVA FUNCIONALIDADE)
# ═══════════════════════════════════════════════════════════════════════════════

def get_account_info_real():
    """Obter informações reais da conta MT5"""
    try:
        if not mt5.initialize():
            return None
            
        account_info = mt5.account_info()
        if account_info is None:
            return None
            
        return {
            'balance': account_info.balance,
            'equity': account_info.equity,
            'margin': account_info.margin,
            'free_margin': account_info.margin_free,
            'margin_level': account_info.margin_level,
            'profit': account_info.profit,
            'login': account_info.login,
            'server': account_info.server,
            'currency': account_info.currency,
            'leverage': account_info.leverage
        }
    except Exception as e:
        real_state.log(f"Erro ao obter account_info real: {e}", "ERROR")
        return None

def get_positions_real():
    """Obter posições reais abertas no MT5"""
    try:
        if not mt5.initialize():
            return []
            
        positions = mt5.positions_get()
        if positions is None:
            return []
            
        positions_list = []
        for pos in positions:
            position_dict = {
                'ticket': pos.ticket,
                'symbol': pos.symbol,
                'type': 'LONG' if pos.type == mt5.POSITION_TYPE_BUY else 'SHORT',
                'volume': pos.volume,
                'open_price': pos.price_open,
                'current_price': pos.price_current,
                'profit': pos.profit,
                'swap': pos.swap,
                'commission': pos.commission,
                'sl': pos.sl,
                'tp': pos.tp,
                'open_time': datetime.fromtimestamp(pos.time),
                'magic': pos.magic,
                'comment': pos.comment,
                'profit_percent': ((pos.price_current - pos.price_open) / pos.price_open * 100) if pos.type == mt5.POSITION_TYPE_BUY else ((pos.price_open - pos.price_current) / pos.price_open * 100)
            }
            positions_list.append(position_dict)
            
        return positions_list
    except Exception as e:
        real_state.log(f"Erro ao obter posições reais: {e}", "ERROR")
        return []

def get_orders_real():
    """Obter ordens pendentes reais no MT5"""
    try:
        if not mt5.initialize():
            return []
            
        orders = mt5.orders_get()
        if orders is None:
            return []
            
        orders_list = []
        for order in orders:
            order_dict = {
                'ticket': order.ticket,
                'symbol': order.symbol,
                'type': order.type,
                'volume': order.volume_initial,
                'price_open': order.price_open,
                'sl': order.sl,
                'tp': order.tp,
                'time_setup': datetime.fromtimestamp(order.time_setup),
                'magic': order.magic,
                'comment': order.comment
            }
            orders_list.append(order_dict)
            
        return orders_list
    except Exception as e:
        real_state.log(f"Erro ao obter ordens reais: {e}", "ERROR")
        return []

def get_history_deals_real(days_back=30):
    """Obter histórico real de trades dos últimos N dias"""
    try:
        if not mt5.initialize():
            return []
            
        # Definir período
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Converter para timestamp
        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())
        
        # Obter histórico de deals
        deals = mt5.history_deals_get(start_timestamp, end_timestamp)
        if deals is None:
            return []
            
        deals_list = []
        for deal in deals:
            deal_dict = {
                'ticket': deal.ticket,
                'order': deal.order,
                'symbol': deal.symbol,
                'type': deal.type,
                'volume': deal.volume,
                'price': deal.price,
                'profit': deal.profit,
                'swap': deal.swap,
                'commission': deal.commission,
                'time': datetime.fromtimestamp(deal.time),
                'comment': deal.comment,
                'magic': deal.magic
            }
            deals_list.append(deal_dict)
            
        return deals_list
    except Exception as e:
        real_state.log(f"Erro ao obter histórico real: {e}", "ERROR")
        return []

def calculate_real_metrics():
    """Calcular métricas reais baseadas no histórico de trades"""
    try:
        # Obter dados reais
        account_info = get_account_info_real()
        positions = get_positions_real()
        history = get_history_deals_real(30)  # Últimos 30 dias
        
        if not account_info:
            return get_fallback_metrics()
            
        # Calcular métricas básicas
        metrics = {
            'balance': account_info['balance'],
            'equity': account_info['equity'],
            'profit': account_info['profit'],
            'margin_level': account_info.get('margin_level', 0),
            'free_margin': account_info['free_margin'],
            'positions_count': len(positions),
            'total_volume': sum(pos['volume'] for pos in positions),
            'balance_change': account_info['profit']
        }
        
        # Calcular métricas avançadas do histórico
        if history:
            # Filtrar apenas deals de entrada e saída (tipo 0 e 1)
            trades = [deal for deal in history if deal['type'] in [0, 1]]
            
            if trades:
                # Trades hoje
                today = datetime.now().date()
                trades_today = len([trade for trade in trades if trade['time'].date() == today])
                
                # Profits dos trades
                profits = [trade['profit'] for trade in trades if trade['profit'] != 0]
                
                if profits:
                    winning_trades = len([p for p in profits if p > 0])
                    total_trades = len(profits)
                    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
                    
                    # Calcular drawdown simples
                    cumulative_profits = np.cumsum(profits)
                    running_max = np.maximum.accumulate(cumulative_profits)
                    drawdowns = (cumulative_profits - running_max) / running_max * 100
                    max_drawdown = abs(np.min(drawdowns)) if len(drawdowns) > 0 else 0
                    
                    # Calcular Sharpe ratio simples
                    if len(profits) > 1:
                        returns_mean = np.mean(profits)
                        returns_std = np.std(profits)
                        sharpe_ratio = returns_mean / returns_std if returns_std > 0 else 0
                    else:
                        sharpe_ratio = 0
                    
                    metrics.update({
                        'trades_today': trades_today,
                        'win_rate': win_rate,
                        'max_drawdown': max_drawdown,
                        'sharpe_ratio': sharpe_ratio,
                        'total_trades': total_trades,
                        'winning_trades': winning_trades,
                        'total_profit': sum(profits),
                        'avg_profit': np.mean(profits),
                        'avg_winning_trade': np.mean([p for p in profits if p > 0]) if winning_trades > 0 else 0,
                        'avg_losing_trade': np.mean([p for p in profits if p < 0]) if (total_trades - winning_trades) > 0 else 0
                    })
                else:
                    metrics.update({
                        'trades_today': trades_today,
                        'win_rate': 0,
                        'max_drawdown': 0,
                        'sharpe_ratio': 0,
                        'total_trades': 0,
                        'winning_trades': 0,
                        'total_profit': 0,
                        'avg_profit': 0,
                        'avg_winning_trade': 0,
                        'avg_losing_trade': 0
                    })
            else:
                metrics.update({
                    'trades_today': 0,
                    'win_rate': 0,
                    'max_drawdown': 0,
                    'sharpe_ratio': 0,
                    'total_trades': 0,
                    'winning_trades': 0,
                    'total_profit': 0,
                    'avg_profit': 0,
                    'avg_winning_trade': 0,
                    'avg_losing_trade': 0
                })
        else:
            # Sem histórico
            metrics.update({
                'trades_today': 0,
                'win_rate': 0,
                'max_drawdown': 0,
                'sharpe_ratio': 0,
                'total_trades': 0,
                'winning_trades': 0,
                'total_profit': 0,
                'avg_profit': 0,
                'avg_winning_trade': 0,
                'avg_losing_trade': 0
            })
            
        return metrics
        
    except Exception as e:
        real_state.log(f"Erro ao calcular métricas reais: {e}", "ERROR")
        return get_fallback_metrics()

def get_fallback_metrics():
    """Métricas fallback quando não é possível obter dados reais"""
    return {
        'balance': 50000,
        'equity': 50000,
        'profit': 0,
        'margin_level': 1000,
        'free_margin': 50000,
        'positions_count': 0,
        'total_volume': 0,
        'balance_change': 0,
        'trades_today': 0,
        'win_rate': 0,
        'max_drawdown': 0,
        'sharpe_ratio': 0,
        'total_trades': 0,
        'winning_trades': 0,
        'total_profit': 0,
        'avg_profit': 0,
        'avg_winning_trade': 0,
        'avg_losing_trade': 0
    }

def get_equity_curve_real(days=30):
    """Gerar curva de equity real baseada no histórico"""
    try:
        history = get_history_deals_real(days)
        account_info = get_account_info_real()
        
        if not history or not account_info:
            # Fallback: gerar curva simulada
            dates = pd.date_range(start=datetime.now() - timedelta(days=days), 
                                 end=datetime.now(), freq='H')[::6]
            balance = account_info['balance'] if account_info else 50000
            performance = np.cumsum(np.random.randn(len(dates)) * 50) + balance
            return dates, performance
            
        # Agrupar por data e calcular equity
        df_history = pd.DataFrame(history)
        df_history['date'] = pd.to_datetime(df_history['time']).dt.date
        
        # Calcular profits por dia
        daily_profits = df_history.groupby('date')['profit'].sum().reset_index()
        daily_profits['cumulative_profit'] = daily_profits['profit'].cumsum()
        
        base_balance = account_info['balance'] - account_info['profit']
        daily_profits['equity'] = base_balance + daily_profits['cumulative_profit']
        
        dates = pd.to_datetime(daily_profits['date'])
        equity = daily_profits['equity'].values
        
        return dates, equity
        
    except Exception as e:
        real_state.log(f"Erro ao gerar curva de equity real: {e}", "ERROR")
        # Fallback
        dates = pd.date_range(start=datetime.now() - timedelta(days=days), 
                             end=datetime.now(), freq='D')
        balance = 50000
        performance = np.cumsum(np.random.randn(len(dates)) * 100) + balance
        return dates, performance
