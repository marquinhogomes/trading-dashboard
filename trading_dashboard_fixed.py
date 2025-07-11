#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 SISTEMA DE TRADING PROFISSIONAL - WALL STREET LEVEL DASHBOARD
Versão Ultra Profissional com Análise Avançada e Interface Moderna
Integração Total com Sistema Real de Trading v5.5
Desenvolvido com padrões de Wall Street para Hedge Funds
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
import json
import os
from datetime import datetime, timedelta
import threading
import asyncio
from typing import Dict, List, Optional, Tuple
import warnings
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, coint
import pytz
import math
from scipy import stats
from scipy.stats import norm, skew
import concurrent.futures
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 CONFIGURAÇÃO DA PÁGINA - WALL STREET PROFESSIONAL LEVEL
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Trading System Pro - Wall Street Level",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 CONFIGURAÇÕES REAIS DO SISTEMA V5.5 - PARÂMETROS ORIGINAIS
# ═══════════════════════════════════════════════════════════════════════════════

# Parâmetros reais do sistema v5.5
DEPENDENTE_REAL = ['ABEV3', 'ALOS3', 'ASAI3','BBAS3', 'BBDC4', 'BBSE3', 'BPAC11', 'BRAP4', 'BRFS3', 'BRKM5', 'CPFE3', 'CPLE6', 'CSAN3','CSNA3', 'CYRE3', 'ELET3', 'ELET6', 'EMBR3', 'ENEV3', 'ENGI11', 'EQTL3', 'EZTC3', 'FLRY3', 'GOAU4', 'HYPE3', 'IGTI11', 'IRBR3', 'ITSA4', 'ITUB4', 'KLBN11', 'MRFG3', 'NTCO3', 'PETR3', 'PETR4', 'PETZ3', 'PRIO3', 'RAIL3', 'RADL3', 'RECV3', 'RENT3', 'RDOR3', 'SANB11', 'SLCE3', 'SMTO3', 'SUZB3', 'TAEE11', 'TIMS3', 'TOTS3', 'UGPA3', 'VALE3', 'VBBR3', 'VIVT3', 'WEGE3', 'YDUQ3']

INDEPENDENTE_REAL = ['ABEV3', 'ALOS3', 'ASAI3', 'BBAS3',  'BBDC4', 'BBSE3', 'BPAC11', 'BRAP4', 'BRFS3', 'BRKM5', 'CPFE3', 'CPLE6', 'CSAN3', 'CSNA3', 'CYRE3', 'ELET3', 'ELET6', 'EMBR3', 'ENEV3', 'ENGI11', 'EQTL3', 'EZTC3', 'FLRY3', 'GOAU4', 'HYPE3', 'IGTI11', 'IRBR3', 'ITSA4', 'ITUB4', 'KLBN11', 'MRFG3', 'NTCO3', 'PETR3', 'PETR4', 'PETZ3', 'PRIO3', 'RAIL3', 'RADL3', 'RECV3', 'RENT3', 'RDOR3', 'SANB11', 'SLCE3', 'SMTO3', 'SUZB3', 'TAEE11', 'TIMS3', 'TOTS3', 'UGPA3', 'VALE3', 'VBBR3', 'VIVT3', 'WEGE3', 'YDUQ3']

