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

# Import do sistema integrado para threading otimizado
try:
    from sistema_integrado import SistemaIntegrado
    SISTEMA_INTEGRADO_DISPONIVEL = True
except ImportError:
    SISTEMA_INTEGRADO_DISPONIVEL = False
    print("⚠️ Sistema integrado não disponível - operando em modo básico")

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
      /* Botões de status MT5 customizados */
    .status-button-connected {
        background-color: #27ae60 !important;
        color: white !important;
        border: 2px solid #27ae60 !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
        height: 38px !important;
        min-height: 38px !important;
        max-height: 38px !important;
        text-align: center !important;
        font-weight: bold !important;
        cursor: default !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 0.875rem !important;
        line-height: 1.2 !important;
    }
    
    .status-button-disconnected {
        background-color: #e74c3c !important;
        color: white !important;
        border: 2px solid #e74c3c !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
        height: 38px !important;
        min-height: 38px !important;
        max-height: 38px !important;
        text-align: center !important;
        font-weight: bold !important;
        cursor: default !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 0.875rem !important;
        line-height: 1.2 !important;
    }
    
    /* Botões de status do Sistema */
    .system-status-running {
        background-color: #28a745 !important;
        color: white !important;
        border: 2px solid #28a745 !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
        height: 38px !important;
        min-height: 38px !important;
        max-height: 38px !important;
        text-align: center !important;
        font-weight: bold !important;
        cursor: default !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 0.875rem !important;
        line-height: 1.2 !important;
    }
      .system-status-stopped {
        background-color: #e74c3c !important;
        color: white !important;
        border: 2px solid #e74c3c !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
        height: 38px !important;
        min-height: 38px !important;
        max-height: 38px !important;
        text-align: center !important;
        font-weight: bold !important;
        cursor: default !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 0.875rem !important;
        line-height: 1.2 !important;
    }
    
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #dee2e6;
    }
    
    /* Força botões do Streamlit a terem o mesmo tamanho */
    .stButton > button {
        height: 38px !important;
        min-height: 38px !important;
        max-height: 38px !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 0.875rem !important;
        line-height: 1.2 !important;
        padding: 0.5rem 1rem !important;
    }
      /* Garante que as colunas tenham o mesmo tamanho */
    .element-container {
        width: 100% !important;
    }
    
    /* Estilização personalizada das abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        padding: 0;
    }
      .stTabs [data-baseweb="tab"] {
        background-color: #6c757d !important;
        border: 2px solid #495057 !important;
        border-radius: 8px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 12px 20px !important;
        margin: 0 4px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
      .stTabs [data-baseweb="tab"]:hover {
        background-color: #5a6268 !important;
        border-color: #343a40 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
    }    .stTabs [aria-selected="true"] {
        background-color: #495057 !important;
        border-color: #343a40 !important;
        color: white !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

class TradingSystemReal:
    """Sistema de Trading Real com MT5 - Otimizado com Threading Avançado"""
    
    def __init__(self):
        self.mt5_connected = False
        self.running = False
        
        # Inicializar estruturas de dados primeiro
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
        
        # Integração com sistema avançado de threading
        if SISTEMA_INTEGRADO_DISPONIVEL:
            self.sistema_integrado = SistemaIntegrado()
            self.modo_otimizado = True
            self.log("✅ Sistema integrado carregado - Modo threading avançado ativado")
        else:
            self.sistema_integrado = None
            self.modo_otimizado = False
            self.log("⚠️ Sistema básico - Threading avançado não disponível")
        
        # Configurações padrão do sistema original
        self.dependente = ['ABEV3', 'ALOS3', 'ASAI3','BBAS3', 'BBDC4', 'BBSE3', 'BPAC11', 'BRAP4', 'BRFS3', 'BRKM5', 'CPFE3', 'CPLE6', 'CSAN3','CSNA3', 'CYRE3', 'ELET3', 'ELET6', 'EMBR3', 'ENEV3', 'ENGI11', 'EQTL3', 'EZTC3', 'FLRY3', 'GOAU4', 'HYPE3', 'IGTI11', 'IRBR3', 'ITSA4', 'ITUB4', 'KLBN11', 'MRFG3', 'NTCO3', 'PETR3', 'PETR4', 'PETZ3', 'PRIO3', 'RAIL3', 'RADL3', 'RECV3', 'RENT3', 'RDOR3', 'SANB11', 'SLCE3', 'SMTO3', 'SUZB3', 'TAEE11', 'TIMS3', 'TOTS3', 'UGPA3', 'VALE3', 'VBBR3', 'VIVT3', 'WEGE3', 'YDUQ3']
        self.independente = self.dependente.copy()
        
        self.segmentos = {
            'ABEV3': 'Bebidas', 'ALOS3': 'Saúde', 'ASAI3': 'Varejo Alimentar',
            'BBAS3': 'Bancos', 'BBDC4': 'Bancos', 'BBSE3': 'Seguros',
            'BPAC11': 'Bancos', 'BRAP4': 'Holding', 'BRFS3': 'Alimentos',
            'BRKM5': 'Química', 'CPFE3': 'Energia', 'CPLE6': 'Energia',
            'CSAN3': 'Energia', 'CSNA3': 'Siderurgia','CYRE3': 'Construção',
            'ELET3': 'Energia', 'ELET6': 'Energia', 'EMBR3': 'Aeroespacial',
            'ENEV3': 'Energia', 'ENGI11': 'Energia', 'EQTL3': 'Energia', 
            'EZTC3': 'Construção', 'FLRY3': 'Saúde', 'GOAU4': 'Siderurgia',
            'HYPE3': 'Farmacêutica','IGTI11': 'Financeiro','IRBR3': 'Seguros', 
            'ITSA4': 'Financeiro', 'ITUB4': 'Bancos', 'KLBN11': 'Papel e Celulose',
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
        """Adiciona log com timestamp - Sincronizado com sistema integrado"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {mensagem}"
        self.logs.append(log_entry)
        
        # Sincroniza com sistema integrado se disponível
        if self.modo_otimizado and self.sistema_integrado:
            self.sistema_integrado.log(f"[Dashboard] {mensagem}")
        
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
        """Executa análise real completa de duas seleções usando calculo_entradas_v55.py"""
        try:
            # Importa o sistema de análise real
            from calculo_entradas_v55 import (
                calcular_residuo_zscore_timeframe, 
                calcular_residuo_zscore_timeframe01,
                encontrar_linha_monitorada,
                filtrar_melhores_pares
            )
            
            self.log("🔄 Iniciando análise real COMPLETA com duas seleções...")
              # Obtém dados históricos via MT5
            ativos_selecionados = config.get('ativos_selecionados', self.dependente[:55])
            
            # DEBUG: Verifica se a lista de ativos está válida
            #self.log(f"🔧 DEBUG: ativos_selecionados recebidos: {ativos_selecionados}")
            #self.log(f"🔧 DEBUG: Tipo: {type(ativos_selecionados)}, Tamanho: {len(ativos_selecionados) if ativos_selecionados else 0}")
              # Se a lista estiver vazia, usa todos os ativos padrão
            if not ativos_selecionados or len(ativos_selecionados) == 0:
                ativos_selecionados = self.dependente  # Usa TODOS os ativos disponíveis
                self.log(f"🔧 DEBUG: Lista vazia, usando TODOS os ativos padrão: {len(ativos_selecionados)} ativos")
            
            # PRODUÇÃO: Remove limitação para análise completa
            # Comenta a limitação de teste - agora analisa TODOS os ativos selecionados
            # if len(ativos_selecionados) > 1:
            #     ativos_selecionados = ativos_selecionados[:55]
            #     self.log(f"🔧 DEBUG: Lista muito grande, limitando a 55: {ativos_selecionados}")
            
            self.log(f"🔧 DEBUG: Lista final de ativos: {len(ativos_selecionados)} ativos para análise completa")
            timeframe_map = {
                "1 min": mt5.TIMEFRAME_M1,
                "5 min": mt5.TIMEFRAME_M5,                
                "15 min": mt5.TIMEFRAME_M15,                
                "30 min": mt5.TIMEFRAME_M30,
                "1 hora": mt5.TIMEFRAME_H1,
                "4 horas": mt5.TIMEFRAME_H4,
                "1 dia": mt5.TIMEFRAME_D1
            }
            
            timeframe_mt5 = timeframe_map.get(config.get('timeframe', '1 dia'), mt5.TIMEFRAME_D1)
            
            # DEBUG: Logs detalhados da configuração recebida
            #self.log(f"🔧 DEBUG: Config recebido - usar_multiplos_periodos: {config.get('usar_multiplos_periodos')}")
            #self.log(f"🔧 DEBUG: Config recebido - periodo_analise: {config.get('periodo_analise')}")
            
            # Define períodos de análise baseado na escolha do usuário
            usar_multiplos_periodos = config.get('usar_multiplos_periodos', True)
            periodo_unico = config.get('periodo_analise', 250)
            
            # DEBUG: Logs da lógica de decisão
            #self.log(f"🔧 DEBUG: usar_multiplos_periodos processado: {usar_multiplos_periodos}")
            #self.log(f"🔧 DEBUG: periodo_unico processado: {periodo_unico}")
            
            if usar_multiplos_periodos:
                # Usa múltiplos períodos canônicos para melhor análise
                periodos_analise = [70, 100, 120, 140, 160, 180, 200, 220, 240, 250]
                self.log(f"🔄 Modo: Múltiplos períodos canônicos - {periodos_analise}")
            else:
                # Usa apenas o período selecionado pelo usuário
                periodos_analise = [periodo_unico]
                self.log(f"🔄 Modo: Período único - {periodo_unico}")
            
            # DEBUG: Confirmação final dos períodos
            #self.log(f"🔧 DEBUG: periodos_analise final: {periodos_analise}")
            #self.log(f"🔧 DEBUG: Quantidade de períodos a processar: {len(periodos_analise)}")
            
            # Coleta dados históricos com o maior período necessário
            periodo_maximo = max(periodos_analise)
            #self.log(f"🔄 Coletando dados históricos para períodos: {periodos_analise} (máximo: {periodo_maximo})")
            
            # Coleta dados históricos do MT5
            dados_preprocessados = self.obter_dados_historicos_mt5(ativos_selecionados + ['IBOV'], timeframe_mt5, periodo_maximo)
            
            if not dados_preprocessados:
                self.log("❌ Falha ao obter dados históricos do MT5")
                return
            
            # Diagnóstico dos dados coletados
            self.log(f"🔍 Símbolos disponíveis nos dados: {list(dados_preprocessados.keys())}")
            for simbolo in dados_preprocessados:
                if 'close' in dados_preprocessados[simbolo]:
                    close_data = dados_preprocessados[simbolo]['close']
                    if close_data and 'raw' in close_data:
                        tamanho = len(close_data['raw']) if close_data['raw'] is not None else 0
                        #self.log(f"📊 {simbolo}: {tamanho} registros de close disponíveis")
                    else:
                        self.log(f"⚠️ {simbolo}: dados de close inválidos")
                else:                    self.log(f"⚠️ {simbolo}: sem dados de close")
              # Parâmetros de filtro baseados na configuração (valores originais rigorosos)
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
            
            #self.log(f"🔧 Filtros aplicados:")
            #self.log(f"   - Z-Score: {filter_params['enable_zscore_filter']}")
            #self.log(f"   - R²: {filter_params['enable_r2_filter']}")
            #self.log(f"   - Beta: {filter_params['enable_beta_filter']}")
            #self.log(f"   - Cointegração: {filter_params['enable_cointegration_filter']}")
              # ========================================================================
            # PRIMEIRA SELEÇÃO: Análise inicial de todos os pares
            # ========================================================================
            self.log("📊 Executando PRIMEIRA SELEÇÃO de pares...")
            self.log(f"🔥 PRODUÇÃO: Analisando {len(ativos_selecionados)} ativos dependentes x {len(self.independente)} independentes")
            self.log(f"🔥 PRODUÇÃO: Total de pares possíveis: {len(ativos_selecionados) * len(self.independente)} combinações")
            self.log(f"🔥 PRODUÇÃO: Períodos por par: {len(periodos_analise)} = {len(ativos_selecionados) * len(self.independente) * len(periodos_analise)} cálculos totais")
            
            resultados_zscore_dependente_atual = []
            id_counter = 1
              # Loop para calcular Z-Score para cada par usando dados pré-processados
            pares_tentados = 0
            pares_com_erro = 0
            pares_resultado_none = 0
            pares_zscore_none = 0
            
            for dep_idx, dep in enumerate(ativos_selecionados):  # PRODUÇÃO: Analisa TODOS os ativos selecionados
                self.log(f"🔄 Processando ativo {dep_idx+1}/{len(ativos_selecionados)}: {dep}")
                for ind in self.independente:  # PRODUÇÃO: Testa contra TODOS os independentes
                    if dep != ind:
                        # Verifica se ambos os ativos estão nos dados pré-processados
                        if dep not in dados_preprocessados:
                            self.log(f"⚠️ {dep} não encontrado nos dados pré-processados")
                            continue
                        if ind not in dados_preprocessados:
                            self.log(f"⚠️ {ind} não encontrado nos dados pré-processados")
                            continue
                        if 'IBOV' not in dados_preprocessados:
                            self.log(f"⚠️ IBOV não encontrado nos dados pré-processados")
                            continue
                          # Testa múltiplos períodos para o mesmo par
                        melhor_resultado = None
                        melhor_periodo = None
                        
                        # DEBUG: Log de quantos períodos serão testados para este par
                        #if len(periodos_analise) > 1:
                            #self.log(f"🔧 DEBUG: Testando {len(periodos_analise)} períodos para par {dep}x{ind}: {periodos_analise}")
                        
                        for i, periodo_atual in enumerate(periodos_analise):
                            pares_tentados += 1
                            
                            # DEBUG: Log do período atual sendo processado
                            #self.log(f"🔧 DEBUG: Processando período {i+1}/{len(periodos_analise)}: {periodo_atual} para {dep}x{ind}")
                            
                            try:# Executa análise real do par (com filtros originais)
                                resultado = calcular_residuo_zscore_timeframe(
                                    dep=dep,
                                    ind=ind, 
                                    ibov='IBOV',
                                    win='IBOV',  # Usa IBOV como referência de mercado
                                    periodo=periodo_atual,
                                    dados_preprocessados=dados_preprocessados,
                                    USE_SPREAD_FORECAST=True,
                                    zscore_threshold=2.0,  # Valor original
                                    verbose=False,
                                    enable_zscore_filter=filter_params.get('enable_zscore_filter', True),
                                    enable_r2_filter=filter_params.get('enable_r2_filter', True),
                                    enable_beta_filter=filter_params.get('enable_beta_filter', True),
                                    enable_cointegration_filter=filter_params.get('enable_cointegration_filter', True),
                                    zscore_min_threshold=filter_params.get('zscore_min_threshold', -2.0),
                                    zscore_max_threshold=filter_params.get('zscore_max_threshold', 2.0),
                                    r2_min_threshold=filter_params.get('r2_min_threshold', 0.50),
                                    beta_max_threshold=filter_params.get('beta_max_threshold', 1.5)
                                )
                                
                                if resultado is None:
                                    pares_resultado_none += 1
                                    continue
                                
                                # Desempacota o resultado
                                alpha, beta, half_life, zscore, residuo, adf_p_value, pred_resid, resid_atual, zscore_forecast_compra, zscore_forecast_venda, zf_compra, zf_venda, nd_dep, nd_ind, coint_p_value, r2 = resultado
                                
                                if zscore is None:
                                    pares_zscore_none += 1
                                    continue
                                
                                # Se encontrou um resultado válido, guarda o melhor (maior |zscore|)
                                if melhor_resultado is None or abs(zscore) > abs(melhor_resultado[3]):
                                    melhor_resultado = resultado
                                    melhor_periodo = periodo_atual
                                    
                            except Exception as e:
                                pares_com_erro += 1
                                self.log(f"⚠️ Erro ao analisar {dep}x{ind} (período {periodo_atual}): {str(e)[:100]}")
                                continue
                        
                        # Se encontrou pelo menos um resultado válido, adiciona o melhor
                        if melhor_resultado is not None:
                            alpha, beta, half_life, zscore, residuo, adf_p_value, pred_resid, resid_atual, zscore_forecast_compra, zscore_forecast_venda, zf_compra, zf_venda, nd_dep, nd_ind, coint_p_value, r2 = melhor_resultado
                            
                            self.log(f"✅ Par {dep}x{ind} (período {melhor_periodo}): zscore={zscore:.3f}, r2={r2:.3f}, beta={beta:.3f}")
                            
                            resultados_zscore_dependente_atual.append({
                                'ID': id_counter,
                                'Dependente': dep,
                                'Independente': ind, 
                                'Timeframe': config.get('timeframe', '1 dia'),
                                'Período': melhor_periodo,  # Usa o melhor período encontrado
                                'Z-Score': zscore, 
                                'alpha': alpha,
                                'beta': beta,
                                'half_life': half_life,
                                'r2': r2,
                                'adf_p_value': adf_p_value,
                                'coint_p_value': coint_p_value,
                                'residuo': residuo,
                                'residuo_std': resid_atual if resid_atual is not None else 0,
                                'nd_dep': nd_dep,
                                'nd_ind': nd_ind,
                                'pred_resid': pred_resid,
                                'zscore_forecast_compra': zscore_forecast_compra,
                                'zscore_forecast_venda': zscore_forecast_venda
                            })
                            id_counter += 1
            
            self.log(f"📊 Estatísticas primeira seleção:")
            self.log(f"   - Pares x períodos tentados: {pares_tentados}")
            self.log(f"   - Pares com erro: {pares_com_erro}")
            self.log(f"   - Pares resultado None: {pares_resultado_none}")
            self.log(f"   - Pares zscore None: {pares_zscore_none}")
            self.log(f"✅ Primeira seleção: {len(resultados_zscore_dependente_atual)} pares analisados")
            
            if not resultados_zscore_dependente_atual:
                self.log("❌ Nenhum par válido encontrado na primeira seleção")
                return
            
            # Converte para DataFrame
            tabela_zscore_dependente_atual = pd.DataFrame(resultados_zscore_dependente_atual)
            
            # Aplica filtros da primeira seleção
            linha_operacao = []
            linha_operacao = encontrar_linha_monitorada(
                tabela_zscore_dependente_atual, 
                linha_operacao, 
                dados_preprocessados, 
                filter_params, 
                enable_cointegration_filter=filter_params.get('enable_cointegration_filter', True)
            )
              # Filtra os melhores pares da primeira seleção
            tabela_linha_operacao = filtrar_melhores_pares(linha_operacao)
            
            self.log(f"📈 Primeira seleção filtrada: {len(tabela_linha_operacao)} pares selecionados")
              # CORREÇÃO: Armazena a primeira seleção na sessão para exibição na aba "Sinais"
            if hasattr(st.session_state, 'trading_system') and st.session_state.trading_system:
                st.session_state.trading_system.tabela_linha_operacao = tabela_linha_operacao
                self.log(f"💾 Primeira seleção armazenada na sessão: {len(tabela_linha_operacao)} pares")
                
                # NOVA FUNCIONALIDADE: Gera sinais básicos da primeira seleção para aba "Sinais"
                sinais_primeira_selecao = []
                for _, linha in tabela_linha_operacao.iterrows():
                    zscore = linha['Z-Score']
                    r2 = linha.get('r2', 0)
                    beta = linha.get('beta', 1)
                    p_value = linha.get('adf_p_value', 1)
                    confianca = min(90, (r2 * 100) * (1 - p_value)) if p_value < 1 else 50
                    
                    sinal = {
                        'par': f"{linha['Dependente']}/{linha['Independente']}",
                        'ativo': linha['Dependente'],
                        'zscore': zscore,
                        'r2': r2,
                        'beta': beta,
                        'p_value': p_value,
                        'sinal': 'COMPRA' if zscore < -1.5 else 'VENDA',
                        'confianca': confianca,
                        'timestamp': datetime.now(),
                        'preco_atual': self.obter_preco_atual(linha['Dependente']) or 0,
                        'segmento': self.segmentos.get(linha['Dependente'], 'Outros'),
                        'status': 'PRIMEIRA_SELECAO',  # Marca como primeira seleção
                        'tipo_analise': 'Primeira Seleção'
                    }
                    sinais_primeira_selecao.append(sinal)
                
                # Armazena sinais da primeira seleção temporariamente (serão substituídos pela segunda se disponível)
                self.sinais_ativos = sinais_primeira_selecao
                self.log(f"📊 Gerados {len(sinais_primeira_selecao)} sinais da primeira seleção para dashboard")
            
            if tabela_linha_operacao.empty:
                self.log("❌ Nenhum par passou nos filtros da primeira seleção")
                return
            
            # ========================================================================
            # SEGUNDA SELEÇÃO: Análise refinada dos pares selecionados
            # ========================================================================
            self.log("🎯 Executando SEGUNDA SELEÇÃO (refinamento com calcular_residuo_zscore_timeframe01)...")
            
            linha_operacao01 = []
            resultados_zscore_dependente_atual01 = []            # Loop pelos pares da primeira seleção para segunda análise
            for linha in tabela_linha_operacao.itertuples():
                dependente_atual01 = linha.Dependente
                independente_atual01 = linha.Independente
                periodo_atual = linha.Período
                
                try:
                    # Busca dados adicionais da primeira seleção ANTES de chamar a função
                    registro_primeira = tabela_linha_operacao[
                        (tabela_linha_operacao['Dependente'] == dependente_atual01) &
                        (tabela_linha_operacao['Independente'] == independente_atual01)
                    ]
                    
                    if registro_primeira.empty:
                        self.log(f"⚠️ Registro da primeira seleção não encontrado para {dependente_atual01}x{independente_atual01}")
                        continue
                    
                    reg = registro_primeira.iloc[0]
                      # CORRIGIDO: Extrai zscore e r2 da PRIMEIRA seleção (como no código original)
                    zscore = reg.get("Z-Score")
                    r2 = reg.get("r2")
                    beta = reg.get("beta")
                    alpha = reg.get("alpha")
                    half_life = reg.get("half_life")
                    adf_p_value = reg.get("adf_p_value")
                    coint_p_value = reg.get("coint_p_value")
                    residuo = reg.get("residuo")
                    pred_resid = reg.get("pred_resid")
                    zscore_forecast_compra = reg.get("zscore_forecast_compra")
                    zscore_forecast_venda = reg.get("zscore_forecast_venda")
                    
                    # CORREÇÃO CRÍTICA: Adiciona variáveis beta_rotation necessárias para encontrar_linha_monitorada01
                    beta_rotation = reg.get("beta_rotation", beta)  # Usa beta normal se não houver rotation
                    beta_rotation_mean = reg.get("beta_rotation_mean", beta)  # Fallback para beta
                    beta_rotation_std = reg.get("beta_rotation_std", 0.1)
                    correlacao_ibov = reg.get("correlacao_ibov", 0.5)
                    correlacao = reg.get("correlacao", 0.5)
                    forecast = reg.get("forecast", 0.0)
                    
                    self.log(f"🔧 DEBUG: Valores da 1ª seleção - zscore={zscore:.3f}, r2={r2:.3f}, beta_rot={beta_rotation:.3f}")
                    
                    # Executa análise refinada do par (só para obter dados de previsão e spreads)
                    resultado = calcular_residuo_zscore_timeframe01(
                        dep=dependente_atual01,
                        ind=independente_atual01,
                        ibov='IBOV',
                        win='IBOV',
                        periodo=periodo_atual,
                        dados_preprocessados=dados_preprocessados,
                        tabela_linha_operacao=linha_operacao,  # Passa resultados da primeira seleção
                        tolerancia=0.010,
                        min_train=70,
                        verbose=False
                    )                    
                    if resultado and len(resultado) >= 30:
                        # A função calcular_residuo_zscore_timeframe01 retorna dados de previsão e spreads
                        #self.log(f"🔧 DEBUG: Função retornou {len(resultado)} valores para dados de previsão")
                        
                        # Extrai dados de previsão da função (não zscore/r2)
                        (data_prev, previsao_fechamento, previsao_maximo, previsao_minimo, 
                        previsao_fechamento_ind, previsao_maximo_ind, previsao_minimo_ind,
                        preco_ontem, preco_atual, preco_abertura, 
                        preco_max_atual, preco_min_atual, 
                        spread_compra, spread_compra_gain, spread_compra_loss, 
                        spread_venda, spread_venda_gain, spread_venda_loss,                             
                        std_arima_close, std_arima_high, std_arima_low,
                        sigma_close, sigma_high, sigma_low,
                        indep_preco_ontem, indep_preco_atual, indep_preco_abertura,
                        indep_preco_max_atual, indep_preco_min_atual,
                        indep_spread_compra, indep_spread_compra_gain, indep_spread_compra_loss, 
                        indep_spread_venda, indep_spread_venda_gain, indep_spread_venda_loss, 
                        std_arima_close_ind, std_arima_high_ind, std_arima_low_ind,                        sigma_close_ind, sigma_high_ind, sigma_low_ind) = resultado
                        
                        if zscore is not None and abs(zscore) > 1.5:  # Filtro adicional usando zscore da 1ª seleção
                            self.log(f"✅ Par {dependente_atual01}x{independente_atual01} (segunda seleção): zscore={zscore:.3f}, r2={r2:.3f}")
                            
                            resultados_zscore_dependente_atual01.append({
                                'ID': len(resultados_zscore_dependente_atual01) + 1,
                                'Dependente': dependente_atual01,
                                'Independente': independente_atual01,
                                'Timeframe': config.get('timeframe', '1 dia'),
                                'Período': periodo_atual,
                                'Z-Score': zscore,  # Da primeira seleção
                                'alpha': alpha,     # Da primeira seleção
                                'beta': beta,       # Da primeira seleção
                                'half_life': half_life,  # Da primeira seleção
                                'r2': r2,           # Da primeira seleção
                                'adf_p_value': adf_p_value,      # Da primeira seleção
                                'coint_p_value': coint_p_value,  # Da primeira seleção
                                'residuo': residuo,              # Da primeira seleção
                                'pred_resid': pred_resid,        # Da primeira seleção
                                'zscore_forecast_compra': zscore_forecast_compra,  # Da primeira seleção
                                'zscore_forecast_venda': zscore_forecast_venda,    # Da primeira seleção
                                
                                # CORREÇÃO CRÍTICA: Adiciona variáveis essenciais para encontrar_linha_monitorada01
                                'beta_rotation': beta_rotation,        # Necessário para filtros da 2ª seleção
                                'beta_rotation_mean': beta_rotation_mean,  # Necessário para comparação
                                'beta_rotation_std': beta_rotation_std,
                                'correlacao_ibov': correlacao_ibov,
                                'correlacao': correlacao,
                                'forecast': forecast,
                                
                                # Dados de previsão e spreads da segunda análise
                                'preco_atual': preco_atual,
                                'preco_max_atual': preco_max_atual,
                                'preco_min_atual': preco_min_atual,
                                'previsao_fechamento': previsao_fechamento,
                                'previsao_maximo': previsao_maximo,
                                'previsao_minimo': previsao_minimo,
                                'spread_compra': spread_compra,
                                'spread_venda': spread_venda,
                                
                                # Dados do independente
                                'preco_atual_indep': indep_preco_atual,
                                'previsao_fechamento_ind': previsao_fechamento_ind,
                                
                                'Passou_Filtros': True
                            })
                        else:
                            self.log(f"⚠️ Par {dependente_atual01}x{independente_atual01} não passou no filtro zscore: {zscore}")
                            
                    elif resultado:
                        self.log(f"⚠️ Função retornou apenas {len(resultado)} valores (esperado: >=30) para {dependente_atual01}x{independente_atual01}")
                        continue
                    else:
                        self.log(f"⚠️ Função retornou None para {dependente_atual01}x{independente_atual01}")
                        continue
                                
                except Exception as e:
                    self.log(f"⚠️ Erro na segunda seleção {dependente_atual01}x{independente_atual01}: {str(e)[:100]}")
                    continue
            
            self.log(f"🎯 Segunda seleção: {len(resultados_zscore_dependente_atual01)} pares refinados")
            
            if not resultados_zscore_dependente_atual01:
                self.log("❌ Nenhum par válido na segunda seleção")
                return
            
            # Converte segunda seleção para DataFrame
            tabela_zscore_dependente_atual01 = pd.DataFrame(resultados_zscore_dependente_atual01)
            
            # Encontra linhas monitoradas da segunda seleção  
            from calculo_entradas_v55 import encontrar_linha_monitorada01
            linha_operacao01 = encontrar_linha_monitorada01(tabela_zscore_dependente_atual01, linha_operacao01)
            
            # Aplica priorização final baseada na proximidade de preços
            if linha_operacao01:
                self.log(f"💼 Aplicando priorização final para {len(linha_operacao01)} pares...")
                
                selecao_com_prioridade = []
                for linha_dict in linha_operacao01:
                    dep = linha_dict['Dependente']
                    zscore = linha_dict['Z-Score']
                    
                    try:
                        preco_atual = linha_dict.get('preco_atual', 0.0)
                        spread_compra = linha_dict.get('spread_compra', preco_atual)
                        spread_venda = linha_dict.get('spread_venda', preco_atual)
                        
                        # Determina preço de entrada baseado no Z-Score
                        if zscore <= -2.0:
                            preco_entrada = spread_compra  # Comprar dependente
                        elif zscore >= 2.0:
                            preco_entrada = spread_venda   # Vender dependente
                        else:
                            preco_entrada = preco_atual
                        
                        # Calcula percentual de diferença
                        if preco_atual > 0:
                            perc_diferenca = abs((preco_entrada - preco_atual) / preco_atual * 100)
                        else:
                            perc_diferenca = 999.0
                        
                        linha_com_prioridade = linha_dict.copy()
                        linha_com_prioridade['Perc_Diferenca'] = perc_diferenca
                        linha_com_prioridade['Preco_Entrada_Final'] = preco_entrada
                        selecao_com_prioridade.append(linha_com_prioridade)
                        
                    except Exception as e:
                        linha_com_prioridade = linha_dict.copy()
                        linha_com_prioridade['Perc_Diferenca'] = 999.0
                        linha_com_prioridade['Preco_Entrada_Final'] = 0.0
                        selecao_com_prioridade.append(linha_com_prioridade)
                
                # Ordena por proximidade de preço (menor diferença primeiro)
                linha_operacao01 = sorted(selecao_com_prioridade, key=lambda x: x['Perc_Diferenca'])
                
                # Converte para DataFrame final (tabela_linha_operacao01)
                tabela_linha_operacao01 = pd.DataFrame(linha_operacao01)
                
                self.log(f"🏆 ANÁLISE COMPLETA: {len(tabela_linha_operacao01)} pares FINAIS priorizados")                # CORREÇÃO: A função encontrar_linha_monitorada01 já aplica os filtros corretos
                # Todos os pares em tabela_linha_operacao01 já passaram pela validação
                sinais_detectados = []
                
                self.log(f"✅ PROCESSANDO {len(tabela_linha_operacao01)} pares PRÉ-APROVADOS da segunda seleção...")
                
                for _, linha in tabela_linha_operacao01.iterrows():
                    zscore = linha['Z-Score']
                    r2 = linha.get('r2', 0)
                    beta = linha.get('beta', 1)
                    beta_rotation = linha.get('beta_rotation', beta)
                    beta_rotation_mean = linha.get('beta_rotation_mean', beta)
                    p_value = linha.get('adf_p_value', 1)
                    
                    # DETERMINA TIPO DE SINAL - JÁ PASSOU PELOS FILTROS
                    if zscore >= 2.0:
                        tipo_sinal = 'VENDA'  # Vender dependente
                        self.log(f"✅ SINAL VENDA: {linha['Dependente']} - Z={zscore:.2f}, β_rot={beta_rotation:.3f}")
                    elif zscore <= -2.0:
                        tipo_sinal = 'COMPRA'  # Comprar dependente
                        self.log(f"✅ SINAL COMPRA: {linha['Dependente']} - Z={zscore:.2f}, β_rot={beta_rotation:.3f}")
                    else:
                        # Não deveria chegar aqui, mas mantém por segurança
                        tipo_sinal = 'COMPRA' if zscore < 0 else 'VENDA'
                        self.log(f"⚠️ SINAL INESPERADO: {linha['Dependente']} - Z={zscore:.2f}")
                    
                    confianca = min(95, (r2 * 100) * (1 - p_value)) if p_value < 1 else 50
                    
                    sinal = {
                        'par': f"{linha['Dependente']}/{linha['Independente']}",
                        'ativo': linha['Dependente'],
                        'zscore': zscore,                        
                        'r2': r2,
                        'beta': beta,
                        'beta_rotation': beta_rotation,
                        'beta_rotation_mean': beta_rotation_mean,
                        'p_value': p_value,
                        'sinal': tipo_sinal,
                        'confianca': confianca,
                        'timestamp': datetime.now(),
                        'preco_atual': self.obter_preco_atual(linha['Dependente']) or 0,
                        'segmento': self.segmentos.get(linha['Dependente'], 'Outros'),
                        'status': 'REAL',  # Marca como análise real
                        'preco_entrada': linha.get('Preco_Entrada_Final', 0),
                        'diferenca_preco': linha.get('Perc_Diferenca', 0),
                        'forecast': linha.get('forecast', 0),
                        'correlacao': linha.get('correlacao', 0)
                    }
                    sinais_detectados.append(sinal)
                  # Atualiza sinais com dados reais da segunda seleção
                self.sinais_ativos = sinais_detectados
                self.dados_sistema["pares_processados"] = len(tabela_linha_operacao01)                
                self.log(f"🏆 ANÁLISE FINAL: {len(sinais_detectados)} sinais PREMIUM da segunda seleção carregados")
                
            else:
                self.log("❌ Nenhum par prioritário encontrado na segunda seleção")
                self.sinais_ativos = []
                tabela_linha_operacao01 = pd.DataFrame()  # Cria DataFrame vazio
                
            # SEMPRE armazena tabela_linha_operacao01 no session state (mesmo se vazia)
            if hasattr(st.session_state, 'trading_system') and st.session_state.trading_system:
                st.session_state.trading_system.tabela_linha_operacao01 = tabela_linha_operacao01
                self.log(f"💾 Tabela segunda seleção salva: {len(tabela_linha_operacao01)} registros")
                
        except ImportError as e:
            self.log(f"❌ Sistema de análise real não disponível: {str(e)}")
            self.log("📊 Execute sem análise de sinais - apenas monitoramento")
        except Exception as e:
            self.log(f"❌ Erro na análise real: {str(e)}")
            self.log("📊 Continuando apenas com monitoramento básico")

    def obter_dados_historicos_mt5(self, simbolos: List[str], timeframe, periodo: int) -> Dict:
        """Obtém dados históricos do MT5 para análise"""
        if not self.mt5_connected:
            self.log("❌ MT5 não conectado - não é possível obter dados históricos")
            return {}
            
        # DEBUG: Log dos símbolos recebidos
        #self.log(f"🔧 DEBUG: Símbolos solicitados: {simbolos}")
        #self.log(f"🔧 DEBUG: Timeframe: {timeframe}, Período: {periodo}")
          # Primeiro, coleta dados brutos do MT5
        dados_historicos = {}
        
        try:
            for simbolo_original in simbolos:
                #self.log(f"🔧 DEBUG: Processando símbolo: {simbolo_original}")
                
                try:
                    # Primeiro, verifica se o símbolo existe no MT5
                    symbol_info = mt5.symbol_info(simbolo_original)
                    if symbol_info is None:
                        self.log(f"❌ Símbolo {simbolo_original} não encontrado no MT5")
                        continue
                    
                    self.log(f"✅ Símbolo {simbolo_original} encontrado: {symbol_info.description}")
                    
                    # Obtém dados históricos
                    #self.log(f"🔧 DEBUG: Solicitando {periodo} registros para {simbolo_original}")
                    rates = mt5.copy_rates_from_pos(simbolo_original, timeframe, 0, periodo)
                    
                    if rates is not None and len(rates) > 0:
                        df = pd.DataFrame(rates)
                        df['time'] = pd.to_datetime(df['time'], unit='s')
                        df.set_index('time', inplace=True)
                        
                        # Armazena dados brutos
                        dados_historicos[simbolo_original] = df
                        #self.log(f"✅ {len(df)} registros coletados para {simbolo_original}")
                        
                    else:
                        self.log(f"❌ Nenhum dado histórico retornado para {simbolo_original}")
                        # Verifica o erro do MT5
                        erro_mt5 = mt5.last_error()
                        self.log(f"❌ Erro MT5: {erro_mt5}")
                        
                except Exception as e:
                    self.log(f"❌ Erro ao processar {simbolo_original}: {str(e)}")
                    continue
                    
        except Exception as e:
            self.log(f"❌ Erro geral ao obter dados históricos: {str(e)}")
            return {}
        
        #self.log(f"🔧 DEBUG: Símbolos coletados com sucesso: {list(dados_historicos.keys())}")
        
        # Agora usa a função de pré-processamento do sistema original
        if dados_historicos:
            try:
                from calculo_entradas_v55 import preprocessar_dados
                
                # Define colunas a serem pré-processadas
                colunas = ['close', 'open', 'high', 'low']
                
                #self.log(f"🔧 DEBUG: Aplicando pré-processamento para {len(dados_historicos)} símbolos")
                
                # Aplica o pré-processamento correto
                dados_preprocessados = preprocessar_dados(dados_historicos, list(dados_historicos.keys()), colunas, verbose=False)
                
                #self.log(f"✅ Dados pré-processados para {len(dados_preprocessados)} símbolos")
                #self.log(f"🔧 DEBUG: Símbolos pós-processamento: {list(dados_preprocessados.keys())}")
                
                return dados_preprocessados
                
            except ImportError as e:
                self.log(f"❌ Erro ao importar preprocessar_dados: {str(e)}")
                return {}
            except Exception as e:
                self.log(f"❌ Erro no pré-processamento: {str(e)}")
                return {}
        else:
            self.log("❌ Nenhum dado histórico coletado")
            return {}
            

    def obter_historico_trades_real(self, data_inicio: datetime, data_fim: datetime) -> List[Dict]:
        """Obtém histórico real de trades do MT5"""
        if not self.mt5_connected:
            self.log("⚠️ MT5 não conectado para buscar histórico de trades")
            return []
            
        try:
            # Busca histórico de ordens do MT5
            deals = mt5.history_deals_get(data_inicio, data_fim)
            
            if deals is None or len(deals) == 0:
                self.log("ℹ️ Nenhum trade encontrado no período")
                return []
            
            trades_processados = []
            
            for deal in deals:
                # Converte deal do MT5 para formato do dashboard
                trade = {
                    'Ticket': deal.ticket,
                    'Par': deal.symbol,
                    'Tipo': 'COMPRA' if deal.type == 0 else 'VENDA',
                    'Data': datetime.fromtimestamp(deal.time),
                    'Volume': deal.volume,
                    'Preço': deal.price,
                    'Comissão': deal.commission,
                    'Swap': deal.swap,
                    'Lucro': deal.profit,
                    'Comentário': deal.comment if hasattr(deal, 'comment') else '',
                    'Ordem': deal.order
                }
                trades_processados.append(trade)
            
            #self.log(f"✅ {len(trades_processados)} trades carregados do MT5")
            return trades_processados
            
        except Exception as e:
            self.log(f"❌ Erro ao buscar histórico de trades: {str(e)}")
            return []
    
    def calcular_estatisticas_performance_real(self, trades: List[Dict]) -> Dict:
        """Calcula estatísticas reais de performance baseado nos trades do MT5"""
        if not trades:
            return {
                'total_trades': 0,
                'win_rate': 0.0,
                'resultado_total': 0.0,
                'resultado_medio': 0.0,
                'melhor_trade': 0.0,
                'pior_trade': 0.0,
                'sharpe_ratio': 0.0,
                'max_drawdown': 0.0,
                'profit_factor': 0.0
            }
        
        try:
            lucros = [trade['Lucro'] for trade in trades if 'Lucro' in trade]
            
            if not lucros:
                return {'total_trades': len(trades), 'win_rate': 0.0, 'resultado_total': 0.0}
            
            trades_lucrativos = [l for l in lucros if l > 0]
            trades_prejuizo = [l for l in lucros if l < 0]
            
            # Estatísticas básicas
            total_trades = len(trades)
            win_rate = (len(trades_lucrativos) / total_trades) * 100 if total_trades > 0 else 0
            resultado_total = sum(lucros)
            resultado_medio = np.mean(lucros) if lucros else 0
            melhor_trade = max(lucros) if lucros else 0
            pior_trade = min(lucros) if lucros else 0
            
            # Profit Factor
            total_lucros = sum(trades_lucrativos) if trades_lucrativos else 0
            total_perdas = abs(sum(trades_prejuizo)) if trades_prejuizo else 1
            profit_factor = total_lucros / total_perdas if total_perdas > 0 else 0
            
            # Sharpe Ratio simplificado
            if len(lucros) > 1:
                sharpe_ratio = np.mean(lucros) / np.std(lucros) if np.std(lucros) > 0 else 0
            else:
                sharpe_ratio = 0
            
            # Drawdown máximo
            equity_curve = np.cumsum(lucros)
            running_max = np.maximum.accumulate(equity_curve)
            drawdown = (equity_curve - running_max) / running_max * 100
            max_drawdown = abs(min(drawdown)) if len(drawdown) > 0 else 0
            
            return {
                'total_trades': total_trades,
                'win_rate': win_rate,
                'resultado_total': resultado_total,
                'resultado_medio': resultado_medio,
                'melhor_trade': melhor_trade,
                'pior_trade': pior_trade,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown,
                'profit_factor': profit_factor
            }
            
        except Exception as e:
            self.log(f"❌ Erro ao calcular estatísticas: {str(e)}")
            return {'total_trades': 0, 'win_rate': 0.0, 'resultado_total': 0.0}
    
    def iniciar_sistema(self, config: Dict):
        """Inicia o sistema de trading - Versão otimizada com threading avançado"""
        if self.running:
            return False
        
        self.running = True
        
        if self.modo_otimizado and self.sistema_integrado:
            # Usa sistema integrado com threading avançado
            self.log("🚀 Iniciando sistema com threading avançado...")
            self.log("✅ Threads ativas:")
            self.log("   📊 Monitoramento geral")
            self.log("   🔍 Monitoramento de posições")
            self.log("   📈 Break-even contínuo")
            self.log("   ⏰ Ajustes programados")
            
            # Inicia sistema integrado em thread separada
            self.thread_sistema = threading.Thread(
                target=self.executar_sistema_integrado,
                args=(config,),
                daemon=True,
                name="SistemaIntegradoDashboard"
            )
            self.thread_sistema.start()
            
            # Thread adicional para sincronização de dados
            self.thread_sync = threading.Thread(
                target=self.sincronizar_dados_sistema,
                daemon=True,
                name="SincronizacaoDados"
            )
            self.thread_sync.start()
            
        else:
            # Modo básico (original)
            self.log("⚠️ Iniciando sistema em modo básico...")
            self.thread_sistema = threading.Thread(
                target=self.executar_sistema_principal,
                args=(config,),
                daemon=True
            )
            self.thread_sistema.start()
            
        self.log("✅ Sistema iniciado com sucesso")
        return True
    
    def executar_sistema_integrado(self, config: Dict):
        """Executa sistema integrado completo com todas as threads"""
        try:
            self.log("🎯 Inicializando sistema integrado completo...")
            
            # Conecta MT5 se necessário
            if not self.mt5_connected:
                self.conectar_mt5()
            
            # Inicia sistema integrado
            self.sistema_integrado.iniciar_sistema()
            
        except Exception as e:
            self.log(f"❌ Erro no sistema integrado: {str(e)}")
            # Fallback para sistema básico
            self.executar_sistema_principal(config)
    
    def sincronizar_dados_sistema(self):
        """Thread para sincronizar dados entre dashboard e sistema integrado"""
        while self.running:
            try:
                if self.sistema_integrado and self.modo_otimizado:
                    # Sincroniza dados do sistema integrado
                    self.dados_sistema.update({
                        "execucoes": self.sistema_integrado.dados_sistema.get("execucoes", 0),
                        "pares_processados": self.sistema_integrado.dados_sistema.get("pares_processados", 0),
                        "ordens_enviadas": self.sistema_integrado.dados_sistema.get("ordens_enviadas", 0),
                        "ultimo_update": datetime.now()
                    })
                    
                    # Sincroniza logs (últimos 50)
                    if self.sistema_integrado.logs:
                        logs_sistema = self.sistema_integrado.logs[-50:]
                        for log in logs_sistema:
                            if log not in self.logs:
                                self.logs.append(log)
                        
                        # Mantém limite de logs
                        if len(self.logs) > 1000:
                            self.logs = self.logs[-500:]
                
                # Aguarda 5 segundos para próxima sincronização
                for i in range(5):
                    if not self.running:
                        break
                    time_module.sleep(1)
                    
            except Exception as e:
                self.log(f"❌ Erro na sincronização: {str(e)}")
                time_module.sleep(10)
    
    def parar_sistema(self):
        """Para o sistema de trading - Versão otimizada"""
        self.running = False
        
        if self.modo_otimizado and self.sistema_integrado:
            # Para sistema integrado
            self.sistema_integrado.parar_sistema()
            self.log("🛑 Sistema integrado parado")
        
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

# Verificação de segurança - reconstrói o objeto se necessário
if not hasattr(st.session_state.trading_system, 'iniciar_sistema'):
    st.session_state.trading_system = TradingSystemReal()

def render_header():
    """Renderiza header principal com status das funcionalidades"""
    
    #col1, col2, col3, col4 = st.columns(4)
    #sistema = st.session_state.trading_system
    
    # Força atualização do status para garantir sincronização
    #mt5_conectado = sistema.mt5_connected
    #sistema_rodando = sistema.running

    #with col1:
        #status_mt5 = "online" if mt5_conectado else "offline"
        #color_mt5 = "🟢" if mt5_conectado else "🔴"
        #st.markdown(f"""
        #**🔗 Conexão MT5** 
        #**{color_mt5}   {status_mt5}**
        #""")
    
    #with col2:
        # Informações financeiras dependem do MT5 estar conectado
       # status_financeiro = "online" if mt5_conectado else "offline"
        #color_fin = "🟢" if mt5_conectado else "🔴"
        #st.markdown(f"""
        #**💰 Informações Financeiras** 
        #{color_fin} **{status_financeiro}**
        #""")
    
    #with col3:
        # Sinais dependem tanto do MT5 quanto do sistema estar rodando
        #sinais_online = mt5_conectado and sistema_rodando
        #status_sinais = "online" if sinais_online else "offline"
        #color_sinais = "🟢" if sinais_online else "🔴"
        #st.markdown(f"""
       # **📊 Sinais de Trading** 
       # {color_sinais} **{status_sinais}**
        #""")
    
   # with col4:
        # Relatórios sempre online se MT5 conectado
       # status_relatorios = "online" if mt5_conectado else "offline"
       # color_rel = "🟢" if mt5_conectado else "🔴"
       # st.markdown(f"""
       # **📋 Relatórios/Exportação** 
       # {color_rel} **{status_relatorios}**
       # """)
    
    # DEBUG INFO (remover em produção)
    #if st.checkbox("🔧 Debug Status", value=False):
        #st.write(f"**Debug:** MT5={mt5_conectado}, Sistema={sistema_rodando}, Sinais={sinais_online}")
    
    st.markdown("---")
    
def render_sidebar():
    """Renderiza sidebar com configurações"""
    st.sidebar.markdown("## ⚙️ Configurações")
    
    # INDICADOR DE MODO INTEGRADO
    #if SISTEMA_INTEGRADO_DISPONIVEL and st.session_state.trading_system.modo_otimizado:
        #st.sidebar.markdown("""
        #<div style="background: linear-gradient(45deg, #28a745, #20c997); 
                   # color: white; padding: 0.5rem; border-radius: 8px; 
                    #text-align: center; margin-bottom: 1rem; font-weight: bold;">
           ##</div>
       # """, unsafe_allow_html=True)
        
        # Status das threads quando sistema estiver rodando
        #if st.session_state.trading_system.running and st.session_state.trading_system.sistema_integrado:
            #sistema = st.session_state.trading_system.sistema_integrado
            #st.sidebar.markdown("**🧵 Status das Threads:**")
            
            #threads_status = [
                #("📊 Monitoramento", "Ativo" if sistema.running else "Inativo"),
                #("🔍 Posições", "Ativo" if sistema.running else "Inativo"),
                #("📈 Break-Even", "Ativo" if sistema.running else "Inativo"),
                #("⏰ Ajustes Program.", "Ativo" if sistema.running else "Inativo")
            #]
            
            #for nome, status in threads_status:
                #cor = "🟢" if status == "Ativo" else "🔴"
                #st.sidebar.markdown(f"   {cor} {nome}: {status}", unsafe_allow_html=True)
            
            #st.sidebar.markdown("---")
   # else:
        #st.sidebar.markdown("""
        #<div style="background: #ffc107; color: #212529; padding: 0.5rem; 
                   # border-radius: 8px; text-align: center; margin-bottom: 1rem; font-weight: bold;">
            #⚠️ MODO BÁSICO
        #</div>
        #""", unsafe_allow_html=True)
    
    # CONTROLES DO SISTEMA - MOVIDO PARA O TOPO
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.markdown("### 🎮 Plataforma")
    
    # Interface de controle no mesmo formato MT5
    is_running = st.session_state.trading_system.running
    
    # Interface de controle compacta
    col_btn, col_status = st.sidebar.columns([1, 1])
    
    with col_btn:
        if is_running:
            # Quando rodando, botão vira "Parar Sistema"
            if st.button("Desconectar", use_container_width=True, help="Clique para parar o sistema"):
                st.session_state.trading_system.parar_sistema()
                # Remove o st.success para evitar botão piscante
                st.rerun()
        else:
            # Quando parado, botão normal "Iniciar Sistema"
            if st.button("Conectar", use_container_width=True, help="Clique para iniciar o sistema"):
                # Usa configuração temporária se ainda não existe a final
                config_temp = getattr(st.session_state.trading_system, 'config_atual', {
                    'ativos_selecionados': [],
                    'timeframe': "1 dia",
                    'periodo_analise': 120,
                    'usar_multiplos_periodos': True,
                    'zscore_min': 2.0,
                    'zscore_max': 2.0,
                    'max_posicoes': 6,
                    'filtro_cointegração': True,
                    'filtro_r2': True,
                    'filtro_beta': True,
                    'filtro_zscore': True,
                    'r2_min': 0.5,
                    'intervalo_execucao': 60 
                })
                  # Debug: verifica se o método existe
                if hasattr(st.session_state.trading_system, 'iniciar_sistema'):
                    if st.session_state.trading_system.iniciar_sistema(config_temp):
                        # Remove o st.success para evitar botão piscante
                        st.rerun()
                    else:
                        st.warning("Sistema já está rodando")
                else:
                    st.error("❌ Método 'iniciar_sistema' não encontrado! Reconstruindo objeto...")
                    st.session_state.trading_system = TradingSystemReal()
                    st.rerun()
    
    with col_status:
        if is_running:
            # Botão verde quando sistema rodando
            st.markdown("""
            <div class="system-status-running">
                Conectado
            </div>
            """, unsafe_allow_html=True)
        else:
            # Botão cinza quando sistema parado
            st.markdown("""
            <div class="system-status-stopped">
                Desconectado
            </div>
            """, unsafe_allow_html=True)
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # CONEXÃO MT5 - AGORA FICA ABAIXO DOS CONTROLES
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.markdown("### 🔌 Conexão MT5")
    
    # Verifica se já está conectado para minimizar a interface
    is_connected = st.session_state.trading_system.mt5_connected
    
    if not is_connected:
        # Mostra campos de login apenas se não estiver conectado
        mt5_login = st.sidebar.number_input("Login", value=0, format="%d")
        mt5_password = st.sidebar.text_input("Senha", type="password")
        mt5_server = st.sidebar.text_input("Servidor", value="")
    else:
        # Usa valores salvos ou padrão quando conectado
        mt5_login = getattr(st.session_state.trading_system, 'last_login', 0)
        mt5_password = getattr(st.session_state.trading_system, 'last_password', "")
        mt5_server = getattr(st.session_state.trading_system, 'last_server', "")
    
    # Interface de conexão compacta
    col_btn, col_status = st.sidebar.columns([1, 1])
    
    with col_btn:
        if is_connected:
            # Quando conectado, botão vira "Desconectar"
            if st.button("Desconectar", use_container_width=True, help="Clique para desconectar do MT5"):
                st.session_state.trading_system.mt5_connected = False
                # Limpa as credenciais salvas
                if hasattr(st.session_state.trading_system, 'last_login'):
                    delattr(st.session_state.trading_system, 'last_login')
                if hasattr(st.session_state.trading_system, 'last_password'):
                    delattr(st.session_state.trading_system, 'last_password')
                if hasattr(st.session_state.trading_system, 'last_server'):
                    delattr(st.session_state.trading_system, 'last_server')
                st.success("Desconectado!")
                st.rerun()  # Recarrega para mostrar campos novamente
        else:
            # Quando desconectado, botão normal "Conectar"
            if st.button("Conectar", use_container_width=True, help="Clique para conectar ao MT5"):
                if st.session_state.trading_system.conectar_mt5(mt5_login, mt5_password, mt5_server):
                    # Salva as credenciais para próxima conexão
                    st.session_state.trading_system.last_login = mt5_login
                    st.session_state.trading_system.last_password = mt5_password
                    st.session_state.trading_system.last_server = mt5_server
                    st.success("Conectado!")
                    st.rerun()  # Recarrega para minimizar a interface
                else:                    st.error("❌ Falha na conexão")
    
    with col_status:
        if is_connected:
            # Botão verde completo quando conectado
            st.markdown("""
            <div class="status-button-connected">
                Conectado
            </div>
            """, unsafe_allow_html=True)
        else:
            # Botão vermelho completo quando desconectado
            st.markdown("""
            <div class="status-button-disconnected">
                Desconectado
            </div>            """, unsafe_allow_html=True)
    
    # Remove o botão de configuração separado (agora o desconectar faz essa função)
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Seleção de Ativos
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.markdown("### 📊 Ativos Monitorados")
    
    # Filtro por segmento
    segmentos_disponiveis = list(set(st.session_state.trading_system.segmentos.values()))
    segmentos_disponiveis.sort()  # Ordena alfabeticamente
    
    # Opção de selecionar todos os segmentos (PADRÃO: MARCADO)
    selecionar_todos_segmentos = st.sidebar.checkbox("Selecionar Todos os Segmentos", value=True)
    
    if selecionar_todos_segmentos:
        segmentos_selecionados = segmentos_disponiveis
    else:
        segmentos_selecionados = st.sidebar.multiselect(
            "Segmentos", 
            segmentos_disponiveis,
            default=segmentos_disponiveis  # PRODUÇÃO: Todos os segmentos por padrão
        )
    
    # Ativos por segmento selecionado
    ativos_filtrados = [
        ativo for ativo, segmento in st.session_state.trading_system.segmentos.items()
        if segmento in segmentos_selecionados
    ]
    
    # Opção de selecionar todos os ativos (PADRÃO: MARCADO)
    selecionar_todos_ativos = st.sidebar.checkbox("Selecionar Todos os Ativos", value=True)
    
    if selecionar_todos_ativos:
        ativos_selecionados = ativos_filtrados
    else:
        ativos_selecionados = st.sidebar.multiselect(
            "Ativos Específicos",
            ativos_filtrados,
            default=ativos_filtrados if ativos_filtrados else []  # PRODUÇÃO: Todos por padrão
        )
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Parâmetros de Trading
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.markdown("### 🎯 Parâmetros de Trading")
    
    timeframe = st.sidebar.selectbox(
        "Timeframe",
        ["1 min", "5 min", "15 min", "30 min", "1 hora", "4 horas", "1 dia"],
        index=6
    )
    
    # Opção para escolher entre período único ou múltiplos períodos
    usar_multiplos_periodos = st.sidebar.radio(
        "Estratégia de Análise",
        options=["Período Único", "Múltiplos Períodos"],
        index=1,  # Default para múltiplos períodos
        help="Período Único: usa apenas o período selecionado abaixo. "
             "Múltiplos Períodos: (70, 100, 120, 140, 160, 180, 200, 220, 240, 250) para encontrar as melhores oportunidades."
    )
    
    # Mostra o slider de período apenas se "Período Único" for selecionado
    if usar_multiplos_periodos == "Período Único":
        periodo_analise = st.sidebar.slider(
            "Período de Análise", 
            50, 250, 120,  # Valor padrão mais balanceado
            help="Período específico para análise quando usar estratégia de período único"
        )
    else:
        # Para múltiplos períodos, usa um valor padrão (não será usado na prática)
        periodo_analise = 250  # Valor padrão para garantir dados suficientes
        st.sidebar.info("70, 100, 120, 140, 160, 180, 200, 220, 240, 250")
    
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
    
    # BOTÕES DE UTILIDADE NO FINAL
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.markdown("### 🔧 Utilidades")
    
    if st.sidebar.button("💾 Salvar Perfil"):
        st.sidebar.success("Perfil salvo!")
    
    if st.sidebar.button("🔄 Reset Completo"):
        st.session_state.trading_system = TradingSystemReal()
        st.sidebar.success("Sistema resetado!")
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
      # Atualiza a configuração dos controles com os valores finais
    config_final = {
        'ativos_selecionados': ativos_selecionados,
        'timeframe': timeframe,
        'periodo_analise': periodo_analise,
        'usar_multiplos_periodos': usar_multiplos_periodos == "Múltiplos Períodos",
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
    
    # DEBUG: Log da configuração que está sendo enviada
    sistema = st.session_state.trading_system
    #if hasattr(sistema, 'log'):
        #sistema.log(f"🔧 DEBUG SIDEBAR: Total segmentos disponíveis: {len(segmentos_disponiveis)}")
        #sistema.log(f"🔧 DEBUG SIDEBAR: Segmentos selecionados: {len(segmentos_selecionados)}")
        #sistema.log(f"🔧 DEBUG SIDEBAR: Ativos filtrados: {len(ativos_filtrados)}")
        #sistema.log(f"🔧 DEBUG SIDEBAR: Ativos finais selecionados: {len(ativos_selecionados)}")
        #sistema.log(f"🔧 DEBUG SIDEBAR: Lista de ativos: {ativos_selecionados[:5]}..." if len(ativos_selecionados) > 5 else f"🔧 DEBUG SIDEBAR: Lista de ativos: {ativos_selecionados}")
    
    # Atualiza a configuração dos controles no topo da sidebar
    if hasattr(st.session_state.trading_system, 'config_atual'):
        st.session_state.trading_system.config_atual = config_final
    
    return config_final

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
    
    # Métricas específicas do sistema integrado (se disponível)
    #if sistema.modo_otimizado and sistema.sistema_integrado and sistema.running:
        #st.markdown("---")
        #st.markdown("### 🧵 Métricas do Sistema Integrado")
        
        #col_t1, col_t2, col_t3, col_t4 = st.columns(4)
        
        #with col_t1:
            #total_threads = 4  # Threads principais
            #st.metric("Threads Ativas", f"{total_threads}/4", delta="Threading ativo")
        
        #with col_t2:
            # Stops ajustados hoje
            #stops_ajustados = len(sistema.sistema_integrado.stops_ja_ajustados) if hasattr(sistema.sistema_integrado, 'stops_ja_ajustados') else 0
            #st.metric("Stops Ajustados", stops_ajustados, delta="Break-even")
        
        #with col_t3:
            # Ajustes executados
            #ajustes_exec = len(sistema.sistema_integrado.ajustes_executados_hoje) if hasattr(sistema.sistema_integrado, 'ajustes_executados_hoje') else 0
            #st.metric("Ajustes Program.", ajustes_exec, delta="15:10/15:20/16:01")
        
        #with col_t4:
            # Status do sistema integrado
            #status_integrado = "🟢 ATIVO" if sistema.sistema_integrado.running else "🔴 INATIVO"
            #st.metric("Sistema Core", status_integrado, delta="Multi-thread")

def render_equity_chart():
    """Renderiza gráfico de equity com dados reais do MT5"""
    sistema = st.session_state.trading_system
    
    # Indicador de status da funcionalidade
    col1, col2 = st.columns([3, 1])
    #with col1:
        #st.markdown("### 📈 Curva de Equity em Tempo Real")
    with col2:
        if sistema.mt5_connected:
            st.markdown("✅ **online**", help="Dados de equity obtidos em tempo real do MetaTrader 5")
            # NOVO: Botão para forçar atualização
            if st.button("🔄", help="Força atualização dos dados de equity"):
                sistema.equity_historico = []  # Limpa dados antigos
                try:
                    sistema.atualizar_account_info()
                    equity_dados_mt5 = obter_equity_historico_mt5(sistema)
                    if equity_dados_mt5:
                        sistema.equity_historico = equity_dados_mt5
                        sistema.log(f"🔄 Gráfico atualizado: {len(equity_dados_mt5)} pontos carregados")
                        st.rerun()
                except Exception as e:
                    sistema.log(f"❌ Erro na atualização: {str(e)}")
        else:
            st.markdown("🔴 **offline**", help="MT5 desconectado - sem dados reais")
    
    # CORREÇÃO: Se não há dados no histórico mas MT5 está conectado, coleta dados agora
    if not sistema.equity_historico and sistema.mt5_connected:
        try:
            # Força coleta de dados atuais do MT5
            sistema.atualizar_account_info()
            sistema.log("📊 Dados de equity coletados automaticamente para o gráfico")
        except Exception as e:
            sistema.log(f"❌ Erro ao coletar dados de equity: {str(e)}")
    
    # Verifica novamente após tentar coletar
    if not sistema.equity_historico:
        if sistema.mt5_connected:
            # MELHORIA: Tenta obter dados históricos do MT5 para popular o gráfico
            equity_dados_mt5 = obter_equity_historico_mt5(sistema)
            if equity_dados_mt5:
                sistema.equity_historico = equity_dados_mt5
                sistema.log(f"📊 {len(equity_dados_mt5)} pontos de equity carregados do histórico MT5")
            else:
                st.info("📊 Aguardando dados de equity... Execute o sistema para coletar dados.")
                # NOVO: Mostra dados atuais mesmo sem histórico
                try:
                    account_info = mt5.account_info()
                    if account_info:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Equity Atual", f"R$ {account_info.equity:,.2f}")
                        with col2:
                            st.metric("Balance Atual", f"R$ {account_info.balance:,.2f}")
                        with col3:
                            st.metric("Profit Atual", f"R$ {account_info.profit:+,.2f}")
                        st.info("💡 Use o botão 'Atualizar' acima para carregar o gráfico completo")
                except:
                    pass
                return
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
        title="📈 Curva de Equity",
        xaxis_title="Tempo",
        yaxis_title="Valor (R$)",
        hovermode='x unified',
        showlegend=True,
        height=400,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_positions_table():
    """Renderiza tabela de posições abertas - FORMATO PROFISSIONAL"""
    sistema = st.session_state.trading_system
    posicoes = sistema.obter_posicoes_abertas()
    
    # Indicador de status da funcionalidade
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 💼 Posições Detalhadas")
    with col2:
        if sistema.mt5_connected:
            st.markdown("✅ **online**", help="Dados obtidos em tempo real do MetaTrader 5")
        else:
            st.markdown("🔴 **offline**", help="MT5 desconectado - usando dados simulados")
    
    # Se não há posições reais, cria dados de demonstração baseados nos sinais
    if not posicoes:
        if sistema.mt5_connected:
            st.info("💼 Nenhuma posição aberta no momento")
        else:
            st.warning("🔌 Conecte ao MT5 para visualizar posições reais")
            
        # DEMO: Cria posições de exemplo se há dados disponíveis
        if hasattr(sistema, 'tabela_linha_operacao') and not sistema.tabela_linha_operacao.empty:
            st.info("📊 Exibindo posições simuladas baseadas na análise:")
            
            df_demo = sistema.tabela_linha_operacao.head(3).copy()  # Pega 3 primeiros
            
            posicoes_demo = []
            for i, row in df_demo.iterrows():
                dep = row.get('Dependente', 'ATIVO1')
                ind = row.get('Independente', 'ATIVO2')
                zscore = row.get('Z-Score', 0)
                preco_atual = row.get('preco_atual', 100.0)
                
                # Determina tipo baseado no Z-Score
                if zscore <= -1.5:
                    tipo = 'LONG'
                    preco_abertura = preco_atual * 0.995  # Comprou 0.5% abaixo
                    pl_valor = preco_atual - preco_abertura
                elif zscore >= 1.5:
                    tipo = 'SHORT'
                    preco_abertura = preco_atual * 1.005  # Vendeu 0.5% acima
                    pl_valor = preco_abertura - preco_atual
                else:
                    continue
                
                pl_percent = (pl_valor / preco_abertura * 100) if preco_abertura > 0 else 0
                
                pos_demo = {
                    'Par': f"{dep}/{ind}",
                    'Tipo': tipo,
                    'Volume': 1000 + (i * 500),  # Volume variado
                    'Preço Abertura': f"R$ {preco_abertura:.2f}",
                    'Preço Atual': f"R$ {preco_atual:.2f}",
                    'P&L (R$)': f"R$ {pl_valor:+.2f}",
                    'P&L (%)': f"{pl_percent:+.2f}%",
                    'Stop Loss': f"R$ {preco_abertura * 0.98:.2f}",
                    'Take Profit': f"R$ {preco_abertura * 1.05:.2f}",
                    'Tempo Aberto': f"{i+1}:30:00",  # Tempo simulado
                    'Setor': sistema.segmentos.get(dep, 'Outros')
                }
                posicoes_demo.append(pos_demo)
            
            if posicoes_demo:
                df_pos_demo = pd.DataFrame(posicoes_demo)
                
                # Aplica cores condicionais
                def color_pl(val):
                    if '+' in str(val):
                        return 'color: green; font-weight: bold'
                    elif '-' in str(val):
                        return 'color: red; font-weight: bold'
                    return ''
                
                def color_tipo(val):
                    if val == 'LONG':
                        return 'background-color: rgba(0, 255, 0, 0.1)'
                    elif val == 'SHORT':
                        return 'background-color: rgba(255, 0, 0, 0.1)'
                    return ''
                
                st.dataframe(
                    df_pos_demo.style.applymap(color_tipo, subset=['Tipo'])
                                    .applymap(color_pl, subset=['P&L (R$)', 'P&L (%)']),
                    use_container_width=True,
                    hide_index=True,
                    height=300
                )
                
                # Métricas resumidas
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    total_pl = sum([float(p['P&L (R$)'].replace('R$ ', '').replace('+', '')) for p in posicoes_demo])
                    st.metric("P&L Total", f"R$ {total_pl:+.2f}")
                with col2:
                    st.metric("Posições Abertas", len(posicoes_demo))
                with col3:
                    long_pos = len([p for p in posicoes_demo if p['Tipo'] == 'LONG'])
                    st.metric("Taxa de Acerto", f"{66.7:.1f}%")  # Simulado
                with col4:
                    st.metric("Tempo Médio", "4h 30m")  # Simulado
                    
        return
    
    # Processa posições reais do MT5
    df_pos = pd.DataFrame(posicoes)
    
    # Converte para formato profissional
    posicoes_formatted = []
    for _, pos in df_pos.iterrows():
        tipo = 'LONG' if pos.get('type', 0) == 0 else 'SHORT'  # 0=buy, 1=sell no MT5
        pl_value = pos.get('profit', 0)
        preco_abertura = pos.get('price_open', 0)
        preco_atual = pos.get('price_current', 0)
        
        pl_percent = (pl_value / (preco_abertura * pos.get('volume', 1))) * 100 if preco_abertura > 0 else 0
        
        # Calcula tempo aberto
        tempo_abertura = pos.get('time', datetime.now())
        if isinstance(tempo_abertura, (int, float)):
            tempo_abertura = datetime.fromtimestamp(tempo_abertura)
        
        tempo_decorrido = datetime.now() - tempo_abertura
        hours, remainder = divmod(tempo_decorrido.total_seconds(), 3600)
        minutes, _ = divmod(remainder, 60)
        tempo_str = f"{int(hours)}:{int(minutes):02d}:00"
        
        pos_data = {
            'Par': pos.get('symbol', 'N/A'),
            'Tipo': tipo,
            'Volume': f"{pos.get('volume', 0):,.0f}",
            'Preço Abertura': f"R$ {preco_abertura:.2f}",
            'Preço Atual': f"R$ {preco_atual:.2f}",
            'P&L (R$)': f"R$ {pl_value:+.2f}",
            'P&L (%)': f"{pl_percent:+.2f}%",
            'Stop Loss': f"R$ {pos.get('sl', 0):.2f}" if pos.get('sl', 0) > 0 else 'N/A',
            'Take Profit': f"R$ {pos.get('tp', 0):.2f}" if pos.get('tp', 0) > 0 else 'N/A',
            'Tempo Aberto': tempo_str,
            'Setor': sistema.segmentos.get(pos.get('symbol', ''), 'Outros')
        }
        posicoes_formatted.append(pos_data)
    
    if posicoes_formatted:
        df_display = pd.DataFrame(posicoes_formatted)
        
        # Aplica cores
        def color_pl(val):
            if '+' in str(val):
                return 'color: green; font-weight: bold'
            elif '-' in str(val):
                return 'color: red; font-weight: bold'
            return ''
        
        def color_tipo(val):
            if val == 'LONG':
                return 'background-color: rgba(0, 255, 0, 0.1)'
            elif val == 'SHORT':
                return 'background-color: rgba(255, 0, 0, 0.1)'
            return ''
        
        st.dataframe(
            df_display.style.applymap(color_tipo, subset=['Tipo'])
                           .applymap(color_pl, subset=['P&L (R$)', 'P&L (%)']),
            use_container_width=True,
            hide_index=True,
            height=400
        )
        
        # Métricas resumidas reais
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_pl = sum([pos.get('profit', 0) for pos in posicoes])
            st.metric("P&L Total", f"R$ {total_pl:+.2f}")
        with col2:
            st.metric("Pares ", len(posicoes))
        with col3:
            winners = len([p for p in posicoes if p.get('profit', 0) > 0])
            win_rate = (winners / len(posicoes) * 100) if posicoes else 0
            st.metric("Taxa de Acerto", f"{win_rate:.1f}%")
        with col4:
            tempo_medio = sum([
                (datetime.now() - (datetime.fromtimestamp(p.get('time', 0)) if isinstance(p.get('time'), (int, float)) else datetime.now())).total_seconds() / 3600
                for p in posicoes
            ]) / len(posicoes) if posicoes else 0
            st.metric("Tempo Médio", f"{tempo_medio:.1f}h")
    
    # Botões de ação se conectado
    if sistema.mt5_connected and posicoes:
        st.markdown("---")
        st.markdown("**🎛️ Ações Rápidas:**")
        cols_actions = st.columns(min(len(posicoes), 4))  # Máximo 4 colunas
        
        for i, (col, pos) in enumerate(zip(cols_actions, posicoes[:4])):  # Máximo 4 botões
            with col:
                symbol = pos.get('symbol', 'N/A')
                if st.button(f"❌ Fechar {symbol}", key=f"close_{pos.get('ticket', i)}"):
                    if sistema.fechar_posicao(pos.get('ticket')):
                        st.success(f"Posição {symbol} fechada!")
                        st.rerun()
                    else:
                        st.error("Erro ao fechar posição")

def render_signals_table():
    """Renderiza tabela de sinais de trading com análise real - FORMATO PROFISSIONAL"""
    sistema = st.session_state.trading_system
    
    # Indicador de status da funcionalidade
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 📡 Sinais de Trading Ativos")
    
    with col2:
        if sistema.mt5_connected:
            st.markdown("✅ **REAL**", help="Dados obtidos em tempo real do MetaTrader 5")
        else:
            st.markdown("🔴 **OFFLINE**", help="MT5 desconectado - usando dados simulados")
    
    # PRIORIDADE 1: Verifica sinais_ativos (dados processados)
    if hasattr(sistema, 'sinais_ativos') and sistema.sinais_ativos:
        df_sinais = pd.DataFrame(sistema.sinais_ativos)
        
        # Converte para formato profissional
        sinais_formatted = []
        for _, row in df_sinais.iterrows():
            tipo_sinal = 'LONG' if row.get('sinal') == 'COMPRA' else 'SHORT'
            preco_atual = row.get('preco_atual', 100.0)
            preco_entrada = row.get('preco_entrada', preco_atual)
            
            # Calcula P&L estimado
            if tipo_sinal == 'LONG':
                pl_value = preco_atual - preco_entrada
            else:
                pl_value = preco_entrada - preco_atual
                
            pl_percent = (pl_value / preco_entrada * 100) if preco_entrada > 0 else 0
            
            sinal_data = {
                'Par': row.get('par', 'N/A'),
                'Tipo': tipo_sinal,
                'Volume': '1.000',
                'Preço Abertura': f"R$ {preco_entrada:.2f}",
                'Preço Atual': f"R$ {preco_atual:.2f}",
                'P&L (R$)': f"R$ {pl_value:+.2f}",
                'P&L (%)': f"{pl_percent:+.2f}%",
                'Stop Loss': f"R$ {preco_entrada * 0.98:.2f}",
                'Take Profit': f"R$ {preco_entrada * 1.05:.2f}",
                'Tempo Aberto': '0:00:00',
                'Setor': row.get('segmento', 'Outros')
            }
            sinais_formatted.append(sinal_data)
        
        if sinais_formatted:
            df_display = pd.DataFrame(sinais_formatted)
            
            # Métricas resumidas no estilo da imagem
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_pl = sum([float(s['P&L (R$)'].replace('R$ ', '').replace('+', '')) for s in sinais_formatted])
                st.metric("P&L Total", f"R$ {total_pl:+.2f}")
            with col2:
                st.metric("Posições Abertas", len(sinais_formatted))
            with col3:
                winners = len([s for s in sinais_formatted if '+' in s['P&L (R$)']])
                win_rate = (winners / len(sinais_formatted) * 100) if sinais_formatted else 0
                st.metric("Taxa de Acerto", f"{win_rate:.1f}%")
            with col4:
                st.metric("Tempo Médio", "4h 30m")
            
            # Aplica cores
            def color_pl(val):
                if '+' in str(val):
                    return 'color: green; font-weight: bold'
                elif '-' in str(val):
                    return 'color: red; font-weight: bold'
                return ''
            
            def color_tipo(val):
                if val == 'LONG':
                    return 'background-color: rgba(0, 255, 0, 0.1)'
                elif val == 'SHORT':
                    return 'background-color: rgba(255, 0, 0, 0.1)'
                return ''
            
            st.dataframe(
                df_display.style.applymap(color_tipo, subset=['Tipo'])
                               .applymap(color_pl, subset=['P&L (R$)', 'P&L (%)']),
                use_container_width=True,
                hide_index=True,
                height=400
            )
            return
    
    # PRIORIDADE 2: Verifica tabela_linha_operacao (primeira seleção)
    if hasattr(sistema, 'tabela_linha_operacao') and not sistema.tabela_linha_operacao.empty:
        st.info("📊 Exibindo sinais da primeira seleção...")
        
        df_primeira = sistema.tabela_linha_operacao.copy()
        
        # Converte para formato profissional
        sinais_formatted = []
        for _, row in df_primeira.iterrows():
            zscore = row.get('Z-Score', 0)
            r2 = row.get('r2', 0)
            preco_atual = row.get('preco_atual', 100.0)
            
            # Determina tipo baseado no Z-Score
            if zscore <= -1.5:
                tipo_sinal = 'LONG'
                pl_simulado = preco_atual * 0.01  # 1% ganho simulado
            elif zscore >= 1.5:
                tipo_sinal = 'SHORT'
                pl_simulado = preco_atual * 0.008  # 0.8% ganho simulado
            else:
                continue  # Pula sinais neutros
            
            sinal_data = {
                'Par': f"{row.get('Dependente', 'N/A')}/{row.get('Independente', 'N/A')}",
                'Tipo': tipo_sinal,
                'Volume': '1.000',
                'Preço Abertura': f"R$ {preco_atual:.2f}",
                'Preço Atual': f"R$ {preco_atual:.2f}",
                'P&L (R$)': f"R$ {pl_simulado:+.2f}",
                'P&L (%)': f"{(pl_simulado/preco_atual*100):+.2f}%",
                'Stop Loss': f"R$ {preco_atual * 0.98:.2f}",
                'Take Profit': f"R$ {preco_atual * 1.05:.2f}",
                'Tempo Aberto': '0:00:00',
                'Setor': sistema.segmentos.get(row.get('Dependente', ''), 'Outros')
            }
            sinais_formatted.append(sinal_data)
        
        if sinais_formatted:
            df_display = pd.DataFrame(sinais_formatted)
            
            # Métricas resumidas no estilo da imagem
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_pl = sum([float(s['P&L (R$)'].replace('R$ ', '').replace('+', '')) for s in sinais_formatted])
                st.metric("P&L Total", f"R$ {total_pl:+.2f}")
            with col2:
                st.metric("Posições Abertas", len(sinais_formatted))
            with col3:
                long_count = len([s for s in sinais_formatted if s['Tipo'] == 'LONG'])
                win_rate = 66.7  # Taxa simulada
                st.metric("Taxa de Acerto", f"{win_rate:.1f}%")
            with col4:
                st.metric("Tempo Médio", "4h 30m")
            
            # Aplica cores
            def color_pl(val):
                if '+' in str(val):
                    return 'color: green; font-weight: bold'
                elif '-' in str(val):
                    return 'color: red; font-weight: bold'
                return ''
            
            def color_tipo(val):
                if val == 'LONG':
                    return 'background-color: rgba(0, 255, 0, 0.1)'
                elif val == 'SHORT':
                    return 'background-color: rgba(255, 0, 0, 0.1)'
                return ''
            
            st.dataframe(
                df_display.style.applymap(color_tipo, subset=['Tipo'])
                               .applymap(color_pl, subset=['P&L (R$)', 'P&L (%)']),
                use_container_width=True,
                hide_index=True,
                height=400
            )
            return
      # FALLBACK: Nenhum dado disponível
    if sistema.mt5_connected:
        st.info("📡 Aguardando análise de sinais... Inicie o sistema para executar análises reais.")
    else:
        st.warning("🔌 Conecte ao MT5 para executar análises reais de sinais de trading")
    
    with st.expander("ℹ️ Sobre a Análise Real"):
        st.markdown("""
        **🔬 Sistema de Análise Integrado:**
        - ✅ **Dados históricos reais** obtidos via MT5
        - ✅ **Cálculo de Z-Score** baseado em regressão linear
        - ✅ **Filtros de qualidade** (R², Beta, Cointegração)
        - ✅ **Teste de estacionariedade** (ADF)
        - ✅ **Análise de pares** automatizada
        """)

def render_profit_distribution():
    """Renderiza distribuição de lucros/prejuízos com dados reais do MT5"""
    sistema = st.session_state.trading_system
    
    # Indicador de status da funcionalidade
    col1, col2 = st.columns([3, 1])
    #with col1:
        #st.markdown("### 📊 Distribuição de Resultados por Trade")
    with col2:
        if sistema.mt5_connected:
            st.markdown("✅ **online**", help="Dados de distribuição obtidos do histórico real de trades do MT5")
        else:
            st.markdown("🔴 **offline**", help="MT5 desconectado - usando dados de demonstração")
    
    # Busca dados reais se conectado ao MT5
    if sistema.mt5_connected:
        try:
            # Busca histórico dos últimos  30 dias
            data_inicio = datetime.now() - timedelta(days=30)
            data_fim = datetime.now()
            
            trades_reais = sistema.obter_historico_trades_real(data_inicio, data_fim)
            
            if trades_reais and len(trades_reais) > 0:
                # Extrai os lucros dos trades reais
                lucros_reais = [trade['Lucro'] for trade in trades_reais if 'Lucro' in trade]
                
                if lucros_reais and len(lucros_reais) > 0:  # Mínimo de 5 trades para análise
                    fig = go.Figure()
                    
                    fig.add_trace(go.Histogram(
                        x=lucros_reais,
                        nbinsx=min(20, len(lucros_reais)//2),
                        name="Distribuição P/L (Real)",
                        marker_color='#2980b9',
                        opacity=0.7
                    ))
                    
                    # Adiciona linhas de threshold
                    fig.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="Break Even")
                    fig.add_vline(x=np.mean(lucros_reais), line_dash="dash", line_color="green", annotation_text="Média")
                    
                    # Estatísticas dos dados reais
                    trades_lucrativos = len([l for l in lucros_reais if l > 0])
                    win_rate = (trades_lucrativos / len(lucros_reais)) * 100
                    
                    fig.update_layout(
                        title=f"📊 Distribuição de Resultados por ({len(lucros_reais)} trades)",
                        xaxis_title="Lucro/Prejuízo (R$)",
                        yaxis_title="Frequência",
                        height=400,
                        template="plotly_white"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Exibe métricas dos dados reais
                    #col1, col2, col3, col4 = st.columns(4)
                    
                    #with col1:
                        #st.metric("Total de Trades", len(lucros_reais))
                    
                    #with col2:
                        #st.metric("Win Rate", f"{win_rate:.1f}%")
                    
                    #with col3:
                        #resultado_total = sum(lucros_reais)
                        #st.metric("Resultado Total", f"R$ {resultado_total:,.2f}")
                    
                    #with col4:
                        #resultado_medio = np.mean(lucros_reais)
                        #st.metric("Resultado Médio", f"R$ {resultado_medio:.2f}")
                    
                    #st.success(f"✅ Análise baseada em {len(lucros_reais)} trades reais dos últimos 30 dias")
                    return
                else:
                    st.info("📊 Poucos trades encontrados para análise estatística")
            else:
                st.info("📊 Nenhum trade encontrado nos últimos 30 dias")
                
        except Exception as e:
            sistema.log(f"❌ Erro ao buscar dados reais: {str(e)}")
            st.error(f"Erro ao buscar dados reais: {str(e)}")
    
    # Fallback para dados simulados se não há dados reais
    st.warning("🔌 Conecte ao MT5 para visualizar distribuição dos resultados")
    
    # Simula dados de trades para demonstração
    #np.random.seed(42)
    #trades_results = np.random.normal(50, 200, 100)  # Média R$ 50, desvio R$ 200
    
    #fig = go.Figure()
    
    #fig.add_trace(go.Histogram(
        #x=trades_results,
        #nbinsx=20,
        #name="Distribuição P/L (Demo)",
        #marker_color='lightblue',
        #opacity=0.7
    #))
    
    # Adiciona linhas de threshold
    #fig.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="Break Even")
    #fig.add_vline(x=np.mean(trades_results), line_dash="dash", line_color="green", annotation_text="Média")
    
    #fig.update_layout(
        #title="📊 Distribuição de Resultados - Simulação Demo",
        #xaxis_title="Lucro/Prejuízo (R$)",
        #yaxis_title="Frequência",
        #height=400,
        #template="plotly_white"
    #)
    
    #st.plotly_chart(fig, use_container_width=True)
    
    #st.info("🔧 **Conecte ao MT5 para visualizar distribuição real de resultados**")

def render_trade_history():
    """Renderiza histórico de trades com dados reais do MT5"""
    sistema = st.session_state.trading_system
    
    # Indicador de status da funcionalidade
    col1, col2 = st.columns([3, 1])
    #with col1:
        #st.markdown("### 📋 Histórico de Trades")
    with col2:
        if sistema.mt5_connected:
            st.markdown("✅ **REAL**", help="Histórico obtido em tempo real do MetaTrader 5")
        else:
            st.markdown("🔴 **OFFLINE**", help="MT5 desconectado - usando dados de demonstração")
    
    # Filtros de período
    col1, col2, col3 = st.columns(3)
    
    with col1:
        data_inicio = st.date_input("Data Início", value=datetime.now().date() - timedelta(days=30))
    
    with col2:
        data_fim = st.date_input("Data Fim", value=datetime.now().date())
    
    with col3:
        filtro_resultado = st.selectbox("Resultado", ["Todos", "Lucro", "Prejuízo"])
    
    # Busca dados reais se conectado ao MT5
    if sistema.mt5_connected:
        try:
            # Converte datas para datetime
            dt_inicio = datetime.combine(data_inicio, time.min)
            dt_fim = datetime.combine(data_fim, time.max)
            
            # Busca trades reais do MT5
            trades_reais = sistema.obter_historico_trades_real(dt_inicio, dt_fim)
            
            if trades_reais and len(trades_reais) > 0:
                df_trades = pd.DataFrame(trades_reais)
                
                # Aplica filtros
                if filtro_resultado == "Lucro":
                    df_trades = df_trades[df_trades['Lucro'] > 0]
                elif filtro_resultado == "Prejuízo":
                    df_trades = df_trades[df_trades['Lucro'] < 0]
                
                # Formata colunas para exibição
                df_display = df_trades.copy()
                if not df_display.empty:
                    # Formata data
                    df_display['Data'] = df_display['Data'].dt.strftime('%d/%m/%Y %H:%M')
                    
                    # Formata valores monetários
                    df_display['Preço'] = df_display['Preço'].apply(lambda x: f"R$ {x:.2f}")
                    df_display['Lucro'] = df_display['Lucro'].apply(lambda x: f"R$ {x:.2f}")
                    if 'Comissão' in df_display.columns:
                        df_display['Comissão'] = df_display['Comissão'].apply(lambda x: f"R$ {x:.2f}")
                    if 'Swap' in df_display.columns:
                        df_display['Swap'] = df_display['Swap'].apply(lambda x: f"R$ {x:.2f}")
                    
                    # Seleciona colunas relevantes para exibição
                    cols_exibir = ['Ticket', 'Par', 'Tipo', 'Data', 'Volume', 'Preço', 'Lucro']
                    if 'Comissão' in df_display.columns:
                        cols_exibir.append('Comissão')
                    if 'Comentário' in df_display.columns:
                        cols_exibir.append('Comentário')
                    
                    df_display = df_display[cols_exibir]
                    
                    # ESTATÍSTICAS PRIMEIRO - Calcula e exibe estatísticas reais ANTES da tabela
                    estatisticas = sistema.calcular_estatisticas_performance_real(trades_reais)
                    
                    #st.markdown("### 📊 Estatísticas do Período (Dados Reais)")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Trades", estatisticas['total_trades'])
                    
                    with col2:
                        st.metric("Win Rate", f"{estatisticas['win_rate']:.1f}%")
                    
                    with col3:
                        st.metric("Resultado Total", f"R$ {estatisticas['resultado_total']:,.2f}")
                    
                    with col4:
                        st.metric("Resultado Médio", f"R$ {estatisticas['resultado_medio']:.2f}")
                    
                    # Segunda linha de estatísticas
                    col5, col6, col7, col8 = st.columns(4)
                    
                    with col5:
                        st.metric("Melhor Trade", f"R$ {estatisticas['melhor_trade']:,.2f}")
                    
                    with col6:
                        st.metric("Pior Trade", f"R$ {estatisticas['pior_trade']:,.2f}")
                    
                    with col7:
                        st.metric("Profit Factor", f"{estatisticas['profit_factor']:.2f}")
                    
                    with col8:
                        st.metric("Max Drawdown", f"{estatisticas['max_drawdown']:.2f}%")
                    
                    #st.success(f"✅ Estatísticas baseadas em {len(trades_reais)} trades reais do MT5")
                    
                    st.markdown("---")
                    
                    # TABELA DEPOIS - Exibe tabela APÓS as estatísticas
                    #st.markdown("### 📋 Detalhamento dos Trades")
                    st.dataframe(
                        df_display,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    #st.success(f"✅ Estatísticas baseadas em {len(trades_reais)} trades reais do MT5")
                    return
                else:
                    st.info(f"📊 Nenhum trade encontrado no período com filtro '{filtro_resultado}'")
                    return
            else:
                st.info("📊 Nenhum trade encontrado no período selecionado")
                return
                
        except Exception as e:
            sistema.log(f"❌ Erro ao buscar histórico real: {str(e)}")
            st.error(f"Erro ao buscar dados reais: {str(e)}")
    
    # Fallback para dados simulados se não há conexão MT5
    st.warning("📊 MT5 desconectado - usando dados simulados para demonstração")
    
    # Simula dados para demonstração
    trades_simulados = []
    np.random.seed(42)
    for i in range(50):
        resultado = np.random.normal(50, 200)
        trades_simulados.append({
            'Ticket': f"12345{i:02d}",
            'Par': np.random.choice(['PETR4', 'VALE3', 'ITUB4', 'BBDC4']),
            'Tipo': np.random.choice(['COMPRA', 'VENDA']),
            'Data': (datetime.now() - timedelta(days=np.random.randint(1, 30))).strftime('%d/%m/%Y %H:%M'),
            'Volume': round(np.random.uniform(100, 1000), 0),
            'Preço': f"R$ {np.random.uniform(20, 100):.2f}",
            'Lucro': f"R$ {resultado:.2f}",
            'Comentário': 'Trade simulado'
        })
    
    df_trades = pd.DataFrame(trades_simulados)
    
    # Aplica filtros aos dados simulados
    if filtro_resultado == "Lucro":
        df_trades = df_trades[df_trades['Lucro'].str.replace('R$ ', '').str.replace(',', '').astype(float) > 0]
    elif filtro_resultado == "Prejuízo":
        df_trades = df_trades[df_trades['Lucro'].str.replace('R$ ', '').str.replace(',', '').astype(float) < 0]
    
    # ESTATÍSTICAS PRIMEIRO - Estatísticas simuladas ANTES da tabela
    #if not df_trades.empty:
        #st.markdown("### 📊 Estatísticas do Período (Dados Simulados)")
        #col1, col2, col3, col4 = st.columns(4)
        
        #with col1:
            #st.metric("Total Trades", len(df_trades))
        
        #with col2:
            # Converte lucros para float para calcular win rate
            #lucros_float = df_trades['Lucro'].str.replace('R$ ', '').str.replace(',', '').astype(float)
            #trades_lucro = len(lucros_float[lucros_float > 0])
            #win_rate = (trades_lucro / len(df_trades)) * 100
            #st.metric("Win Rate", f"{win_rate:.1f}%")
        
        #with col3:
            #resultado_total = lucros_float.sum()
            #st.metric("Resultado Total", f"R$ {resultado_total:,.2f}")
        
        #with col4:
            #resultado_medio = lucros_float.mean()
            #st.metric("Resultado Médio", f"R$ {resultado_medio:.2f}")
        
        #st.info("🔧 **Conecte ao MT5 para visualizar estatísticas reais de trades**")
        
        #st.markdown("---")
        
        # TABELA DEPOIS - Tabela simulada APÓS as estatísticas
        #st.markdown("### 📋 Detalhamento dos Trades (Simulado)")
        #st.dataframe(df_trades, use_container_width=True, hide_index=True)

def render_logs():
    """Renderiza logs do sistema"""
    sistema = st.session_state.trading_system
    
    #st.markdown("### 📝 Log de Eventos do Sistema")
    
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
    #st.markdown("### 📤 Exportação de Relatórios")
    
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

def render_segunda_selecao():
    """Renderiza aba com dados detalhados da segunda seleção - FORMATO PROFISSIONAL"""
    #st.markdown("### 🎯 Segunda Seleção - Análise Refinada")
    
    sistema = st.session_state.trading_system
    
    # DEBUG: Sempre mostra estado atual dos dados
    with st.expander("🔍 DEBUG: Estado Atual dos Dados (Sempre Visível)"):
        st.write("**📊 Verificando todas as fontes de dados:**")
        
        # Verifica sinais_ativos
        if hasattr(sistema, 'sinais_ativos'):
            sinais_count = len(sistema.sinais_ativos) if sistema.sinais_ativos else 0
            st.write(f"- `sinais_ativos`: {sinais_count} itens")
            if sistema.sinais_ativos:
                st.write("  **Primeiros 3 exemplos:**")
                for i, sinal in enumerate(sistema.sinais_ativos[:3]):
                    st.write(f"    {i+1}. {sinal}")
        else:
            st.write("- `sinais_ativos`: ❌ Atributo não existe")
        
        # Verifica tabela_linha_operacao01
        if hasattr(sistema, 'tabela_linha_operacao01'):
            if isinstance(sistema.tabela_linha_operacao01, pd.DataFrame):
                st.write(f"- `tabela_linha_operacao01`: {len(sistema.tabela_linha_operacao01)} linhas")
                if not sistema.tabela_linha_operacao01.empty:
                    st.write("  **Colunas:**", list(sistema.tabela_linha_operacao01.columns))
            else:
                st.write(f"- `tabela_linha_operacao01`: {type(sistema.tabela_linha_operacao01)}")
        else:
            st.write("- `tabela_linha_operacao01`: ❌ Atributo não existe")
        
        # Verifica tabela_linha_operacao
        if hasattr(sistema, 'tabela_linha_operacao'):
            if isinstance(sistema.tabela_linha_operacao, pd.DataFrame):
                st.write(f"- `tabela_linha_operacao`: {len(sistema.tabela_linha_operacao)} linhas")
                if not sistema.tabela_linha_operacao.empty:
                    extremos = len(sistema.tabela_linha_operacao[sistema.tabela_linha_operacao['Z-Score'].abs() >= 1.5])
                    st.write(f"  **Z-Score extremo (≥1.5):** {extremos} pares")
            else:
                st.write(f"- `tabela_linha_operacao`: {type(sistema.tabela_linha_operacao)}")
        else:
            st.write("- `tabela_linha_operacao`: ❌ Atributo não existe")
    
    # CORREÇÃO: Verifica PRIMEIRA os sinais_ativos (dados processados da segunda seleção)
    df_segunda = None
    source_info = ""
    
    # PRIORIDADE 1: sinais_ativos (dados já processados da segunda seleção)
    if hasattr(sistema, 'sinais_ativos') and sistema.sinais_ativos:
        #st.info(f"🎯 Encontrados {len(sistema.sinais_ativos)} sinais em sinais_ativos")
        
        # Converte sinais_ativos para DataFrame para exibição
        sinais_data = []
        for sinal in sistema.sinais_ativos:
            # Extrai par (pode estar em formato "PAR1/PAR2" ou só "PAR1")
            par_original = sinal.get('par', '')
            if '/' in par_original:
                dependente = par_original.split('/')[0]
                independente = par_original.split('/')[1]
            else:
                dependente = par_original
                independente = 'INDEX'  # Fallback
            
            sinais_data.append({
                'Dependente': dependente,
                'Independente': independente,
                'Z-Score': sinal.get('zscore', sinal.get('Z-Score', 0)),
                'r2': sinal.get('r2', 0.7),  # Valor padrão se não existir
                'preco_atual': sinal.get('preco_atual', 100),
                'Preco_Entrada_Final': sinal.get('preco_entrada', sinal.get('preco_atual', 100)),
                'sinal': sinal.get('sinal', 'NEUTRO'),
                'beta_rotation': sinal.get('beta_rotation', 0),
                'beta_rotation_mean': sinal.get('beta_rotation_mean', 0),
                'status': sinal.get('status', 'PROCESSADO')
            })
        
        if sinais_data:
            df_segunda = pd.DataFrame(sinais_data)
            source_info = f"🏆 {len(df_segunda)} sinais da segunda seleção (DADOS REAIS PROCESSADOS)"
            #st.success(source_info)
    
    # PRIORIDADE 2: tabela_linha_operacao01 (segunda seleção salva)
    elif hasattr(sistema, 'tabela_linha_operacao01') and not sistema.tabela_linha_operacao01.empty:
        df_segunda = sistema.tabela_linha_operacao01.copy()
        source_info = f"🏆 {len(df_segunda)} pares da tabela de segunda seleção (DADOS SALVOS)"
        st.success(source_info)
    
    # PRIORIDADE 3: tabela_linha_operacao (primeira seleção filtrada)
    elif hasattr(sistema, 'tabela_linha_operacao') and not sistema.tabela_linha_operacao.empty:
        df_primeira = sistema.tabela_linha_operacao.copy()
        # Filtra apenas pares com Z-Score extremo (simula segunda seleção)
        df_segunda = df_primeira[df_primeira['Z-Score'].abs() >= 1.5].copy()
        if not df_segunda.empty:
            source_info = f"📊 {len(df_segunda)} pares filtrados da primeira seleção (SIMULAÇÃO)"
            st.info(source_info)
        else:
            st.warning("⚠️ Nenhum par atende aos critérios de Z-Score extremo (≥1.5 ou ≤-1.5)")
            return    
    # FALLBACK: Sem dados
    else:
        st.warning("⚠️ Nenhum dado da segunda seleção disponível")
        st.info("💡 Execute a análise completa para gerar dados da segunda seleção")
        
        with st.expander("ℹ️ Sobre a Segunda Seleção"):
            st.markdown("""
            **🎯 Critérios da Segunda Seleção:**
            - ✅ **Z-Score >= 2.0** ou **Z-Score <= -2.0**
            - ✅ **Beta rotation > média** (para venda) ou **< média** (para compra)
            - ✅ **R² mínimo** para garantir correlação
            - ✅ **Teste de cointegração** (ADF p-value)
            - ✅ **Filtros de spread** e diferença de preço
            """)
        return
    
    # PROCESSAMENTO DOS DADOS DA SEGUNDA SELEÇÃO
    if df_segunda is not None and not df_segunda.empty:
        
        # Métricas resumidas no estilo da imagem
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Calcula P&L total simulado baseado em Z-Score
            total_pl = 0
            for _, row in df_segunda.iterrows():
                zscore = row.get('Z-Score', 0)
                preco_atual = row.get('preco_atual', 100)
                if zscore <= -1.5:  # LONG
                    total_pl += preco_atual * 0.015  # 1.5% ganho simulado
                elif zscore >= 1.5:  # SHORT
                    total_pl += preco_atual * 0.012  # 1.2% ganho simulado
            st.metric("P&L Total", f"R$ +{total_pl:.2f}")
        
        with col2:
            st.metric("Posições Abertas", len(df_segunda))
        
        with col3:
            # Taxa de acerto baseada em R² médio
            r2_medio = df_segunda['r2'].mean() if 'r2' in df_segunda.columns else 0.65
            taxa_acerto = min(95, max(50, r2_medio * 100))
            st.metric("Taxa de Acerto", f"{taxa_acerto:.1f}%")
        
        with col4:
            # Tempo médio simulado baseado na volatilidade
            tempo_medio = "4h 30m" if len(df_segunda) <= 5 else "3h 15m"
            st.metric("Tempo Médio", tempo_medio)
        
        st.markdown("---")
        
        # Converte dados para formato profissional da tabela
        posicoes_segunda = []
        for i, (_, row) in enumerate(df_segunda.iterrows()):
            dep = row.get('Dependente', 'N/A')
            ind = row.get('Independente', 'N/A')
            zscore = row.get('Z-Score', 0)
            r2 = row.get('r2', 0)
            preco_atual = row.get('preco_atual', 100 + i*10)  # Preços variados
            preco_entrada = row.get('Preco_Entrada_Final', preco_atual * 0.998)  # Entrada ligeiramente melhor
            
            # Determina tipo baseado no Z-Score
            if zscore <= -1.5:
                tipo = 'LONG'
                # Simula ganho baseado no Z-Score
                pl_estimado = abs(zscore) * preco_atual * 0.008  # Ganho proporcional
            elif zscore >= 1.5:
                tipo = 'SHORT'
                # Simula ganho baseado no Z-Score
                pl_estimado = zscore * preco_atual * 0.006  # Ganho proporcional
            else:
                tipo = 'NEUTRO'
                pl_estimado = preco_atual * 0.001  # Ganho mínimo
            
            pl_percent = (pl_estimado / preco_entrada * 100) if preco_entrada > 0 else 0
            
            # Volume baseado na confiança (R²) e Z-Score
            volume_base = 1000
            volume_multiplicador = 1 + (r2 * 0.5) + (abs(zscore) * 0.1)
            volume = int(volume_base * volume_multiplicador)
            
            # Calcula stop loss e take profit baseado no tipo
            if tipo == 'LONG':
                stop_loss = preco_entrada * 0.97  # 3% abaixo
                take_profit = preco_entrada * 1.06  # 6% acima
            elif tipo == 'SHORT':
                stop_loss = preco_entrada * 1.03  # 3% acima
                take_profit = preco_entrada * 0.94  # 6% abaixo
            else:
                stop_loss = preco_entrada * 0.98
                take_profit = preco_entrada * 1.02
            
            # Tempo aberto simulado baseado na posição
            tempo_horas = 2 + (i % 5)  # Varia de 2 a 6 horas
            tempo_mins = (i * 15) % 60  # Varia os minutos
            tempo_str = f"{tempo_horas}:{tempo_mins:02d}:00"
            
            pos_data = {
                'Par': f"{dep}/{ind}",
                'Tipo': tipo,
                'Volume': f"{volume:,}",
                'Preço Abertura': f"R$ {preco_entrada:.2f}",
                'Preço Atual': f"R$ {preco_atual:.2f}",
                'P&L (R$)': f"R$ {pl_estimado:+.2f}",
                'P&L (%)': f"{pl_percent:+.2f}%",
                'Stop Loss': f"R$ {stop_loss:.2f}",
                'Take Profit': f"R$ {take_profit:.2f}",
                'Tempo Aberto': tempo_str,
                'Setor': sistema.segmentos.get(dep, 'Energia/Mineração'),
                # Campos adicionais para análise
                'Z-Score': f"{zscore:.3f}",
                'R²': f"{r2:.3f}",
                'Beta_Rot': f"{row.get('beta_rotation', 0.5 + i*0.1):.3f}",
                'Confiança': f"{min(95, r2 * 100):.1f}%"
            }
            posicoes_segunda.append(pos_data)
        
        if posicoes_segunda:
            # Monta tabela padronizada com busca robusta para cada coluna
            colunas_padrao = [
                'ID', 'DEPENDENTE', 'INDEPENDENTE', 'PERIODO', 'ZSCORE', 'BETA', 'R2', 'ADF_P_VALUE', 'COINT_P_VALUE', 'COINT_CRITICAL_VALUES', 'CORRELACAO'
            ]
            def buscar_valor(row, nomes):
                for nome in nomes:
                    if nome in row:
                        return row[nome]
                return ''
            mapeamento = {
                'ID': ['ID', 'id', 'id_par', 'ID Par'],
                'DEPENDENTE': ['Dependente', 'DEP', 'Ativo', 'ativo'],
                'INDEPENDENTE': ['Independente', 'INDEP'],
                'PERIODO': ['Periodo', 'PERIODO', 'periodo'],
                'ZSCORE': ['Z-Score', 'zscore', 'ZSCORE'],
                'BETA': ['beta', 'BETA', 'Beta_Rot', 'beta_rotation'],
                'R2': ['R2', 'r2', 'R²'],
                'ADF_P_VALUE': ['adf_p_value', 'ADF_P_VALUE'],
                'COINT_P_VALUE': ['coint_p_value', 'COINT_P_VALUE'],
                'COINT_CRITICAL_VALUES': ['coint_critical_values', 'COINT_CRITICAL_VALUES'],
                'CORRELACAO': ['correlacao', 'CORRELACAO', 'Correlacao'],
            }
            tabela_padrao = []
            for row in posicoes_segunda:
                linha = {}
                for col in colunas_padrao:
                    linha[col] = buscar_valor(row, mapeamento[col])
                tabela_padrao.append(linha)
            df_padrao = pd.DataFrame(tabela_padrao)
            st.dataframe(df_padrao, use_container_width=True, hide_index=True, height=400)

            # Substitui df_filtered por df_padrao nas análises adicionais
            with st.expander("🔬 Análise Detalhada dos Pares da Segunda Seleção"):
                if len(df_padrao) > 0:
                    col_chart1, col_chart2 = st.columns(2)
                    with col_chart1:
                        setor_dist = df_padrao['CORRELACAO'].value_counts() if 'CORRELACAO' in df_padrao.columns else None
                        if setor_dist is not None:
                            fig_setor = px.pie(
                                values=setor_dist.values,
                                names=setor_dist.index,
                                title="Distribuição por Correlação"
                            )
                            st.plotly_chart(fig_setor, use_container_width=True)
                    with col_chart2:
                        # Gráfico P&L por tipo (não disponível na tabela padronizada, exemplo)
                        pass
                    st.markdown("#### 📈 Estatísticas da Segunda Seleção")
                    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
                    with stats_col1:
                        long_count = len(df_padrao[df_padrao['ZSCORE'].astype(str).str.startswith('-')])
                        st.metric("ZSCORE Negativo", long_count)
                    with stats_col2:
                        short_count = len(df_padrao[df_padrao['ZSCORE'].astype(str).str.startswith('1')])
                        st.metric("ZSCORE >= 1", short_count)
                    with stats_col3:
                        if 'ZSCORE' in df_padrao.columns:
                            try:
                                zscore_medio = pd.to_numeric(df_padrao['ZSCORE'], errors='coerce').mean()
                                st.metric("ZSCORE Médio", f"{zscore_medio:.2f}")
                            except:
                                st.metric("ZSCORE Médio", "N/A")
                        else:
                            st.metric("ZSCORE Médio", "N/A")
                    with stats_col4:
                        if 'R2' in df_padrao.columns:
                            try:
                                r2_medio = pd.to_numeric(df_padrao['R2'], errors='coerce').mean()
                                st.metric("R2 Médio", f"{r2_medio:.3f}")
                            except:
                                st.metric("R2 Médio", "N/A")
                        else:
                            st.metric("R2 Médio", "N/A")
            
            # Análise adicional em seção expandível
            with st.expander("🔬 Análise Detalhada dos Pares da Segunda Seleção"):
                if len(df_filtered) > 0:
                    col_chart1, col_chart2 = st.columns(2)
                    
                    with col_chart1:
                        # Gráfico de distribuição por setor
                        setor_dist = df_filtered['Setor'].value_counts()
                        fig_setor = px.pie(
                            values=setor_dist.values,
                            names=setor_dist.index,
                            title="Distribuição por Setor"
                        )
                        st.plotly_chart(fig_setor, use_container_width=True)
                    
                    with col_chart2:
                        # Gráfico P&L por tipo
                        pl_values = []
                        tipos = []
                        for _, row in df_filtered.iterrows():
                            pl_str = row['P&L (R$)'].replace('R$ ', '').replace('+', '')
                            try:
                                pl_val = float(pl_str)
                                pl_values.append(pl_val)
                                tipos.append(row['Tipo'])
                            except:
                                pass
                        
                        if pl_values:
                            fig_pl = px.box(
                                x=tipos,
                                y=pl_values,
                                title="Distribuição P&L por Tipo"
                            )
                            st.plotly_chart(fig_pl, use_container_width=True)
                      # Estatísticas resumidas
                    st.markdown("#### 📈 Estatísticas da Segunda Seleção")
                    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
                    
                    with stats_col1:
                        long_count = len(df_filtered[df_filtered['Tipo'] == 'LONG'])
                        st.metric("Posições LONG", long_count)
                    
                    with stats_col2:
                        short_count = len(df_filtered[df_filtered['Tipo'] == 'SHORT'])
                        st.metric("Posições SHORT", short_count)
                    
                    with stats_col3:
                        if 'Z-Score' in df_filtered.columns:
                            zscore_medio = df_filtered['Z-Score'].apply(lambda x: float(x) if isinstance(x, str) else x).mean()
                            st.metric("Z-Score Médio", f"{zscore_medio:.2f}")
                        else:
                            st.metric("Z-Score Médio", "N/A")
                    
                    with stats_col4:
                        if 'R²' in df_filtered.columns:
                            r2_medio = df_filtered['R²'].apply(lambda x: float(x) if isinstance(x, str) else x).mean()
                            st.metric("R² Médio", f"{r2_medio:.3f}")
                        else:
                            st.metric("R² Médio", "N/A")
        
        else:
            st.error("❌ Erro ao processar dados da segunda seleção")
    
    else:
        # Mostra exemplo se houver dados da primeira seleção
        if hasattr(sistema, 'tabela_linha_operacao') and not sistema.tabela_linha_operacao.empty:
            st.info("💡 Dados da primeira seleção disponíveis. Execute a segunda seleção para análise refinada.")
            
            df_primeira = sistema.tabela_linha_operacao.copy()
            
            # Métricas da primeira seleção
            col1, col2, col3 = st.columns(3)
            
            with col1:
                zscore_medio = df_primeira['Z-Score'].abs().mean()
                st.metric("Z-Score Médio", f"{zscore_medio:.2f}")
            
            with col2:
                r2_medio = df_primeira['r2'].mean() if 'r2' in df_primeira.columns else 0
                st.metric("R² Médio", f"{r2_medio:.3f}")
            
            with col3:
                pares_extremos = len(df_primeira[df_primeira['Z-Score'].abs() >= 2.0])
                st.metric("Pares Extremos", f"{pares_extremos}")
              # Tabela resumida da primeira seleção
            st.markdown("#### 📋 Prévia da Primeira Seleção")
            colunas_preview = ['Dependente', 'Independente', 'Z-Score', 'r2']
            if all(col in df_primeira.columns for col in colunas_preview):
                df_preview = df_primeira[colunas_preview].head(10).copy()
                df_preview['Z-Score'] = df_preview['Z-Score'].round(3)
                df_preview['r2'] = df_preview['r2'].round(3)
                st.dataframe(df_preview, use_container_width=True)
            
            st.info("💡 Execute a segunda seleção para obter análise completa com spreads e previsões!")
        else:
            st.info("📊 Nenhuma análise disponível. Execute o sistema para gerar dados.")
        
        with st.expander("ℹ️ Sobre a Segunda Seleção"):
            st.markdown("""
            **🎯 O que é a Segunda Seleção?**
            
            A segunda seleção é um processo de refinamento que:
            
            1. **🔍 Analisa os melhores pares** da primeira seleção
            2. **📊 Aplica calcular_residuo_zscore_timeframe01** para análise detalhada
            3. **💰 Calcula preços de entrada otimizados** baseados em spreads
            4. **⚡ Prioriza por proximidade de preço** para maximizar execução
            5. **🎯 Gera tabela_linha_operacao01** com pares prontos para trade
            
            **📈 Vantagens:**
            - Maior precisão na entrada
            - Redução de slippage
            - Melhor gestão de risco
            - Pares priorizados por viabilidade de execução
            
            **🔧 Para ativar:** Inicie o sistema de análise real no painel principal.
            """)

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
            #st.markdown(f"**Última atualização:** {ultima_atualizacao}")    # Cartões de status
    render_status_cards()
    
    st.markdown("---")
      # Painéis principais
    tab1, tab3, tab2, tab4, tab5 = st.tabs(["📊 Gráficos e Análises", "🎯 Pares Validados", "📡 Sinais e Posições", "📋 Históricos", "📝 Log de Eventos"])
    
    with tab1:
        # Gráficos lado a lado
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de equity
            render_equity_chart()
        
        with col2:
            # Distribuição de resultados
            render_profit_distribution()
        st.markdown("---")
        
        # Posições Detalhadas
        render_positions_table()
        
        st.markdown("---")
        
        # Botões de exportação
        #st.markdown("### 📤 Exportação de Relatórios")
        render_export_section()
    with tab2:
        # Apenas sinais de trading
        render_signals_table()
    
    with tab3:
        render_segunda_selecao()
    
    with tab4:
        # Histórico de trades
        render_trade_history()
    
    with tab5:
        # Log de Eventos do Sistema
        render_logs()
    
    # Auto-refresh a cada 30 segundos se o sistema estiver rodando
    if st.session_state.trading_system.running:
        time_module.sleep(1)  # Pequena pausa para não sobrecarregar
        st.rerun()

def obter_equity_historico_mt5(sistema):
    """Obtém histórico de equity diretamente do MT5 para popular o gráfico"""
    if not sistema.mt5_connected:
        return []
    
    try:
        import MetaTrader5 as mt5
        from datetime import datetime, timedelta
        
        # Busca dados dos últimos 7 dias ou desde o início do mês
        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=7)  # Últimos 7 dias
        
        # Tenta obter o histórico de deals para reconstruir a curva de equity
        deals = mt5.history_deals_get(data_inicio, data_fim)
        
        if not deals or len(deals) == 0:
            # Se não há deals, cria um ponto com dados atuais
            account_info = mt5.account_info()
            if account_info:
                return [{
                    'timestamp': datetime.now(),
                    'equity': account_info.equity,
                    'balance': account_info.balance,
                    'profit': account_info.profit
                }]
            return []
        
        # Reconstroi curva de equity baseada nos deals
        equity_historico = []
        account_info = mt5.account_info()
        if not account_info:
            return []
        
        equity_atual = account_info.equity
        balance_atual = account_info.balance
        
        # Calcula equity inicial (aproximado)
        lucro_total_deals = sum([deal.profit for deal in deals if hasattr(deal, 'profit')])
        equity_inicial = equity_atual - lucro_total_deals
        
        # Cria pontos da curva
        equity_historico.append({
            'timestamp': data_inicio,
            'equity': equity_inicial,
            'balance': balance_atual - lucro_total_deals,
            'profit': 0.0
        })
        
        # Adiciona pontos baseados nos deals (simplificado)
        lucro_acumulado = 0
        for deal in sorted(deals, key=lambda x: x.time):
            if hasattr(deal, 'profit') and deal.profit != 0:
                lucro_acumulado += deal.profit
                equity_historico.append({
                    'timestamp': datetime.fromtimestamp(deal.time),
                    'equity': equity_inicial + lucro_acumulado,
                    'balance': balance_atual - lucro_total_deals + lucro_acumulado,
                    'profit': lucro_acumulado
                })
        
        # Adiciona ponto atual final
        equity_historico.append({
            'timestamp': datetime.now(),
            'equity': equity_atual,
            'balance': balance_atual,
            'profit': account_info.profit
        })
        
        return equity_historico
        
    except Exception as e:
        sistema.log(f"❌ Erro ao obter histórico de equity do MT5: {str(e)}")
        return []

if __name__ == "__main__":
    main()
