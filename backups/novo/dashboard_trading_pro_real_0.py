#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard Trading Profissional - Operações Reais MT5
Sistema completo de monitoramento e controle de trading com base em calculo_entradas_v55.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import MetaTrader5 as mt5
import pytz
from datetime import datetime, timedelta, time
import json
import os
import threading
import time as time_module
import io
import random
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# Imports do sistema original
import sys
sys.path.append('.')

# Configuração da página
st.set_page_config(
    page_title="Trading Dashboard Pro - MT5 Real",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para interface profissional
st.markdown("""
<style>
    /* Remove barras brancas e espaços desnecessários */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: none;
    }
    
    /* Remove espaçamentos extras da sidebar */
    .css-1d391kg {
        padding-top: 1rem;
    }
    
    /* Remove espaços em branco acima e abaixo */
    .main .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
    
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2980b9 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: white;
        text-align: center;
    }
    
    .status-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2980b9;
        margin: 0.5rem 0;
    }
    
    .metric-positive { color: #27ae60; font-weight: bold; }
    .metric-negative { color: #e74c3c; font-weight: bold; }
    .metric-neutral { color: #34495e; font-weight: bold; }
    
    .trade-table {
        font-size: 0.85rem;
        background: white;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .log-container {
        background: #2c3e50;
        color: #ecf0f1;
        padding: 1rem;
        border-radius: 8px;
        height: 300px;
        overflow-y: auto;
        font-family: 'Courier New', monospace;
        font-size: 0.8rem;
    }
    
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #dee2e6;
    }
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
            "ordens_enviadas": 0,
            "posicoes_abertas": 0,
            "lucro_diario": 0.0,
            "equity_atual": 0.0,
            "saldo_inicial": 0.0,
            "drawdown_max": 0.0,
            "win_rate": 0.0,
            "sharpe_ratio": 0.0,
            "ultimo_update": None
        }
        self.logs = []
        self.trade_history = []
        self.posicoes_abertas = []
        self.sinais_ativos = []
        self.equity_historico = []
        
        # Configurações padrão do sistema original
        self.dependente = ['ABEV3', 'ALOS3', 'ASAI3','BBAS3', 'BBDC4', 'BBSE3', 'BPAC11', 'BRAP4', 'BRFS3', 'BRKM5', 'CPFE3', 'CPLE6', 'CSAN3','CSNA3', 'CYRE3', 'ELET3', 'ELET6', 'EMBR3', 'ENEV3', 'ENGI11', 'EQTL3', 'EZTC3', 'FLRY3', 'GOAU4', 'HYPE3', 'IGTI11', 'IRBR3', 'ITSA4', 'ITUB4', 'KLBN11', 'MRFG3', 'NTCO3', 'PETR3', 'PETR4', 'PETZ3', 'PRIO3', 'RAIL3', 'RADL3', 'RECV3', 'RENT3', 'RDOR3', 'SANB11', 'SLCE3', 'SMTO3', 'SUZB3', 'TAEE11', 'TIMS3', 'TOTS3', 'UGPA3', 'VALE3', 'VBBR3', 'VIVT3', 'WEGE3', 'YDUQ3']
        self.independente = self.dependente.copy()
        
        self.segmentos = {
            'ABEV3': 'Bebidas', 'ALOS3': 'Saúde', 'ASAI3': 'Varejo Alimentar',
            'BBAS3': 'Bancos', 'BBDC4': 'Bancos', 'BBSE3': 'Seguros',
            'BPAC11': 'Bancos', 'BRAP4': 'Holding', 'BRFS3': 'Alimentos',
            'BRKM5': 'Química', 'CPFE3': 'Energia', 'CPLE6': 'Energia',
            'CSNA3': 'Siderurgia','CYRE3': 'Construção','ELET3': 'Energia',
            'ELET6': 'Energia', 'EMBR3': 'Aeroespacial','ENEV3': 'Energia',
            'ENGI11': 'Energia', 'EQTL3': 'Energia', 'EZTC3': 'Construção',
            'FLRY3': 'Saúde', 'GOAU4': 'Siderurgia','HYPE3': 'Farmacêutica',
            'IGTI11': 'Financeiro','IRBR3': 'Seguros', 'ITSA4': 'Financeiro',
            'ITUB4': 'Bancos', 'KLBN11': 'Papel e Celulose',
            'MRFG3': 'Alimentos', 'NTCO3': 'Higiene/Beleza','PETR3': 'Petróleo',
            'PETR4': 'Petróleo', 'PETZ3': 'Varejo', 'PRIO3': 'Petróleo',
            'RAIL3': 'Logística', 'RADL3': 'Varejo', 'RECV3': 'Petróleo',
            'RENT3': 'Locação', 'RDOR3': 'Saúde', 'SANB11': 'Bancos',
            'SLCE3': 'Agro', 'SMTO3': 'Agro', 'SUZB3': 'Papel e Celulose',
            'TAEE11': 'Energia', 'TIMS3': 'Telecom', 'TOTS3': 'Tecnologia',
            'UGPA3': 'Distribuição','VALE3': 'Mineração','VBBR3': 'Transporte',
            'VIVT3': 'Telecom', 'WEGE3': 'Industrial','YDUQ3': 'Educação'
        }
        
        # Thread para execução do sistema
        self.thread_sistema = None
        
    def conectar_mt5(self, login: int = None, password: str = None, server: str = None) -> bool:
        """Conecta ao MT5"""
        try:
            if not mt5.initialize():
                self.log("❌ Falha ao inicializar MT5")
                return False
                
            if login and password and server:
                if not mt5.login(login, password=password, server=server):
                    self.log(f"❌ Falha no login MT5: {mt5.last_error()}")
                    return False
                    
            account_info = mt5.account_info()
            if account_info:
                self.dados_sistema["saldo_inicial"] = account_info.balance
                self.dados_sistema["equity_atual"] = account_info.equity
                self.mt5_connected = True
                self.log(f"✅ MT5 conectado - Conta: {account_info.login}")
                return True
            else:
                self.log("❌ Falha ao obter informações da conta")
                return False
                
        except Exception as e:
            self.log(f"❌ Erro ao conectar MT5: {str(e)}")
            return False
    
    def log(self, mensagem: str):
        """Adiciona log com timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {mensagem}"
        self.logs.append(log_entry)
        if len(self.logs) > 1000:  # Limita logs
            self.logs = self.logs[-500:]
        print(log_entry)  # Debug
    
    def obter_posicoes_abertas(self) -> List[Dict]:
        """Obtém posições abertas do MT5"""
        if not self.mt5_connected:
            return []
            
        try:
            positions = mt5.positions_get()
            if positions is None:
                return []
                
            posicoes = []
            for pos in positions:
                preco_atual = self.obter_preco_atual(pos.symbol)
                if preco_atual:
                    pl_atual = (preco_atual - pos.price_open) * pos.volume if pos.type == 0 else (pos.price_open - preco_atual) * pos.volume
                else:
                    pl_atual = pos.profit
                    
                posicoes.append({
                    'ticket': pos.ticket,
                    'symbol': pos.symbol,
                    'type': 'COMPRA' if pos.type == 0 else 'VENDA',
                    'volume': pos.volume,
                    'price_open': pos.price_open,
                    'price_current': preco_atual or pos.price_current,
                    'sl': pos.sl,
                    'tp': pos.tp,
                    'profit': pl_atual,
                    'time': datetime.fromtimestamp(pos.time),
                    'magic': pos.magic,
                    'comment': pos.comment
                })
            
            self.posicoes_abertas = posicoes
            self.dados_sistema["posicoes_abertas"] = len(posicoes)
            return posicoes
            
        except Exception as e:
            self.log(f"❌ Erro ao obter posições: {str(e)}")
            return []
    
    def obter_preco_atual(self, symbol: str) -> Optional[float]:
        """Obtém preço atual do símbolo"""
        try:
            tick = mt5.symbol_info_tick(symbol)
            return tick.bid if tick else None
        except:
            return None
    
    def fechar_posicao(self, ticket: int) -> bool:
        """Fecha posição específica"""
        try:
            positions = mt5.positions_get(ticket=ticket)
            if not positions:
                return False
                
            position = positions[0]
            symbol = position.symbol
            volume = position.volume
            
            # Determina tipo de fechamento
            if position.type == mt5.ORDER_TYPE_BUY:
                order_type = mt5.ORDER_TYPE_SELL
                price = mt5.symbol_info_tick(symbol).bid
            else:
                order_type = mt5.ORDER_TYPE_BUY
                price = mt5.symbol_info_tick(symbol).ask
            
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": order_type,
                "position": ticket,
                "price": price,
                "magic": position.magic,
                "comment": "Fechamento manual dashboard",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            result = mt5.order_send(request)
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                self.log(f"✅ Posição {ticket} fechada com sucesso")
                return True
            else:
                self.log(f"❌ Erro ao fechar posição {ticket}: {result.comment}")
                return False
                
        except Exception as e:
            self.log(f"❌ Erro ao fechar posição {ticket}: {str(e)}")
            return False
    
    def atualizar_account_info(self):
        """Atualiza informações da conta"""
        if not self.mt5_connected:
            return
            
        try:
            account_info = mt5.account_info()
            if account_info:
                self.dados_sistema["equity_atual"] = account_info.equity
                equity_entry = {
                    'timestamp': datetime.now(),
                    'equity': account_info.equity,
                    'balance': account_info.balance,
                    'profit': account_info.profit
                }
                self.equity_historico.append(equity_entry)
                
                # Calcula lucro diário
                if self.dados_sistema["saldo_inicial"] > 0:
                    self.dados_sistema["lucro_diario"] = account_info.equity - self.dados_sistema["saldo_inicial"]
                  # Calcula drawdown
                if self.equity_historico:
                    max_equity = max([entry['equity'] for entry in self.equity_historico])
                    current_equity = account_info.equity
                    self.dados_sistema["drawdown_max"] = max(0, (max_equity - current_equity) / max_equity * 100)
                
                self.dados_sistema["ultimo_update"] = datetime.now()
                
        except Exception as e:
            self.log(f"❌ Erro ao atualizar conta: {str(e)}")
      def executar_sistema_principal(self, config: Dict):
        """Executa o sistema principal de trading com análise real"""
        self.log("🚀 Iniciando sistema principal de trading...")
        
        try:
            # Verifica se o sistema de análise real está disponível
            try:
                from calculo_entradas_v55 import calcular_residuo_zscore_timeframe
                self.log("✅ Sistema de análise real carregado com sucesso")
                usar_analise_real = True
            except ImportError as e:
                self.log(f"⚠️ Sistema de análise real não disponível: {str(e)}")
                self.log("📊 Continuando com sistema básico")
                usar_analise_real = False
            
            # Executa sistema principal
            while self.running:
                try:
                    self.dados_sistema["execucoes"] += 1
                    self.log(f"📊 Executando ciclo #{self.dados_sistema['execucoes']}")
                    
                    # Atualiza informações da conta
                    self.atualizar_account_info()
                    
                    # Atualiza posições
                    self.obter_posicoes_abertas()
                    
                    # Executa análise (real ou básica)
                    if usar_analise_real and self.mt5_connected:
                        self.executar_analise_real(config)
                    else:
                        # Sistema básico - apenas verifica posições e atualiza dados
                        self.log("📊 Executando monitoramento básico (sem análise de sinais)")
                    
                    self.log(f"✅ Ciclo #{self.dados_sistema['execucoes']} concluído")
                    
                    # Aguarda próximo ciclo (configurável)
                    intervalo = config.get('intervalo_execucao', 60)
                    time_module.sleep(intervalo)
                    
                except Exception as e:
                    self.log(f"❌ Erro no ciclo: {str(e)}")
                    time_module.sleep(30)
                    
        except Exception as e:
            self.log(f"❌ Erro no sistema principal: {str(e)}")
      def executar_analise_real(self, config: Dict):
        """Executa análise real de pares usando calculo_entradas_v55.py"""
        try:
            # Importa o sistema de análise real
            from calculo_entradas_v55 import calcular_residuo_zscore_timeframe, get_dados_preprocessados
            
            self.log("🔄 Iniciando análise real de pares...")
            
            # Obtém dados históricos via MT5
            ativos_selecionados = config.get('ativos_selecionados', self.dependente[:10])
            timeframe_map = {
                "1 min": mt5.TIMEFRAME_M1,
                "5 min": mt5.TIMEFRAME_M5, 
                "15 min": mt5.TIMEFRAME_M15,
                "30 min": mt5.TIMEFRAME_M30,
                "1 hora": mt5.TIMEFRAME_H1,
                "4 horas": mt5.TIMEFRAME_H4,
                "1 dia": mt5.TIMEFRAME_D1
            }
            
            timeframe_mt5 = timeframe_map.get(config.get('timeframe', '15 min'), mt5.TIMEFRAME_M15)
            periodo_analise = config.get('periodo_analise', 200)
            
            # Coleta dados históricos do MT5
            dados_preprocessados = self.obter_dados_historicos_mt5(ativos_selecionados + ['IBOV'], timeframe_mt5, periodo_analise)
            
            if not dados_preprocessados:
                self.log("❌ Falha ao obter dados históricos do MT5")
                return
            
            # Parâmetros de filtro baseados na configuração
            filter_params = {
                'enable_zscore_filter': config.get('filtro_zscore', True),
                'enable_r2_filter': config.get('filtro_r2', True), 
                'enable_beta_filter': config.get('filtro_beta', True),
                'enable_cointegration_filter': config.get('filtro_cointegração', True),
                'zscore_min_threshold': -config.get('zscore_min', 2.0),
                'zscore_max_threshold': config.get('zscore_max', 2.0),
                'r2_min_threshold': config.get('r2_min', 0.50),
                'beta_max_threshold': 1.5
            }
            
            sinais_detectados = []
            pares_analisados = 0
            
            # Análise de pares
            for dep in ativos_selecionados[:10]:  # Máximo 10 ativos por ciclo
                for ind in self.independente[:5]:  # Máximo 5 independentes por dependente
                    if dep != ind:
                        try:
                            # Executa análise real do par
                            resultado = calcular_residuo_zscore_timeframe(
                                dep=dep,
                                ind=ind, 
                                ibov='IBOV',
                                win=config.get('timeframe', 'M15'),
                                periodo=periodo_analise,
                                dados_preprocessados=dados_preprocessados,
                                **filter_params
                            )
                            
                            pares_analisados += 1
                            
                            if resultado and 'zscore_atual' in resultado:
                                zscore = resultado['zscore_atual']
                                r2 = resultado.get('r2', 0)
                                beta = resultado.get('beta', 0)
                                p_value = resultado.get('p_value', 1)
                                
                                # Verifica se atende aos critérios
                                if (abs(zscore) > config.get('zscore_min', 1.5) and 
                                    r2 > config.get('r2_min', 0.5) and
                                    p_value < 0.05):
                                    
                                    # Calcula confiança baseada nos parâmetros
                                    confianca = min(95, (r2 * 100) * (1 - p_value))
                                    
                                    sinal = {
                                        'par': f"{dep}/{ind}",
                                        'ativo': dep,
                                        'zscore': zscore,
                                        'r2': r2,
                                        'beta': beta,
                                        'p_value': p_value,
                                        'sinal': 'COMPRA' if zscore < -1.5 else 'VENDA',
                                        'confianca': confianca,
                                        'timestamp': datetime.now(),
                                        'preco_atual': self.obter_preco_atual(dep) or 0,
                                        'segmento': self.segmentos.get(dep, 'Outros'),
                                        'status': 'REAL'  # Marca como análise real
                                    }
                                    sinais_detectados.append(sinal)
                                    
                        except Exception as e:
                            self.log(f"⚠️ Erro na análise {dep}/{ind}: {str(e)}")
                            continue
            
            # Atualiza sinais com dados reais
            self.sinais_ativos = sinais_detectados
            self.dados_sistema["pares_processados"] += pares_analisados
            
            if sinais_detectados:
                self.log(f"✅ {len(sinais_detectados)} sinais reais detectados de {pares_analisados} pares analisados")
            else:
                self.log(f"📊 {pares_analisados} pares analisados - nenhum sinal encontrado")
                
        except ImportError as e:
            self.log(f"❌ Erro ao importar sistema de análise: {str(e)}")
            self.log("📊 Voltando para modo de demonstração")
            self.simular_analise_trading(config)
        except Exception as e:
            self.log(f"❌ Erro na análise real: {str(e)}")
            self.log("� Voltando para modo de demonstração") 
            self.simular_analise_trading(config)
    
    def obter_dados_historicos_mt5(self, simbolos: List[str], timeframe, periodo: int) -> Dict:
        """Obtém dados históricos do MT5 para análise"""
        if not self.mt5_connected:
            return {}
            
        dados_preprocessados = {}
        
        try:
            for simbolo in simbolos:
                # Obtém dados históricos
                rates = mt5.copy_rates_from_pos(simbolo, timeframe, 0, periodo)
                
                if rates is not None and len(rates) > 0:
                    df = pd.DataFrame(rates)
                    df['time'] = pd.to_datetime(df['time'], unit='s')
                    df.set_index('time', inplace=True)
                    
                    # Prepara dados no formato esperado
                    dados_preprocessados[simbolo] = {
                        'close': df['close'],
                        'open': df['open'],
                        'high': df['high'],
                        'low': df['low'],
                        'volume': df['tick_volume']
                    }
                    
                else:
                    self.log(f"⚠️ Sem dados históricos para {simbolo}")
                    
        except Exception as e:
            self.log(f"❌ Erro ao obter dados históricos: {str(e)}")
            return {}
            
        return dados_preprocessados
    
    def iniciar_sistema(self, config: Dict):
        """Inicia o sistema de trading"""
        if self.running:
            return False
            
        self.running = True
        self.thread_sistema = threading.Thread(
            target=self.executar_sistema_principal,
            args=(config,),
            daemon=True
        )
        self.thread_sistema.start()
        self.log("✅ Sistema iniciado com sucesso")
        return True
    
    def parar_sistema(self):
        """Para o sistema de trading"""
        self.running = False
        self.log("🛑 Sistema parado")
    
    def exportar_relatorio_excel(self) -> bytes:
        """Exporta relatório para Excel"""
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Resumo geral
            resumo = pd.DataFrame([self.dados_sistema])
            resumo.to_excel(writer, sheet_name='Resumo', index=False)
            
            # Posições abertas
            if self.posicoes_abertas:
                pos_df = pd.DataFrame(self.posicoes_abertas)
                pos_df.to_excel(writer, sheet_name='Posições Abertas', index=False)
            
            # Sinais
            if self.sinais_ativos:
                sinais_df = pd.DataFrame(self.sinais_ativos)
                sinais_df.to_excel(writer, sheet_name='Sinais', index=False)
            
            # Equity histórico
            if self.equity_historico:
                equity_df = pd.DataFrame(self.equity_historico)
                equity_df.to_excel(writer, sheet_name='Equity Histórico', index=False)
            
            # Logs
            logs_df = pd.DataFrame({'Log': self.logs})
            logs_df.to_excel(writer, sheet_name='Logs', index=False)
        
        output.seek(0)
        return output.getvalue()

# Inicializa sistema global
if 'trading_system' not in st.session_state:
    st.session_state.trading_system = TradingSystemReal()

def render_header():
    """Renderiza header principal com status das funcionalidades"""
    st.markdown("""
    <div class="main-header">
        <h1>🏆 Trading Dashboard Professional - MT5 Real Operations</h1>
        <p>Sistema Completo de Monitoramento e Controle de Trading Algorítmico</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Status das funcionalidades - Indicador visual
    st.markdown("### 🎛️ Status das Funcionalidades")
    
    col1, col2, col3, col4 = st.columns(4)
    
    sistema = st.session_state.trading_system
    
    with col1:
        status_mt5 = "✅ CONECTADO" if sistema.mt5_connected else "🔴 DESCONECTADO"
        st.markdown(f"""
        **🔗 Conexão MT5**  
        {status_mt5}  
        *Dados reais*
        """)
    
    with col2:
        st.markdown(f"""
        **💰 Informações Financeiras**  
        ✅ REAL  
        *Saldo, equity, posições*
        """)
    
    with col3:
        st.markdown(f"""
        **📡 Sinais de Trading**  
        ⚠️ SIMULADO  
        *Análise em desenvolvimento*
        """)
    
    with col4:
        st.markdown(f"""
        **📊 Relatórios/Exportação**  
        ✅ REAL  
        *Dados reais do sistema*
        """)
    
    # Link para documentação detalhada
    with st.expander("📋 Ver Status Completo das Funcionalidades"):
        st.markdown("""
        **🟢 FUNCIONALIDADES REAIS (70%):**
        - ✅ Conexão e autenticação MT5
        - ✅ Saldo, equity, margem (dados reais)
        - ✅ Posições abertas e histórico 
        - ✅ Preços em tempo real
        - ✅ Fechamento de posições
        - ✅ Exportação Excel/JSON
        - ✅ Interface e controles
        
        **⚠️ FUNCIONALIDADES SIMULADAS (25%):**
        - ⚠️ Geração de sinais de trading
        - ⚠️ Análise técnica (Z-Score, R²)
        - ⚠️ Sugestões de operação
        
        **❌ NÃO IMPLEMENTADO (5%):**
        - ❌ Execução automática de trades
        - ❌ Gestão de risco avançada
        
        **📖 Documentação completa:** `STATUS_FUNCIONALIDADES_REAL_VS_SIMULACAO.md`
        """)
    
    st.markdown("---")

def render_sidebar():
    """Renderiza sidebar com configurações"""
    st.sidebar.markdown("## ⚙️ Configurações do Sistema")
    
    # Conexão MT5
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.markdown("### 🔌 Conexão MT5")
    
    mt5_login = st.sidebar.number_input("Login", value=0, format="%d")
    mt5_password = st.sidebar.text_input("Senha", type="password")
    mt5_server = st.sidebar.text_input("Servidor", value="")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🔗 Conectar"):
            if st.session_state.trading_system.conectar_mt5(mt5_login, mt5_password, mt5_server):
                st.success("✅ Conectado!")
            else:
                st.error("❌ Falha na conexão")
    
    with col2:
        connection_status = "🟢 Conectado" if st.session_state.trading_system.mt5_connected else "🔴 Desconectado"
        st.markdown(f"**Status:** {connection_status}")
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
      # Seleção de Ativos
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.markdown("### 📊 Ativos Monitorados")
    
    # Filtro por segmento
    segmentos_disponiveis = list(set(st.session_state.trading_system.segmentos.values()))
    segmentos_disponiveis.sort()  # Ordena alfabeticamente
    
    # Opção de selecionar todos os segmentos
    selecionar_todos_segmentos = st.sidebar.checkbox("Selecionar Todos os Segmentos")
    
    if selecionar_todos_segmentos:
        segmentos_selecionados = segmentos_disponiveis
    else:
        segmentos_selecionados = st.sidebar.multiselect(
            "Segmentos", 
            segmentos_disponiveis,
            default=segmentos_disponiveis[:5]
        )
    
    # Ativos por segmento selecionado
    ativos_filtrados = [
        ativo for ativo, segmento in st.session_state.trading_system.segmentos.items()
        if segmento in segmentos_selecionados
    ]
    
    # Opção de selecionar todos os ativos
    selecionar_todos_ativos = st.sidebar.checkbox("Selecionar Todos os Ativos")
    
    if selecionar_todos_ativos:
        ativos_selecionados = ativos_filtrados
    else:
        ativos_selecionados = st.sidebar.multiselect(
            "Ativos Específicos",
            ativos_filtrados,
            default=ativos_filtrados[:10] if ativos_filtrados else []
        )
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Parâmetros de Trading
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.markdown("### 🎯 Parâmetros de Trading")
    
    timeframe = st.sidebar.selectbox(
        "Timeframe",
        ["1 min", "5 min", "15 min", "30 min", "1 hora", "4 horas", "1 dia"],
        index=2
    )
    
    periodo_analise = st.sidebar.slider("Período de Análise", 50, 300, 200)
    
    zscore_threshold = st.sidebar.slider(
        "Limiar Z-Score", 
        0.5, 3.0, 2.0, 0.1,
        help="Limiar mínimo para considerar sinais"
    )
    
    max_posicoes = st.sidebar.slider("Máx. Posições Simultâneas", 1, 20, 6)
    
    # Filtros
    st.sidebar.markdown("**Filtros Avançados:**")
    filtro_cointegração = st.sidebar.checkbox("Cointegração", value=True)
    filtro_r2 = st.sidebar.checkbox("R² Mínimo", value=True)
    filtro_beta = st.sidebar.checkbox("Beta Máximo", value=True)
    filtro_zscore = st.sidebar.checkbox("Z-Score Range", value=True)
    
    r2_min = st.sidebar.slider("R² Mínimo", 0.1, 0.9, 0.5, 0.05)
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Controles do Sistema
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.markdown("### 🎮 Controles")
    
    config = {
        'ativos_selecionados': ativos_selecionados,
        'timeframe': timeframe,
        'periodo_analise': periodo_analise,
        'zscore_min': zscore_threshold,
        'zscore_max': zscore_threshold,
        'max_posicoes': max_posicoes,
        'filtro_cointegração': filtro_cointegração,
        'filtro_r2': filtro_r2,
        'filtro_beta': filtro_beta,
        'filtro_zscore': filtro_zscore,
        'r2_min': r2_min,
        'intervalo_execucao': 60
    }
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("▶️ Iniciar Sistema", type="primary"):
            if st.session_state.trading_system.iniciar_sistema(config):
                st.success("Sistema Iniciado!")
            else:
                st.warning("Sistema já está rodando")
    
    with col2:
        if st.button("⏹️ Parar Sistema"):
            st.session_state.trading_system.parar_sistema()
            st.success("Sistema Parado!")
    
    # Botões de utilidade
    if st.sidebar.button("💾 Salvar Perfil"):
        st.sidebar.success("Perfil salvo!")
    
    if st.sidebar.button("🔄 Reset Completo"):
        st.session_state.trading_system = TradingSystemReal()
        st.sidebar.success("Sistema resetado!")
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    return config

def render_status_cards():
    """Renderiza cartões de status"""
    sistema = st.session_state.trading_system
    dados = sistema.dados_sistema
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Pares Processados",
            f"{dados['pares_processados']:,}",
            delta=f"+{dados['execucoes']}"
        )
    
    with col2:
        st.metric(
            "Posições Abertas",
            dados['posicoes_abertas'],
            delta=None
        )
    
    with col3:
        equity_delta = dados['equity_atual'] - dados['saldo_inicial'] if dados['saldo_inicial'] > 0 else 0
        st.metric(
            "Equity Atual",
            f"R$ {dados['equity_atual']:,.2f}",
            delta=f"R$ {equity_delta:,.2f}"
        )
    
    with col4:
        lucro_cor = "normal" if dados['lucro_diario'] >= 0 else "inverse"
        st.metric(
            "Lucro/Prejuízo Diário",
            f"R$ {dados['lucro_diario']:,.2f}",
            delta=f"{(dados['lucro_diario']/dados['saldo_inicial']*100) if dados['saldo_inicial'] > 0 else 0:.2f}%"
        )
    
    # Segunda linha de métricas
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric("Win Rate", f"{dados['win_rate']:.1f}%")
    
    with col6:
        st.metric("Sharpe Ratio", f"{dados['sharpe_ratio']:.2f}")
    
    with col7:
        st.metric("Drawdown Máx.", f"{dados['drawdown_max']:.2f}%")
    
    with col8:
        ultimo_update = dados['ultimo_update'].strftime("%H:%M:%S") if dados['ultimo_update'] else "Nunca"
        st.metric("Última Atualização", ultimo_update)

def render_equity_chart():
    """Renderiza gráfico de equity com dados reais do MT5"""
    sistema = st.session_state.trading_system
    
    # Indicador de status da funcionalidade
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 📈 Curva de Equity em Tempo Real")
    with col2:
        if sistema.mt5_connected:
            st.markdown("✅ **REAL**", help="Dados de equity obtidos em tempo real do MetaTrader 5")
        else:
            st.markdown("🔴 **OFFLINE**", help="MT5 desconectado - sem dados reais")
    
    if not sistema.equity_historico:
        if sistema.mt5_connected:
            st.info("📊 Aguardando dados de equity... Execute o sistema para coletar dados.")
        else:
            st.warning("🔌 Conecte ao MT5 para visualizar curva de equity real")
        return
    
    df_equity = pd.DataFrame(sistema.equity_historico)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_equity['timestamp'],
        y=df_equity['equity'],
        mode='lines+markers',
        name='Equity (Real)',
        line=dict(color='#2980b9', width=2),
        marker=dict(size=4)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_equity['timestamp'],
        y=df_equity['balance'],
        mode='lines',
        name='Balance (Real)',
        line=dict(color='#27ae60', width=1, dash='dash')
    ))
    
    fig.update_layout(
        title="📈 Curva de Equity - Dados Reais MT5",
        xaxis_title="Tempo",
        yaxis_title="Valor (R$)",
        hovermode='x unified',
        showlegend=True,
        height=400,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_positions_table():
    """Renderiza tabela de posições abertas"""
    sistema = st.session_state.trading_system
    posicoes = sistema.obter_posicoes_abertas()
    
    # Indicador de status da funcionalidade
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 💼 Posições Abertas")
    with col2:
        if sistema.mt5_connected:
            st.markdown("✅ **REAL**", help="Dados obtidos em tempo real do MetaTrader 5")
        else:
            st.markdown("🔴 **OFFLINE**", help="MT5 desconectado - sem dados reais")
    
    if not posicoes:
        if sistema.mt5_connected:
            st.info("💼 Nenhuma posição aberta no momento")
        else:
            st.warning("🔌 Conecte ao MT5 para visualizar posições reais")
        return
    
    # Converte para DataFrame
    df_pos = pd.DataFrame(posicoes)
    
    # Formata valores
    df_pos['profit_formatted'] = df_pos['profit'].apply(lambda x: f"R$ {x:,.2f}")
    df_pos['profit_color'] = df_pos['profit'].apply(lambda x: "🟢" if x >= 0 else "🔴")
    
    # Seleciona colunas para exibição
    cols_display = ['symbol', 'type', 'volume', 'price_open', 'price_current', 'sl', 'tp', 'profit_formatted', 'time']
    df_display = df_pos[cols_display].copy()
    
    # Renomeia colunas
    df_display.columns = ['Ativo', 'Tipo', 'Volume', 'Preço Entrada', 'Preço Atual', 'Stop Loss', 'Take Profit', 'P/L', 'Horário']
    
    # Exibe tabela
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )
    
    # Botões de ação
    if sistema.mt5_connected:
        st.markdown("**Ações Rápidas:**")
        cols_actions = st.columns(len(posicoes))
        
        for i, (col, pos) in enumerate(zip(cols_actions, posicoes)):
            with col:
                if st.button(f"❌ Fechar {pos['symbol']}", key=f"close_{pos['ticket']}"):
                    if sistema.fechar_posicao(pos['ticket']):
                        st.success(f"Posição {pos['symbol']} fechada!")
                        st.rerun()
                    else:
                        st.error("Erro ao fechar posição")

def render_signals_table():
    """Renderiza tabela de sinais de trading"""
    sistema = st.session_state.trading_system
    
    # Indicador de status da funcionalidade
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 📡 Sinais de Trading Ativos")
    with col2:
        st.markdown("⚠️ **SIMULADO**", help="Esta funcionalidade está em modo demonstração. Os sinais são gerados aleatoriamente para fins de teste.")
    
    if not sistema.sinais_ativos:
        st.info("📡 Aguardando sinais de trading...")
        st.warning("🔧 **Próxima atualização:** Integração com análise real baseada em `calculo_entradas_v55.py` e modelo IA.")
        return
    
    df_sinais = pd.DataFrame(sistema.sinais_ativos)
    
    # Formata colunas
    df_sinais['confianca_formatted'] = df_sinais['confianca'].apply(lambda x: f"{x:.1f}%")
    df_sinais['zscore_formatted'] = df_sinais['zscore'].apply(lambda x: f"{x:.2f}")
    df_sinais['r2_formatted'] = df_sinais['r2'].apply(lambda x: f"{x:.3f}")
    df_sinais['preco_formatted'] = df_sinais['preco_atual'].apply(lambda x: f"R$ {x:.2f}")
    
    # Cores por sinal
    df_sinais['sinal_color'] = df_sinais['sinal'].apply(lambda x: "🟢" if x == "COMPRA" else "🔴")
    
    # Seleciona colunas
    cols_display = ['par', 'sinal', 'zscore_formatted', 'r2_formatted', 'confianca_formatted', 'preco_formatted', 'segmento', 'timestamp']
    df_display = df_sinais[cols_display].copy()
    
    df_display.columns = ['Par', 'Sinal', 'Z-Score', 'R²', 'Confiança', 'Preço', 'Segmento', 'Timestamp']
    
    # Ordena por confiança
    df_display = df_display.sort_values('Confiança', ascending=False)
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )

def render_profit_distribution():
    """Renderiza distribuição de lucros/prejuízos simulada"""
    
    # Indicador de status da funcionalidade
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 📊 Distribuição de Resultados por Trade")
    with col2:
        st.markdown("⚠️ **SIMULADO**", help="Dados de demonstração. Será substituído por histórico real de trades do MT5.")
    
    # Simula dados de trades para demonstração
    np.random.seed(42)
    trades_results = np.random.normal(50, 200, 100)  # Média R$ 50, desvio R$ 200
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=trades_results,
        nbinsx=20,
        name="Distribuição P/L (Demo)",
        marker_color='lightblue',
        opacity=0.7
    ))
    
    # Adiciona linhas de threshold
    fig.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="Break Even")
    fig.add_vline(x=np.mean(trades_results), line_dash="dash", line_color="green", annotation_text="Média")
    
    fig.update_layout(
        title="📊 Distribuição de Resultados - Simulação Demo",
        xaxis_title="Lucro/Prejuízo (R$)",
        yaxis_title="Frequência",
        height=400,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("🔧 **Próxima atualização:** Esta análise será baseada no histórico real de trades do MT5.")

def render_trade_history():
    """Renderiza histórico de trades"""
    st.markdown("### 📋 Histórico de Trades")
    
    # Filtros de período
    col1, col2, col3 = st.columns(3)
    
    with col1:
        data_inicio = st.date_input("Data Início", value=datetime.now().date() - timedelta(days=30))
    
    with col2:
        data_fim = st.date_input("Data Fim", value=datetime.now().date())
    
    with col3:
        filtro_resultado = st.selectbox("Resultado", ["Todos", "Lucro", "Prejuízo"])
    
    # Simula dados para demonstração
    trades_simulados = []
    for i in range(50):
        resultado = np.random.normal(50, 200)
        trades_simulados.append({
            'Par': f"PETR4/VALE3",
            'Tipo': np.random.choice(['COMPRA', 'VENDA']),
            'Data Entrada': datetime.now() - timedelta(days=np.random.randint(1, 30)),
            'Data Saída': datetime.now() - timedelta(days=np.random.randint(0, 29)),
            'Preço Entrada': round(np.random.uniform(20, 100), 2),
            'Preço Saída': round(np.random.uniform(20, 100), 2),
            'Resultado': round(resultado, 2),
            'Duração': f"{np.random.randint(1, 1440)} min",
            'Motivo': np.random.choice(['Take Profit', 'Stop Loss', 'Manual', 'Timeout']),
            'Comentário': 'Trade automático'
        })
    
    df_trades = pd.DataFrame(trades_simulados)
    
    # Aplica filtros
    if filtro_resultado == "Lucro":
        df_trades = df_trades[df_trades['Resultado'] > 0]
    elif filtro_resultado == "Prejuízo":
        df_trades = df_trades[df_trades['Resultado'] < 0]
    
    st.dataframe(df_trades, use_container_width=True, hide_index=True)
    
    # Estatísticas do período
    if not df_trades.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Trades", len(df_trades))
        
        with col2:
            trades_lucro = len(df_trades[df_trades['Resultado'] > 0])
            win_rate = (trades_lucro / len(df_trades)) * 100
            st.metric("Win Rate", f"{win_rate:.1f}%")
        
        with col3:
            resultado_total = df_trades['Resultado'].sum()
            st.metric("Resultado Total", f"R$ {resultado_total:,.2f}")
        
        with col4:
            resultado_medio = df_trades['Resultado'].mean()
            st.metric("Resultado Médio", f"R$ {resultado_medio:.2f}")

def render_logs():
    """Renderiza logs do sistema"""
    sistema = st.session_state.trading_system
    
    st.markdown("### 📝 Log de Eventos do Sistema")
    
    # Container com scroll para logs
    if sistema.logs:
        logs_text = "\n".join(sistema.logs[-50:])  # Últimos 50 logs
        st.text_area(
            "Logs",
            value=logs_text,
            height=300,
            disabled=True,
            label_visibility="collapsed"
        )
    else:
        st.info("Nenhum log disponível ainda")
    
    # Botão para limpar logs
    if st.button("🗑️ Limpar Logs"):
        sistema.logs.clear()
        st.rerun()

def render_export_section():
    """Renderiza seção de exportação"""
    st.markdown("### 📤 Exportação de Relatórios")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Exportar Excel", use_container_width=True):
            try:
                excel_data = st.session_state.trading_system.exportar_relatorio_excel()
                st.download_button(
                    label="💾 Download Excel",
                    data=excel_data,
                    file_name=f"relatorio_trading_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Erro ao gerar Excel: {str(e)}")
    
    with col2:
        if st.button("📋 Relatório PDF", use_container_width=True):
            st.info("Funcionalidade PDF em desenvolvimento")
    
    with col3:
        if st.button("📈 Relatório Diário", use_container_width=True):
            st.info("Funcionalidade de relatório diário em desenvolvimento")

def main():
    """Função principal do dashboard"""
    # Header
    render_header()
    
    # Sidebar com configurações
    config = render_sidebar()
    
    # Status da última atualização no header
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.session_state.trading_system.dados_sistema['ultimo_update']:
            ultima_atualizacao = st.session_state.trading_system.dados_sistema['ultimo_update'].strftime("%H:%M:%S")
            st.markdown(f"**Última atualização:** {ultima_atualizacao}")
    
    # Cartões de status
    render_status_cards()
    
    # Botões de exportação no topo
    render_export_section()
    
    st.markdown("---")
    
    # Painéis principais
    tab1, tab2, tab3 = st.tabs(["📊 Gráficos e Análises", "📡 Sinais e Posições", "📋 Histórico e Logs"])
    
    with tab1:
        # Gráfico de equity
        render_equity_chart()
        
        st.markdown("---")
        
        # Distribuição de resultados
        render_profit_distribution()
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            render_signals_table()
        
        with col2:
            render_positions_table()
    
    with tab3:
        # Histórico de trades
        render_trade_history()
        
        st.markdown("---")
        
        # Logs do sistema
        render_logs()
    
    # Auto-refresh a cada 30 segundos se o sistema estiver rodando
    if st.session_state.trading_system.running:
        time_module.sleep(1)  # Pequena pausa para não sobrecarregar
        st.rerun()

if __name__ == "__main__":
    main()
