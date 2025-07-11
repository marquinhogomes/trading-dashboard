"""
Trading Core - Módulo de integração com as funções do sistema original
Contém as funções principais adaptadas para uso no Streamlit
"""

import pandas as pd
import numpy as np
import MetaTrader5 as mt5
from datetime import datetime, timedelta
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Importar funções do sistema original
import sys
import os
sys.path.append('.')

try:
    # Importar funções específicas do código original
    from calculo_entradas_v55 import (
        extrair_dados, preprocessar_dados, calcular_residuo_zscore_timeframe,
        encontrar_linha_monitorada, verificar_operacao_aberta,
        calcular_quantidade, get_mt5_connection_status,
        calcular_volatilidade_garch, prever_residuo_spread
    )
    HAS_ORIGINAL_FUNCTIONS = True
except ImportError:
    HAS_ORIGINAL_FUNCTIONS = False
    st.warning("⚠️ Funções originais não encontradas. Usando versões simplificadas.")

class TradingAnalyzer:
    """Analisador principal do sistema de trading"""
    
    def __init__(self, config):
        self.config = config
        self.data_cache = {}
        self.analysis_cache = {}
        
    @st.cache_data(ttl=300)  # Cache por 5 minutos
    def get_market_data(_self, symbols, timeframe='H1', count=1000):
        """Obtém dados de mercado com cache"""
        if not get_mt5_connection_status():
            return None
            
        data = {}
        for symbol in symbols:
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
                    df.set_index('time', inplace=True)
                    data[symbol] = df
                    
            except Exception as e:
                st.error(f"Erro ao obter dados de {symbol}: {e}")
                
        return data
    
    def analyze_pairs(self, symbols, progress_bar=None):
        """Análise completa de pares"""
        results = {
            'pairs_analyzed': 0,
            'cointegrated_pairs': 0,
            'signals_found': 0,
            'pair_details': [],
            'signals': [],
            'last_update': datetime.now()
        }
        
        if not symbols or len(symbols) < 2:
            return results
        
        # Obter dados de mercado
        market_data = self.get_market_data(symbols, self.config['timeframe'])
        if not market_data:
            return results
        
        total_pairs = len(symbols) * (len(symbols) - 1) // 2
        current_pair = 0
        
        # Analisar todos os pares possíveis
        for i, symbol1 in enumerate(symbols):
            for j, symbol2 in enumerate(symbols[i+1:], i+1):
                current_pair += 1
                
                if progress_bar:
                    progress_bar.progress(current_pair / total_pairs)
                
                pair_result = self._analyze_single_pair(
                    symbol1, symbol2, market_data
                )
                
                if pair_result:
                    results['pairs_analyzed'] += 1
                    results['pair_details'].append(pair_result)
                    
                    if pair_result['is_cointegrated']:
                        results['cointegrated_pairs'] += 1
                    
                    if pair_result['has_signal']:
                        results['signals_found'] += 1
                        results['signals'].append({
                            'pair': f"{symbol1}/{symbol2}",
                            'signal_type': pair_result['signal_type'],
                            'z_score': pair_result['z_score'],
                            'confidence': pair_result['confidence'],
                            'timestamp': datetime.now()
                        })
        
        return results
    
    def _analyze_single_pair(self, symbol1, symbol2, market_data):
        """Análise de um par específico"""
        try:
            if symbol1 not in market_data or symbol2 not in market_data:
                return None
            
            df1 = market_data[symbol1]
            df2 = market_data[symbol2]
            
            # Alinhar dados por timestamp
            common_index = df1.index.intersection(df2.index)
            if len(common_index) < self.config['min_train']:
                return None
            
            df1_aligned = df1.loc[common_index]
            df2_aligned = df2.loc[common_index]
            
            # Calcular spread
            spread = df1_aligned['close'] - df2_aligned['close']
            
            # Teste de cointegração simples (ADF)
            from statsmodels.tsa.stattools import adfuller
            adf_result = adfuller(spread)
            is_cointegrated = adf_result[1] < 0.05  # p-value < 5%
            
            # Calcular Z-Score
            z_score = (spread.iloc[-1] - spread.mean()) / spread.std()
            
            # Determinar sinal
            has_signal = abs(z_score) > self.config['zscore_threshold']
            signal_type = None
            confidence = 0.0
            
            if has_signal:
                if z_score > self.config['zscore_threshold']:
                    signal_type = 'SELL'  # Spread alto, vender par
                elif z_score < -self.config['zscore_threshold']:
                    signal_type = 'BUY'   # Spread baixo, comprar par
                
                # Calcular confiança baseada no Z-Score
                confidence = min(abs(z_score) / 5.0, 0.95)
            
            return {
                'symbol1': symbol1,
                'symbol2': symbol2,
                'is_cointegrated': is_cointegrated,
                'cointegration_pvalue': adf_result[1],
                'z_score': float(z_score),
                'spread_mean': float(spread.mean()),
                'spread_std': float(spread.std()),
                'has_signal': has_signal,
                'signal_type': signal_type,
                'confidence': confidence,
                'data_points': len(common_index)
            }
            
        except Exception as e:
            st.error(f"Erro na análise do par {symbol1}/{symbol2}: {e}")
            return None
    
    def get_position_analysis(self, symbol1, symbol2, position_type, entry_price):
        """Análise de uma posição específica"""
        try:
            market_data = self.get_market_data([symbol1, symbol2])
            if not market_data or symbol1 not in market_data or symbol2 not in market_data:
                return None
            
            current_price1 = market_data[symbol1]['close'].iloc[-1]
            current_price2 = market_data[symbol2]['close'].iloc[-1]
            
            # Calcular P&L simplificado
            if position_type.upper() == 'BUY':
                pnl = (current_price1 - entry_price) * 100  # Assumindo 100 unidades
            else:
                pnl = (entry_price - current_price1) * 100
            
            # Calcular Z-Score atual
            df1 = market_data[symbol1]
            df2 = market_data[symbol2]
            spread = df1['close'] - df2['close']
            current_z_score = (spread.iloc[-1] - spread.mean()) / spread.std()
            
            return {
                'current_price1': float(current_price1),
                'current_price2': float(current_price2),
                'pnl': float(pnl),
                'current_z_score': float(current_z_score),
                'spread_current': float(spread.iloc[-1]),
                'should_close': abs(current_z_score) < 0.5  # Fechar quando Z-Score volta ao normal
            }
            
        except Exception as e:
            st.error(f"Erro na análise da posição {symbol1}/{symbol2}: {e}")
            return None