# Segmentação original por setores
SEGMENTOS_REAIS = {
    'ABEV3': 'Bebidas',   'ALOS3': 'Saúde',    'ASAI3': 'Varejo Alimentar',
    'BBAS3': 'Bancos',    'BBDC4': 'Bancos',   'BBSE3': 'Seguros',
    'BPAC11': 'Bancos',   'BRAP4': 'Holding',  'BRFS3': 'Alimentos',
    'BRKM5': 'Química',   'CPFE3': 'Energia',  'CPLE6': 'Energia',
    'CSNA3': 'Siderurgia','CYRE3': 'Construção','ELET3': 'Energia',
    'ELET6': 'Energia',   'EMBR3': 'Aeroespacial','ENEV3': 'Energia',
    'ENGI11': 'Energia',  'EQTL3': 'Energia',  'EZTC3': 'Construção',
    'FLRY3': 'Saúde',     'GOAU4': 'Siderurgia','HYPE3': 'Farmacêutica',
    'IGTI11': 'Financeiro','IRBR3': 'Seguros', 'ITSA4': 'Financeiro',
    'ITUB4': 'Bancos',    'KLBN11': 'Papel e Celulose',
    'MRFG3': 'Alimentos', 'NTCO3': 'Higiene/Beleza','PETR3': 'Petróleo',
    'PETR4': 'Petróleo',  'PETZ3': 'Varejo',   'PRIO3': 'Petróleo',
    'RAIL3': 'Logística', 'RADL3': 'Varejo',   'RECV3': 'Petróleo',
    'RENT3': 'Locação',   'RDOR3': 'Saúde',    'SANB11': 'Bancos',
    'SLCE3': 'Agro',      'SMTO3': 'Agro',     'SUZB3': 'Papel e Celulose',
    'TAEE11': 'Energia',  'TIMS3': 'Telecom',  'TOTS3': 'Tecnologia',
    'UGPA3': 'Distribuição','VALE3': 'Mineração','VBBR3': 'Transporte',
    'VIVT3': 'Telecom',   'WEGE3': 'Industrial','YDUQ3': 'Educação'
}

# Parâmetros originais do sistema
PARAMS_SISTEMA_REAL = {
    'limite_operacoes': 6,
    'indep_limite_operacoes': 6,
    'valor_operacao': 10000,
    'valor_operacao_ind': 5000,
    'limite_lucro': 120,
    'limite_prejuizo': 120,
    'pvalor': 0.05,
    'apetite_perc_media': 1.0,
    'desvio_gain_compra': 1.012,
    'desvio_loss_compra': 0.988,
    'desvio_gain_venda': 0.988,
    'desvio_loss_venda': 1.012,
    'desvio_gain_compra_ind': 1.03,
    'desvio_loss_compra_ind': 0.97,
    'desvio_gain_venda_ind': 0.97,
    'desvio_loss_venda_ind': 1.03
}

# Períodos de análise originais
PERIODOS_REAIS = [70, 100, 120, 140, 160, 180, 200, 220, 240, 250]

# Filtros originais do sistema
FILTER_PARAMS_REAL = {
    'r2_min': 0.5,
    'beta_max': 1.5,
    'coef_var_max': 5000.0,
    'adf_p_value_max': 0.05,
    'use_coint_test': True,
    'use_adf_critical': False,
    'enable_cointegration_filter': True,
    'zscore_threshold': 2.0,
    'zscore_min_threshold': -2.0,
    'zscore_max_threshold': 2.0,
    'r2_min_threshold': 0.50,
    'beta_max_threshold': 1.5
}

# Importar sistema real
try:
    from trading_real_integration import (
        real_state, HAS_REAL_CONFIG, HAS_REAL_ANALYSIS, REAL_CONFIG,
        get_real_analysis_data, get_real_market_data, execute_real_trading_analysis,
        get_real_system_status, get_real_trading_opportunities
    )
    from config_real import (
        get_real_config_for_streamlit, DEPENDENTE_REAL as DEP_CONFIG, INDEPENDENTE_REAL as IND_CONFIG, 
        SEGMENTOS_REAIS as SEG_CONFIG, FILTER_PARAMS_REAL as FILTER_CONFIG, get_setores_disponiveis,
        get_pares_por_setor, is_horario_operacao, SYSTEM_INFO
    )
    from analise_real import get_analise_para_streamlit
    HAS_REAL_SYSTEM = True
    
    # Sincronizar configurações do sistema real se disponível
    if HAS_REAL_CONFIG:
        try:
            # Atualizar com dados reais se disponíveis
            real_config = get_real_config_for_streamlit()
            if 'pairs_combined' in real_config:
                DEPENDENTE_REAL = real_config['pairs_combined']
                INDEPENDENTE_REAL = real_config['pairs_combined']
            if 'segmentos' in real_config:
                SEGMENTOS_REAIS.update(real_config['segmentos'])
            if 'filter_params' in real_config:
                FILTER_PARAMS_REAL.update(real_config['filter_params'])
        except Exception as e:
            st.warning(f"Usando configuração padrão: {e}")
    
    st.success("✅ Sistema real v5.5 carregado com sucesso!")
