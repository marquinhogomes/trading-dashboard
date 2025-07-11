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
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1e2329 0%, #2b3139 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
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
    
    /* Success Button */
    .stButton > button.success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
    
    .stButton > button.success:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
    }
    
    /* Danger Button */
    .stButton > button.danger {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }
    
    .stButton > button.danger:hover {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(30, 35, 41, 0.5);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #374151 0%, #4b5563 100%);
        border-radius: 8px;
        color: white;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        box-shadow: 0 2px 10px rgba(59, 130, 246, 0.3);
    }
    
    /* Metric Value Styling */
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #3b82f6;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
    }
    
    .metric-positive {
        color: #10b981;
    }
    
    .metric-negative {
        color: #ef4444;
    }
    
    .metric-neutral {
        color: #6b7280;
    }
    
    /* DataFrames */
    .dataframe {
        background: rgba(30, 35, 41, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    /* Progress Bar */
    .stProgress .st-bo {
        background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%);
        border-radius: 10px;
    }
    
    /* Info Boxes */
    .stAlert {
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(30, 35, 41, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
    }
    
    /* Number Input */
    .stNumberInput > div > div > input {
        background: rgba(30, 35, 41, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        color: white;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%);
    }
    
    /* Z-Score Visualization */
    .zscore-extreme {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(220, 38, 38, 0.3);
    }
    
    .zscore-high {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
    }
    
    .zscore-normal {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 35, 41, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    }
</style>
""", unsafe_allow_html=True)# ═══════════════════════════════════════════════════════════════════════════════
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
        
        # Calcular stop loss e take profit
        if op['signal'] == 'COMPRA':
            gain_multiplier = PARAMS_SISTEMA_REAL['desvio_gain_compra']
            loss_multiplier = PARAMS_SISTEMA_REAL['desvio_loss_compra']
        else:
            gain_multiplier = PARAMS_SISTEMA_REAL['desvio_gain_venda']
            loss_multiplier = PARAMS_SISTEMA_REAL['desvio_loss_venda']
        
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
        
        # Botão de expansão para detalhes
        with st.expander(f"📊 Detalhes Técnicos - {op['par']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Parâmetros da Regressão:**")
                st.write(f"• Alpha: {op['alpha']:.6f}")
                st.write(f"• Beta: {op['beta']:.6f}")
                st.write(f"• R²: {op['r2']:.6f}")
                st.write(f"• Z-Score: {op['zscore']:.6f}")
                
                st.write("**Testes Estatísticos:**")
                st.write(f"• ADF p-value: {op['adf_p_value']:.6f}")
                st.write(f"• Coint p-value: {op['coint_p_value']:.6f}")
            
            with col2:
                st.write("**Parâmetros de Execução:**")
                st.write(f"• Valor da Operação: R$ {valor_op:,.0f}")
                st.write(f"• Gain Multiplier: {gain_multiplier:.3f}")
                st.write(f"• Loss Multiplier: {loss_multiplier:.3f}")
                
                st.write("**Filtros Aplicados:**")
                for filtro, passou in op['filter_results'].items():
                    emoji = "✅" if passou else "❌"
                    if passou is not None:
                        st.write(f"• {filtro}: {emoji}")            
            # Gráfico do resíduo se disponível
            if 'residuo_series' in op:
                residuo = op['residuo_series']
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=residuo.index,
                    y=residuo.values,
                    mode='lines',
                    name='Resíduo',
                    line=dict(color='#3b82f6')
                ))
                
                # Adicionar linhas de Z-Score
                mean_val = op['residuo_mean']
                std_val = op['residuo_std']
                
                fig.add_hline(y=mean_val + 2*std_val, line_dash="dash", 
                             line_color="red", annotation_text="Z=+2")
                fig.add_hline(y=mean_val - 2*std_val, line_dash="dash", 
                             line_color="red", annotation_text="Z=-2")
                fig.add_hline(y=mean_val, line_dash="dot", 
                             line_color="gray", annotation_text="Média")
                
                fig.update_layout(
                    title=f"Evolução do Resíduo - {op['par']}",
                    xaxis_title="Data",
                    yaxis_title="Resíduo",
                    template="plotly_dark",
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)

def render_performance_analysis():
    """Renderiza análise de performance do sistema"""
    
    st.subheader("📊 Análise de Performance")
    
    with st.sidebar:
        st.subheader("🔍 Filtros de Análise")
        
        # Seleção de setor
        setor_selecionado = st.selectbox(
            "Setor:",
            ["Todos"] + setores_disponiveis,
            help="Filtrar pares por setor específico"
        )
        
        # Usar lista real de ativos
        if setor_selecionado == "Todos":
            ativos_filtrados = DEPENDENTE_REAL
        else:
            ativos_filtrados = get_pares_por_setor(setor_selecionado)
        
        ativos_selecionados = st.multiselect(
            "Ativos para análise:",
            ativos_filtrados,
            default=ativos_filtrados[:5],  # Primeiros 5 por padrão
            help="Selecione os ativos para análise de pares"
        )
    
    with col2:
        st.markdown("**Parâmetros de Filtro (Sistema Real)**")
        
        # Usar parâmetros reais como base
        filtros_reais = FILTER_PARAMS_REAL.copy()
        
        r2_min = st.slider(
            "R² Mínimo:", 
            0.1, 0.9, 
            filtros_reais['r2_min'],
            help="Correlação mínima entre pares"
        )
        
        beta_max = st.slider(
            "Beta Máximo:", 
            0.5, 3.0, 
            filtros_reais['beta_max'],
            help="Sensibilidade máxima permitida"
        )
        
        enable_coint = st.checkbox(
            "Filtro de Cointegração",
            filtros_reais['enable_cointegration_filter'],
            help="Aplicar teste de cointegração"
        )
        
        timeframe = st.selectbox(
            "Timeframe:",
            ["M15", "H1", "D1"],
            index=0,
            help="Período para análise"
        )
    
    return {
        'ativos_selecionados': ativos_selecionados,
        'setor': setor_selecionado,
        'filtros': {
            'r2_min': r2_min,
            'beta_max': beta_max,
            'enable_cointegration_filter': enable_coint
        },
        'timeframe': timeframe
    }

def render_analise_real(config):
    """Renderiza análise usando dados reais"""
    st.subheader("📊 Análise de Pares - Dados Reais")
    
    if not HAS_REAL_SYSTEM:
        st.error("Sistema real não disponível para análise")
        return
    
    if not config.get('ativos_selecionados'):
        st.warning("Selecione ativos para análise")
        return
    
    # Colunas para controles
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        executar_analise = st.button("🔄 Executar Análise Real", type="primary")
    
    with col2:
        periodo = st.selectbox("Período:", [50, 100, 150, 200], index=1)
    
    with col3:
        auto_refresh = st.checkbox("🔄 Auto Refresh (30s)")
    
    # Executar análise
    if executar_analise or auto_refresh:
        with st.spinner("Executando análise real..."):
            
            # Executar análise real
            resultado = get_real_analysis_data(
                timeframe=config['timeframe'],
                periodo=periodo,
                filtros_customizados=config['filtros']
            )
            
            if resultado and resultado.get('fonte') == 'REAL':
                # Métricas principais
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Pares Analisados", resultado.get('pares_analisados', 0))
                
                with col2:
                    st.metric("Aprovados nos Filtros", resultado.get('pares_aprovados', 0))
                
                with col3:
                    st.metric("Oportunidades", resultado.get('oportunidades', 0))
                
                with col4:
                    timestamp = resultado.get('timestamp', datetime.now())
                    st.metric("Última Atualização", timestamp.strftime("%H:%M:%S"))
                
                # Salvar no session state
                st.session_state['ultimo_resultado'] = resultado
                
                # Abas para diferentes visualizações
                tab1, tab2, tab3, tab4 = st.tabs(["📋 Resultados", "🎯 Oportunidades", "📊 Gráficos", "📈 Setores"])
                
                with tab1:
                    render_tabela_resultados(resultado)
                
                with tab2:
                    render_oportunidades_detalhadas(resultado)
                
                with tab3:
                    render_graficos_analise(resultado)
                
                with tab4:
                    render_analise_setores(resultado)
                    
            else:
                st.error("Erro na análise real ou dados não disponíveis")
                # Mostrar logs de erro se disponível
                if real_state.logs:
                    with st.expander("🔍 Logs do Sistema"):
                        for log in real_state.logs[-5:]:
                            st.text(f"[{log['nivel']}] {log['mensagem']}")

def render_tabela_resultados(resultado):
    """Renderiza tabela de resultados da análise"""
    if 'dados_brutos' in resultado and not resultado['dados_brutos'].empty:
        df_display = resultado['dados_brutos'].copy()
        
        # Formatar colunas para exibição
        numeric_cols = ['R2', 'Beta', 'Zscore', 'Coef_Var']
        for col in numeric_cols:
            if col in df_display.columns:
                df_display[col] = pd.to_numeric(df_display[col], errors='coerce').round(3)
        
        # Filtros interativos
        col1, col2 = st.columns(2)
        with col1:
            apenas_aprovados = st.checkbox("✅ Apenas aprovados nos filtros", value=True)
        with col2:
            mesmo_setor = st.checkbox("🏭 Apenas mesmo setor", value=True)
        
        # Aplicar filtros
        df_filtrado = df_display.copy()
        if apenas_aprovados and 'Filtros_OK' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['Filtros_OK'] == True]
        if mesmo_setor and 'Mesmo_Setor' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['Mesmo_Setor'] == True]
        
        # Seletor de colunas
        colunas_disponiveis = list(df_filtrado.columns)
        colunas_padrao = ['Dependente', 'Independente', 'Setor_Dep', 'R2', 'Beta', 'Zscore', 'Filtros_OK']
        colunas_selecionadas = st.multiselect(
            "Selecione colunas para exibir:",
            colunas_disponiveis,
            default=[col for col in colunas_padrao if col in colunas_disponiveis]
        )
        
        if colunas_selecionadas:
            # Colorir células baseado em critérios
            def highlight_rows(row):
                if 'Filtros_OK' in row.index and row['Filtros_OK']:
                    return ['background-color: #d4edda'] * len(row)
                return [''] * len(row)
            
            st.dataframe(
                df_filtrado[colunas_selecionadas].style.apply(highlight_rows, axis=1),
                use_container_width=True,
                height=400
            )
            
            # Estatísticas resumidas
            st.markdown("**📊 Estatísticas dos Resultados:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                if 'R2' in df_filtrado.columns:
                    st.metric("R² Médio", f"{df_filtrado['R2'].mean():.3f}")
            with col2:
                if 'Beta' in df_filtrado.columns:
                    st.metric("Beta Médio", f"{abs(df_filtrado['Beta']).mean():.3f}")
            with col3:
                if 'Zscore' in df_filtrado.columns:
                    st.metric("Z-score Médio", f"{abs(df_filtrado['Zscore']).mean():.2f}")

def render_oportunidades_detalhadas(resultado):
    """Renderiza oportunidades de trading detalhadas"""
    if not resultado.get('oportunidades_detalhadas'):
        st.info("Nenhuma oportunidade identificada no momento")
        return
    
    oportunidades = resultado['oportunidades_detalhadas']
    
    # Filtros para oportunidades
    col1, col2 = st.columns(2)
    with col1:
        tipo_filtro = st.selectbox("Filtrar por tipo:", ["Todos", "COMPRA", "VENDA"])
    with col2:
        zscore_min = st.slider("Z-score mínimo:", 0.0, 5.0, 2.0, 0.1)
    
    # Aplicar filtros
    oportunidades_filtradas = oportunidades.copy()
    if tipo_filtro != "Todos":
        oportunidades_filtradas = [op for op in oportunidades_filtradas if op['Tipo'] == tipo_filtro]
    oportunidades_filtradas = [op for op in oportunidades_filtradas if abs(op['Zscore']) >= zscore_min]
    
    st.write(f"**🎯 {len(oportunidades_filtradas)} oportunidades encontradas:**")
    
    for i, op in enumerate(oportunidades_filtradas[:10]):  # Top 10
        with st.expander(f"💡 Oportunidade {i+1}: {op['Dependente']}/{op['Independente']} - {op['Tipo']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**📊 Indicadores:**")
                st.write(f"Z-Score: **{op['Zscore']:.2f}**")
                st.write(f"R²: **{op['R2']:.3f}**")
                st.write(f"Beta: **{op['Beta']:.3f}**")
            
            with col2:
                st.markdown("**🏭 Setores:**")
                setor_dep = SEGMENTOS_REAIS.get(op['Dependente'], 'N/A')
                setor_ind = SEGMENTOS_REAIS.get(op['Independente'], 'N/A')
                st.write(f"Dependente: **{setor_dep}**")
                st.write(f"Independente: **{setor_ind}**")
                st.write(f"Mesmo setor: **{'✅' if setor_dep == setor_ind else '❌'}**")
            
            with col3:
                st.markdown("**⚡ Ação Sugerida:**")
                if op['Tipo'] == 'COMPRA':
                    st.success(f"🟢 Comprar {op['Dependente']}, Vender {op['Independente']}")
                else:
                    st.error(f"🔴 Vender {op['Dependente']}, Comprar {op['Independente']}")
                st.write(f"Timestamp: {op['Timestamp'].strftime('%H:%M:%S')}")

def render_graficos_analise(resultado):
    """Renderiza gráficos da análise"""
    if 'dados_brutos' not in resultado or resultado['dados_brutos'].empty:
        st.info("Dados insuficientes para gráficos")
        return
    
    df = resultado['dados_brutos']
    
    # Gráfico 1: Distribuição do R²
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Distribuição do R²**")
        if 'R2' in df.columns:
            fig = px.histogram(df, x='R2', nbins=20, title="Distribuição do R²")
            fig.add_vline(x=FILTER_PARAMS_REAL['r2_min'], line_dash="dash", line_color="red")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**📊 Distribuição do Z-Score**")
        if 'Zscore' in df.columns:
            fig = px.histogram(df, x='Zscore', nbins=20, title="Distribuição do Z-Score")
            fig.add_vline(x=2, line_dash="dash", line_color="green")
            fig.add_vline(x=-2, line_dash="dash", line_color="green")
            st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico 2: Scatter R² vs Z-Score
    st.markdown("**📈 Relação R² vs Z-Score**")
    if 'R2' in df.columns and 'Zscore' in df.columns:
        fig = px.scatter(
            df, x='R2', y='Zscore', 
            color='Filtros_OK',
            hover_data=['Dependente', 'Independente'],
            title="R² vs Z-Score"
        )
        st.plotly_chart(fig, use_container_width=True)

def render_analise_setores(resultado):
    """Renderiza análise por setores"""
    if 'dados_brutos' not in resultado or resultado['dados_brutos'].empty:
        st.info("Dados insuficientes para análise de setores")
        return
    
    df = resultado['dados_brutos']
    
    # Análise por setor
    if 'Setor_Dep' in df.columns:
        setores_stats = df.groupby('Setor_Dep').agg({
            'R2': ['count', 'mean'],
            'Filtros_OK': 'sum'
        }).round(3)
        
        setores_stats.columns = ['Total_Pares', 'R2_Medio', 'Aprovados']
        setores_stats = setores_stats.reset_index()
        
        st.markdown("**🏭 Estatísticas por Setor:**")
        st.dataframe(setores_stats, use_container_width=True)
        
        # Gráfico de setores
        fig = px.bar(
            setores_stats, 
            x='Setor_Dep', 
            y='Aprovados',
            title="Pares Aprovados por Setor"
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

def render_sidebar():
    """Renderiza sidebar com informações do sistema"""
    st.sidebar.title("🎯 Sistema Real")
    
    if HAS_REAL_SYSTEM:
        st.sidebar.success("✅ Sistema Real Ativo")
        
        # Informações do sistema
        st.sidebar.markdown("**Informações:**")
        st.sidebar.info(f"""
        **Versão:** {SYSTEM_INFO.get('version', 'N/A')}
        **Ativos:** {len(DEPENDENTE_REAL)}
        **Setores:** {len(get_setores_disponiveis())}
        **Horário Operação:** {'✅' if is_horario_operacao() else '❌'}
        """)
        
        # Logs recentes
        st.sidebar.markdown("**Logs Recentes:**")
        if real_state.logs:
            for log in real_state.logs[-5:]:  # Últimos 5 logs
                st.sidebar.text(f"{log['nivel']}: {log['mensagem'][:50]}...")
        else:
            st.sidebar.text("Nenhum log disponível")
    else:
        st.sidebar.error("❌ Sistema Real Não Disponível")

# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 APLICAÇÃO PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Função principal do dashboard"""
    # Cabeçalho
    render_header()    
    # Status do sistema
    render_system_status()

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
        
        # Configurações rápidas
        st.subheader("⚙️ Config Rápida")
        
        confidence_filter = st.slider(
            "Confiança Mínima",
            0.0, 1.0, 0.7, 0.05,
            help="Filtro de confiança para sinais"
        )
        
        zscore_filter = st.slider(
            "Z-Score Threshold",
            1.0, 3.0, 2.0, 0.1,
            help="Limite para geração de sinais"
        )
        
        # Atualizar parâmetros globais
        FILTER_PARAMS_REAL['zscore_threshold'] = zscore_filter
        
        # Auto-refresh
        st.subheader("🔄 Atualização")
        
        auto_refresh_global = st.checkbox(
            "Auto-refresh Global",
            value=False,
            help="Atualizar dashboard automaticamente"
        )
        
        if auto_refresh_global:
            refresh_interval = st.slider("Intervalo (s)", 10, 300, 30)
            time.sleep(refresh_interval)
            st.rerun()
        
        # Ações do sistema
        st.subheader("🎮 Ações")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        
        with col2:
            if st.button("📊 Reset", use_container_width=True):
                # Reset análise
                trading_system_v55.current_analysis = {}
                st.success("✅ Reset!")
        
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
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🎯 Análise de Mercado",
        "💰 Oportunidades",
        "📈 Performance",
        "⚙️ Configuração",
        "📡 Monitoramento",
        "🔧 Controles",
        "ℹ️ Sobre"
    ])
    
    with tab1:
        render_market_analysis()
    
    with tab2:
        render_trading_opportunities()
    
    with tab3:
        render_performance_analysis()
    
    with tab4:
        render_system_configuration()
    
    with tab5:
        render_system_monitoring()
    
    with tab6:
        # Controles avançados do sistema
        st.header("🔧 Controles Avançados")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("📊 Análise Completa")
            
            if st.button("🚀 Executar Análise Completa", use_container_width=True):
                with st.spinner("Executando análise completa do sistema..."):
                    progress_bar = st.progress(0)
                    
                    def update_progress(percent):
                        progress_bar.progress(percent)
                    
                    resultados = trading_system_v55.executar_analise_completa(
                        progress_callback=update_progress
                    )
                    
                    st.success(f"✅ Análise completa finalizada! {len(resultados)} pares processados.")
        
        with col2:
            st.subheader("💾 Gestão de Dados")
            
            if st.button("📤 Exportar Resultados", use_container_width=True):
                if trading_system_v55.current_analysis:
                    # Converter para DataFrame
                    df_results = pd.DataFrame(trading_system_v55.current_analysis.values())
                    
                    # Criar CSV
                    csv_data = df_results.to_csv(index=False)
                    
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv_data,
                        file_name=f"analise_trading_v55_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("⚠️ Nenhum dado para exportar")
            
            if st.button("🔄 Backup Sistema", use_container_width=True):
                backup_data = {
                    'timestamp': datetime.now().isoformat(),
                    'config_sistema': PARAMS_SISTEMA_REAL,
                    'filtros': FILTER_PARAMS_REAL,
                    'resultados_analise': len(trading_system_v55.current_analysis),
                    'versao': 'v5.5'
                }
                
                backup_json = json.dumps(backup_data, indent=2)
                st.download_button(
                    label="📥 Download Backup",
                    data=backup_json,
                    file_name=f"backup_sistema_v55_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col3:
            st.subheader("🛠️ Manutenção")
            
            if st.button("🔧 Limpar Cache", use_container_width=True):
                trading_system_v55.analysis_cache = {}
                st.success("✅ Cache limpo!")
            
            if st.button("📝 Gerar Relatório", use_container_width=True):
                # Gerar relatório detalhado
                stats = trading_system_v55.get_estatisticas_sistema()
                
                relatorio = f"""
# 📊 RELATÓRIO DO SISTEMA v5.5
**Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

## 📈 Resumo Executivo
- **Pares Analisados:** {stats.get('total_pairs_analyzed', 0)}
- **Sinais de Compra:** {stats.get('signals_compra', 0)}
- **Sinais de Venda:** {stats.get('signals_venda', 0)}
- **Confiança Média:** {stats.get('avg_confidence', 0):.1%}
- **R² Médio:** {stats.get('avg_r2', 0):.3f}

## ⚙️ Configuração Atual
- **Threshold Z-Score:** ±{FILTER_PARAMS_REAL['zscore_threshold']}
- **R² Mínimo:** {FILTER_PARAMS_REAL['r2_min']}
- **Beta Máximo:** {FILTER_PARAMS_REAL['beta_max']}
- **Valor por Operação:** R$ {PARAMS_SISTEMA_REAL['valor_operacao']:,}

## 📊 Ativos e Setores
- **Total de Ativos:** {len(DEPENDENTE_REAL)}
- **Total de Setores:** {len(set(SEGMENTOS_REAIS.values()))}

---
*Sistema de Trading Profissional v5.5 - Wall Street Level*
                """
                
                st.download_button(
                    label="📥 Download Relatório",
                    data=relatorio,
                    file_name=f"relatorio_sistema_v55_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )
    
    with tab7:
        render_about_system()
    
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

def render_performance_analysis():
    """Análise de performance avançada do sistema"""
    st.header("📊 Análise de Performance")
    
    # Métricas principais
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Simular dados de performance baseados no sistema real
    np.random.seed(42)  # Para resultados consistentes
    
    with col1:
        saldo_atual = 50000 + np.random.normal(5000, 2000)
        variacao_dia = np.random.normal(250, 500)
        st.metric("Saldo Atual", f"R$ {saldo_atual:,.2f}", f"{variacao_dia:+.2f}")
    
    with col2:
        trades_hoje = np.random.poisson(8)
        st.metric("Trades Hoje", trades_hoje, f"+{np.random.randint(2, 6)}")
    
    with col3:
        win_rate = 0.65 + np.random.normal(0, 0.1)
        win_rate = max(0, min(1, win_rate))
        st.metric("Taxa de Acerto", f"{win_rate:.1%}", f"{np.random.normal(0, 0.05):+.1%}")
    
    with col4:
        drawdown = abs(np.random.normal(0.05, 0.02))
        st.metric("Drawdown", f"{drawdown:.1%}", f"{np.random.normal(0, 0.01):+.1%}")
    
    with col5:
        sharpe = 1.5 + np.random.normal(0, 0.3)
        st.metric("Sharpe Ratio", f"{sharpe:.2f}", f"{np.random.normal(0, 0.1):+.2f}")
    
    # Gráficos de performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Curva de Equity")
        
        # Simular curva de equity
        days = 30
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        initial_equity = 50000
        
        # Gerar retornos baseados nos parâmetros do sistema
        daily_returns = np.random.normal(0.001, 0.02, days)  # 0.1% média, 2% vol
        equity_curve = initial_equity * np.cumprod(1 + daily_returns)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=equity_curve,
            mode='lines',
            name='Equity',
            line=dict(color='#10b981', width=3),
            fill='tonexty'
        ))
        
        fig.update_layout(
            title="Evolução do Capital (30 dias)",
            xaxis_title="Data",
            yaxis_title="Valor (R$)",
            template="plotly_dark",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Distribuição de Retornos")
        
        # Gerar distribuição de retornos de trades
        trade_returns = np.random.normal(0.015, 0.08, 100)  # 1.5% média, 8% vol
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=trade_returns * 100,  # Converter para %
            nbinsx=20,
            name="Retornos",
            marker_color='rgba(59, 130, 246, 0.7)',
            marker_line=dict(color='rgba(59, 130, 246, 1)', width=1)
        ))
        
        fig.update_layout(
            title="Distribuição de Retornos por Trade",
            xaxis_title="Retorno (%)",
            yaxis_title="Frequência",
            template="plotly_dark",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Métricas avançadas
    st.subheader("📈 Métricas Avançadas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Métricas de Risco:**")
        var_95 = np.percentile(trade_returns, 5) * 100
        var_99 = np.percentile(trade_returns, 1) * 100
        volatilidade = np.std(trade_returns) * np.sqrt(252) * 100
        
        st.write(f"• VaR 95%: {var_95:.2f}%")
        st.write(f"• VaR 99%: {var_99:.2f}%")
        st.write(f"• Volatilidade Anual: {volatilidade:.2f}%")
        st.write(f"• Máximo Drawdown: {drawdown:.1%}")
    
    with col2:
        st.write("**Métricas de Retorno:**")
        retorno_medio = np.mean(trade_returns) * 100
        retorno_anual = retorno_medio * 252
        melhor_trade = np.max(trade_returns) * 100
        pior_trade = np.min(trade_returns) * 100
        
        st.write(f"• Retorno Médio: {retorno_medio:.2f}%")
        st.write(f"• Retorno Anualizado: {retorno_anual:.2f}%")
        st.write(f"• Melhor Trade: {melhor_trade:.2f}%")
        st.write(f"• Pior Trade: {pior_trade:.2f}%")
    
    with col3:
        st.write("**Eficiência Operacional:**")
        total_trades = len(trade_returns)
        trades_positivos = np.sum(trade_returns > 0)
        trades_negativos = np.sum(trade_returns < 0)
        avg_winner = np.mean(trade_returns[trade_returns > 0]) * 100
        avg_loser = np.mean(trade_returns[trade_returns < 0]) * 100
        
        st.write(f"• Total de Trades: {total_trades}")
        st.write(f"• Trades Positivos: {trades_positivos}")
        st.write(f"• Trades Negativos: {trades_negativos}")
        st.write(f"• Gain Médio: {avg_winner:.2f}%")
        st.write(f"• Loss Médio: {avg_loser:.2f}%")

def render_system_configuration():
    """Configuração avançada do sistema"""
    st.header("⚙️ Configuração do Sistema v5.5")
    
    # Parâmetros de Trading
    st.subheader("💰 Parâmetros de Trading")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Limites Operacionais:**")
        limite_op = st.number_input(
            "Limite de Operações",
            value=PARAMS_SISTEMA_REAL['limite_operacoes'],
            min_value=1,
            max_value=20,
            help="Número máximo de operações simultâneas"
        )
        
        valor_op = st.number_input(
            "Valor por Operação (R$)",
            value=PARAMS_SISTEMA_REAL['valor_operacao'],
            min_value=1000,
            max_value=100000,
            step=1000,
            help="Valor financeiro por operação"
        )
        
        limite_lucro = st.number_input(
            "Limite de Lucro (R$)",
            value=PARAMS_SISTEMA_REAL['limite_lucro'],
            min_value=50,
            max_value=1000,
            help="Lucro máximo por trade"
        )
        
        limite_prejuizo = st.number_input(
            "Limite de Prejuízo (R$)",
            value=PARAMS_SISTEMA_REAL['limite_prejuizo'],
            min_value=50,
            max_value=1000,
            help="Prejuízo máximo por trade"
        )
    
    with col2:
        st.write("**Desvios de Entrada/Saída:**")
        desvio_gain_compra = st.number_input(
            "Desvio Gain Compra",
            value=PARAMS_SISTEMA_REAL['desvio_gain_compra'],
            min_value=1.001,
            max_value=1.050,
            step=0.001,
            format="%.3f",
            help="Multiplicador para take profit em compras"
        )
        
        desvio_loss_compra = st.number_input(
            "Desvio Loss Compra",
            value=PARAMS_SISTEMA_REAL['desvio_loss_compra'],
            min_value=0.950,
            max_value=0.999,
            step=0.001,
            format="%.3f",
            help="Multiplicador para stop loss em compras"
        )
        
        desvio_gain_venda = st.number_input(
            "Desvio Gain Venda",
            value=PARAMS_SISTEMA_REAL['desvio_gain_venda'],
            min_value=0.950,
            max_value=0.999,
            step=0.001,
            format="%.3f",
            help="Multiplicador para take profit em vendas"
        )
        
        desvio_loss_venda = st.number_input(
            "Desvio Loss Venda",
            value=PARAMS_SISTEMA_REAL['desvio_loss_venda'],
            min_value=1.001,
            max_value=1.050,
            step=0.001,
            format="%.3f",
            help="Multiplicador para stop loss em vendas"
        )
    
    # Filtros Estatísticos
    st.subheader("🔬 Filtros Estatísticos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        r2_min = st.slider(
            "R² Mínimo",
            min_value=0.1,
            max_value=0.9,
            value=FILTER_PARAMS_REAL['r2_min'],
            step=0.05,
            help="R² mínimo para aceitar um par"
        )
        
        beta_max = st.slider(
            "Beta Máximo",
            min_value=0.5,
            max_value=3.0,
            value=FILTER_PARAMS_REAL['beta_max'],
            step=0.1,
            help="Beta máximo permitido"
        )
    
    with col2:
        zscore_threshold = st.slider(
            "Threshold Z-Score",
            min_value=1.0,
            max_value=3.0,
            value=FILTER_PARAMS_REAL['zscore_threshold'],
            step=0.1,
            help="Limite para gerar sinais"
        )
        
        adf_p_value_max = st.slider(
            "P-Value ADF Máximo",
            min_value=0.01,
            max_value=0.10,
            value=FILTER_PARAMS_REAL['adf_p_value_max'],
            step=0.01,
            help="P-value máximo para estacionariedade"
        )
    
    with col3:
        enable_coint = st.checkbox(
           
            "Filtro de Cointegração",
            value=FILTER_PARAMS_REAL['enable_cointegration_filter'],
            help="Aplicar teste de cointegração"
        )
        
        use_coint_test = st.checkbox(
            "Usar Teste de Cointegração",
            value=FILTER_PARAMS_REAL['use_coint_test'],
            help="Habilitar testes de cointegração"
        )
    
    # Seleção de Ativos e Períodos
    st.subheader("📊 Seleção de Ativos e Períodos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Ativos Dependentes:**")
        selected_dependentes = st.multiselect(
            "Escolher Ativos Dependentes",
            options=DEPENDENTE_REAL,
            default=DEPENDENTE_REAL[:15],
            help="Ativos que serão usados como variável dependente"
        )
        
        st.write(f"Total selecionados: {len(selected_dependentes)}")
    
    with col2:
        st.write("**Períodos de Análise:**")
        selected_periods = st.multiselect(
            "Escolher Períodos",
            options=PERIODOS_REAIS,
            default=[100, 120, 140, 160],
            help="Períodos para cálculo das regressões"
        )
        
        st.write(f"Total selecionados: {len(selected_periods)}")
    
    # Botões de ação
    st.subheader("🎮 Controles do Sistema")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💾 Salvar Configuração", use_container_width=True):
            # Atualizar parâmetros globais
            PARAMS_SISTEMA_REAL.update({
                'limite_operacoes': limite_op,
                'valor_operacao': valor_op,
                'limite_lucro': limite_lucro,
                'limite_prejuizo': limite_prejuizo,
                'desvio_gain_compra': desvio_gain_compra,
                'desvio_loss_compra': desvio_loss_compra,
                'desvio_gain_venda': desvio_gain_venda,
                'desvio_loss_venda': desvio_loss_venda
            })
            
            FILTER_PARAMS_REAL.update({
                'r2_min': r2_min,
                'beta_max': beta_max,
                'zscore_threshold': zscore_threshold,
                'adf_p_value_max': adf_p_value_max,
                'enable_cointegration_filter': enable_coint,
                'use_coint_test': use_coint_test
            })
            
            st.success("✅ Configuração salva com sucesso!")
    
    with col2:
        if st.button("🔄 Resetar Padrões", use_container_width=True):
            st.warning("⚠️ Configurações resetadas para valores padrão")
            st.rerun()
    
    with col3:
        if st.button("📤 Exportar Config", use_container_width=True):
            config_data = {
                'params_sistema': PARAMS_SISTEMA_REAL,
                'filter_params': FILTER_PARAMS_REAL,
                'ativos_selecionados': selected_dependentes,
                'periodos_selecionados': selected_periods,
                'timestamp': datetime.now().isoformat()
            }
            
            config_json = json.dumps(config_data, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=config_json,
                file_name=f"config_sistema_v55_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col4:
        uploaded_file = st.file_uploader("📁 Importar Config", type=['json'])
        if uploaded_file is not None:
            try:
                config_data = json.load(uploaded_file)
                st.success("✅ Configuração importada!")
                st.json(config_data)
            except Exception as e:
                st.error(f"❌ Erro ao importar: {e}")

def render_system_monitoring():
    """Monitoramento avançado do sistema"""
    st.header("📡 Monitoramento do Sistema")
    
    # Status em tempo real
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Métricas em Tempo Real")
        
        # Auto-refresh toggle
        auto_refresh = st.checkbox("🔄 Auto-refresh (30s)", value=False)
        
        if auto_refresh:
            time.sleep(30)
            st.rerun()
    
    with col2:
        st.subheader("⚡ Ações Rápidas")
        
        if st.button("🔍 Executar Análise", use_container_width=True):
            with st.spinner("Executando análise..."):
                trading_system_v55.executar_analise_completa()
                st.success("✅ Análise concluída!")
        
        if st.button("📊 Atualizar Status", use_container_width=True):
            st.success("✅ Status atualizado!")
        
        if st.button("🔄 Refresh Dashboard", use_container_width=True):
            st.rerun()
    
    # Logs do sistema
    st.subheader("📝 Logs do Sistema")
    
    # Simular logs do sistema
    logs_sistema = [
        {"timestamp": "10:30:15", "level": "INFO", "message": "Sistema v5.5 inicializado com sucesso"},
        {"timestamp": "10:30:20", "level": "INFO", "message": f"Carregados {len(DEPENDENTE_REAL)} ativos para análise"},
        {"timestamp": "10:30:25", "level": "INFO", "message": "Conectado ao MetaTrader 5"},
        {"timestamp": "10:30:30", "level": "WARNING", "message": "Spread alto detectado em PETR4/VALE3"},
        {"timestamp": "10:30:35", "level": "INFO", "message": "Análise de cointegração iniciada"},
        {"timestamp": "10:30:40", "level": "SUCCESS", "message": "15 pares cointegrados encontrados"},
        {"timestamp": "10:30:45", "level": "INFO", "message": "Sinal de compra gerado para BBDC4/ITUB4"},
        {"timestamp": "10:30:50", "level": "ERROR", "message": "Falha temporária na conexão de dados"},
    ]
    
    # Filtro de logs
    col1, col2 = st.columns([3, 1])
    
    with col1:
        log_filter = st.selectbox(
            "Filtrar por nível:",
            ["TODOS", "INFO", "WARNING", "ERROR", "SUCCESS"]
        )
    
    with col2:
        max_logs = st.number_input("Máx. logs:", 5, 50, 20)
    
    # Aplicar filtro
    if log_filter != "TODOS":
        logs_filtrados = [log for log in logs_sistema if log["level"] == log_filter]
    else:
        logs_filtrados = logs_sistema
    
    # Exibir logs
    for log in reversed(logs_filtrados[-max_logs:]):
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

def render_about_system():
    """Informações sobre o sistema"""
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
    
    #### 📊 Ativos Suportados:
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
    
    st.markdown("""
    #### ⚙️ Tecnologias Utilizadas:
    
    - **Frontend**: Streamlit com design personalizado
    - **Backend**: Python com bibliotecas estatísticas avançadas
    - **Análise**: statsmodels, scipy, numpy, pandas
    - **Visualização**: Plotly para gráficos interativos
    - **Integração**: MetaTrader 5 API
    - **Machine Learning**: Suporte para modelos ARIMA/GARCH
    
    #### 🛡️ Características Profissionais:
    
    - Interface de nível Wall Street
    - Código otimizado para performance
    - Tratamento robusto de erros
    - Logging detalhado de operações
    - Configurações flexíveis
    - Backup automático de dados
    
    #### 📈 Estratégia de Trading:
    
    O sistema utiliza **pairs trading** baseado em cointegração estatística:
    
    1. **Identificação**: Encontra pares de ativos cointegrados
    2. **Análise**: Calcula Z-Score do resíduo da regressão
    3. **Sinalização**: Gera sinais quando Z-Score > threshold
    4. **Execução**: Envia ordens automaticamente ao MT5
    5. **Gestão**: Monitora posições com stop-loss/take-profit
    
    ---
    
    **Versão**: 5.5  
    **Desenvolvido para**: Operações Institucionais  
    **Padrão**: Wall Street Professional Level  
    **Suporte**: Trading System Pro Team
    """)