class RealTimeMonitor:
    """Monitor em tempo real"""
    
    def __init__(self):
        self.is_running = False
        self.data_buffer = {}
        
    def start_monitoring(self, symbols, callback=None):
        """Inicia monitoramento em tempo real"""
        self.is_running = True
        # Implementar lógica de monitoramento
        
    def stop_monitoring(self):
        """Para o monitoramento"""
        self.is_running = False
        
    def get_live_prices(self, symbols):
        """Obtém preços em tempo real"""
        prices = {}
        
        for symbol in symbols:
            try:
                tick = mt5.symbol_info_tick(symbol)
                if tick:
                    prices[symbol] = {
                        'bid': tick.bid,
                        'ask': tick.ask,
                        'last': tick.last,
                        'time': datetime.fromtimestamp(tick.time)
                    }
            except Exception as e:
                st.error(f"Erro ao obter preço de {symbol}: {e}")
                
        return prices

class OrderManager:
    """Gerenciador de ordens"""
    
    def __init__(self):
        self.magic_number = 123456
        
    def send_order(self, symbol, order_type, volume, price=None, sl=None, tp=None):
        """Envia uma ordem"""
        try:
            if not get_mt5_connection_status():
                return {'success': False, 'message': 'MT5 não conectado'}
            
            # Preparar requisição
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": order_type,
                "magic": self.magic_number,
                "comment": "TradingSystem_Auto",
            }
            
            if price:
                request["price"] = price
            if sl:
                request["sl"] = sl
            if tp:
                request["tp"] = tp
            
            # Enviar ordem
            result = mt5.order_send(request)
            
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                return {
                    'success': True,
                    'ticket': result.order,
                    'price': result.price,
                    'message': 'Ordem executada com sucesso'
                }
            else:
                return {
                    'success': False,
                    'retcode': result.retcode,
                    'message': f'Falha na execução: {result.comment}'
                }
                
        except Exception as e:
            return {'success': False, 'message': f'Erro: {str(e)}'}
    
    def close_position(self, ticket):
        """Fecha uma posição"""
        try:
            position = mt5.positions_get(ticket=ticket)
            if not position:
                return {'success': False, 'message': 'Posição não encontrada'}
            
            position = position[0]
            
            # Determinar tipo de fechamento
            if position.type == mt5.POSITION_TYPE_BUY:
                order_type = mt5.ORDER_TYPE_SELL
            else:
                order_type = mt5.ORDER_TYPE_BUY
            
            # Preparar requisição de fechamento
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": position.symbol,
                "volume": position.volume,
                "type": order_type,
                "position": ticket,
                "magic": self.magic_number,
                "comment": "TradingSystem_Close",
            }
            
            result = mt5.order_send(request)
            
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                return {
                    'success': True,
                    'message': 'Posição fechada com sucesso'
                }
            else:
                return {
                    'success': False,
                    'retcode': result.retcode,
                    'message': f'Falha no fechamento: {result.comment}'
                }
                
        except Exception as e:
            return {'success': False, 'message': f'Erro: {str(e)}'}
    
    def get_open_positions(self):
        """Obtém posições abertas"""
        try:
            positions = mt5.positions_get()
            if positions:
                return [
                    {
                        'ticket': pos.ticket,
                        'symbol': pos.symbol,
                        'type': 'BUY' if pos.type == mt5.POSITION_TYPE_BUY else 'SELL',
                        'volume': pos.volume,
                        'price_open': pos.price_open,
                        'price_current': pos.price_current,
                        'profit': pos.profit,
                        'time': datetime.fromtimestamp(pos.time)
                    }
                    for pos in positions
                    if pos.magic == self.magic_number
                ]
            return []
        except Exception as e:
            st.error(f"Erro ao obter posições: {e}")
            return []