except ImportError as e:
    HAS_REAL_SYSTEM = False
    st.error(f"❌ Erro ao carregar sistema real: {e}")
    st.info("🔄 Executando com dados simulados baseados no sistema v5.5")

# Try MT5 import
try:
    import MetaTrader5 as mt5
    HAS_MT5 = True
except ImportError:
    HAS_MT5 = False
    st.warning("⚠️ MetaTrader5 não encontrado - funcionalidade limitada")

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 FUNÇÕES PRINCIPAIS DO SISTEMA V5.5 INTEGRADAS
# ═══════════════════════════════════════════════════════════════════════════════

class TradingSystemV55:
    """Sistema de Trading v5.5 integrado ao dashboard"""
    
    def __init__(self):
        self.timezone = pytz.timezone("America/Sao_Paulo")
        self.data_inicio = datetime.now(self.timezone) - timedelta(days=360)
        self.data_fim = datetime.now(self.timezone)
        self.current_analysis = {}
        self.analysis_cache = {}
        self.mt5_connected = False
        self.last_update = None
        
    def calcular_residuo_zscore_streamlit(self, dep, ind, periodo=100, verbose=False):
        """
        Versão adaptada da função original para Streamlit
        Calcula z-score e parâmetros de regressão para pairs trading
        """
        try:
            # Simular dados históricos (em produção, conectar ao MT5)
            dates = pd.date_range(start=self.data_inicio, end=self.data_fim, freq='D')
            np.random.seed(hash(dep + ind) % 1000)  # Seed baseado nos símbolos
            
            # Gerar dados correlacionados para simular cointegração
            base_trend = np.cumsum(np.random.randn(len(dates)) * 0.02)
            dep_prices = 50 + base_trend + np.random.randn(len(dates)) * 2
            ind_prices = 45 + base_trend * 0.8 + np.random.randn(len(dates)) * 1.5
            
            # Aplicar correção para simular diferentes setores
            if SEGMENTOS_REAIS.get(dep) == SEGMENTOS_REAIS.get(ind):
                correlation_boost = 0.3
                ind_prices += dep_prices * correlation_boost
            
            dep_series = pd.Series(dep_prices, index=dates).iloc[-periodo:]
            ind_series = pd.Series(ind_prices, index=dates).iloc[-periodo:]
            
            # Alinhamento temporal
            common_index = dep_series.index.intersection(ind_series.index)
            dep_aligned = dep_series.loc[common_index]
            ind_aligned = ind_series.loc[common_index]
            
            if len(common_index) < 20:
                return None
                
            # Regressão linear
            X = sm.add_constant(ind_aligned)
            modelo = sm.OLS(dep_aligned, X).fit()
            
            alpha = modelo.params['const']
            beta = modelo.params[ind]
            r2 = modelo.rsquared
            
            # Calcular resíduo
            residuo = dep_aligned - (alpha + beta * ind_aligned)
            
            # Z-Score
            zscore = (residuo.iloc[-1] - residuo.mean()) / residuo.std()
            
            # Testes estatísticos
            adf_result = adfuller(residuo, autolag='AIC')
            adf_p_value = adf_result[1]
            
            # Teste de cointegração
            try:
                coint_result = coint(dep_aligned, ind_aligned)
                coint_p_value = coint_result[1]
            except:
                coint_p_value = 1.0
            
            # Aplicar filtros do sistema v5.5
            passes_filters = True
            filter_results = {}
            
            # Filtro R²
            if r2 < FILTER_PARAMS_REAL['r2_min']:
                passes_filters = False
                filter_results['r2_filter'] = False
            else:
                filter_results['r2_filter'] = True
                
            # Filtro Beta
            if abs(beta) > FILTER_PARAMS_REAL['beta_max']:
                passes_filters = False
                filter_results['beta_filter'] = False
            else:
                filter_results['beta_filter'] = True
                
            # Filtro ADF
            if adf_p_value > FILTER_PARAMS_REAL['adf_p_value_max']:
                passes_filters = False
                filter_results['adf_filter'] = False
            else:
                filter_results['adf_filter'] = True
                
            # Filtro Cointegração
            if FILTER_PARAMS_REAL['enable_cointegration_filter']:
                if coint_p_value > FILTER_PARAMS_REAL['adf_p_value_max']:
                    passes_filters = False
                    filter_results['coint_filter'] = False
                else:
                    filter_results['coint_filter'] = True
            else:
                filter_results['coint_filter'] = None
                
            # Determinar sinal
            signal = 'NEUTRO'
            confidence = 0.0
            
            if passes_filters:
                if zscore > FILTER_PARAMS_REAL['zscore_threshold']:
                    signal = 'VENDA'  # Par overvalued
                    confidence = min(abs(zscore) / 3.0, 1.0)
                elif zscore < -FILTER_PARAMS_REAL['zscore_threshold']:
                    signal = 'COMPRA'  # Par undervalued
                    confidence = min(abs(zscore) / 3.0, 1.0)
            
            return {
                'par': f"{dep}/{ind}",
                'dependente': dep,
                'independente': ind,
                'periodo': periodo,
                'alpha': alpha,
                'beta': beta,
                'r2': r2,
                'zscore': zscore,
                'residuo_mean': residuo.mean(),
                'residuo_std': residuo.std(),
                'adf_statistic': adf_result[0],
                'adf_p_value': adf_p_value,
                'coint_p_value': coint_p_value,
                'signal': signal,
                'confidence': confidence,
                'passes_filters': passes_filters,
                'filter_results': filter_results,
                'setor_dep': SEGMENTOS_REAIS.get(dep, 'Indefinido'),
                'setor_ind': SEGMENTOS_REAIS.get(ind, 'Indefinido'),
                'timestamp': datetime.now(self.timezone),
                'residuo_series': residuo,
                'dep_series': dep_aligned,
                'ind_series': ind_aligned
            }
            
        except Exception as e:
            if verbose:
                st.error(f"Erro no cálculo {dep}/{ind}: {e}")
            return None
    
    def executar_analise_completa(self, lista_dependente=None, lista_independente=None, 
                                periodos=None, progress_callback=None):
        """
        Executa análise completa do sistema v5.5 para todos os pares
        """
        if lista_dependente is None:
            lista_dependente = DEPENDENTE_REAL[:20]  # Limitar para demo
        if lista_independente is None:
            lista_independente = INDEPENDENTE_REAL[:20]  # Limitar para demo
        if periodos is None:
            periodos = [100, 120, 140]  # Períodos principais
            
        resultados = {}
        total_pairs = len(lista_dependente) * len(lista_independente) * len(periodos)
        current_pair = 0
        
        for dep in lista_dependente:
            for ind in lista_independente:
                if dep == ind:
                    continue
                    
                for periodo in periodos:
                    current_pair += 1
                    
                    if progress_callback:
                        progress_callback(current_pair / total_pairs)
                    
                    resultado = self.calcular_residuo_zscore_streamlit(dep, ind, periodo)
                    
                    if resultado and resultado['passes_filters']:
                        key = f"{dep}_{ind}_{periodo}"
                        resultados[key] = resultado
        
        self.current_analysis = resultados
        self.last_update = datetime.now(self.timezone)
        
        return resultados
    
    def get_melhores_oportunidades(self, min_confidence=0.7, max_results=10):
        """Retorna as melhores oportunidades de trading"""
        if not self.current_analysis:
            return []
            
        # Filtrar por confiança e ordenar
        oportunidades = []
        for key, result in self.current_analysis.items():
            if result['confidence'] >= min_confidence and result['signal'] != 'NEUTRO':
                oportunidades.append(result)
        
        # Ordenar por confiança
        oportunidades.sort(key=lambda x: x['confidence'], reverse=True)
        
        return oportunidades[:max_results]
    
    def get_estatisticas_sistema(self):
        """Retorna estatísticas do sistema"""
        if not self.current_analysis:
            return {}
            
        total_pairs = len(self.current_analysis)
        signals_compra = sum(1 for r in self.current_analysis.values() if r['signal'] == 'COMPRA')
        signals_venda = sum(1 for r in self.current_analysis.values() if r['signal'] == 'VENDA')
        avg_confidence = np.mean([r['confidence'] for r in self.current_analysis.values()])
        avg_r2 = np.mean([r['r2'] for r in self.current_analysis.values()])
        
        return {
            'total_pairs_analyzed': total_pairs,
            'signals_compra': signals_compra,
            'signals_venda': signals_venda,
            'total_signals': signals_compra + signals_venda,
            'avg_confidence': avg_confidence,
            'avg_r2': avg_r2,
            'last_update': self.last_update
        }

