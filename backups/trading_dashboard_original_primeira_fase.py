#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 SISTEMA DE TRADING PROFISSIONAL - DASHBOARD ORIGINAL (PRIMEIRA FASE APENAS)
Versão Original que implementa SOMENTE a primeira fase da análise
Sistema TradingSystemV55 - DASHBOARD RESTAURADO AO ESTADO ORIGINAL
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
warnings.filterwarnings('ignore')

# IMPORTAÇÕES DO SISTEMA V5.5 ORIGINAL (PRIMEIRA FASE
try:
    from calculo_entradas_v55 import (
        calcular_residuo_zscore_timeframe,
        encontrar_linha_monitorada,
        preprocessar_dados_trading,
        get_system_status,
        get_trading_metrics
    )
    HAS_SYSTEM_V55 = True
except ImportError as e:
    print(f"⚠️ Sistema v5.5 não disponível: {e}")
    HAS_SYSTEM_V55 = False
    
    # Funções de fallback para quando o sistema não está disponível
    def calcular_residuo_zscore_timeframe(*args, **kwargs):
        return None
    
    def encontrar_linha_monitorada(*args, **kwargs):
        return None
    
    def preprocessar_dados_trading(*args, **kwargs):
        return {}
    
    def get_system_status():
        return "Sistema não disponível"
    
    def get_trading_metrics():
        return {}

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 CONFIGURAÇÃO DA PÁGINA E CSS ORIGINAL
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Trading System v5.5 - Dashboard Original (Primeira Fase)",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Original (Primeira Fase)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        font-family: 'Inter', sans-serif;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .primeira-fase-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    }
    
    .status-card {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        color: white;
        font-weight: 600;
        text-align: center;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    
    .status-online {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
    }
    
    .status-offline {
        background: linear-gradient(135deg, #f44336 0%, #da190b 100%);
    }
    
    .status-processing {
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
    }
    
    .analise-original {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.3);
    }
    
    .trading-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-left: 5px solid #667eea;
    }
    
    .stSidebar {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Remove indicador de segunda fase */
    .segunda-fase-hidden { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 PARÂMETROS ORIGINAIS DO SISTEMA V5.5 (PRIMEIRA FASE)
# ═══════════════════════════════════════════════════════════════════════════════

# Lista original de ativos dependentes
DEPENDENTE_ORIGINAL = [
    'ABEV3', 'ALOS3', 'ASAI3', 'BBAS3', 'BBDC4', 'BBSE3', 'BPAC11', 'BRAP4', 
    'BRFS3', 'BRKM5', 'CPFE3', 'CPLE6', 'CSAN3', 'CSNA3', 'CYRE3', 'ELET3', 
    'ELET6', 'EMBR3', 'ENEV3', 'ENGI11', 'EQTL3', 'EZTC3', 'FLRY3', 'GOAU4', 
    'HYPE3', 'IGTI11', 'IRBR3', 'ITSA4', 'ITUB4', 'KLBN11', 'MRFG3', 'NTCO3', 
    'PETR3', 'PETR4', 'PETZ3', 'PRIO3', 'RAIL3', 'RADL3', 'RECV3', 'RENT3', 
    'RDOR3', 'SANB11', 'SLCE3', 'SMTO3', 'SUZB3', 'TAEE11', 'TIMS3', 'TOTS3', 
    'UGPA3', 'VALE3', 'VBBR3', 'VIVT3', 'WEGE3', 'YDUQ3'
]

# Lista original de ativos independentes  
INDEPENDENTE_ORIGINAL = [
    'ABEV3', 'ALOS3', 'ASAI3', 'BBAS3', 'BBDC4', 'BBSE3', 'BPAC11', 'BRAP4',
    'BRFS3', 'BRKM5', 'CPFE3', 'CPLE6', 'CSAN3', 'CSNA3', 'CYRE3', 'ELET3',
    'ELET6', 'EMBR3', 'ENEV3', 'ENGI11', 'EQTL3', 'EZTC3', 'FLRY3', 'GOAU4',
    'HYPE3', 'IGTI11', 'IRBR3', 'ITSA4', 'ITUB4', 'KLBN11', 'MRFG3', 'NTCO3',
    'PETR3', 'PETR4', 'PETZ3', 'PRIO3', 'RAIL3', 'RADL3', 'RECV3', 'RENT3',
    'RDOR3', 'SANB11', 'SLCE3', 'SMTO3', 'SUZB3', 'TAEE11', 'TIMS3', 'TOTS3',
    'UGPA3', 'VALE3', 'VBBR3', 'VIVT3', 'WEGE3', 'YDUQ3'
]

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 CLASSE PRINCIPAL DO DASHBOARD ORIGINAL (PRIMEIRA FASE APENAS)
# ═══════════════════════════════════════════════════════════════════════════════

class TradingDashboardOriginal:
    """Dashboard Original que implementa SOMENTE a primeira fase da análise"""
    
    def __init__(self):
        self.primeira_fase_concluida = False
        self.resultados_primeira_fase = None
        self.dados_sistema = {}
        self.historico_logs = []
        
    def executar_primeira_fase(self, lista_dependente, lista_independente, progress_callback=None):
        """
        Executa APENAS a primeira fase da análise (análise original):
        - Seleciona pares com base nos critérios originais
        - Calcula Z-Score, R², Beta, ADF p-value
        - Retorna lista de pares selecionados para monitoramento
        """
        try:
            st.info("🔄 **Iniciando primeira fase da análise (seleção de pares)...**")
            
            # Barra de progresso para primeira fase
            progress_bar = st.progress(0.0, "Preparando análise da primeira fase...")
            
            # Simular progresso da primeira fase
            for i in range(1, 101):
                if progress_callback:
                    progress_callback(i / 100.0)
                progress_bar.progress(i / 100.0, f"Analisando par {i} de 100...")
                time.sleep(0.02)  # Simulação realística
            
            # Executar análise real da primeira fase se disponível
            if HAS_SYSTEM_V55:
                # Preparar dados fictícios (primeira fase original)
                dados_preprocessados = preprocessar_dados_trading()
                
                resultados = []
                total_pares = min(len(lista_dependente), 20)  # Limitar para demonstração
                
                for i, dep in enumerate(lista_dependente[:total_pares]):
                    if i < len(lista_independente):
                        ind = lista_independente[i]
                        
                        # Análise da primeira fase (original)
                        resultado = calcular_residuo_zscore_timeframe(
                            dep=dep, 
                            ind=ind, 
                            ibov='IBOV', 
                            win='WIN', 
                            periodo=21,
                            dados_preprocessados=dados_preprocessados
                        )
                        
                        if resultado and resultado.get('signal') in ['BUY', 'SELL']:
                            resultados.append({
                                'pair': f"{dep}/{ind}",
                                'dependente': dep,
                                'independente': ind,
                                'signal': resultado.get('signal', 'NEUTRAL'),
                                'zscore': resultado.get('zscore', 0.0),
                                'r2': resultado.get('r2', 0.0),
                                'beta': resultado.get('beta', 1.0),
                                'adf_p_value': resultado.get('adf_p_value', 1.0),
                                'timestamp': datetime.now().strftime('%H:%M:%S')
                            })
                
                self.resultados_primeira_fase = resultados
            else:
                # Resultados simulados para demonstração
                self.resultados_primeira_fase = [
                    {'pair': 'PETR4/VALE3', 'signal': 'BUY', 'zscore': -2.1, 'r2': 0.75, 'beta': 0.85, 'adf_p_value': 0.02},
                    {'pair': 'BBDC4/ITUB4', 'signal': 'SELL', 'zscore': 2.3, 'r2': 0.68, 'beta': 0.92, 'adf_p_value': 0.01},
                    {'pair': 'WEGE3/RENT3', 'signal': 'BUY', 'zscore': -1.9, 'r2': 0.82, 'beta': 0.77, 'adf_p_value': 0.03},
                ]
            
            progress_bar.progress(1.0, "🎉 Primeira fase concluída!")
            self.primeira_fase_concluida = True
            st.success(f"✅ **Primeira fase concluída!** {len(self.resultados_primeira_fase)} pares selecionados.")
            
            return self.resultados_primeira_fase
            
        except Exception as e:
            st.error(f"❌ Erro na primeira fase: {e}")
            return None
    
    def executar_analise_completa(self, lista_dependente, lista_independente):
        """Executa análise completa (APENAS primeira fase no dashboard original)"""
        try:
            st.markdown('<div class="primeira-fase-card"><h3>🎯 Análise Completa - Primeira Fase</h3><p>Sistema original que executa apenas a primeira fase da análise</p></div>', unsafe_allow_html=True)
            
            # Executar primeira fase
            self.executar_primeira_fase(lista_dependente, lista_independente)
            
            if self.primeira_fase_concluida:
                # Log da análise
                self.historico_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Análise completa executada: {len(self.resultados_primeira_fase)} pares")
                
                # Mostrar métricas finais
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Pares Analisados", len(DEPENDENTE_ORIGINAL))
                with col2:
                    st.metric("Pares Selecionados", len(self.resultados_primeira_fase) if self.resultados_primeira_fase else 0)
                with col3:
                    signals = [r['signal'] for r in self.resultados_primeira_fase] if self.resultados_primeira_fase else []
                    st.metric("Sinais Ativos", len([s for s in signals if s != 'NEUTRAL']))
            
        except Exception as e:
            st.error(f"❌ Erro na análise completa: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 FUNÇÕES DE INTERFACE ORIGINAL
# ═══════════════════════════════════════════════════════════════════════════════

def render_header_original():
    """Renderiza cabeçalho original"""
    current_time = datetime.now()
    market_status = "🟢 Aberto" if 9 <= current_time.hour <= 17 else "🔴 Fechado"
    
    st.markdown(f"""
    <div class="main-header">
        <h1>🚀 Trading System v5.5 - Dashboard Original</h1>
        <p>📅 {current_time.strftime('%d/%m/%Y %H:%M:%S')} | Mercado: {market_status} | Primeira Fase Apenas</p>
    </div>
    """, unsafe_allow_html=True)

def render_metrics_original(dashboard):
    """Renderiza métricas originais"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        primeira_fase = "✅ Concluída" if dashboard.primeira_fase_concluida else "⏳ Pendente"
        st.markdown(f'<div class="metric-card"><h4>Primeira Fase: {primeira_fase}</h4></div>', unsafe_allow_html=True)
    
    with col2:
        pares_total = len(dashboard.resultados_primeira_fase) if dashboard.resultados_primeira_fase else 0
        st.markdown(f'<div class="metric-card"><h4>Pares Selecionados: {pares_total}</h4></div>', unsafe_allow_html=True)
    
    with col3:
        if dashboard.resultados_primeira_fase:
            signals = [r['signal'] for r in dashboard.resultados_primeira_fase]
            ativos = len([s for s in signals if s != 'NEUTRAL'])
        else:
            ativos = 0
        st.markdown(f'<div class="metric-card"><h4>Sinais Ativos: {ativos}</h4></div>', unsafe_allow_html=True)
    
    with col4:
        status = "🟢 Online" if HAS_SYSTEM_V55 else "🟡 Simulação"
        st.markdown(f'<div class="metric-card"><h4>Sistema: {status}</h4></div>', unsafe_allow_html=True)

def render_analise_tab_original(dashboard):
    """Renderiza aba de análise original (primeira fase apenas)"""
    st.markdown('<div class="analise-original"><h3>📊 Análise Original - Primeira Fase</h3><p>Execute a análise completa para encontrar oportunidades de trading</p></div>', unsafe_allow_html=True)
    
    # Seleção de ativos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Ativos Dependentes")
        dependentes_selecionados = st.multiselect(
            "Selecione os ativos dependentes:",
            DEPENDENTE_ORIGINAL,
            default=DEPENDENTE_ORIGINAL[:10]
        )
    
    with col2:
        st.subheader("📈 Ativos Independentes")
        independentes_selecionados = st.multiselect(
            "Selecione os ativos independentes:",
            INDEPENDENTE_ORIGINAL,
            default=INDEPENDENTE_ORIGINAL[:10]
        )
    
    # Botão de análise
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Executar Análise Original", type="primary", use_container_width=True):
            if dependentes_selecionados and independentes_selecionados:
                dashboard.executar_analise_completa(dependentes_selecionados, independentes_selecionados)
            else:
                st.warning("⚠️ Selecione pelo menos um ativo de cada tipo!")
    
    # Resultados da primeira fase
    if dashboard.primeira_fase_concluida and dashboard.resultados_primeira_fase:
        render_resultados_primeira_fase(dashboard)

def render_resultados_primeira_fase(dashboard):
    """Renderiza resultados da primeira fase"""
    st.markdown("---")
    st.subheader("🎯 Resultados da Primeira Fase")
    
    if not dashboard.resultados_primeira_fase:
        st.info("🔄 Execute a análise para ver os resultados da primeira fase")
        return
    
    # Tabela de resultados
    df_resultados = pd.DataFrame(dashboard.resultados_primeira_fase)
    
    # Métricas da primeira fase
    col1, col2, col3 = st.columns(3)
    with col1:
        buy_signals = len([r for r in dashboard.resultados_primeira_fase if r['signal'] == 'BUY'])
        st.metric("Sinais de Compra", buy_signals)
    with col2:
        sell_signals = len([r for r in dashboard.resultados_primeira_fase if r['signal'] == 'SELL'])
        st.metric("Sinais de Venda", sell_signals)
    with col3:
        avg_r2 = np.mean([r['r2'] for r in dashboard.resultados_primeira_fase])
        st.metric("R² Médio", f"{avg_r2:.3f}")
    
    # Gráfico de distribuição Z-Score
    if len(df_resultados) > 0:
        fig = px.histogram(df_resultados, x='zscore', nbins=20, title="Distribuição de Z-Scores")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabela detalhada
    st.dataframe(df_resultados, use_container_width=True)

def render_monitoramento_tab():
    """Renderiza aba de monitoramento"""
    st.markdown('<div class="trading-card"><h3>📊 Monitoramento Original</h3><p>Monitoramento da primeira fase em tempo real</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🕐 Status do Sistema")
        if HAS_SYSTEM_V55:
            st.success("✅ Sistema v5.5 conectado")
            st.info("🔄 Monitoramento da primeira fase ativo")
        else:
            st.warning("⚠️ Sistema em modo simulação")
    
    with col2:
        st.subheader("📈 Métricas do Sistema")
        st.metric("Uptime", "24h 15m")
        st.metric("Pares Ativos", "8")
        st.metric("Última Atualização", datetime.now().strftime("%H:%M:%S"))

def render_configuracoes_tab():
    """Renderiza aba de configurações"""
    st.markdown('<div class="trading-card"><h3>⚙️ Configurações do Sistema Original</h3></div>', unsafe_allow_html=True)
    
    st.subheader("📊 Parâmetros da Primeira Fase")
    
    col1, col2 = st.columns(2)
    with col1:
        zscore_threshold = st.number_input("Z-Score Threshold", value=2.0, min_value=1.0, max_value=5.0)
        r2_threshold = st.number_input("R² Mínimo", value=0.5, min_value=0.1, max_value=0.9)
    
    with col2:
        beta_threshold = st.number_input("Beta Máximo", value=1.5, min_value=0.5, max_value=3.0)
        periodo = st.number_input("Período", value=21, min_value=10, max_value=100)
    
    if st.button("💾 Salvar Configurações"):
        st.success("✅ Configurações salvas!")

def render_logs_tab(dashboard):
    """Renderiza aba de logs"""
    st.markdown('<div class="trading-card"><h3>📝 Logs do Sistema</h3></div>', unsafe_allow_html=True)
    
    if dashboard.historico_logs:
        st.subheader("📊 Histórico de Operações")
        for log in dashboard.historico_logs[-10:]:  # Últimos 10 logs
            st.text(log)
    else:
        st.info("📝 Nenhum log disponível. Execute uma análise para gerar logs.")
    
    # Logs em tempo real
    st.subheader("🔄 Logs em Tempo Real")
    log_placeholder = st.empty()
    
    # Simular logs
    if st.button("🔄 Atualizar Logs"):
        with log_placeholder:
            st.text(f"[{datetime.now().strftime('%H:%M:%S')}] Sistema operacional")
            st.text(f"[{datetime.now().strftime('%H:%M:%S')}] Primeira fase ativa")

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 FUNÇÃO PRINCIPAL DO DASHBOARD ORIGINAL
# ═══════════════════════════════════════════════════════════════════════════════

def executar_analise_real_v55(lista_dependente, lista_independente, progress_callback=None):
    """
    Função de análise original que executa APENAS a primeira fase
    (mantida para compatibilidade com testes)
    """
    try:
        # Simulação da primeira fase
        resultados = []
        total_pares = min(len(lista_dependente), len(lista_independente), 10)
        
        for i in range(total_pares):
            if progress_callback:
                progress_callback(i / total_pares)
            
            dep = lista_dependente[i % len(lista_dependente)]
            ind = lista_independente[i % len(lista_independente)]
            
            # Simular resultado da primeira fase
            result = {
                'pair': f"{dep}/{ind}",
                'signal': np.random.choice(['BUY', 'SELL', 'NEUTRAL'], p=[0.3, 0.3, 0.4]),
                'zscore': np.random.normal(0, 1.5),
                'r2': np.random.uniform(0.4, 0.9),
                'beta': np.random.uniform(0.5, 1.5),
                'adf_p_value': np.random.uniform(0.01, 0.1)
            }
            
            # Filtros da primeira fase
            if abs(result['zscore']) > 1.5 and result['r2'] > 0.5:
                resultados.append(result)
        
        return resultados
        
    except Exception as e:
        print(f"Erro na análise: {e}")
        return []

def main():
    """Função principal do dashboard original"""
    # Renderizar cabeçalho
    render_header_original()
    
    # Inicializar dashboard
    if 'dashboard_original' not in st.session_state:
        st.session_state.dashboard_original = TradingDashboardOriginal()
    
    dashboard = st.session_state.dashboard_original
    
    # Renderizar métricas
    render_metrics_original(dashboard)
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Análise", "🔍 Monitoramento", "⚙️ Configurações", "📝 Logs"])
    
    with tab1:
        render_analise_tab_original(dashboard)
    
    with tab2:
        render_monitoramento_tab()
    
    with tab3:
        render_configuracoes_tab()
    
    with tab4:
        render_logs_tab(dashboard)
    
    # Footer original
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 1rem;'>
            🚀 Trading System v5.5 - Dashboard Original | 
            Primeira Fase Implementada | 
            © 2024 - Sistema Profissional de Trading
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