class ChartGenerator:
    """Gerador de gráficos avançados"""
    
    @staticmethod
    def create_pair_analysis_chart(df1, df2, symbol1, symbol2):
        """Cria gráfico de análise de pares"""
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=[
                f'Preços: {symbol1} vs {symbol2}',
                'Spread',
                'Z-Score'
            ],
            vertical_spacing=0.08,
            row_heights=[0.4, 0.3, 0.3]
        )
        
        # Gráfico de preços
        fig.add_trace(
            go.Scatter(
                x=df1.index, y=df1['close'],
                name=symbol1,
                line=dict(color='blue')
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df2.index, y=df2['close'],
                name=symbol2,
                line=dict(color='red'),
                yaxis='y2'
            ),
            row=1, col=1
        )
        
        # Spread
        spread = df1['close'] - df2['close']
        fig.add_trace(
            go.Scatter(
                x=df1.index, y=spread,
                name='Spread',
                line=dict(color='green')
            ),
            row=2, col=1
        )
        
        # Z-Score
        z_score = (spread - spread.mean()) / spread.std()
        fig.add_trace(
            go.Scatter(
                x=df1.index, y=z_score,
                name='Z-Score',
                line=dict(color='purple')
            ),
            row=3, col=1
        )
        
        # Linhas de threshold
        fig.add_hline(y=2, line_dash="dash", line_color="red", row=3, col=1)
        fig.add_hline(y=-2, line_dash="dash", line_color="red", row=3, col=1)
        fig.add_hline(y=0, line_dash="dot", line_color="gray", row=3, col=1)
        
        fig.update_layout(
            title=f'Análise de Pares: {symbol1}/{symbol2}',
            height=800,
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def create_performance_chart(equity_data):
        """Cria gráfico de performance"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=equity_data.index,
            y=equity_data['equity'],
            mode='lines',
            name='Equity',
            line=dict(color='blue', width=2),
            fill='tonexty'
        ))
        
        fig.update_layout(
            title='Curva de Equity',
            xaxis_title='Data',
            yaxis_title='Valor da Conta',
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_drawdown_chart(equity_data):
        """Cria gráfico de drawdown"""
        # Calcular drawdown
        peak = equity_data['equity'].expanding().max()
        drawdown = (equity_data['equity'] - peak) / peak * 100
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=equity_data.index,
            y=drawdown,
            mode='lines',
            name='Drawdown',
            line=dict(color='red', width=2),
            fill='tonexty'
        ))
        
        fig.update_layout(
            title='Drawdown',
            xaxis_title='Data',
            yaxis_title='Drawdown (%)',
            showlegend=False
        )
        
        return fig

# Funções auxiliares
def format_currency(value, currency='R$'):
    """Formata valor como moeda"""
    return f"{currency} {value:,.2f}"

def format_percentage(value):
    """Formata valor como percentagem"""
    return f"{value:.2%}"

def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    """Calcula o Sharpe Ratio"""
    excess_returns = returns - risk_free_rate/252  # Daily risk-free rate
    return excess_returns.mean() / excess_returns.std() * np.sqrt(252)

def calculate_max_drawdown(equity_curve):
    """Calcula o drawdown máximo"""
    peak = equity_curve.expanding().max()
    drawdown = (equity_curve - peak) / peak
    return drawdown.min()

def validate_symbol(symbol):
    """Valida se um símbolo existe no MetaTrader"""
    try:
        info = mt5.symbol_info(symbol)
        return info is not None
    except:
        return False

# Cache para dados de mercado
@st.cache_data(ttl=60)  # Cache por 1 minuto
def get_cached_market_data(symbols, timeframe, count):
    """Versão cacheada dos dados de mercado"""
    analyzer = TradingAnalyzer({})
    return analyzer.get_market_data(symbols, timeframe, count)