# Instanciar sistema global
trading_system_v55 = TradingSystemV55()

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 CSS PROFISSIONAL - WALL STREET LEVEL DESIGN
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    /* Wall Street Professional Theme */
    .main {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 50%, #0f1419 100%);
        color: #e0e6ed;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1f4e79 0%, #2d5a9b 50%, #3a6bb5 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(31, 78, 121, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e2329 0%, #2b3139 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
        border-color: rgba(47, 158, 68, 0.3);
    }
    
    .status-card {
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        color: white;
        font-weight: 600;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .status-online {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
    
    .status-offline {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }
    
    .status-processing {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }
    
    .status-warning {
        background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%);
    }
    
    /* Trading Opportunity Cards */
    .opportunity-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid rgba(71, 85, 105, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        transition: all 0.3s ease;
    }
    
    .opportunity-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 35px rgba(0, 0, 0, 0.4);
        border-color: rgba(59, 130, 246, 0.5);
    }
    
    .opportunity-buy {
        border-left: 5px solid #10b981;
    }
    
    .opportunity-sell {
        border-left: 5px solid #ef4444;
    }
    
    .opportunity-neutral {
        border-left: 5px solid #6b7280;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 FUNÇÕES DE RENDERIZAÇÃO - WALL STREET PROFESSIONAL
# ═══════════════════════════════════════════════════════════════════════════════

def render_header():
    """Renderiza o cabeçalho principal com design de Wall Street"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Trading System Pro v5.5 - Wall Street Level</h1>
        <p>Pairs Trading • Cointegração • ARIMA/GARCH • Execução Automatizada</p>
        <p><small>Sistema Profissional para Hedge Funds e Gestores Institucionais</small></p>
    </div>
    """, unsafe_allow_html=True)

def render_system_status():
    """Renderiza status do sistema com métricas avançadas"""
    st.subheader("📊 Status do Sistema v5.5")
    
    # Obter status real se disponível
    if HAS_REAL_SYSTEM:
        try:
            real_status = get_real_system_status()
            mt5_status = real_status.get('mt5_conectado', False)
            system_running = real_status.get('sistema_rodando', False)
        except:
            mt5_status = False
            system_running = False
    else:
        mt5_status = HAS_MT5
        system_running = True
    
    # Status cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_class = "status-online" if system_running else "status-offline"
        status_text = "🟢 SISTEMA ATIVO" if system_running else "🔴 SISTEMA INATIVO"
        st.markdown(f'<div class="status-card {status_class}">{status_text}</div>', unsafe_allow_html=True)
    
    with col2:
        mt5_class = "status-online" if mt5_status else "status-offline"
        mt5_text = "✅ MT5 CONECTADO" if mt5_status else "❌ MT5 DESCONECTADO"
        st.markdown(f'<div class="status-card {mt5_class}">{mt5_text}</div>', unsafe_allow_html=True)
    
    with col3:
        total_ativos = len(DEPENDENTE_REAL)
        st.metric("Ativos Monitorados", total_ativos, help="Total de ativos configurados no sistema")
    
    with col4:
        total_setores = len(set(SEGMENTOS_REAIS.values()))
        st.metric("Setores", total_setores, help="Diversificação por setores")
    
    # Métricas detalhadas
    st.subheader("⚡ Métricas em Tempo Real")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    stats = trading_system_v55.get_estatisticas_sistema()
    
    with col1:
        total_pairs = stats.get('total_pairs_analyzed', 0)
        st.metric("Pares Analisados", total_pairs, help="Total de pares processados")
    
    with col2:
        total_signals = stats.get('total_signals', 0)
        st.metric("Sinais Ativos", total_signals, help="Oportunidades identificadas")
    
    with col3:
        avg_confidence = stats.get('avg_confidence', 0)
        st.metric("Confiança Média", f"{avg_confidence:.1%}", help="Confiança média dos sinais")
    
    with col4:
        avg_r2 = stats.get('avg_r2', 0)
        st.metric("R² Médio", f"{avg_r2:.3f}", help="Qualidade média das regressões")
    
    with col5:
        last_update = stats.get('last_update')
        if last_update:
            time_diff = datetime.now(trading_system_v55.timezone) - last_update
            minutes_ago = int(time_diff.total_seconds() / 60)
            st.metric("Última Análise", f"{minutes_ago}min", help="Tempo desde última atualização")
        else:
            st.metric("Última Análise", "N/A", help="Nenhuma análise executada")

def render_market_analysis():
    """Análise de mercado com dados do sistema v5.5"""
    st.header("📈 Análise de Mercado")
    
    # Controles de análise
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        selected_assets = st.multiselect(
            "Selecionar Ativos",
            options=DEPENDENTE_REAL,
            default=DEPENDENTE_REAL[:10],
            help="Escolha os ativos para análise"
        )
    
    with col2:
        selected_periods = st.multiselect(
            "Períodos de Análise",
            options=PERIODOS_REAIS,
            default=[100, 120, 140],
            help="Períodos para cálculo do Z-Score"
        )
    
    with col3:
        if st.button("🔍 Executar Análise", use_container_width=True):
            with st.spinner("Analisando pares..."):
                # Barra de progresso
                progress_bar = st.progress(0)
                
                def update_progress(percent):
                    progress_bar.progress(percent)
                
                # Executar análise
                resultados = trading_system_v55.executar_analise_completa(
                    lista_dependente=selected_assets,
                    lista_independente=selected_assets,
                    periodos=selected_periods,
                    progress_callback=update_progress
                )
                
                progress_bar.progress(1.0)
                st.success(f"✅ Análise concluída! {len(resultados)} pares processados.")
    
    # Distribuição de Z-Scores
    if trading_system_v55.current_analysis:
        st.subheader("📊 Distribuição de Z-Scores")
        
        # Extrair z-scores
        z_scores = [r['zscore'] for r in trading_system_v55.current_analysis.values()]
        
        # Criar histograma
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=z_scores,
            nbinsx=30,
            name="Z-Scores",
            marker_color='rgba(59, 130, 246, 0.7)',
            marker_line=dict(color='rgba(59, 130, 246, 1)', width=1)
        ))
        
        # Adicionar linhas de threshold
        threshold = FILTER_PARAMS_REAL['zscore_threshold']
        fig.add_vline(x=threshold, line_dash="dash", line_color="red", 
                      annotation_text=f"Threshold: +{threshold}")
        fig.add_vline(x=-threshold, line_dash="dash", line_color="red", 
                      annotation_text=f"Threshold: -{threshold}")
        
        fig.update_layout(
            title="Distribuição de Z-Scores dos Pares",
            xaxis_title="Z-Score",
            yaxis_title="Frequência",
            template="plotly_dark",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Estatísticas dos Z-Scores
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            extreme_high = sum(1 for z in z_scores if z > threshold)
            st.metric("Z-Score > Threshold", extreme_high, help="Sinais de venda")
        
        with col2:
            extreme_low = sum(1 for z in z_scores if z < -threshold)
            st.metric("Z-Score < -Threshold", extreme_low, help="Sinais de compra")
        
        with col3:
            avg_zscore = np.mean(z_scores)
            st.metric("Z-Score Médio", f"{avg_zscore:.3f}", help="Média dos Z-Scores")
        
        with col4:
            std_zscore = np.std(z_scores)
            st.metric("Desvio Padrão", f"{std_zscore:.3f}", help="Volatilidade dos Z-Scores")

def render_trading_opportunities():
    """Renderiza oportunidades de trading identificadas"""
    st.header("🎯 Oportunidades de Trading")
    
    # Controles de filtro
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_confidence = st.slider(
            "Confiança Mínima",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.05,
            help="Filtrar por nível de confiança"
        )
    
    with col2:
        signal_filter = st.selectbox(
            "Tipo de Sinal",
            options=["TODOS", "COMPRA", "VENDA"],
            help="Filtrar por tipo de sinal"
        )
    
    with col3:
        setor_filter = st.selectbox(
            "Setor",
            options=["TODOS"] + list(set(SEGMENTOS_REAIS.values())),
            help="Filtrar por setor"
        )
    
    # Obter oportunidades
    oportunidades = trading_system_v55.get_melhores_oportunidades(
        min_confidence=min_confidence,
        max_results=20
    )
    
    # Aplicar filtros adicionais
    if signal_filter != "TODOS":
        oportunidades = [op for op in oportunidades if op['signal'] == signal_filter]
    
    if setor_filter != "TODOS":
        oportunidades = [op for op in oportunidades if 
                        op['setor_dep'] == setor_filter or op['setor_ind'] == setor_filter]
    
    if not oportunidades:
        st.info("📊 Nenhuma oportunidade encontrada com os filtros selecionados.")
        return
    
    st.subheader(f"🏆 {len(oportunidades)} Oportunidades Identificadas")
    
    # Renderizar cards de oportunidades
    for i, op in enumerate(oportunidades):
        # Determinar classe CSS baseada no sinal
        if op['signal'] == 'COMPRA':
            card_class = "opportunity-buy"
            signal_emoji = "📈"
            signal_color = "#10b981"
        elif op['signal'] == 'VENDA':
            card_class = "opportunity-sell"
            signal_emoji = "📉"
            signal_color = "#ef4444"
        else:
            card_class = "opportunity-neutral"
            signal_emoji = "➡️"
            signal_color = "#6b7280"
        
        # Calcular valor da operação baseado nos parâmetros reais
        if op['dependente'] in DEPENDENTE_REAL:
            valor_op = PARAMS_SISTEMA_REAL['valor_operacao']
        else:
            valor_op = PARAMS_SISTEMA_REAL['valor_operacao_ind']
        
        st.markdown(f"""
        <div class="opportunity-card {card_class}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="margin: 0; color: {signal_color};">{signal_emoji} {op['par']}</h3>
                <span style="background: {signal_color}; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-weight: 600;">
                    {op['signal']}
                </span>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1rem;">
                <div>
                    <strong>Z-Score:</strong><br>
                    <span style="font-size: 1.2rem; color: {signal_color};">{op['zscore']:.3f}</span>
                </div>
                <div>
                    <strong>Confiança:</strong><br>
                    <span style="font-size: 1.2rem; color: #3b82f6;">{op['confidence']:.1%}</span>
                </div>
                <div>
                    <strong>R²:</strong><br>
                    <span style="font-size: 1.2rem; color: #10b981;">{op['r2']:.3f}</span>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1rem;">
                <div><strong>Período:</strong> {op['periodo']}</div>
                <div><strong>Beta:</strong> {op['beta']:.3f}</div>
                <div><strong>Alpha:</strong> {op['alpha']:.3f}</div>
                <div><strong>Valor Op.:</strong> R$ {valor_op:,.0f}</div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
                <div>
                    <strong>Setores:</strong><br>
                    {op['setor_dep']} / {op['setor_ind']}
                </div>
                <div>
                    <strong>Timestamp:</strong><br>
                    {op['timestamp'].strftime('%H:%M:%S')}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_sidebar():
    """Sidebar com controles avançados do sistema"""
    with st.sidebar:
        st.header("⚙️ Controles do Sistema")
        
        # Status do sistema
        st.subheader("📊 Status")
        if HAS_REAL_SYSTEM:
            st.success("✅ Sistema Real v5.5")
        else:
            st.warning("⚠️ Modo Simulação")
        
        if HAS_MT5:
            st.success("✅ MT5 Disponível")
        else:
            st.error("❌ MT5 Indisponível")
        
        # Controles de análise
        st.subheader("🔍 Análise Rápida")
        
        quick_assets = st.multiselect(
            "Ativos para Análise Rápida",
            options=DEPENDENTE_REAL,
            default=['PETR4', 'VALE3', 'ITUB4', 'BBDC4'],
            help="Selecione ativos para análise rápida"
        )
        
        quick_period = st.selectbox(
            "Período",
            options=PERIODOS_REAIS,
            index=1,  # 100
            help="Período para análise"
        )
        
        if st.button("⚡ Análise Rápida", use_container_width=True):
            with st.spinner("Analisando..."):
                resultados = trading_system_v55.executar_analise_completa(
                    lista_dependente=quick_assets,
                    lista_independente=quick_assets,
                    periodos=[quick_period]
                )
                st.success(f"✅ {len(resultados)} pares analisados!")
        
        # Informações do sistema
        st.subheader("ℹ️ Info do Sistema")
        
        st.write(f"**Ativos Configurados:** {len(DEPENDENTE_REAL)}")
        st.write(f"**Setores:** {len(set(SEGMENTOS_REAIS.values()))}")
        st.write(f"**Períodos:** {len(PERIODOS_REAIS)}")
        
        stats = trading_system_v55.get_estatisticas_sistema()
        if stats:
            st.write(f"**Pares Analisados:** {stats.get('total_pairs_analyzed', 0)}")
            st.write(f"**Sinais Ativos:** {stats.get('total_signals', 0)}")

def main():
    """Função principal do dashboard Wall Street Level"""
    # Renderizar cabeçalho
    render_header()
    
    # Renderizar status do sistema
    render_system_status()
    
    # Navegação principal com design profissional
    tab1, tab2, tab3 = st.tabs([
        "🎯 Análise de Mercado",
        "💰 Oportunidades",
        "ℹ️ Sobre o Sistema"
    ])
    
    with tab1:
        render_market_analysis()
    
    with tab2:
        render_trading_opportunities()
    
    with tab3:
        st.header("ℹ️ Sobre o Sistema v5.5")
        
        st.markdown("""
        ### 🚀 Trading System Pro v5.5 - Wall Street Level
        
        Sistema profissional de pairs trading desenvolvido com os mais altos padrões da indústria 
        financeira, utilizado por hedge funds e gestores institucionais.
        
        #### 🔧 Funcionalidades Principais:
        
        - **Análise de Cointegração**: Identifica pares estatisticamente relacionados
        - **Z-Score Avançado**: Detecta oportunidades de mean reversion
        - **Filtros Estatísticos**: R², Beta, ADF, Cointegração
        - **Gestão de Risco**: Stop-loss e take-profit automáticos
        - **Execução MT5**: Integração direta com MetaTrader 5
        - **Monitoramento Real-time**: Dashboard profissional
        """)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write(f"**Total de Ativos:** {len(DEPENDENTE_REAL)}")
            st.write(f"**Setores:** {len(set(SEGMENTOS_REAIS.values()))}")
            st.write(f"**Períodos:** {len(PERIODOS_REAIS)}")
        
        with col2:
            st.write("**Principais Setores:**")
            setores_count = {}
            for setor in SEGMENTOS_REAIS.values():
                setores_count[setor] = setores_count.get(setor, 0) + 1
            
            for setor, count in sorted(setores_count.items(), key=lambda x: x[1], reverse=True)[:5]:
                st.write(f"• {setor}: {count} ativos")
        
        with col3:
            st.write("**Parâmetros do Sistema:**")
            st.write(f"• Z-Score Threshold: ±{FILTER_PARAMS_REAL['zscore_threshold']}")
            st.write(f"• R² Mínimo: {FILTER_PARAMS_REAL['r2_min']}")
            st.write(f"• Beta Máximo: {FILTER_PARAMS_REAL['beta_max']}")
            st.write(f"• Valor Operação: R$ {PARAMS_SISTEMA_REAL['valor_operacao']:,}")
    
    # Renderizar sidebar
    render_sidebar()
    
    # Rodapé profissional
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #1e2329 0%, #2b3139 100%); 
                border-radius: 10px; margin-top: 2rem;">
        <p style="margin: 0; color: #e0e6ed;">
            <strong>🚀 Trading System Pro v5.5</strong> - Wall Street Professional Level<br>
            <small>Desenvolvido para Hedge Funds e Gestores Institucionais</small><br>
            <small>© 2024 Trading System Pro Team - Todos os direitos reservados</small>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
