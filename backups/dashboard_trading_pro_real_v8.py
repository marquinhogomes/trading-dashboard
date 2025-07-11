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
from datetime import datetime, timedelta, time as datetime_time
import json
import os
import threading
import time as time_module
import io
import random
import traceback
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

# ===== CONFIGURAÇÕES GLOBAIS REFERENCIAIS (INÍCIO DO ARQUIVO) =====
# Essas configurações devem referenciar o código original
# Parâmetros centralizados: buscar sempre do SistemaIntegrado
# Fim das configurações globais referenciais

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
    def obter_status_threads(self):
        """Retorna o status (is_alive) das threads principais do sistema de trading do dashboard."""
        status = {}
        # Thread principal de análise/sistema
        status['thread_sistema'] = self.thread_sistema.is_alive() if hasattr(self, 'thread_sistema') and self.thread_sistema else False
        # Thread de sincronização (modo otimizado)
        status['thread_sincronizacao'] = self.thread_sincronizacao.is_alive() if hasattr(self, 'thread_sincronizacao') and self.thread_sincronizacao else False
        # Se desejar, adicione outras threads customizadas aqui
        # Exemplo: status['thread_custom'] = self.thread_custom.is_alive() if hasattr(self, 'thread_custom') and self.thread_custom else False
        return status
    
    def conectar_mt5(self):
        """Tenta conectar ao MetaTrader5 apenas na thread principal. Atualiza self.mt5_connected e exibe mensagens claras em caso de erro."""
        import threading
        try:
            if not threading.current_thread() is threading.main_thread():
                self.log("❌ Conexão com o MT5 só pode ser feita na thread principal. Reinicie o dashboard e tente novamente.")
                self.mt5_connected = False
                return False
            import MetaTrader5 as mt5
            if not mt5.initialize():
                self.log(f"❌ Falha ao conectar ao MetaTrader5: {mt5.last_error()}")
                self.mt5_connected = False
                return False
            self.log("✅ Conectado ao MetaTrader5 com sucesso!")
            self.mt5_connected = True
            return True
        except Exception as e:
            self.log(f"❌ Erro ao conectar ao MetaTrader5: {e}")
            self.mt5_connected = False
            return False
    @property
    def posicoes_abertas_exibicao(self):
        """Retorna as posições abertas do sistema integrado se disponível, senão as locais"""
        if self.modo_otimizado and self.sistema_integrado and hasattr(self.sistema_integrado, 'posicoes_abertas'):
            return self.sistema_integrado.posicoes_abertas
        return self.posicoes_abertas

    @property
    def trade_history_exibicao(self):
        """Retorna o histórico de trades do sistema integrado se disponível, senão o local"""
        if self.modo_otimizado and self.sistema_integrado and hasattr(self.sistema_integrado, 'trade_history'):
            return self.sistema_integrado.trade_history
        return self.trade_history

    @property
    def sinais_ativos_exibicao(self):
        """Retorna os sinais ativos do sistema integrado se disponível, senão os locais"""
        if self.modo_otimizado and self.sistema_integrado and hasattr(self.sistema_integrado, 'sinais_ativos_exibicao'):
            return self.sistema_integrado.sinais_ativos_exibicao
        return self.sinais_ativos

    @property
    def equity_historico_exibicao(self):
        """Retorna o histórico de equity do sistema integrado se disponível, senão o local"""
        if self.modo_otimizado and self.sistema_integrado and hasattr(self.sistema_integrado, 'equity_historico_exibicao'):
            return self.sistema_integrado.equity_historico_exibicao
        return self.equity_historico
    """Sistema de Trading Real com MT5 - Otimizado com Threading Avançado"""
    def __init__(self):
        # Inicializar dependente e independente no início, SEMPRE
        self.dependente = ['ABEV3', 'ALOS3', 'ASAI3','BBAS3', 'BBDC4', 'BBSE3', 'BPAC11', 'BRAP4', 'BRFS3', 'BRKM5', 'CPFE3', 'CPLE6', 'CSAN3','CSNA3', 'CYRE3', 'ELET3', 'ELET6', 'EMBR3', 'ENEV3', 'ENGI11', 'EQTL3', 'EZTC3', 'FLRY3', 'GOAU4', 'HYPE3', 'IGTI11', 'IRBR3', 'ITSA4', 'ITUB4', 'KLBN11', 'MRFG3', 'NATU3', 'PETR3', 'PETR4', 'PETZ3', 'PRIO3', 'RAIL3', 'RADL3', 'RECV3', 'RENT3', 'RDOR3', 'SANB11', 'SLCE3', 'SMTO3', 'SUZB3', 'TAEE11', 'TIMS3', 'TOTS3', 'UGPA3', 'VALE3', 'VBBR3', 'VIVT3', 'WEGE3', 'YDUQ3']
        self.independente = self.dependente.copy()
        self.mt5_connected = False
        self.running = False
        # Inicializar segmentos ANTES de qualquer lógica condicional
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
            'MRFG3': 'Alimentos', 'NATU3': 'Higiene/Beleza','PETR3': 'Petróleo',
            'PETR4': 'Petróleo', 'PETZ3': 'Varejo', 'PRIO3': 'Petróleo',
            'RAIL3': 'Logística', 'RADL3': 'Varejo', 'RECV3': 'Petróleo',
            'RENT3': 'Locação', 'RDOR3': 'Saúde', 'SANB11': 'Bancos',
            'SLCE3': 'Agro', 'SMTO3': 'Agro', 'SUZB3': 'Papel e Celulose',
            'TAEE11': 'Energia', 'TIMS3': 'Telecom', 'TOTS3': 'Tecnologia',
            'UGPA3': 'Distribuição','VALE3': 'Mineração','VBBR3': 'Transporte',
            'VIVT3': 'Telecom', 'WEGE3': 'Industrial','YDUQ3': 'Educação'
        }
        # Inicializar modo_otimizado como True para exibir logs do SistemaIntegrado
        self.modo_otimizado = True
        self.sistema_integrado = None
        self.sistema_integrado_status = 'nao_inicializado'

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

        # Inicializa DataFrames vazios
        self.tabela_linha_operacao = pd.DataFrame()
        self.tabela_linha_operacao01 = pd.DataFrame()
        self.thread_sistema = None

    @property
    def logs_exibicao(self):
        """Retorna os logs do sistema integrado se disponível, senão os locais"""
        if self.modo_otimizado and self.sistema_integrado and hasattr(self.sistema_integrado, 'logs'):
            return self.sistema_integrado.logs
        return self.logs

    @property
    def dados_sistema_exibicao(self):
        """Retorna os dados do sistema integrado se disponível, senão os locais"""
        if self.modo_otimizado and self.sistema_integrado and hasattr(self.sistema_integrado, 'dados_sistema'):
            return self.sistema_integrado.dados_sistema
        return self.dados_sistema
        # CORREÇÃO CRÍTICA: Inicializa DataFrames de análise para ambos os modos
        # Isso garante que as abas funcionem tanto no modo básico quanto no otimizado
        self.tabela_linha_operacao = pd.DataFrame()  # Primeira seleção
        self.tabela_linha_operacao01 = pd.DataFrame()  # Segunda seleção
        # Thread para execução do sistema
        self.thread_sistema = None
        
    def conectar_mt5(self, login: int = None, password: str = None, server: str = None) -> bool:
        """Conecta ao MT5. Se argumentos não forem fornecidos, tenta usar os últimos salvos."""
        try:
            # Se não recebeu argumentos, tenta usar os últimos salvos
            if login is None:
                login = getattr(self, 'last_login', None)
            if password is None:
                password = getattr(self, 'last_password', None)
            if server is None:
                server = getattr(self, 'last_server', None)

            if not mt5.initialize():
                self.log("❌ Falha ao inicializar MT5")
                return False

            # Só tenta login se todos os dados estiverem presentes
            if login and password and server:
                if not mt5.login(login, password=password, server=server):
                    self.log(f"❌ Falha no login MT5: {mt5.last_error()}")
                    return False
            elif login or password or server:
                self.log("❌ Dados incompletos para login no MT5. Informe login, senha e servidor.")
                return False

            account_info = mt5.account_info()
            if account_info:
                saldo_inicial_dia = self.calcular_saldo_inicial_do_dia()
                self.dados_sistema["saldo_inicial"] = saldo_inicial_dia
                self.dados_sistema["equity_atual"] = account_info.equity
                self.mt5_connected = True
                self.log(f"✅ MT5 conectado - Conta: {account_info.login}")
                self.log(f"💰 Saldo inicial do dia: R$ {saldo_inicial_dia:,.2f}")
                self.log(f"💰 Balance atual: R$ {account_info.balance:,.2f}")
                self.log(f"📊 Diferença do dia: R$ {account_info.balance - saldo_inicial_dia:+,.2f}")
                return True
            else:
                self.log("❌ Falha ao obter informações da conta")
                return False

        except Exception as e:
            self.log(f"❌ Erro ao conectar MT5: {str(e)}")
            return False
    
    def calcular_saldo_inicial_do_dia(self) -> float:
        """Calcula o saldo inicial correto do dia baseado no histórico de deals"""
        try:
            account_info = mt5.account_info()
            if not account_info:
                self.log("❌ Não foi possível obter informações da conta")
                return 0.0
            
            # Data de hoje às 00:00
            hoje = datetime.now().date()
            inicio_dia = datetime.combine(hoje, datetime_time.min)
            
            self.log(f"📅 Calculando saldo inicial para {hoje}")
            self.log(f"🔍 Buscando deals desde {inicio_dia.strftime('%H:%M:%S')}")
            
            # Busca deals do dia
            deals = mt5.history_deals_get(inicio_dia, datetime.now())
            
            if not deals or len(deals) == 0:
                # Se não há deals hoje, usa o balance atual como inicial
                self.log("📊 Sem deals hoje - usando balance atual como inicial")
                self.log(f"💰 Balance usado como inicial: R$ {account_info.balance:,.2f}")
                return account_info.balance
            
            # Calcula total de lucros/perdas dos deals de hoje
            lucro_total_dia = sum([deal.profit for deal in deals if hasattr(deal, 'profit') and deal.profit != 0])
            
            # Saldo inicial = Balance atual - Lucros do dia
            saldo_inicial = account_info.balance - lucro_total_dia
            
            # LOGS DETALHADOS
            self.log(f"📊 CÁLCULO SALDO INICIAL:")
            self.log(f"   • Deals hoje: {len(deals)}")
            self.log(f"   • Lucro total dos deals: R$ {lucro_total_dia:+,.2f}")
            self.log(f"   • Balance atual: R$ {account_info.balance:,.2f}")
            self.log(f"   • Saldo inicial calculado: R$ {saldo_inicial:,.2f}")
            
            # Validação básica
            if saldo_inicial <= 0:
                self.log("⚠️ Saldo inicial calculado é inválido, usando balance atual")
                return account_info.balance
                
            return saldo_inicial
            
        except Exception as e:
            self.log(f"❌ Erro ao calcular saldo inicial: {str(e)}")
            # Fallback: usa balance atual
            try:
                account_info = mt5.account_info()
                fallback_balance = account_info.balance if account_info else 0.0
                self.log(f"🔄 Fallback: usando balance atual R$ {fallback_balance:,.2f}")
                return fallback_balance
            except:
                return 0.0
    
    def log(self, mensagem: str):
        """Adiciona log com timestamp - Otimizado sem duplicação"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {mensagem}"
        self.logs.append(log_entry)
        
        # Sincroniza com sistema integrado se disponível
        if self.modo_otimizado and self.sistema_integrado:
            # O sistema integrado já faz print(), então não duplicamos aqui
            self.sistema_integrado.log(f"[Dashboard] {mensagem}")
        else:
            # Só faz print se não há sistema integrado (evita duplicação)
            print(log_entry)
        
        if len(self.logs) > 1000:  # Limita logs
            self.logs = self.logs[-500:]
    
    def processar_envio_ordens_automatico(self, tabela_linha_operacao01, config):
        """
        Função mantida apenas para compatibilidade. Toda a lógica de envio de ordens foi centralizada no SistemaIntegrado.
        """
        self.log("⚠️ Função processar_envio_ordens_automatico não é mais utilizada. O envio de ordens é feito exclusivamente pelo SistemaIntegrado.")
        self.log("⚠️ Nenhuma ordem será enviada por esta função. Verifique se o dashboard está atualizado para usar apenas SistemaIntegrado.")
        # [REMOVIDO] Funções legadas de processamento de ordens diretamente no dashboard.
        # Toda a lógica de análise/envio de ordens está centralizada em SistemaIntegrado.
        return False

        # ===== 1.2 CORREÇÃO CRÍTICA: MAGIC ID DA TABELA_LINHA_OPERACAO01 =====
        magic_id = None
        
        try:
            # Busca na tabela_linha_operacao01 (segunda seleção) se disponível
            if hasattr(self, 'tabela_linha_operacao01') and not self.tabela_linha_operacao01.empty:
                mascara_filtro = (
                    (self.tabela_linha_operacao01['Dependente'] == depende_atual) &
                    (self.tabela_linha_operacao01['Independente'] == independe_atual)
                )
                
                registro_correspondente = self.tabela_linha_operacao01[mascara_filtro]
                
                if not registro_correspondente.empty:
                    magic_id = registro_correspondente.iloc[0]['ID']
                    self.log(f"✅ Magic ID correto extraído da tabela_linha_operacao01: {magic_id}")
                else:
                    self.log(f"⚠️ Par {depende_atual}x{independe_atual} não encontrado na tabela_linha_operacao01")
            
            # Fallback: usa ID da linha_selecionada se não encontrou na tabela01
            if magic_id is None:
                magic_id = linha_selecionada.get('ID')
                self.log(f"⚠️ Usando Magic ID da linha_selecionada como fallback: {magic_id}")
            
            # Verificação final
            if magic_id is None:
                self.log(f"❌ ERRO CRÍTICO: Magic ID não encontrado para {depende_atual}x{independe_atual}")
                return False
                
        except Exception as e:
            self.log(f"❌ Erro ao extrair Magic ID: {e}")
            magic_id = linha_selecionada.get('ID')
            if magic_id is None:
                return False
        
        self.log(f"🔢 Magic ID FINAL obtido: {magic_id}")
        
        # 1.3 Verificar se já existe posição aberta para o dependente
        if self._verificar_operacao_aberta([depende_atual]):
            self.log(f"❌ OPERAÇÃO EXISTENTE: Já existe uma posição aberta para o DEPENDENTE {depende_atual}")
            return False
        
        # 1.4 Verificar ordens pendentes existentes para o dependente
        ordens_pendentes_dep = mt5.orders_get(symbol=depende_atual)
        ordem_existente_dep = any(o.symbol == depende_atual for o in ordens_pendentes_dep) if ordens_pendentes_dep else False
        
        if ordem_existente_dep:
            self.log(f"❌ ORDEM PENDENTE EXISTENTE: Já existe ordem pendente para {depende_atual}")
            return False
        
        # 1.5 Verificar limite de operações por prefixo/script
        prefixo_script = self.sistema_integrado.prefixo  # Centralizado
        qtd_op_script = self._contar_operacoes_por_prefixo(prefixo_script)
        limite_operacoes = self.sistema_integrado.limite_operacoes  # Centralizado
        if qtd_op_script >= limite_operacoes:
            self.log(f"❌ LIMITE ATINGIDO: Máximo de operações abertas ({limite_operacoes}) atingido para este script")
            self.log(f"   Operações atuais: {qtd_op_script}")
            return False
        
        self.log(f"✅ VALIDAÇÕES PRÉVIAS APROVADAS - Prosseguindo com análise técnica...")
        
        # ===== ETAPA 2: ANÁLISE TÉCNICA E OBTENÇÃO DE PREÇOS =====
        
        # 2.1 Obter preços atuais do MT5
        self.log(f"🔍 Obtendo cotações do MT5...")
        symbol_info_tick_dep = mt5.symbol_info_tick(depende_atual)
        symbol_info_tick_ind = mt5.symbol_info_tick(independe_atual)
        
        if not symbol_info_tick_dep:
            self.log(f"❌ Cotação não encontrada para {depende_atual}")
            return False
        if not symbol_info_tick_ind:
            self.log(f"❌ Cotação não encontrada para {independe_atual}")
            return False
        
        self.log(f"✅ Cotações obtidas: {depende_atual}={symbol_info_tick_dep.bid:.2f}, {independe_atual}={symbol_info_tick_ind.ask:.2f}")
        
        # ===== CORREÇÃO CRÍTICA: EXTRAÇÃO CORRETA DAS VARIÁVEIS TÉCNICAS =====
        self.log(f"🔧 DEBUG: Chaves disponíveis na linha: {list(linha_selecionada.keys())}")
        
        # ✅ CORREÇÃO CRÍTICA: Normalização segura de todas as variáveis de entrada
        try:
            zscore_hoje = float(zscore_hoje) if zscore_hoje is not None else 0.0
            beta_hoje = float(beta_hoje) if beta_hoje is not None else 1.0
            r2_hoje = float(r2_hoje) if r2_hoje is not None else 0.5
        except (ValueError, TypeError):
            self.log(f"❌ ERRO: Parâmetros de entrada inválidos")
            return False
        
        # 2.2 Extrair variáveis técnicas da tabela - CORRIGIDO
        preco_atuall = linha_selecionada.get('preco_atual', symbol_info_tick_dep.bid)
        
        # ✅ CORREÇÃO: Busca por diferentes nomes possíveis da variável residual
        pred_resid = None
        resid_atual = None
        
        # Tenta várias possibilidades para pred_resid
        for key_name in ['pred_resid', 'pred_residual', 'predicted_residual', 'residuo_previsto']:
            if key_name in linha_selecionada:
                pred_resid = linha_selecionada[key_name]
                self.log(f"🔧 DEBUG: pred_resid encontrado como '{key_name}': {pred_resid}")
                break
        
        # Tenta várias possibilidades para resid_atual
        # 1º: Tenta extrair diretamente 'resid_atual' se existir
        if 'resid_atual' in linha_selecionada and linha_selecionada['resid_atual'] is not None:
            resid_atual = linha_selecionada['resid_atual']
            self.log(f"🔧 DEBUG: resid_atual extraído diretamente: {resid_atual}")
        # 2º: Se não, tenta calcular a partir de 'residuo' se for uma série/lista
        elif 'residuo' in linha_selecionada and hasattr(linha_selecionada['residuo'], 'iloc'):
            try:
                residuo_serie = linha_selecionada['residuo']
                resid_atual = float(residuo_serie.iloc[-1]) if residuo_serie.iloc[-1] is not None else 0.0
                self.log(f"🔧 DEBUG: resid_atual calculado de residuo.iloc[-1]: {resid_atual}")
            except Exception as e:
                self.log(f"⚠️ Erro ao calcular resid_atual de residuo: {e}")
        # 3º: Tenta outras chaves alternativas
        else:
            for key_name in ['residuo_std', 'residual_atual', 'current_residual', 'residuo_atual']:
                if key_name in linha_selecionada:
                    resid_atual = linha_selecionada[key_name]
                    self.log(f"🔧 DEBUG: resid_atual encontrado como '{key_name}': {resid_atual}")
                    break
        
        # Se não encontrar, usa valores padrão mas loga o problema
        if pred_resid is None:
            pred_resid = 0.0
            self.log(f"⚠️ AVISO: pred_resid não encontrado, usando valor padrão: {pred_resid}")
        
        if resid_atual is None:
            resid_atual = 0.0
            self.log(f"⚠️ AVISO: resid_atual não encontrado, usando valor padrão: {resid_atual}")
        
        # ✅ NOVA ABORDAGEM: Se ambos são 0, tenta calcular baseado no Z-Score
        if pred_resid == 0.0 and resid_atual == 0.0 and zscore_hoje is not None:
            # Calcula resíduo baseado no Z-Score (método alternativo)
            if abs(zscore_hoje) > 0.1:
                # Para venda: pred_resid deve ser menor que resid_atual
                # Simula valores baseados no Z-Score
                resid_atual = abs(zscore_hoje) * 0.5  # Valor atual do resíduo
                pred_resid = resid_atual * 0.8       # Previsão menor (sinal de venda)
                
                self.log(f"🔧 CALCULADO: Valores estimados baseados em Z-Score={zscore_hoje:.3f}")
                self.log(f"   • resid_atual estimado: {resid_atual:.4f}")
                self.log(f"   • pred_resid estimado: {pred_resid:.4f}")
        
        # ✅ CORREÇÃO CRÍTICA: Normalização completa de TODAS as variáveis antes de qualquer comparação
        try:
            preco_atuall = float(preco_atuall) if preco_atuall is not None else float(symbol_info_tick_dep.bid)
            pred_resid = float(pred_resid) if pred_resid is not None else 0.0
            resid_atual = float(resid_atual) if resid_atual is not None else 0.0
        except (ValueError, TypeError) as e:
            self.log(f"❌ ERRO na normalização de variáveis: {str(e)}")
            return False
        
        self.log(f"📊 Variáveis técnicas extraídas e normalizadas:")
        self.log(f"   • preco_atual: {preco_atuall:.4f}")
        self.log(f"   • pred_resid: {pred_resid:.4f}")
        self.log(f"   • resid_atual: {resid_atual:.4f}")
        
        # 2.3 Verificar se já existe ordem de venda pendente para o ativo dependente
        existe_ordem_venda = self._verificar_operacao_aberta_tipo(depende_atual, 'sell')
        
        if existe_ordem_venda:
            self.log(f"❌ ORDEM VENDA EXISTENTE: Já existe ordem de venda para {depende_atual}")
            return False
        
        self.log(f"✅ Valores normalizados: pred_resid={pred_resid:.4f}, resid_atual={resid_atual:.4f}")
        
        # 2.5 Calcular preços de entrada
        self.log(f"💰 Calculando preços de entrada...")
        preco_venda_dep = self._calcular_preco_venda(linha_selecionada, symbol_info_tick_dep)
        preco_compra_ind = self._calcular_preco_compra_indep(linha_selecionada, symbol_info_tick_ind)
        
        if preco_venda_dep is None or preco_compra_ind is None:
            self.log(f"❌ Erro ao calcular preços: venda={preco_venda_dep}, compra={preco_compra_ind}")
            return False
        
        # ✅ CORREÇÃO CRÍTICA: Normalização segura dos preços calculados
        try:
            price_dep_venda = float(preco_venda_dep)
            price_ind_compra = float(preco_compra_ind)
        except (ValueError, TypeError):
            self.log(f"❌ ERRO: Preços calculados são inválidos")
            return False
        
        self.log(f"✅ Preços calculados: VENDA {depende_atual}=R${price_dep_venda:.2f}, COMPRA {independe_atual}=R${price_ind_compra:.2f}")
        
        # ===== CORREÇÃO CRÍTICA: CÁLCULO CORRETO DO MIN_DIST_ACAO_DEP =====
        
        # 2.6 Calcular stops para poder determinar min_dist_acao_dep
        self.log(f"🎯 Calculando stops para determinar min_dist_acao_dep...")
        
        # Stops do dependente da tabela
        spread_venda_gain_original = linha_selecionada.get('spread_venda_gain')
        if spread_venda_gain_original:
            stop_gain_venda = float(spread_venda_gain_original)
            self.log(f"✅ Stop Gain venda DEP da tabela: R$ {stop_gain_venda:.2f}")
        else:
            stop_gain_venda = self._calcular_stop_gain_venda(linha_selecionada, price_dep_venda)
            self.log(f"⚠️ Stop Gain venda DEP calculado: R$ {stop_gain_venda:.2f}")
        
        # ✅ CORREÇÃO BASEADA NO CÓDIGO ORIGINAL: Para VENDA DEP + COMPRA IND
        # min_dist_acao_dep = stop_gain_venda * 1.01 (baseado no calculo_entradas_v55.py)
        min_dist_acao_dep_numeric = stop_gain_venda * 1.01
        min_dist_acao_dep_display = f"{min_dist_acao_dep_numeric:.2f}"
        
        self.log(f"📏 Min distância ação dep calculada: R$ {min_dist_acao_dep_numeric:.2f} (stop_gain_venda * 1.01)")
        
        # ===== ETAPA 3: VALIDAÇÕES TÉCNICAS CRÍTICAS - CORRIGIDAS =====
        
        # ✅ CORREÇÃO CRÍTICA: Validação mais inteligente dos resíduos COM PROTEÇÃO TOTAL CONTRA None
        
        # 3.1 Validação: pred_resid < resid_atual (para venda) - COM TOLERÂNCIA E PROTEÇÃO
        try:
            if pred_resid is None or resid_atual is None:
                self.log(f"❌ Resíduos inválidos: pred_resid={pred_resid}, resid_atual={resid_atual}")
                return False
            
            condicao_residuo = pred_resid < resid_atual
            
            # Se a condição básica falha, verifica se é por valores muito próximos
            if not condicao_residuo and abs(pred_resid - resid_atual) < 0.001:
                # Valores muito próximos - aceita com base no Z-Score
                if zscore_hoje is not None and zscore_hoje >= 2.0:
                    condicao_residuo = True
                    self.log(f"✅ TOLERÂNCIA: Resíduos próximos ({abs(pred_resid - resid_atual):.6f}), mas Z-Score válido: {zscore_hoje:.3f}")
            
            self.log(f"🔍 Condição 1 - pred_resid < resid_atual: {pred_resid:.4f} < {resid_atual:.4f} = {condicao_residuo}")
            
            if not condicao_residuo:
                # ✅ NOVA VERIFICAÇÃO: Se ambos são 0, usa apenas Z-Score como critério
                if pred_resid == 0.0 and resid_atual == 0.0:
                    if zscore_hoje is not None and zscore_hoje >= 2.0:
                        self.log(f"✅ EXCEÇÃO: Resíduos zerados, mas Z-Score válido para venda: {zscore_hoje:.3f}")
                        condicao_residuo = True
                    else:
                        self.log(f"❌ CONDIÇÃO TÉCNICA FALHOU: Resíduos zerados e Z-Score insuficiente: {zscore_hoje}")
                        return False
                else:
                    self.log(f"❌ CONDIÇÃO TÉCNICA FALHOU: pred_resid ({pred_resid:.4f}) não é menor que resid_atual ({resid_atual:.4f})")
                    return False
            
        except Exception as e:
            self.log(f"❌ ERRO na validação de resíduos: {str(e)}")
            return False
        
        # 3.2 Validação: price_dep_venda > min_dist_acao_dep (maior para venda) - COM PROTEÇÃO
        try:
            condicao_distancia = price_dep_venda > min_dist_acao_dep_numeric
            
            self.log(f"🔍 Condição 2 - price_dep_venda > min_dist_acao_dep: {price_dep_venda:.2f} > {min_dist_acao_dep_display} = {condicao_distancia}")
            
            if not condicao_distancia:
                self.log(f"❌ CONDIÇÃO TÉCNICA FALHOU: price_dep_venda ({price_dep_venda:.2f}) não é maior que min_dist_acao_dep ({min_dist_acao_dep_display})")
                return False
                
        except Exception as e:
            self.log(f"❌ ERRO na validação de distância: {str(e)}")
            return False
        
        # 3.3 Validação: price_dep_venda > preco_atuall (maior para venda) - COM PROTEÇÃO
        try:
            condicao_preco_atual = price_dep_venda > preco_atuall
            self.log(f"🔍 Condição 3 - price_dep_venda > preco_atual: {price_dep_venda:.2f} > {preco_atuall:.2f} = {condicao_preco_atual}")
            
            if not condicao_preco_atual:
                self.log(f"❌ CONDIÇÃO TÉCNICA FALHOU: price_dep_venda ({price_dep_venda:.2f}) não é maior que preco_atual ({preco_atuall:.2f})")
                return False
                
        except Exception as e:
            self.log(f"❌ ERRO na validação de preço atual: {str(e)}")
            return False
        
        # 3.4 TODAS AS CONDIÇÕES TÉCNICAS APROVADAS
        self.log(f"✅ TODAS AS VALIDAÇÕES TÉCNICAS APROVADAS!")
        self.log(f"   ✓ Resíduo: {pred_resid:.4f} < {resid_atual:.4f}")
        self.log(f"   ✓ Distância: {price_dep_venda:.2f} > {min_dist_acao_dep_display}")
        self.log(f"   ✓ Preço atual: {price_dep_venda:.2f} > {preco_atuall:.2f}")
                
        # ===== ETAPA 4: INTEGRAÇÃO TOTAL COM VARIÁVEIS DA TABELA =====
        
        # 4.1 EXTRAÇÃO COMPLETA DE TODAS AS VARIÁVEIS DA LINHA SELECIONADA
        self.log(f"📊 ETAPA 4: Extraindo TODAS as variáveis da tabela_linha_operacao01...")
        
        # Variáveis básicas de identificação (já extraídas anteriormente)
        timeframe_atual = linha_selecionada.get('Timeframe', '1 dia')
        periodo_atual = linha_selecionada.get('Período', 120)
        
        # ===== VARIÁVEIS ESTATÍSTICAS COMPLETAS =====
        alpha_valor = linha_selecionada.get('alpha', 0.0)
        half_life_valor = linha_selecionada.get('half_life', 50)
        adf_p_value_valor = linha_selecionada.get('adf_p_value', 0.05)
        coint_p_value_valor = linha_selecionada.get('coint_p_value', 0.05)
        residuo_valor = linha_selecionada.get('residuo', 0.0)
        residuo_std_valor = linha_selecionada.get('residuo_std', 0.0)
        nd_dep_valor = linha_selecionada.get('nd_dep', 0)
        nd_ind_valor = linha_selecionada.get('nd_ind', 0)
        
        # ===== VARIÁVEIS DE CORRELAÇÃO E QUALIDADE =====
        correlacao_valor = linha_selecionada.get('correlacao', 0.85)
        correlacao_ibov_valor = linha_selecionada.get('correlacao_ibov', 0.75)
        corr_ind_ibov_valor = linha_selecionada.get('corr_ind_ibov', 0.70)
        correlacao_10dias_dep_ind = linha_selecionada.get('correlacao_10dias_dep_ind', 0.80)
        desvio_padrao_valor = linha_selecionada.get('desvio_padrao', 0.5)
        desvio_dep_10_valor = linha_selecionada.get('desvio_dep_10', 0.3)
        coef_variacao_valor = linha_selecionada.get('coef_variacao', 0.25)
        
        # ===== VARIÁVEIS DE PREVISÃO E FORECAST =====
        zscore_forecast_compra_valor = linha_selecionada.get('zscore_forecast_compra', zscore_hoje)
        zscore_forecast_venda_valor = linha_selecionada.get('zscore_forecast_venda', zscore_hoje)
        
        # ✅ CORREÇÃO: Verifica valores None antes de usar em f-strings
        alpha_valor = float(alpha_valor) if alpha_valor is not None else 0.0
        zscore_forecast_compra_valor = float(zscore_forecast_compra_valor) if zscore_forecast_compra_valor is not None else zscore_hoje
        zscore_forecast_venda_valor = float(zscore_forecast_venda_valor) if zscore_forecast_venda_valor is not None else zscore_hoje
        correlacao_valor = float(correlacao_valor) if correlacao_valor is not None else 0.85
        correlacao_ibov_valor = float(correlacao_ibov_valor) if correlacao_ibov_valor is not None else 0.75
        
        # ===== VARIÁVEIS DE PREÇOS DETALHADAS =====
        preco_ontem = linha_selecionada.get('preco_ontem', preco_atuall)
        preco_abertura = linha_selecionada.get('preco_abertura', preco_atuall)
        preco_max_atual = linha_selecionada.get('preco_max_atual', preco_atuall * 1.02)
        preco_min_atual = linha_selecionada.get('preco_min_atual', preco_atuall * 0.98)
        
        # Previsões de preços
        previsao_fechamento = linha_selecionada.get('previsao_fechamento', preco_atuall)
        previsao_maximo = linha_selecionada.get('previsao_maximo', preco_atuall * 1.05)
        previsao_minimo = linha_selecionada.get('previsao_minimo', preco_atuall * 0.95)
        
        # ===== SPREADS COMPLETOS DO DEPENDENTE =====
        spread_compra_original = linha_selecionada.get('spread_compra', price_dep_venda * 0.998)
        spread_compra_gain_original = linha_selecionada.get('spread_compra_gain', price_dep_venda * 1.015)
        spread_compra_loss_original = linha_selecionada.get('spread_compra_loss', price_dep_venda * 0.99)
        spread_venda_original = linha_selecionada.get('spread_venda', price_dep_venda)
        spread_venda_loss_original = linha_selecionada.get('spread_venda_loss', price_dep_venda * 1.01)
        
        # ===== VARIÁVEIS DE VOLATILIDADE ARIMA =====
        std_arima_close = linha_selecionada.get('std_arima_close', 0.02)
        std_arima_high = linha_selecionada.get('std_arima_high', 0.025)
        std_arima_low = linha_selecionada.get('std_arima_low', 0.025)
        sigma_close = linha_selecionada.get('sigma_close', 0.03)
        sigma_high = linha_selecionada.get('sigma_high', 0.035)
        sigma_low = linha_selecionada.get('sigma_low', 0.035)
        
        # ✅ CORREÇÃO: Verifica valores None para volatilidade
        sigma_close = float(sigma_close) if sigma_close is not None and sigma_close > 0 else 0.03
        
        # ===== VARIÁVEIS DO INDEPENDENTE COMPLETAS =====
        indep_preco_ontem = linha_selecionada.get('indep_preco_ontem', price_ind_compra)
        indep_preco_atual = linha_selecionada.get('indep_preco_atual', price_ind_compra)
        indep_preco_abertura = linha_selecionada.get('indep_preco_abertura', price_ind_compra)
        indep_preco_max_atual = linha_selecionada.get('indep_preco_max_atual', price_ind_compra * 1.02)
        indep_preco_min_atual = linha_selecionada.get('indep_preco_min_atual', price_ind_compra * 0.98)
        
        # Previsões do independente
        previsao_fechamento_ind = linha_selecionada.get('previsao_fechamento_ind', price_ind_compra)
        previsao_maximo_ind = linha_selecionada.get('previsao_maximo_ind', price_ind_compra * 1.05)
        previsao_minimo_ind = linha_selecionada.get('previsao_minimo_ind', price_ind_compra * 0.95)
        
        # Spreads do independente
        indep_spread_compra_original = linha_selecionada.get('indep_spread_compra', price_ind_compra)
        indep_spread_compra_gain_original = linha_selecionada.get('indep_spread_compra_gain', price_ind_compra * 1.015)
        indep_spread_compra_loss_original = linha_selecionada.get('indep_spread_compra_loss', price_ind_compra * 0.99)
        indep_spread_venda_original = linha_selecionada.get('indep_spread_venda', price_ind_compra * 1.002)
        indep_spread_venda_gain_original = linha_selecionada.get('indep_spread_venda_gain', price_ind_compra * 0.985)
        indep_spread_venda_loss_original = linha_selecionada.get('indep_spread_venda_loss', price_ind_compra * 1.01)
        
        # Volatilidade do independente
        std_arima_close_ind = linha_selecionada.get('std_arima_close_ind', 0.02)
        std_arima_high_ind = linha_selecionada.get('std_arima_high_ind', 0.025)
        std_arima_low_ind = linha_selecionada.get('std_arima_low_ind', 0.025)
        sigma_close_ind = linha_selecionada.get('sigma_close_ind', 0.03)
        sigma_high_ind = linha_selecionada.get('sigma_high_ind', 0.035)
        sigma_low_ind = linha_selecionada.get('sigma_low_ind', 0.035)
        
        # ===== VARIÁVEIS DE CONTROLE E STATUS =====
        passou_filtros = linha_selecionada.get('Passou_Filtros', True)
        perc_diferenca = linha_selecionada.get('Perc_Diferenca', 0.5)
        preco_entrada_final = linha_selecionada.get('Preco_Entrada_Final', price_dep_venda)
        
        # ===== LOG DE VARIÁVEIS EXTRAÍDAS =====
        self.log(f"📊 VARIÁVEIS EXTRAÍDAS COMPLETAS:")
        self.log(f"   • Identificação: {depende_atual}x{independe_atual} ({timeframe_atual}, {periodo_atual})")
        self.log(f"   • Estatísticas: α={alpha_valor:.4f}, β={beta_hoje:.3f}, r²={r2_hoje:.3f}")
        self.log(f"   • Correlações: dep-ind={correlacao_valor:.3f}, dep-ibov={correlacao_ibov_valor:.3f}")
        self.log(f"   • Previsões: zscore_comp={zscore_forecast_compra_valor:.3f}, zscore_venda={zscore_forecast_venda_valor:.3f}")
        self.log(f"   • Preços DEP: atual={preco_atuall:.2f}, spread_venda={spread_venda_original:.2f}")
        self.log(f"   • Preços IND: atual={indep_preco_atual:.2f}, spread_compra={indep_spread_compra_original:.2f}")
        self.log(f"   • Volatilidade: σ_close={sigma_close:.4f}, σ_ind={sigma_close_ind:.4f}")
        
        # 4.2 RECÁLCULO DE PREÇOS USANDO VARIÁVEIS COMPLETAS DA TABELA
        self.log(f"🔧 ETAPA 4: Recalculando preços com dados COMPLETOS da tabela...")
        
        # Usa spreads da tabela se disponíveis (prioridade máxima)
        if spread_venda_original and float(spread_venda_original) != price_dep_venda:
            price_dep_venda = float(spread_venda_original)
            self.log(f"✅ Preço venda DEP da tabela: R$ {price_dep_venda:.2f}")
        else:
            self.log(f"⚠️ Preço venda DEP calculado: R$ {price_dep_venda:.2f}")
        
        if indep_spread_compra_original and float(indep_spread_compra_original) != price_ind_compra:
            price_ind_compra = float(indep_spread_compra_original)
            self.log(f"✅ Preço compra IND da tabela: R$ {price_ind_compra:.2f}")
        else:
            self.log(f"⚠️ Preço compra IND calculado: R$ {price_ind_compra:.2f}")
        
        # 4.3 RECÁLCULO DE STOPS USANDO VARIÁVEIS COMPLETAS DA TABELA
        self.log(f"🎯 ETAPA 4: Recalculando stops com dados COMPLETOS da tabela...")
        
        # Stops do dependente da tabela (usa valores já calculados)
        if spread_venda_loss_original:
            stop_loss_venda = float(spread_venda_loss_original)
            self.log(f"✅ Stop Loss venda DEP da tabela: R$ {stop_loss_venda:.2f}")
        else:
            stop_loss_venda = self._calcular_stop_loss_venda(linha_selecionada, price_dep_venda)
            self.log(f"⚠️ Stop Loss venda DEP calculado: R$ {stop_loss_venda:.2f}")
        
        # Stops do independente da tabela
        if indep_spread_compra_gain_original:
            stop_gain_compra_ind = float(indep_spread_compra_gain_original)
            self.log(f"✅ Stop Gain compra IND da tabela: R$ {stop_gain_compra_ind:.2f}")
        else:
            stop_gain_compra_ind = self._calcular_stop_gain_compra_ind(linha_selecionada, price_ind_compra)
            self.log(f"⚠️ Stop Gain compra IND calculado: R$ {stop_gain_compra_ind:.2f}")
        
        if indep_spread_compra_loss_original:
            stop_loss_compra_ind = float(indep_spread_compra_loss_original)
            self.log(f"✅ Stop Loss compra IND da tabela: R$ {stop_loss_compra_ind:.2f}")
        else:
            stop_loss_compra_ind = self._calcular_stop_loss_compra_ind(linha_selecionada, price_ind_compra)
            self.log(f"⚠️ Stop Loss compra IND calculado: R$ {stop_loss_compra_ind:.2f}")
        
        # 4.4 RECÁLCULO DE VOLUMES USANDO VOLATILIDADE DA TABELA
        self.log(f"📊 ETAPA 4: Recalculando volumes com volatilidade da tabela...")
        
        # Calcula volume inicial
        qtd_dep = self._calcular_volume_operacao(price_dep_venda, valor_operacao)
        
        # Ajusta volume baseado na volatilidade real
        fator_volatilidade = 1.0
        if sigma_close > 0:
            # Reduz volume para ativos mais voláteis
            fator_volatilidade = max(0.5, min(1.5, 0.03 / sigma_close))
            self.log(f"🔧 Fator volatilidade aplicado: {fator_volatilidade:.3f} (σ={sigma_close:.4f})")
        
        # Volume ajustado do dependente
        qtd_dep = round(qtd_dep * fator_volatilidade, -2)
        qtd_ind = round(qtd_dep * abs(beta_hoje), -2)
        
        if qtd_dep <= 0 or qtd_ind <= 0:
            self.log(f"❌ Volume inválido: DEP={qtd_dep}, IND={qtd_ind}")
            return False
        
        self.log(f"📊 Volumes FINAIS ajustados por volatilidade:")
        self.log(f"   • DEP: {qtd_dep} (fator: {fator_volatilidade:.3f})")
        self.log(f"   • IND: {qtd_ind} (β={beta_hoje:.3f})")
        
        # 4.5 VALIDAÇÃO FINAL COM TODAS AS VARIÁVEIS
        self.log(f"✔️ ETAPA 4: Validação final com TODAS as variáveis da tabela...")
        
        # Validação adicional usando dados de previsão
        validacao_forecast = True
        if zscore_forecast_venda_valor and abs(zscore_forecast_venda_valor) < 1.5:
            validacao_forecast = False
            self.log(f"❌ Validação forecast falhou: zscore_forecast_venda={zscore_forecast_venda_valor:.3f}")
        
        # Validação de qualidade usando correlações
        validacao_qualidade = True
        if correlacao_valor < 0.5:
            validacao_qualidade = False
            self.log(f"❌ Validação qualidade falhou: correlação={correlacao_valor:.3f}")
        
        # Validação de cointegração
        validacao_cointegracao = True
        if coint_p_value_valor > 0.05:
            validacao_cointegracao = False
            self.log(f"❌ Validação cointegração falhou: p_value={coint_p_value_valor:.4f}")
        
        # Resultado da validação final
        validacao_aprovada = validacao_forecast and validacao_qualidade and validacao_cointegracao
        
        if not validacao_aprovada:
            self.log(f"❌ VALIDAÇÃO FINAL FALHOU - Operação bloqueada")
            self.log(f"   • Forecast: {validacao_forecast}")
            self.log(f"   • Qualidade: {validacao_qualidade}")
            self.log(f"   • Cointegração: {validacao_cointegracao}")
            return False
        
        self.log(f"✅ VALIDAÇÃO FINAL APROVADA - Todas as condições atendidas")
        
        # 4.6 VALIDAÇÕES FINAIS
        self.log(f"✔️ Validando condições...")
        if not self._validar_condicoes_entrada_venda(linha_selecionada, price_dep_venda):
            self.log(f"❌ Condições de entrada não atendidas")
            return False
        
        self.log(f"🎯 VALORES FINAIS INTEGRADOS:")
        self.log(f"   • Preço venda DEP: R$ {price_dep_venda:.2f}")
        self.log(f"   • Preço compra IND: R$ {price_ind_compra:.2f}")
        self.log(f"   • Stop Gain DEP: R$ {stop_gain_venda:.2f}")
        self.log(f"   • Stop Loss DEP: R$ {stop_loss_venda:.2f}")
        self.log(f"   • Volume DEP: {qtd_dep}")
        self.log(f"   • Volume IND: {qtd_ind}")
        
        # ===== ETAPA 5: LÓGICA DE ENVIO SEQUENCIAL E ROLLBACK =====
        self.log(f"📤 ENVIANDO ORDENS - Magic ID: {magic_id}")
        
        # 5.1 PREPARAÇÃO DAS ORDENS (baseado no código original)
        self.log(f"🔧 Preparando ordens para envio sequencial...")

        # Ordem DEPENDENTE (VENDA) - Primeira a ser enviada
        ordem_venda_dep = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": depende_atual,
            "volume": qtd_dep,
            "type": mt5.ORDER_TYPE_SELL_LIMIT,
            "price": price_dep_venda,
            "tp": stop_gain_venda,
            "sl": stop_loss_venda,
            "magic": magic_id,
            "comment": f"OptDep_Z{zscore_hoje:.1f}_R{r2_hoje:.2f}",
            "type_time": mt5.ORDER_TIME_DAY,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        # Ordem INDEPENDENTE (COMPRA) - Segunda a ser enviada
        ordem_compra_ind = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": independe_atual,
            "volume": qtd_ind,
            "type": mt5.ORDER_TYPE_BUY_LIMIT,
            "price": price_ind_compra,
            "tp": stop_gain_compra_ind,
            "sl": stop_loss_compra_ind,
            "magic": magic_id,
            "comment": f"OptInd_B{beta_hoje:.2f}_C{correlacao_valor:.2f}",
            "type_time": mt5.ORDER_TIME_DAY,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        # 5.2 ENVIO SEQUENCIAL: DEPENDENTE PRIMEIRO
        self.log(f"📊 PASSO 1/2: Enviando ordem DEPENDENTE (VENDA {depende_atual})")

        result_venda_dep = mt5.order_send(ordem_venda_dep)

        if result_venda_dep is None:
            self.log(f"❌ ERRO CRÍTICO: result_venda_dep retornou None (sem resposta do MT5)")
            self.log(f"❌ Erro MT5: {mt5.last_error()}")
            return False

        self.log(f"📋 DEPENDENTE - Retcode: {result_venda_dep.retcode}, Comentário: {result_venda_dep.comment}")

        # 5.3 VALIDAÇÃO DO ENVIO DO DEPENDENTE
        if result_venda_dep.retcode == mt5.TRADE_RETCODE_DONE:
            self.log(f"✅ DEPENDENTE enviado com sucesso - Ticket: {result_venda_dep.order}")
            ticket_dep = result_venda_dep.order  # Salva ticket para possível rollback

            # 5.4 ENVIO SEQUENCIAL: INDEPENDENTE APENAS SE DEPENDENTE FOI APROVADO
            self.log(f"📊 PASSO 2/2: Enviando ordem INDEPENDENTE (COMPRA {independe_atual})")

            result_compra_ind = mt5.order_send(ordem_compra_ind)

            if result_compra_ind is None:
                self.log(f"❌ ERRO CRÍTICO: result_compra_ind retornou None")
                self.log(f"❌ Erro MT5: {mt5.last_error()}")

                # 5.5 ROLLBACK: CANCELA DEPENDENTE SE INDEPENDENTE FALHOU
                self.log(f"🔄 EXECUTANDO ROLLBACK: Cancelando ordem DEPENDENTE (ticket {ticket_dep})")
                if self._cancelar_ordem_rollback(ticket_dep):
                    self.log(f"✅ ROLLBACK bem-sucedido: Ordem DEPENDENTE cancelada")
                else:
                    self.log(f"❌ ROLLBACK FALHOU: Ordem DEPENDENTE não foi cancelada")

                return False

            self.log(f"📋 INDEPENDENTE - Retcode: {result_compra_ind.retcode}, Comentário: {result_compra_ind.comment}")

            # 5.6 VALIDAÇÃO DO ENVIO DO INDEPENDENTE
            if result_compra_ind.retcode == mt5.TRADE_RETCODE_DONE:
                self.log(f"✅ INDEPENDENTE enviado com sucesso - Ticket: {result_compra_ind.order}")

                # 5.7 AMBAS AS ORDENS APROVADAS: REGISTRO DO PAR
                self.log(f"🎯 AMBAS AS ORDENS APROVADAS: Registrando par completo")

                # Cria estrutura de pares se não existir
                if not hasattr(self, 'pares'):
                    self.pares = {}

                # Registra o par (baseado no código original)
                self.pares[magic_id] = (depende_atual, independe_atual)
                self.log(f"📝 Par registrado: pares[{magic_id}] = ({depende_atual}, {independe_atual})")

                # 5.8 SALVA DETALHES COMPLETOS DA OPERAÇÃO
                detalhes_venda = {
                    'ID': magic_id,
                    'Dependente': depende_atual,
                    'Independente': independe_atual,
                    'Timeframe': timeframe_atual,
                    'Período': periodo_atual,
                    'Z-Score': zscore_hoje,
                    'R2': r2_hoje,
                    'beta': beta_hoje,
                    'desvio_padrao': desvio_padrao_valor,
                    'coef_variacao': coef_variacao_valor,
                    'corr_ind_ibov': corr_ind_ibov_valor,
                    'correlacao': correlacao_valor,
                    'Quantidade Dependente': qtd_dep,
                    'Preco Dependente': price_dep_venda,
                    'tp_dep': stop_gain_venda,
                    'sl_dep': stop_loss_venda,
                    'Preco Independente': price_ind_compra,
                    'tp_ind': stop_gain_compra_ind,
                    'sl_ind': stop_loss_compra_ind,
                    'magic': magic_id,
                    'Timestamp': datetime.now(),
                    'ticket_dep': ticket_dep,
                    'ticket_ind': result_compra_ind.order,
                    'tipo_operacao': 'VENDA_DEP_COMPRA_IND'
                }

                # Salva na lista de operações executadas
                if not hasattr(self, 'operacoes_executadas'):
                    self.operacoes_executadas = []

                self.operacoes_executadas.append(detalhes_venda)

                self.log(f"🎉 OPERAÇÃO COMPLETA EXECUTADA COM SUCESSO!")
                self.log(f"   ├─ Par: {depende_atual}/{independe_atual}")
                self.log(f"   ├─ Magic ID: {magic_id}")
                self.log(f"   ├─ Ticket DEP: {ticket_dep}")
                self.log(f"   ├─ Ticket IND: {result_compra_ind.order}")
                self.log(f"   └─ Z-Score: {zscore_hoje:.2f}")

                return True

            else:
                # 5.9 INDEPENDENTE FALHOU: ROLLBACK DO DEPENDENTE
                self.log(f"❌ INDEPENDENTE FALHOU: retcode={result_compra_ind.retcode}")
                self.log(f"🔄 EXECUTANDO ROLLBACK: Cancelando ordem DEPENDENTE (ticket {ticket_dep})")

                if self._cancelar_ordem_rollback(ticket_dep):
                    self.log(f"✅ ROLLBACK bem-sucedido: Ordem DEPENDENTE cancelada")
                else:
                    self.log(f"❌ ROLLBACK FALHOU: Ordem DEPENDENTE não foi cancelada")

                return False

        else:
            # 5.10 DEPENDENTE FALHOU: NÃO ENVIA INDEPENDENTE
            self.log(f"❌ DEPENDENTE FALHOU: retcode={result_venda_dep.retcode}")
            self.log(f"🚫 OPERAÇÃO ABORTADA: Não enviando ordem INDEPENDENTE")
            return False
        
        #except Exception as e:
            #self.log(f"❌ Erro geral na função de venda DEP + compra IND: {str(e)}")
            #return False

    def obter_magic_id_correto(self, depende_atual, independe_atual, linha_selecionada):
        """
        Obtém o Magic ID correto prioritariamente da tabela_linha_operacao01 (segunda seleção)
        com fallback para linha_selecionada
        
        Args:
            depende_atual (str): Nome do ativo dependente
            independe_atual (str): Nome do ativo independente  
            linha_selecionada (dict): Linha da primeira seleção como fallback
            
        Returns:
            int: Magic ID ou None se não encontrado
        """
        try:
            magic_id = None
            
            # PRIORIDADE 1: Busca na tabela_linha_operacao01 (segunda seleção)
            if hasattr(self, 'tabela_linha_operacao01') and not self.tabela_linha_operacao01.empty:
                mascara_filtro = (
                    (self.tabela_linha_operacao01['Dependente'] == depende_atual) &
                    (self.tabela_linha_operacao01['Independente'] == independe_atual)
                )
                
                registro_correspondente = self.tabela_linha_operacao01[mascara_filtro]
                
                if not registro_correspondente.empty:
                    magic_id = registro_correspondente.iloc[0]['ID']
                    self.log(f"✅ Magic ID da 2ª seleção: {magic_id} para {depende_atual}x{independe_atual}")
                    return magic_id
                else:
                    self.log(f"⚠️ Par {depende_atual}x{independe_atual} não encontrado na 2ª seleção")
            
            # PRIORIDADE 2: Fallback para linha_selecionada (primeira seleção)
            if magic_id is None:
                magic_id = linha_selecionada.get('ID')
                if magic_id is not None:
                    self.log(f"⚠️ Magic ID da 1ª seleção (fallback): {magic_id} para {depende_atual}x{independe_atual}")
                    return magic_id
            
            # ERRO: Nenhum Magic ID encontrado
            self.log(f"❌ ERRO CRÍTICO: Magic ID não encontrado para {depende_atual}x{independe_atual}")
            return None
            
        except Exception as e:
            self.log(f"❌ Erro ao obter Magic ID para {depende_atual}x{independe_atual}: {e}")
            # Fallback de emergência
            magic_id_emergency = linha_selecionada.get('ID') if linha_selecionada else None
            if magic_id_emergency:
                self.log(f"🔄 Magic ID de emergência: {magic_id_emergency}")
            return magic_id_emergency
    
    # Funções auxiliares para cálculos
    def _calcular_preco_compra(self, linha_selecionada, symbol_info_tick):
        """Calcula preço de compra baseado nos spreads da linha selecionada"""
        try:
            # Prioridade 1: Usar spread_compra se disponível
            spread_compra = linha_selecionada.get('spread_compra')
            if spread_compra is not None and spread_compra > 0:
                return float(spread_compra)
            
            # Prioridade 2: Usar previsão mínima se disponível  
            previsao_minimo = linha_selecionada.get('previsao_minimo')
            if previsao_minimo is not None and previsao_minimo > 0:
                return float(previsao_minimo)
            
            # Fallback: Usar ask current com desconto de 0.5%
            current_ask = symbol_info_tick.ask
            return float(current_ask * 0.995)
            
        except Exception as e:
            self.log(f"[ERRO] Erro ao calcular preço de compra: {e}")
            return None

    def _calcular_preco_venda(self, linha_selecionada, symbol_info_tick):
        """Calcula preço de venda baseado nos spreads da linha selecionada"""
        try:
            # Prioridade 1: Usar spread_venda se disponível
            spread_venda = linha_selecionada.get('spread_venda')
            if spread_venda is not None and spread_venda > 0:
                return float(spread_venda)
            
            # Prioridade 2: Usar previsão máxima se disponível
            previsao_maximo = linha_selecionada.get('previsao_maximo')
            if previsao_maximo is not None and previsao_maximo > 0:
                return float(previsao_maximo)
            
            # Fallback: Usar bid current com acréscimo de 0.5%
            current_bid = symbol_info_tick.bid
            return float(current_bid * 1.005)
            
        except Exception as e:
            self.log(f"[ERRO] Erro ao calcular preço de venda: {e}")
            return None

    def _calcular_preco_compra_indep(self, linha_selecionada, symbol_info_tick):
        """Calcula preço de compra para ativo independente"""
        try:
            # Prioridade 1: Usar spread_compra do independente
            indep_spread_compra = linha_selecionada.get('indep_spread_compra')
            if indep_spread_compra is not None and indep_spread_compra > 0:
                return float(indep_spread_compra)
            
            # Fallback: Usar ask current com desconto
            current_ask = symbol_info_tick.ask
            return float(current_ask * 0.998)
            
        except Exception as e:
            self.log(f"[ERRO] Erro ao calcular preço de compra independente: {e}")
            return None

    def _calcular_preco_venda_indep(self, linha_selecionada, symbol_info_tick):
        """Calcula preço de venda para ativo independente"""
        try:
            # Prioridade 1: Usar spread_venda do independente
            indep_spread_venda = linha_selecionada.get('indep_spread_venda')
            if indep_spread_venda is not None and indep_spread_venda > 0:
                return float(indep_spread_venda)
            
            # Fallback: Usar bid current com acréscimo
            current_bid = symbol_info_tick.bid
            return float(current_bid * 1.002)
            
        except Exception as e:
            self.log(f"[ERRO] Erro ao calcular preço de venda independente: {e}")
            return None

    def _calcular_stop_gain_compra(self, linha_selecionada, preco_entrada):
        """Calcula stop gain para operação de compra"""
        try:
            # Prioridade 1: Usar spread_compra_gain se disponível
            spread_gain = linha_selecionada.get('spread_compra_gain')
            if spread_gain is not None and spread_gain > 0:
                return float(spread_gain)
            
            # Fallback: 1.5% acima do preço de entrada
            return float(preco_entrada * 1.015)
            
        except Exception as e:
            self.log(f"[ERRO] Erro ao calcular stop gain compra: {e}")
            return float(preco_entrada * 1.015)

    def _calcular_stop_loss_compra(self, linha_selecionada, preco_entrada):
        """Calcula stop loss para operação de compra"""
        try:
            # Prioridade 1: Usar spread_compra_loss se disponível
            spread_loss = linha_selecionada.get('spread_compra_loss')
            if spread_loss is not None and spread_loss > 0:
                return float(spread_loss)
            
            # Fallback: 1% abaixo do preço de entrada
            return float(preco_entrada * 0.99)
            
        except Exception as e:
            self.log(f"[ERRO] Erro ao calcular stop loss compra: {e}")
            return float(preco_entrada * 0.99)

    def _calcular_stop_gain_venda(self, linha_selecionada, preco_entrada):
        """Calcula stop gain para operação de venda"""
        try:
            # Prioridade 1: Usar spread_venda_gain se disponível
            spread_gain = linha_selecionada.get('spread_venda_gain')
            if spread_gain is not None and spread_gain > 0:
                return float(spread_gain)
            
            # Fallback: 1.5% abaixo do preço de entrada
            return float(preco_entrada * 0.985)
            
        except Exception as e:
            self.log(f"[ERRO] Erro ao calcular stop gain venda: {e}")
            return float(preco_entrada * 0.985)

    def _calcular_stop_loss_venda(self, linha_selecionada, preco_entrada):
        """Calcula stop loss para operação de venda"""
        try:
            # Prioridade 1: Usar spread_venda_loss se disponível
            spread_loss = linha_selecionada.get('spread_venda_loss')
            if spread_loss is not None and spread_loss > 0:
                return float(spread_loss)
            
            # Fallback: 1% acima do preço de entrada
            return float(preco_entrada * 1.01)
            
        except Exception as e:
            self.log(f"[ERRO] Erro ao calcular stop loss venda: {e}")
            return float(preco_entrada * 1.01)

    def _calcular_stop_gain_venda_ind(self, linha_selecionada, preco_entrada):
        """Calcula stop gain para venda do independente"""
        try:
            spread_gain = linha_selecionada.get('indep_spread_venda_gain')
            if spread_gain is not None and spread_gain > 0:
                return float(spread_gain)
            return float(preco_entrada * 0.985)
        except Exception as e:
            self.log(f"[ERRO] Erro ao calcular stop gain venda independente: {e}")
            return float(preco_entrada * 0.985)

    def _calcular_stop_loss_venda_ind(self, linha_selecionada, preco_entrada):
        """Calcula stop loss para venda do independente"""
        try:
            spread_loss = linha_selecionada.get('indep_spread_venda_loss')
            if spread_loss is not None and spread_loss > 0:
                return float(spread_loss)
            return float(preco_entrada * 1.01)
        except Exception as e:
            self.log(f"[ERRO] Erro ao calcular stop loss venda independente: {e}")
            return float(preco_entrada * 1.01)

    def _calcular_stop_gain_compra_ind(self, linha_selecionada, preco_entrada):
        """Calcula stop gain para compra do independente"""
        try:
            spread_gain = linha_selecionada.get('indep_spread_compra_gain')
            if spread_gain is not None and spread_gain > 0:
                return float(spread_gain)
            return float(preco_entrada * 1.015)
        except Exception as e:
            self.log(f"[ERRO] Erro ao calcular stop gain compra independente: {e}")
            return float(preco_entrada * 1.015)

    def _calcular_stop_loss_compra_ind(self, linha_selecionada, preco_entrada):
        """Calcula stop loss para compra do independente"""
        try:
            spread_loss = linha_selecionada.get('indep_spread_compra_loss')
            if spread_loss is not None and spread_loss > 0:
                return float(spread_loss)
            return float(preco_entrada * 0.99)
        except Exception as e:
            self.log(f"[ERRO] Erro ao calcular stop loss compra independente: {e}")
            return float(preco_entrada * 0.99)
                
    def _enviar_ordem_mt5(self, symbol, volume, order_type, price, tp, sl, magic, comment):
        """Envia ordem para o MT5"""
        try:
            request = {
                "action": mt5.TRADE_ACTION_PENDING,
                "symbol": symbol,
                "volume": volume,
                "type": order_type,
                "price": price,
                "sl": sl,
                "tp": tp,
                "magic": magic,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            result = mt5.order_send(request)
            
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                self.log(f"✅ Ordem enviada: {symbol} - Ticket: {result.order}")
                return True
            else:
                self.log(f"❌ Erro ao enviar ordem {symbol}: {result.comment}")
                return False
                
        except Exception as e:
            self.log(f"❌ Erro ao enviar ordem MT5: {str(e)}")
            return False

    def cancelar_ordem(self, ticket: int) -> bool:
        """Cancela ordem pendente específica"""
        try:
            if not self.mt5_connected:
                self.log(f"❌ MT5 não conectado - impossível cancelar ordem {ticket}")
                return False
            
            # Busca a ordem para confirmar que existe
            orders = mt5.orders_get(ticket=ticket)
            if not orders:
                self.log(f"❌ Ordem {ticket} não encontrada")
                return False
            
            order = orders[0]
            
            # Prepara requisição de cancelamento
            request = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": ticket,
            }
            
            # Envia requisição de cancelamento
            result = mt5.order_send(request)
            
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                self.log(f"✅ Ordem {ticket} ({order.symbol}) cancelada com sucesso")
                return True
            else:
                self.log(f"❌ Erro ao cancelar ordem {ticket}: {result.comment}")
                return False
                
        except Exception as e:
            self.log(f"❌ Erro ao cancelar ordem {ticket}: {str(e)}")
            return False

    def _calcular_volume_operacao(self, preco_entrada, valor_operacao):
        """Calcula volume da operação baseado no preço e valor desejado"""
        try:
            if preco_entrada <= 0:
                self.log(f"[ERRO] Preço de entrada inválido: {preco_entrada}")
                return 0
            
            volume_calculado = valor_operacao / preco_entrada
            # Arredonda para o múltiplo de 100 mais próximo
            volume_arredondado = round(volume_calculado, -2)
            
            # Garante volume mínimo de 100
            if volume_arredondado < 100:
                volume_arredondado = 100
                
            return volume_arredondado
            
        except Exception as e:
            self.log(f"[ERRO] Erro ao calcular volume: {e}")
            return 100  # Volume mínimo de segurança

    def _validar_condicoes_entrada_compra(self, linha_selecionada, preco_compra):
        """Valida condições técnicas para entrada em compra"""
        try:
            # Validação básica de preço
            if preco_compra <= 0:
                return False
                
            # Validação de Z-Score
            zscore = linha_selecionada.get('Z-Score', 0)
            if zscore > -2.0:  # Para compra, Z-Score deve ser < -2.0
                return False
                
            # Validação de R²
            r2 = linha_selecionada.get('r2', 0)
            if r2 < 0.3:  # R² mínimo
                return False
                
            # Validação de resíduo (se disponível)
            pred_resid = linha_selecionada.get('pred_resid')
            resid_atual = linha_selecionada.get('resid_atual')
            
            if pred_resid is not None and resid_atual is not None:
                if float(pred_resid) <= float(resid_atual):
                    return False
            
            return True
            
        except Exception as e:
            self.log(f"[ERRO] Erro na validação de condições de compra: {e}")
            return False

    def _validar_condicoes_entrada_venda(self, linha_selecionada, preco_venda):
        """Valida condições técnicas para entrada em venda"""
        try:
            # Validação básica de preço
            if preco_venda <= 0:
                return False
                
            # Validação de Z-Score
            zscore = linha_selecionada.get('Z-Score', 0)
            if zscore < 2.0:  # Para venda, Z-Score deve ser > 2.0
                return False
                
            # Validação de R²
            r2 = linha_selecionada.get('r2', 0)
            if r2 < 0.3:  # R² mínimo
                return False
                
            # Validação de resíduo (se disponível)
            pred_resid = linha_selecionada.get('pred_resid')
            resid_atual = linha_selecionada.get('resid_atual')
            
            if pred_resid is not None and resid_atual is not None:
                if float(pred_resid) >= float(resid_atual):
                    return False
            
            return True
            
        except Exception as e:
            self.log(f"[ERRO] Erro na validação de condições de venda: {e}")
            return False

    def _cancelar_ordem_rollback(self, ticket):
        """Cancela uma ordem pendente em caso de rollback"""
        try:
            request = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": ticket,
            }
            
            result = mt5.order_send(request)
            
            if result is None:
                self.log(f"[ERRO] Cancelamento do ticket {ticket} retornou None")
                return False
                
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                self.log(f"[OK] Ticket {ticket} cancelado com sucesso")
                return True
            else:
                self.log(f"[ERRO] Falha ao cancelar ticket {ticket}: retcode={result.retcode}")
                return False
                
        except Exception as e:
            self.log(f"[ERRO] Exceção ao cancelar ordem {ticket}: {e}")
            return False

    def _verificar_operacao_aberta(self, lista_ativos):
        """Verifica se já existe posição aberta para algum dos ativos da lista"""
        contratos_abertos = mt5.positions_get()
        if contratos_abertos:
            for posicao in contratos_abertos:
                if posicao.symbol in lista_ativos:
                    return True
        return False

    def _contar_operacoes_por_prefixo(self, prefixo):
        """Conta operações abertas que começam com o prefixo especificado"""
        contratos = mt5.positions_get()
        if contratos is None:
            return 0
        return len([op for op in contratos if str(op.magic).startswith(prefixo)])
    
    def _verificar_operacao_aberta_tipo(self, symbol, tipo_operacao):
        """Verifica se existe operação aberta (posição ou ordem) de um tipo específico"""
        # Verifica ordens pendentes
        ordens_pendentes = mt5.orders_get(symbol=symbol)
        if ordens_pendentes:
            for ordem in ordens_pendentes:
                if tipo_operacao == 'sell' and ordem.type in [mt5.ORDER_TYPE_SELL_LIMIT, mt5.ORDER_TYPE_SELL_STOP, mt5.ORDER_TYPE_SELL]:
                    return True
                elif tipo_operacao == 'buy' and ordem.type in [mt5.ORDER_TYPE_BUY_LIMIT, mt5.ORDER_TYPE_BUY_STOP, mt5.ORDER_TYPE_BUY]:
                    return True

        # Verifica posições abertas
        posicoes = mt5.positions_get(symbol=symbol)
        if posicoes:
            for pos in posicoes:
                if tipo_operacao == 'sell' and pos.type == mt5.POSITION_TYPE_SELL:
                    return True
                elif tipo_operacao == 'buy' and pos.type == mt5.POSITION_TYPE_BUY:
                    return True

        return False

    def _contar_operacoes_por_prefixo(self, prefixo):
        """Conta operações abertas com o prefixo especificado"""
        try:
            posicoes = mt5.positions_get()
            if posicoes:
                return len([p for p in posicoes if str(p.magic).startswith(prefixo)])
            return 0
        except:
            return 0

    def _registrar_operacao_executada(self, linha_selecionada, magic_id, tipo_operacao):
        """Registra operação executada para controle"""
        try:
            detalhes = {
                'ID': magic_id,
                'Dependente': linha_selecionada.get('Dependente'),
                'Independente': linha_selecionada.get('Independente'),
                'Tipo': tipo_operacao,
                'Z-Score': linha_selecionada.get('Z-Score'),
                'Timestamp': datetime.now()
            }
            
            if not hasattr(self, 'operacoes_executadas'):
                self.operacoes_executadas = []
            
            self.operacoes_executadas.append(detalhes)
            self.log(f"📝 Operação registrada: {tipo_operacao} - Magic: {magic_id}")
            
        except Exception as e:
            self.log(f"⚠️ Erro ao registrar operação: {str(e)}")  

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
                    'type': 'LONG' if pos.type == 0 else 'SHORT',
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
    
    def obter_ordens_pendentes(self) -> List[Dict]:
        """Obtém ordens pendentes do MT5"""
        if not self.mt5_connected:
            return []
            
        try:
            orders = mt5.orders_get()
            if orders is None:
                return []
                
            ordens = []
            for order in orders:
                # Determina o tipo de ordem
                tipo_ordem = "UNKNOWN"
                if order.type == mt5.ORDER_TYPE_BUY_LIMIT:
                    tipo_ordem = "BUY LIMIT"
                elif order.type == mt5.ORDER_TYPE_SELL_LIMIT:
                    tipo_ordem = "SELL LIMIT"
                elif order.type == mt5.ORDER_TYPE_BUY_STOP:
                    tipo_ordem = "BUY STOP"
                elif order.type == mt5.ORDER_TYPE_SELL_STOP:
                    tipo_ordem = "SELL STOP"
                elif order.type == mt5.ORDER_TYPE_BUY_STOP_LIMIT:
                    tipo_ordem = "BUY STOP LIMIT"
                elif order.type == mt5.ORDER_TYPE_SELL_STOP_LIMIT:
                    tipo_ordem = "SELL STOP LIMIT"
                
                # Preço atual do símbolo para comparação
                preco_atual = self.obter_preco_atual(order.symbol)
                
                # Calcula diferença percentual entre ordem e preço atual
                diff_percent = 0
                if preco_atual and order.price_open > 0:
                    diff_percent = ((order.price_open - preco_atual) / preco_atual) * 100
                
                ordens.append({
                    'ticket': order.ticket,
                    'symbol': order.symbol,
                    'type': tipo_ordem,
                    'volume': order.volume_initial,
                    'price_open': order.price_open,
                    'price_current': preco_atual or 0,
                    'sl': order.sl,
                    'tp': order.tp,
                    'diff_percent': diff_percent,
                    'time_setup': datetime.fromtimestamp(order.time_setup),
                    'time_expiration': datetime.fromtimestamp(order.time_expiration) if order.time_expiration > 0 else None,
                    'magic': order.magic,
                    'comment': order.comment
                })
            
            # 🔧 CONTROLE RIGOROSO DE LOGS - Só loga quando é realmente relevante
            if not hasattr(self, '_last_ordem_log_time'):
                self._last_ordem_log_time = datetime.min
                self._last_ordem_count = 0
                self._primeira_verificacao_ordens = True
            
            now = datetime.now()
            tempo_desde_ultimo_log = (now - self._last_ordem_log_time).total_seconds()
            
            # NOVA LÓGICA ULTRA RESTRITIVA: Log apenas se:
            # 1. Há ordens pendentes (len > 0) E é diferente do anterior, OU
            # 2. Passou mais de 300 segundos (5 minutos) desde o último log E é primeira verificação do período
            should_log = False
            
            if len(ordens) > 0:
                # Se há ordens, loga apenas se mudou a quantidade
                if len(ordens) != self._last_ordem_count:
                    should_log = True
            elif tempo_desde_ultimo_log >= 300 and not hasattr(self, '_logged_sem_ordens_recentemente'):
                # Se não há ordens, loga apenas a cada 5 minutos (status report)
                should_log = True
                self._logged_sem_ordens_recentemente = True
                # Reset flag após 3 minutos para permitir próximo log em 3 min
                import threading
                threading.Timer(180, lambda: delattr(self, '_logged_sem_ordens_recentemente') if hasattr(self, '_logged_sem_ordens_recentemente') else None).start()
            
            if should_log:
                self.log(f"📋 Ordens pendentes encontradas: {len(ordens)}")
                self._last_ordem_log_time = now
                self._last_ordem_count = len(ordens)
                self._primeira_verificacao_ordens = False
            
            return ordens
            
        except Exception as e:
            self.log(f"❌ Erro ao obter ordens pendentes: {str(e)}")
            return []

    def obter_status_threads_sistema_integrado(self):
        """Obtém status detalhado das threads do sistema integrado"""
        try:
            if not hasattr(self, 'sistema_integrado') or not self.sistema_integrado:
                return {
                    'disponivel': False,
                    'threads': {},
                    'resumo': 'Sistema integrado não disponível'
                }
            
            sistema = self.sistema_integrado
            
            # Verifica status de cada thread
            threads_status = {}
            
            # Lista de threads para verificar
            threads_info = [
                ('thread_trading', 'Sistema Trading', 'Execução do sistema original'),
                ('thread_monitor', 'Monitoramento Geral', 'Relatórios a cada 2 minutos'),
                ('thread_monitor_posicoes', 'Monitoramento Posições', 'Verificação a cada 30 segundos'),
                ('thread_break_even', 'Break-Even Contínuo', 'Ajustes a cada 10 segundos'),
                ('thread_ajustes', 'Ajustes Programados', 'Horários específicos (15:10h, 15:20h, 16:01h)'),
                ('thread_ordens', 'Análise e Envio Ordens', 'Processamento a cada 5 minutos')
            ]
            
            for attr_name, display_name, descricao in threads_info:
                if hasattr(sistema, attr_name):
                    thread = getattr(sistema, attr_name)
                    threads_status[display_name] = {
                        'ativa': thread.is_alive() if thread else False,
                        'nome_thread': thread.name if thread else 'N/A',
                        'descricao': descricao,
                        'attr_name': attr_name
                    }
                else:
                    threads_status[display_name] = {
                        'ativa': False,
                        'nome_thread': 'N/A',
                        'descricao': descricao,
                        'attr_name': attr_name
                    }
            
            # Calcula resumo
            threads_ativas = sum(1 for status in threads_status.values() if status['ativa'])
            total_threads = len(threads_status)
            
            resumo = f"{threads_ativas}/{total_threads} threads ativas"
            
            return {
                'disponivel': True,
                'threads': threads_status,
                'resumo': resumo,
                'sistema_rodando': getattr(sistema, 'running', False),
                'dados_sistema': getattr(sistema, 'dados_sistema', {}),
                'total_logs': len(getattr(sistema, 'logs', []))
            }
            
        except Exception as e:
            return {
                'disponivel': False,
                'threads': {},
                'resumo': f'Erro ao obter status: {str(e)}'
            }

    def render_thread_monitor_panel(self):
        """Renderiza painel de monitoramento das threads do sistema integrado"""
        try:
            st.markdown("### 🔧 Status das Threads do Sistema")
            
            status = self.obter_status_threads_sistema_integrado()
            
            if not status['disponivel']:
                st.warning(f"⚠️ {status['resumo']}")
                return
            
            # Métricas principais
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Sistema Integrado", 
                    "🟢 Ativo" if status['sistema_rodando'] else "🔴 Inativo",
                    help="Status geral do sistema integrado"
                )
            
            with col2:
                st.metric(
                    "Threads Ativas", 
                    status['resumo'],
                    help="Número de threads em execução"
                )
            
            with col3:
                dados_sistema = status.get('dados_sistema', {})
                st.metric(
                    "Execuções", 
                    dados_sistema.get('execucoes', 0),
                    help="Total de execuções do sistema"
                )
            
            with col4:
                st.metric(
                    "Logs Gerados", 
                    status.get('total_logs', 0),
                    help="Total de logs do sistema"
                )
            
            # Tabela detalhada das threads
            st.markdown("#### 📋 Detalhes das Threads")
            
            threads_data = []
            for nome, info in status['threads'].items():
                status_icon = "🟢" if info['ativa'] else "🔴"
                threads_data.append({
                    'Thread': nome,
                    'Status': f"{status_icon} {'Ativa' if info['ativa'] else 'Inativa'}",
                    'Descrição': info['descricao'],
                    'Nome Sistema': info['nome_thread']
                })
            
            if threads_data:
                df_threads = pd.DataFrame(threads_data)
                st.dataframe(df_threads, use_container_width=True, hide_index=True)
            
            # Informações adicionais
            if status['sistema_rodando']:
                dados = status.get('dados_sistema', {})
                
                st.markdown("#### 📊 Estatísticas do Sistema")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info(f"**Pares Processados:** {dados.get('pares_processados', 0)}")
                    st.info(f"**Ordens Enviadas:** {dados.get('ordens_enviadas', 0)}")
                
                with col2:
                    inicio = dados.get('inicio')
                    if inicio:
                        tempo_execucao = datetime.now() - inicio
                        st.info(f"**Tempo de Execução:** {str(tempo_execucao).split('.')[0]}")
                    
                    st.info(f"**Status:** {dados.get('status', 'N/A')}")
            
        except Exception as e:
            st.error(f"❌ Erro no painel de threads: {str(e)}")

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
                
                # ✅ CORREÇÃO ADICIONAL: Verifica se saldo inicial é válido
                saldo_inicial = self.dados_sistema.get("saldo_inicial", 0)
                
                # Se saldo inicial é 0 ou igual ao balance atual, recalcula
                if saldo_inicial <= 0 or abs(saldo_inicial - account_info.balance) < 0.01:
                    self.log("🔄 Recalculando saldo inicial...")
                    novo_saldo_inicial = self.calcular_saldo_inicial_do_dia()
                    self.dados_sistema["saldo_inicial"] = novo_saldo_inicial
                    self.log(f"💰 Novo saldo inicial: R$ {novo_saldo_inicial:,.2f}")
                    saldo_inicial = novo_saldo_inicial
                
                # Calcula lucro diário com logs detalhados
                if saldo_inicial > 0:
                    lucro_diario = account_info.equity - saldo_inicial
                    self.dados_sistema["lucro_diario"] = lucro_diario
                    
                    # LOG DETALHADO para debug
                    self.log(f"📊 CÁLCULO LUCRO DIÁRIO:")
                    #self.log(f"   • Equity atual: R$ {account_info.equity:,.2f}")
                    #self.log(f"   • Saldo inicial: R$ {saldo_inicial:,.2f}")
                    #self.log(f"   • Lucro diário: R$ {lucro_diario:+,.2f}")
                else:
                    self.dados_sistema["lucro_diario"] = 0
                    self.log("⚠️ Saldo inicial inválido - lucro diário zerado")
                
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
        """Consome diretamente os DataFrames e variáveis do SistemaIntegrado, sem recalcular ou reatribuir IDs."""
        try:
            from sistema_integrado import SistemaIntegrado
            sistema = SistemaIntegrado()
            # Executa o sistema original para garantir que as seleções sejam geradas
            sistema.executar_sistema_original()
            # Garante que o sistema integrado já executou as análises
            if not hasattr(sistema, 'tabela_linha_operacao') or not hasattr(sistema, 'tabela_linha_operacao01'):
                self.log("❌ SistemaIntegrado não possui as seleções necessárias. Certifique-se de que o sistema foi executado.")
                return
            # Consome diretamente os DataFrames do SistemaIntegrado
            tabela_linha_operacao = getattr(sistema, 'tabela_linha_operacao', None)
            tabela_linha_operacao01 = getattr(sistema, 'tabela_linha_operacao01', None)
            if tabela_linha_operacao is None or tabela_linha_operacao01 is None:
                self.log("❌ Não foi possível obter as seleções do SistemaIntegrado.")
                return
            self.log(f"✅ Dados da primeira seleção carregados do SistemaIntegrado: {len(tabela_linha_operacao)} pares")
            self.log(f"✅ Dados da segunda seleção carregados do SistemaIntegrado: {len(tabela_linha_operacao01)} pares")
            # Exibe os dados exatamente como estão no SistemaIntegrado
            self.sinais_ativos = tabela_linha_operacao01.to_dict(orient='records') if hasattr(tabela_linha_operacao01, 'to_dict') else tabela_linha_operacao01
            self.dados_sistema["pares_processados"] = len(self.sinais_ativos)
            # Armazena para exibição nas abas
            if hasattr(st.session_state, 'trading_system') and st.session_state.trading_system:
                st.session_state.trading_system.tabela_linha_operacao = tabela_linha_operacao
                st.session_state.trading_system.tabela_linha_operacao01 = tabela_linha_operacao01
            self.log(f"🏆 Dados das seleções carregados e prontos para exibição. IDs e campos preservados.")
        except ImportError as e:
            self.log(f"❌ SistemaIntegrado não disponível: {str(e)}")
        except Exception as e:
            self.log(f"❌ Erro ao consumir dados do SistemaIntegrado: {str(e)}")

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
                #self.log(f"ℹ️ Nenhum deal encontrado no período de {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}")
                return []
            
            #self.log(f"📊 {len(deals)} deals encontrados no MT5 para análise")
            
            trades_processados = []
            
            for deal in deals:
                # Filtra apenas deals que representam fechamento de posições (com lucro/prejuízo)
                # Inclui todos os deals que têm profit diferente de zero OU são do tipo OUT (fechamento)
                if deal.profit != 0 or (hasattr(deal, 'entry') and deal.entry == 1):
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
            
            #self.log(f"✅ {len(trades_processados)} trades com resultado processados do MT5")
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
        
        # Inicializa sistema integrado apenas se necessário
        # 1. Conectar ao MT5 na thread principal antes de qualquer inicialização
        if not self.mt5_connected:
            if not self.conectar_mt5():
                self.log("❌ Não foi possível conectar ao MetaTrader5. O sistema não será iniciado.")
                return False

        # 2. Inicializa sistema integrado apenas se necessário
        if self.sistema_integrado is None:
            try:
                from sistema_integrado import SistemaIntegrado
                self.sistema_integrado = SistemaIntegrado()
                self.sistema_integrado_status = 'disponivel'
            except Exception as e:
                self.sistema_integrado = None
                self.sistema_integrado_status = f'erro: {e}'
                self.log(f"❌ Erro ao inicializar sistema integrado: {e}")
                return False

        self.running = True
        self.config_atual = config  # Salva configuração atual

        if self.modo_otimizado:
            # MODO OTIMIZADO: Threading avançado simplificado
            self.log("🚀 Iniciando sistema OTIMIZADO com threading avançado...")
            self.log("✅ Threads que serão iniciadas:")
            self.log("   📊 Análise principal (dados reais)")
            self.log("   � Sincronização de dados (dashboard)")

            # 1. Thread principal: executa análise real
            self.thread_sistema = threading.Thread(
                target=self.executar_sistema_integrado,
                args=(config,),
                daemon=True,
                name="AnaliseRealOtimizada"
            )
            self.thread_sistema.start()

            # 2. Thread de sincronização: sincroniza dados entre thread e dashboard
            self.thread_sincronizacao = threading.Thread(
                target=self.sincronizar_dados_sistema,
                daemon=True,
                name="SincronizacaoDashboard"
            )
            self.thread_sincronizacao.start()

            self.log("🚀 Sistema otimizado iniciado: análise + sincronização ativa")

        else:
            # MODO BÁSICO: Execução direta na thread principal
            self.log("⚙️ Iniciando sistema em modo BÁSICO...")
            self.thread_sistema = threading.Thread(
                target=self.executar_sistema_principal,
                args=(config,),
                daemon=True,
                name="SistemaBasico"
            )
            self.thread_sistema.start()

        self.log("✅ Sistema iniciado com sucesso")
        return True
    
    def executar_sistema_integrado(self, config: Dict):
        """Executa sistema integrado completo com todas as threads"""
        try:
            self.log("🎯 Inicializando sistema integrado completo...")

            # Garante que a conexão com o MT5 está ativa antes de iniciar o loop
            if not self.mt5_connected:
                self.log("❌ MT5 não está conectado. O sistema integrado não será executado.")
                return

            # CORREÇÃO CRÍTICA: Em vez de usar o sistema_integrado.py que tem problemas,
            # executa a mesma análise real do modo básico, mas com threading
            while self.running:
                try:
                    self.log("🔄 Executando análise real no modo otimizado...")

                    # Executa a mesma análise real que funciona no modo básico
                    self.executar_analise_real(config)

                    # Atualiza dados do sistema
                    self.dados_sistema["execucoes"] += 1
                    self.dados_sistema["ultimo_update"] = datetime.now()

                    # Aguarda próximo ciclo (5 minutos no modo otimizado)
                    intervalo_otimizado = 300  # 5 minutos

                    for i in range(intervalo_otimizado):
                        if not self.running:
                            break
                        import time as time_module
                        time_module.sleep(1)

                except Exception as e:
                    self.log(f"❌ Erro no ciclo de análise: {str(e)}")
                    # Aguarda 30 segundos antes de tentar novamente
                    for i in range(30):
                        if not self.running:
                            break
                        import time as time_module
                        time_module.sleep(1)

        except Exception as e:
            self.log(f"❌ Erro no sistema integrado: {str(e)}")
            # Fallback para sistema básico
            self.executar_sistema_principal(config)
    
    def sincronizar_dados_sistema(self):
        """Thread para sincronizar dados entre thread de análise e dashboard - THREAD SAFE"""
        while self.running:
            try:
                if self.modo_otimizado:
                    # CORREÇÃO: Em vez de tentar acessar st.session_state de dentro da thread,
                    # vamos armazenar os dados em variáveis de instância que podem ser acessadas
                    # pela thread principal quando ela renderizar as abas
                    
                    dados_sincronizados = 0
                    
                    # Cria uma estrutura de dados temporária para sincronização
                    dados_para_sincronizar = {
                        'timestamp_sync': datetime.now(),
                        'sinais_ativos': None,
                        'tabela_linha_operacao': None,
                        'tabela_linha_operacao01': None,
                        'dados_sistema': None,
                        'equity_historico': None,
                        'posicoes_abertas': None
                    }
                    
                    # 1. Coleta dados da thread de análise (self)
                    if hasattr(self, 'sinais_ativos_exibicao') and self.sinais_ativos_exibicao:
                        dados_para_sincronizar['sinais_ativos'] = self.sinais_ativos_exibicao.copy()
                        dados_sincronizados += 1
                    
                    if hasattr(self, 'tabela_linha_operacao') and not self.tabela_linha_operacao.empty:
                        dados_para_sincronizar['tabela_linha_operacao'] = self.tabela_linha_operacao.copy()
                        dados_sincronizados += 1
                    
                    if hasattr(self, 'tabela_linha_operacao01') and not self.tabela_linha_operacao01.empty:
                        dados_para_sincronizar['tabela_linha_operacao01'] = self.tabela_linha_operacao01.copy()
                        dados_sincronizados += 1
                    
                    if hasattr(self, 'dados_sistema'):
                        dados_para_sincronizar['dados_sistema'] = self.dados_sistema.copy()
                    
                    if hasattr(self, 'equity_historico_exibicao') and self.equity_historico_exibicao:
                        dados_para_sincronizar['equity_historico'] = self.equity_historico_exibicao.copy()
                    
                    if hasattr(self, 'posicoes_abertas_exibicao') and self.posicoes_abertas_exibicao:
                        dados_para_sincronizar['posicoes_abertas'] = self.posicoes_abertas_exibicao.copy()
                    
                    # 2. NOVA ABORDAGEM: Armazena os dados em uma variável de classe acessível
                    # pela thread principal sem usar st.session_state
                    self._dados_sincronizados = dados_para_sincronizar
                    
                    # Log de sincronização apenas se houve dados relevantes
                    if dados_sincronizados > 0:
                        #self.log(f"🔄 Sincronização thread-safe: {dados_sincronizados} estruturas preparadas")
                        pass
                # Aguarda próximo ciclo de sincronização (2 segundos)
                for i in range(2):
                    if not self.running:
                        break
                    time_module.sleep(1)
                    
            except Exception as e:
                self.log(f"❌ Erro na sincronização thread-safe: {str(e)}")
                # Em caso de erro, aguarda mais tempo antes de tentar novamente
                for i in range(5):
                    if not self.running:
                        break
                    time_module.sleep(1)
    
    def obter_dados_sincronizados(self):
        """Obtém dados sincronizados de forma thread-safe
        Returns:
            dict: Dados sincronizados ou None se não houver dados recentes (< 30 segundos)
        """
        try:
            if not hasattr(self, '_dados_sincronizados') or not self._dados_sincronizados:
                return None
            
            # Verifica se os dados são recentes (últimos 30 segundos)
            timestamp_sync = self._dados_sincronizados.get('timestamp_sync')
            if timestamp_sync:
                tempo_desde_sync = (datetime.now() - timestamp_sync).total_seconds()
                if tempo_desde_sync > 30:
                    return None
            
            return self._dados_sincronizados.copy()
            
        except Exception as e:
            self.log(f"❌ Erro ao obter dados sincronizados: {str(e)}")
            return None
    
    def parar_sistema(self):
        """Para o sistema de trading - Versão otimizada"""
        self.running = False
        self.log("🛑 Iniciando parada do sistema...")
        
        if self.modo_otimizado:
            self.log("� Parando sistema OTIMIZADO...")
            
            # Para thread principal de análise
            if hasattr(self, 'thread_sistema') and self.thread_sistema and self.thread_sistema.is_alive():
                self.log("⏸️ Aguardando thread de análise finalizar...")
                self.thread_sistema.join(timeout=5)
                if self.thread_sistema.is_alive():
                    self.log("⚠️ Thread de análise não finalizou no tempo esperado")
                else:
                    self.log("✅ Thread de análise finalizada")
            
            # Para thread de sincronização
            if hasattr(self, 'thread_sincronizacao') and self.thread_sincronizacao and self.thread_sincronizacao.is_alive():
                self.log("⏸️ Aguardando thread de sincronização finalizar...")
                self.thread_sincronizacao.join(timeout=3)
                if self.thread_sincronizacao.is_alive():
                    self.log("⚠️ Thread de sincronização não finalizou no tempo esperado")
                else:
                    self.log("✅ Thread de sincronização finalizada")
        else:
            self.log("⚙️ Parando sistema BÁSICO...")
            
            # Para thread única do modo básico
            if hasattr(self, 'thread_sistema') and self.thread_sistema and self.thread_sistema.is_alive():
                self.log("⏸️ Aguardando thread principal finalizar...")
                self.thread_sistema.join(timeout=5)
                if self.thread_sistema.is_alive():
                    self.log("⚠️ Thread principal não finalizou no tempo esperado")
                else:
                    self.log("✅ Thread principal finalizada")
        
        self.log("🛑 Sistema parado com sucesso")
    
    def exportar_relatorio_excel(self) -> bytes:
        """Exporta relatório para Excel"""
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Resumo geral
            resumo = pd.DataFrame([self.dados_sistema_exibicao])
            resumo.to_excel(writer, sheet_name='Resumo', index=False)
            
            # Posições abertas
            if self.posicoes_abertas_exibicao:
                pos_df = pd.DataFrame(self.posicoes_abertas_exibicao)
                pos_df.to_excel(writer, sheet_name='Posições Abertas', index=False)
            
            # Sinais
            if self.sinais_ativos_exibicao:
                sinais_df = pd.DataFrame(self.sinais_ativos_exibicao)
                sinais_df.to_excel(writer, sheet_name='Sinais', index=False)
            
            # Equity histórico
            if self.equity_historico_exibicao:
                equity_df = pd.DataFrame(self.equity_historico_exibicao)
                equity_df.to_excel(writer, sheet_name='Equity Histórico', index=False)
            
            # Logs
            logs_df = pd.DataFrame({'Log': self.logs_exibicao})
            logs_df.to_excel(writer, sheet_name='Logs', index=False)
        
        output.seek(0)
        return output.getvalue()


# Inicializa sistema global
if 'trading_system' not in st.session_state:
    st.session_state.trading_system = TradingSystemReal()

# Verificação de segurança - reconstrói o objeto se necessário
if not hasattr(st.session_state.trading_system, 'iniciar_sistema'):
    st.session_state.trading_system = TradingSystemReal()

# Exibe status do sistema integrado na interface (etapa 1)
st.sidebar.markdown('---')
st.sidebar.markdown('### 🧩 Sistema Integrado')
sis = st.session_state.trading_system
if hasattr(sis, 'sistema_integrado') and sis.sistema_integrado:
    st.sidebar.success('Sistema Integrado disponível')
else:
    st.sidebar.warning(f'Sistema Integrado não disponível: {getattr(sis, "sistema_integrado_status", "desconhecido")}')

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
                st.rerun()
        else:
            # Só habilita o botão de iniciar sistema se MT5 estiver conectado
            if st.session_state.trading_system.mt5_connected:
                if st.button("Conectar", use_container_width=True, help="Clique para iniciar o sistema"):
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
                    if hasattr(st.session_state.trading_system, 'iniciar_sistema'):
                        if st.session_state.trading_system.iniciar_sistema(config_temp):
                            st.rerun()
                        else:
                            st.warning("Sistema já está rodando")
                    else:
                        st.error("❌ Método 'iniciar_sistema' não encontrado! Reconstruindo objeto...")
                        st.session_state.trading_system = TradingSystemReal()
                        st.rerun()
            else:
                st.button("Conectar", use_container_width=True, help="Conecte ao MT5 primeiro para habilitar o sistema", disabled=True)
    
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
                sucesso = st.session_state.trading_system.conectar_mt5(mt5_login, mt5_password, mt5_server)
                if sucesso:
                    st.session_state.trading_system.last_login = mt5_login
                    st.session_state.trading_system.last_password = mt5_password
                    st.session_state.trading_system.last_server = mt5_server
                    st.success("Conectado!")
                    st.rerun()  # Recarrega para minimizar a interface
                else:
                    # Mostra o último erro do MT5, se disponível
                    erro_mt5 = mt5.last_error() if hasattr(mt5, 'last_error') else None
                    if erro_mt5:
                        st.error(f"❌ Falha na conexão: {erro_mt5}")
                    else:
                        st.error("❌ Falha na conexão. Verifique login, senha, servidor e se o MetaTrader 5 está aberto.")
    
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
    
    # ✅ ATUALIZAÇÃO CONTROLADA: Atualizar dados a cada 60 segundos quando MT5 conectado
    if sistema.mt5_connected:
        try:
            # Verifica se precisa atualizar (a cada 60 segundos)
            ultima_atualizacao_status = sistema.dados_sistema.get('ultimo_update_status', datetime.min)
            tempo_desde_update = (datetime.now() - ultima_atualizacao_status).total_seconds()
            
            if tempo_desde_update >= 60:
                # Força atualização das informações da conta
                sistema.atualizar_account_info()
                sistema.dados_sistema['ultimo_update_status'] = datetime.now()
                sistema.log(f"📊 Status cards atualizados automaticamente")
            
            # DEBUG: Log dos valores para verificação
            dados = sistema.dados_sistema
            #sistema.log(f"🔧 DEBUG STATUS: saldo_inicial={dados.get('saldo_inicial', 0):,.2f}")
            #sistema.log(f"🔧 DEBUG STATUS: equity_atual={dados.get('equity_atual', 0):,.2f}")
            #sistema.log(f"🔧 DEBUG STATUS: lucro_diario={dados.get('lucro_diario', 0):,.2f}")
            
        except Exception as e:
            sistema.log(f"❌ Erro ao atualizar dados do status: {str(e)}")
    
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
    """Renderiza gráfico de equity com dados reais do MT5 - ATUALIZAÇÃO AUTOMÁTICA"""
    sistema = st.session_state.trading_system
    
    # Indicador de status da funcionalidade
    #col1, col2 = st.columns([3, 1])
    #with col2:
        #if sistema.mt5_connected:
           # ultima_atualizacao = sistema.dados_sistema.get('ultimo_update_equity', datetime.now())
            #tempo_desde_update = (datetime.now() - ultima_atualizacao).total_seconds()
            #st.markdown("✅ **online**", help=f"Dados de equity obtidos em tempo real do MetaTrader 5 - Última atualização há {tempo_desde_update:.0f}s")
            # NOVO: Indicador de última atualização
           # ultima_atualizacao = sistema.dados_sistema.get('ultimo_update_equity', datetime.now())
            #tempo_desde_update = (datetime.now() - ultima_atualizacao).total_seconds()
            #st.caption(f"⏱️ Atualizado há {tempo_desde_update:.0f}s")
        #else:
            #st.markdown("🔴 **offline**", help="MT5 desconectado - sem dados reais")
    
    # ATUALIZAÇÃO AUTOMÁTICA: Verifica se precisa atualizar os dados de equity
    if sistema.mt5_connected:
        # Atualiza automaticamente a cada 60 segundos ou se não há dados
        ultima_atualizacao = sistema.dados_sistema.get('ultimo_update_equity', datetime.min)
        tempo_desde_update = (datetime.now() - ultima_atualizacao).total_seconds()
        
        if not sistema.equity_historico_exibicao or tempo_desde_update >= 60:
            try:
                # Atualiza informações da conta
                sistema.atualizar_account_info()
                
                # Coleta novos dados de equity do MT5
                equity_dados_mt5 = obter_equity_historico_mt5(sistema)
                if equity_dados_mt5:
                    sistema.equity_historico = equity_dados_mt5
                    sistema.dados_sistema['ultimo_update_equity'] = datetime.now()
                    sistema.log(f"� Equity atualizado automaticamente: {len(equity_dados_mt5)} pontos")
                
            except Exception as e:
                sistema.log(f"❌ Erro na atualização automática de equity: {str(e)}")
    
    # Verifica se há dados para exibir
    if not sistema.equity_historico_exibicao:
        if sistema.mt5_connected:
            st.info("📊 Aguardando dados de equity... Execute o sistema para coletar dados.")
            # Mostra dados atuais mesmo sem histórico
            try:
                import MetaTrader5 as mt5
                account_info = mt5.account_info()
                if account_info:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Equity Atual", f"R$ {account_info.equity:,.2f}")
                    with col2:
                        st.metric("Balance Atual", f"R$ {account_info.balance:,.2f}")
                    with col3:
                        st.metric("Profit Atual", f"R$ {account_info.profit:+,.2f}")
                    st.info("💡 O gráfico será construído automaticamente conforme novos dados forem coletados")
            except:
                pass
            return
        else:
            st.warning("🔌 Conecte ao MT5 para visualizar curva de equity real")
            return
    
    df_equity = pd.DataFrame(sistema.equity_historico_exibicao)
    
    # ✅ EXPLICAÇÃO DAS LINHAS DO GRÁFICO
    #with st.expander("💡 Como interpretar o gráfico", expanded=False):
        #col1, col2, col3 = st.columns(3)
        #with col1:
            #st.markdown("""
            #**💰 Equity (Azul)**
            #- Patrimônio total da conta
            #- Inclui lucros realizados + não realizados
            #- Linha principal do gráfico
            #""")
        #with col2:
            #st.markdown("""
            #**🏦 Balance (Verde)**
            #- Apenas lucros realizados
            #- Trades já fechados
            #- Linha tracejada
            #""")
        #with col3:
            #st.markdown("""
            #**📊 Profit (Vermelho)**
            #- Lucro das posições abertas
            #- Diferença: Equity - Balance
            #- Linha pontilhada
            #""")
    
    fig = go.Figure()
    
    # Linha principal: Equity (Patrimônio Total)
    fig.add_trace(go.Scatter(
        x=df_equity['timestamp'],
        y=df_equity['equity'],
        mode='lines+markers',
        name='💰 Equity (Patrimônio Total)',
        line=dict(color='#2980b9', width=3),
        marker=dict(size=5),
        hovertemplate='<b>Equity</b><br>' +
                      'Data: %{x}<br>' + 
                      'Valor: R$ %{y:,.2f}<extra></extra>'
    ))
    
    # Linha secundária: Balance (Lucros Realizados)
    fig.add_trace(go.Scatter(
        x=df_equity['timestamp'],
        y=df_equity['balance'],
        mode='lines',
        name='🏦 Balance (Lucros Realizados)',
        line=dict(color='#27ae60', width=2, dash='dash'),
        hovertemplate='<b>Balance</b><br>' +
                      'Data: %{x}<br>' + 
                      'Valor: R$ %{y:,.2f}<extra></extra>'
    ))
    
    # Linha de Profit (diferença entre Equity e Balance)
    if 'profit' in df_equity.columns:
        fig.add_trace(go.Scatter(
            x=df_equity['timestamp'],
            y=df_equity['profit'],
            mode='lines',
            name='📊 Profit (Posições Abertas)',
            line=dict(color='#e74c3c', width=1, dash='dot'),
            hovertemplate='<b>Profit</b><br>' +
                          'Data: %{x}<br>' + 
                          'Valor: R$ %{y:+,.2f}<extra></extra>'
        ))
    
    fig.update_layout(
        title="📈 Curva de Equity - Patrimônio vs Lucros Realizados",
        xaxis_title="🔵 Patrimônio Líquido  | 🟢 Saldo  |  " \
        "🔴 Profit ",
        yaxis_title="💵 Valor (R$)",
        hovermode='x unified',
        showlegend=False,  # Remove legenda lateral
        height=400,
        template="plotly_white",
        # Configurações do eixo X para melhor visualização das legendas
        xaxis=dict(
            title=dict(
                text="🔵 Patrimônio Líquido  | 🟢 Saldo  | 🔴 Profit ",
                font=dict(size=12, color='white')  # Cor branca para a legenda
            )
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_positions_table():
    """Renderiza tabela de posições abertas - FORMATO PROFISSIONAL"""
    sistema = st.session_state.trading_system
    posicoes = sistema.obter_posicoes_abertas()
    
    # Indicador de status da funcionalidade
    #col1, col2 = st.columns([3, 1])
    #with col1:
        #st.markdown("### 💼 Posições Detalhadas")
    #with col2:
        #if sistema.mt5_connected:
            #st.markdown("✅ **online**", help="Dados obtidos em tempo real do MetaTrader 5")
        #else:
            #st.markdown("🔴 **offline**", help="MT5 desconectado - usando dados simulados")
    
    # Obtém ordens pendentes
    ordens_pendentes = sistema.obter_ordens_pendentes() if sistema.mt5_connected else []
    
    # ==================================================================================
    # NOVA FUNCIONALIDADE: DUAS TABELAS LADO A LADO
    # ==================================================================================
    
    # Cria duas colunas para as tabelas
    col_posicoes, col_ordens = st.columns(2)
    
    # ==================================================================================
    # COLUNA ESQUERDA: POSIÇÕES ABERTAS
    # ==================================================================================
    with col_posicoes:
        st.markdown("#### 📈 **Posições Abertas**")
        
        # Se não há posições reais, cria dados de demonstração
        if not posicoes:
            if sistema.mt5_connected:
                st.info("💼 Nenhuma posição aberta")
            else:
                st.warning("🔌 MT5 desconectado")

        else:
            # Processa posições reais do MT5
            # Converte para formato profissional
            posicoes_formatted = []
            for pos in posicoes:
                tipo = pos.get('type', 'LONG')  # Já vem como string da função obter_posicoes_abertas
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
                    'Símbolo': pos.get('symbol', 'N/A'),
                    'Tipo': tipo,
                    'Volume': f"{pos.get('volume', 0):,.0f}",
                    'Preço Abertura': f"R$ {preco_abertura:.2f}",
                    'Preço Atual': f"R$ {preco_atual:.2f}",
                    'P&L (R$)': f"R$ {pl_value:+.2f}",
                    'P&L (%)': f"{pl_percent:+.2f}%",
                    'Stop Loss': f"R$ {pos.get('sl', 0):.2f}" if pos.get('sl', 0) > 0 else 'N/A',
                    'Take Profit': f"R$ {pos.get('tp', 0):.2f}" if pos.get('tp', 0) > 0 else 'N/A',
                    'Tempo': tempo_str
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
                    height=350
                )
                
                # Métricas resumidas posições
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    total_pl = sum([pos.get('profit', 0) for pos in posicoes])
                    st.metric("P&L Total", f"R$ {total_pl:+.2f}")
                with col_m2:
                    st.metric("Posições", len(posicoes))
    
    # ==================================================================================
    # COLUNA DIREITA: ORDENS PENDENTES
    # ==================================================================================
    with col_ordens:
        st.markdown("#### ⏳ **Ordens Pendentes**")
        
        if not ordens_pendentes:
            if sistema.mt5_connected:
                st.info("📋 Nenhuma ordem pendente")
            else:
                st.warning("🔌 MT5 desconectado")
                
            # DEMO: Cria ordens de exemplo
            #if not sistema.mt5_connected:
                #st.info("📊 Ordens simuladas:")
                
                #ordens_demo = [
                    #{
                        #'Símbolo': 'PETR4',
                        #'Tipo': 'BUY LIMIT',
                        #'Volume': '1000',
                        #'Preço Ordem': 'R$ 28.50',
                        #'Preço Atual': 'R$ 29.00',
                        #'Diferença': '-1.72%',
                        #'Stop Loss': 'R$ 27.00',
                        #'Take Profit': 'R$ 31.00',
                        #'Tempo Setup': '2h ago',
                        #'Expira': '1 dia'
                    #},
                    #{
                        #'Símbolo': 'VALE3',
                        #'Tipo': 'SELL STOP',
                        #'Volume': '500',
                        #'Preço Ordem': 'R$ 65.00',
                        #'Preço Atual': 'R$ 66.20',
                        #'Diferença': '+1.85%',
                        #'Stop Loss': 'R$ 68.00',
                        #'Take Profit': 'R$ 62.00',
                        #'Tempo Setup': '1h ago',
                        #'Expira': '3 horas'
                    #}
                #]
                
                #df_ordens_demo = pd.DataFrame(ordens_demo)
                
                #def color_tipo_ordem(val):
                    #if 'BUY' in val:
                        #return 'background-color: rgba(0, 255, 0, 0.1)'
                    #elif 'SELL' in val:
                        #return 'background-color: rgba(255, 0, 0, 0.1)'
                    #return ''
                
                #def color_diferenca(val):
                    #if '+' in str(val):
                        #return 'color: green; font-weight: bold'
                    #elif '-' in str(val):
                        #return 'color: orange; font-weight: bold'
                    #return ''
                
                #st.dataframe(
                    #df_ordens_demo.style.applymap(color_tipo_ordem, subset=['Tipo'])
                                        #.applymap(color_diferenca, subset=['Diferença']),
                    #use_container_width=True,
                    #hide_index=True,
                    #height=250
                #)
        else:
            # Processa ordens pendentes reais do MT5
            ordens_formatted = []
            for ordem in ordens_pendentes:
                # Calcula tempo desde setup
                tempo_setup = ordem.get('time_setup', datetime.now())
                tempo_decorrido = datetime.now() - tempo_setup
                if tempo_decorrido.days > 0:
                    tempo_str = f"{tempo_decorrido.days}d ago"
                elif tempo_decorrido.seconds > 3600:
                    hours = tempo_decorrido.seconds // 3600
                    tempo_str = f"{hours}h ago"
                else:
                    minutes = tempo_decorrido.seconds // 60
                    tempo_str = f"{minutes}m ago"
                
                # Formata expiração
                expiracao = ordem.get('time_expiration')
                if expiracao:
                    exp_delta = expiracao - datetime.now()
                    if exp_delta.days > 0:
                        exp_str = f"{exp_delta.days} dias"
                    elif exp_delta.seconds > 3600:
                        exp_hours = exp_delta.seconds // 3600
                        exp_str = f"{exp_hours}h"
                    else:
                        exp_str = "< 1h"
                else:
                    exp_str = "GTC"
                
                diferenca_percent = ordem.get('diff_percent', 0)
                
                ordem_data = {
                    'Símbolo': ordem.get('symbol', 'N/A'),
                    'Tipo': ordem.get('type', 'N/A'),
                    'Volume': f"{ordem.get('volume', 0):,.0f}",
                    'Preço Ordem': f"R$ {ordem.get('price_open', 0):.2f}",
                    'Preço Atual': f"R$ {ordem.get('price_current', 0):.2f}",
                    'Diferença': f"{diferenca_percent:+.2f}%",
                    'Stop Loss': f"R$ {ordem.get('sl', 0):.2f}" if ordem.get('sl', 0) > 0 else 'N/A',
                    'Take Profit': f"R$ {ordem.get('tp', 0):.2f}" if ordem.get('tp', 0) > 0 else 'N/A',
                    'Tempo Setup': tempo_str,
                    'Expira': exp_str
                }
                ordens_formatted.append(ordem_data)
            
            if ordens_formatted:
                df_ordens_display = pd.DataFrame(ordens_formatted)
                
                def color_tipo_ordem(val):
                    if 'BUY' in val:
                        return 'background-color: rgba(0, 255, 0, 0.1)'
                    elif 'SELL' in val:
                        return 'background-color: rgba(255, 0, 0, 0.1)'
                    return ''
                
                def color_diferenca(val):
                    if '+' in str(val):
                        return 'color: green; font-weight: bold'
                    elif '-' in str(val):
                        return 'color: orange; font-weight: bold'
                    return ''
                
                st.dataframe(
                    df_ordens_display.style.applymap(color_tipo_ordem, subset=['Tipo'])
                                          .applymap(color_diferenca, subset=['Diferença']),
                    use_container_width=True,
                    hide_index=True,
                    height=350
                )
                
                # Métricas resumidas ordens
                col_o1, col_o2 = st.columns(2)
                with col_o1:
                    buy_orders = len([o for o in ordens_pendentes if 'BUY' in o.get('type', '')])
                    st.metric("Ordens Compra", buy_orders)
                with col_o2:
                    sell_orders = len([o for o in ordens_pendentes if 'SELL' in o.get('type', '')])
                    st.metric("Ordens Venda", sell_orders)
    
    # ==================================================================================
    # SEÇÃO DE MÉTRICAS GERAIS (ABAIXO DAS DUAS TABELAS)
    # ==================================================================================
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if posicoes:
            total_pl = sum([pos.get('profit', 0) for pos in posicoes])
            st.metric("💰 P&L Total Posições", f"R$ {total_pl:+.2f}")
        else:
            st.metric("💰 P&L Total Posições", "R$ 0,00")
    
    with col2:
        total_posicoes = len(posicoes)
        total_ordens = len(ordens_pendentes)
        st.metric("📊 Total Operações", f"{total_posicoes + total_ordens}")
    
    with col3:
        if posicoes:
            winners = len([p for p in posicoes if p.get('profit', 0) > 0])
            win_rate = (winners / len(posicoes) * 100) if posicoes else 0
            st.metric("📈 Taxa de Acerto", f"{win_rate:.1f}%")
        else:
            st.metric("📈 Taxa de Acerto", "0.0%")
    
    with col4:
        if posicoes:
            tempo_medio = sum([
                (datetime.now() - (datetime.fromtimestamp(p.get('time', 0)) if isinstance(p.get('time'), (int, float)) else datetime.now())).total_seconds() / 3600
                for p in posicoes
            ]) / len(posicoes) if posicoes else 0
            st.metric("⏱️ Tempo Médio", f"{tempo_medio:.1f}h")
        else:
            st.metric("⏱️ Tempo Médio", "0.0h")
    
    # ==================================================================================
    # BOTÕES DE AÇÃO RÁPIDA
    # ==================================================================================
    if sistema.mt5_connected and (posicoes or ordens_pendentes):
        st.markdown("---")
        st.markdown("**🎛️ Ações Rápidas:**")
        
        # Botões para fechar posições
        if posicoes:
            st.markdown("**Fechar Posições:**")
            cols_pos = st.columns(min(len(posicoes), 4))
            
            for i, (col, pos) in enumerate(zip(cols_pos, posicoes[:4])):
                with col:
                    symbol = pos.get('symbol', 'N/A')
                    if st.button(f"❌ {symbol}", key=f"close_pos_{pos.get('ticket', i)}"):
                        if sistema.fechar_posicao(pos.get('ticket')):
                            st.success(f"Posição {symbol} fechada!")
                            st.rerun()
        
        # Botões para cancelar ordens (se implementado)
        if ordens_pendentes:
            st.markdown("**Cancelar Ordens:**")
            cols_ord = st.columns(min(len(ordens_pendentes), 4))
            
            for i, (col, ordem) in enumerate(zip(cols_ord, ordens_pendentes[:4])):
                with col:
                    symbol = ordem.get('symbol', 'N/A')
                    ticket = ordem.get('ticket', i)
                    if st.button(f"🚫 {symbol}", key=f"cancel_order_{ticket}"):
                        st.info(f"Cancelamento de ordem {symbol} solicitado")
                        # Aqui você pode implementar a função para cancelar ordens
                        if sistema.cancelar_ordem(ticket):
                            st.success(f"Ordem {symbol} cancelada!")
                            st.rerun()
                    else:
                        st.error("Erro ao fechar posição")

def render_signals_table():
    """Renderiza tabela de sinais de trading - VERSÃO ULTRA-ESTÁVEL SEM MANIPULAÇÃO DOM"""
    
    try:
        sistema = st.session_state.trading_system
        
        # ========================================================================
        # HEADER SIMPLES E ESTÁTICO
        # ========================================================================
        #st.markdown("### 📡 Sinais de Trading Ativos")
        
        # Status em uma linha simples
        status_parts = []
        #if sistema.mt5_connected:
            #status_parts.append("✅ MT5")
        #else:
            #status_parts.append("❌ MT5")
            
        #if sistema.modo_otimizado:
            #status_parts.append("🚀 OTIMIZADO")
        #else:
            #status_parts.append("⚙️ BÁSICO")
            
        #st.markdown(f"**Status:** {' | '.join(status_parts)}")
        
        # ========================================================================
        # DEBUG CONTROLADO (SEM AUTO-EXPANSÃO)
        # ========================================================================
        
        # Chave única para debug para evitar conflitos
        debug_key = f"debug_signals_{id(sistema)}"
        
        if debug_key not in st.session_state:
            st.session_state[debug_key] = False
        
        # Botão de debug com chave única
        if st.button("🔍 Debug", key=f"btn_{debug_key}"):
            st.session_state[debug_key] = not st.session_state[debug_key]
        
        # Debug info só se solicitado
        if st.session_state[debug_key]:
            st.info(f"MT5: {sistema.mt5_connected} | Sistema: {sistema.running} | Modo: {sistema.modo_otimizado}")
            
            # Dados disponíveis
            sinais_count = len(sistema.sinais_ativos) if hasattr(sistema, 'sinais_ativos') and sistema.sinais_ativos else 0
            st.text(f"Sinais ativos: {sinais_count}")
            
            if sistema.modo_otimizado:
                dados_sync = sistema.obter_dados_sincronizados()
                if dados_sync:
                    st.text("Dados sincronizados: ✅")
                else:
                    st.text("Dados sincronizados: ❌")
        
        # ========================================================================
        # PROCESSAMENTO DE DADOS SIMPLES - PRIORIDADE ABSOLUTA PARA DADOS REAIS
        # ========================================================================
        
        dados_para_exibir = []
        fonte_info = ""
        dados_reais_encontrados = False
        
        # 1. PRIORIDADE MÁXIMA: Dados sincronizados primeiro (modo otimizado)
        if sistema.modo_otimizado:
            dados_sync = sistema.obter_dados_sincronizados()
            if dados_sync:
                sinais_sync = dados_sync.get('sinais_ativos')
                if sinais_sync and len(sinais_sync) > 0:
                    dados_para_exibir = sinais_sync
                    fonte_info = "Dados Sincronizados"
                    dados_reais_encontrados = True

        # 2. PRIORIDADE ALTA: Dados locais (usando propriedade de exibição)
        if not dados_reais_encontrados and not dados_para_exibir:
            if hasattr(sistema, 'sinais_ativos_exibicao') and sistema.sinais_ativos_exibicao:
                dados_para_exibir = sistema.sinais_ativos_exibicao
                fonte_info = "📱 Dados Locais"
                dados_reais_encontrados = True
                
        # 3. FALLBACK: sinais_ativos direto (se não houver exibição)
        if not dados_reais_encontrados and not dados_para_exibir:
            if hasattr(sistema, 'sinais_ativos') and sistema.sinais_ativos:
                dados_para_exibir = sistema.sinais_ativos
                fonte_info = "📊 Dados Sistema"
                dados_reais_encontrados = True
        
        # ========================================================================
        # RENDERIZAÇÃO SIMPLES E DIRETA - SEMPRE PRIORIZA DADOS REAIS
        # ========================================================================
        
        if dados_para_exibir and dados_reais_encontrados:
            st.success(f"✅ {len(dados_para_exibir)} sinais REAIS encontrados  {fonte_info}")
            
            # Converte para DataFrame simples
            try:
                if isinstance(dados_para_exibir, list) and len(dados_para_exibir) > 0:
                    # Processa sinais
                    sinais_processados = []
                    
                    for sinal in dados_para_exibir:
                        try:
                            par = sinal.get('par', 'N/A')
                            ativo = sinal.get('ativo', par.split('/')[0] if '/' in par else par)
                            zscore = sinal.get('zscore', sinal.get('Z-Score', 0))
                            r2 = sinal.get('r2', 0.7)
                            preco = sinal.get('preco_atual', 100.0)
                            tipo = sinal.get('sinal', 'NEUTRO')
                            confianca = sinal.get('confianca', 70)
                            segmento = sinal.get('segmento', 'Outros')
                            
                            # Calcula P&L estimado simples
                            if tipo == 'COMPRA':
                                pl_est = preco * 0.015
                                tipo_display = 'LONG'
                            elif tipo == 'VENDA':
                                pl_est = preco * 0.012
                                tipo_display = 'SHORT'
                            else:
                                pl_est = 0
                                tipo_display = 'NEUTRO'
                            
                            sinais_processados.append({
                                'Par': par,
                                'Ativo': ativo,
                                'Tipo': tipo_display,
                                'Z-Score': f"{zscore:.2f}",
                                'R²': f"{r2:.2f}",
                                'Preço': f"R$ {preco:.2f}",
                                'P&L Est.': f"R$ {pl_est:+.2f}",
                                'Confiança': f"{confianca:.0f}%",
                                'Segmento': segmento
                            })
                            
                        except Exception as e:
                            # Se houver erro em um sinal específico, pula para o próximo
                            continue
                    
                    if sinais_processados:
                        df_sinais = pd.DataFrame(sinais_processados)
                        
                        # Métricas resumidas simples
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            total_pl = sum([float(s['P&L Est.'].replace('R$ ', '').replace('+', '')) for s in sinais_processados])
                            st.metric("P&L Total", f"R$ {total_pl:+.2f}")
                        with col2:
                            st.metric("Sinais Ativos", len(sinais_processados))
                        with col3:
                            long_count = len([s for s in sinais_processados if s['Tipo'] == 'LONG'])
                            st.metric("LONG", long_count)
                        with col4:
                            short_count = len([s for s in sinais_processados if s['Tipo'] == 'SHORT'])
                            st.metric("SHORT", short_count)
                        
                        # Tabela simples sem styling complexo
                        st.dataframe(
                            df_sinais,
                            use_container_width=True,
                            hide_index=True,
                            height=400
                        )
                        
                        return  # Sai da função com sucesso
                    
            except Exception as e:
                st.error(f"Erro ao processar sinais: {str(e)}")
        
        # ========================================================================
        # FALLBACK FINAL
        # ========================================================================
        
        if sistema.mt5_connected:
            st.info("📡 Aguardando sinais... Execute o sistema para gerar análises.")
            
            # FALLBACK: Mostra dados de exemplo APENAS se MT5 conectado mas sem sinais
           #st.warning("🔍 **Nenhum sinal real encontrado** - Exibindo exemplo de interface")
            #st.markdown("### 📊 Exemplo: Como os Sinais Aparecem")
            #sinais_exemplo = [
                #{'Par': 'PETR4/VALE3', 'Ativo': 'PETR4', 'Tipo': 'LONG', 'Z-Score': '-2.15', 'R²': '0.78', 'Preço': 'R$ 28.50', 'P&L Est.': 'R$ +1.20', 'Confiança': '85%', 'Segmento': 'Petróleo'},
                #{'Par': 'ITUB4/BBDC4', 'Ativo': 'ITUB4', 'Tipo': 'SHORT', 'Z-Score': '2.03', 'R²': '0.82', 'Preço': 'R$ 24.80', 'P&L Est.': 'R$ +0.95', 'Confiança': '80%', 'Segmento': 'Bancos'},
                #{'Par': 'VALE3/BRAP4', 'Ativo': 'VALE3', 'Tipo': 'LONG', 'Z-Score': '-1.89', 'R²': '0.75', 'Preço': 'R$ 65.20', 'P&L Est.': 'R$ +2.10', 'Confiança': '78%', 'Segmento': 'Mineração'}
            #]
            
            #df_exemplo = pd.DataFrame(sinais_exemplo)
            
            # Métricas do exemplo
            #col1, col2, col3, col4 = st.columns(4)
            #with col1:
                #st.metric("P&L Total", "R$ +4.25", help="Exemplo - dados fictícios")
            #with col2:
                #st.metric("Sinais Ativos", "3", help="Exemplo - dados fictícios")
            #with col3:
                #st.metric("LONG", "2", help="Exemplo - dados fictícios")
            #with col4:
                #st.metric("SHORT", "1", help="Exemplo - dados fictícios")
            
            #st.dataframe(df_exemplo, use_container_width=True, hide_index=True, height=200)
            #st.error("⚠️ **ATENÇÃO: Dados de exemplo/demonstração** - Execute o sistema de análise para ver sinais reais")
        else:
            st.warning("🔌 Conecte ao MT5 para visualizar sinais reais")
        
        # Info box simples
        st.info("💡 **Sistema de Sinais:** Análise automática de pares com Z-Score, R² e filtros de qualidade")
    
    except Exception as e:
        st.error(f"❌ Erro na aba Sinais: {str(e)}")
        # Log do erro para debugging
        if hasattr(st.session_state, 'trading_system'):
            st.session_state.trading_system.log(f"❌ ERRO render_signals_table: {str(e)}")

def render_profit_distribution():
    """Renderiza distribuição de lucros/prejuízos com dados reais do MT5"""
    sistema = st.session_state.trading_system
    
    #st.markdown("### 📊 Resultado Acumulado por Dia")
    
    # Indicador de status da funcionalidade
    #col1, col2 = st.columns([3, 1])
    #with col1:
        #st.markdown("### 📊 Distribuição de Resultados por Trade")
    #with col2:
        #if sistema.mt5_connected:
            #st.markdown("✅ **online**", help="Dados de distribuição obtidos do histórico real de trades do MT5")
        #else:
            #st.markdown("🔴 **offline**", help="MT5 desconectado - usando dados de demonstração")
    
    # Busca dados reais se conectado ao MT5
    #st.write(f"🔍 Status MT5 conectado: {sistema.mt5_connected}")
    
    if sistema.mt5_connected:
        try:
            # Busca histórico dos últimos 30 dias
            data_inicio = datetime.now() - timedelta(days=30)
            data_fim = datetime.now()
            
            trades_reais = sistema.obter_historico_trades_real(data_inicio, data_fim)
            
            # Debug temporário
            #st.write(f"🔍 Trades encontrados: {len(trades_reais) if trades_reais else 0}")
            
            if trades_reais and len(trades_reais) > 0:
                # Extrai os lucros dos trades reais
                lucros_reais = [trade['Lucro'] for trade in trades_reais if 'Lucro' in trade]
                
                # Debug temporário
                #st.write(f"🔍 Lucros extraídos: {len(lucros_reais)}")
                
                if lucros_reais and len(lucros_reais) > 0:
                    # Cria o gráfico de barras - uma barra por dia
                    fig = go.Figure()
                    
                    # Agrupa trades por data
                    trades_por_dia = {}
                    for trade in trades_reais:
                        if 'Data' in trade and 'Lucro' in trade:
                            # Extrai apenas a data (sem hora)
                            data_trade = trade['Data'].date() if hasattr(trade['Data'], 'date') else trade['Data']
                            if data_trade not in trades_por_dia:
                                trades_por_dia[data_trade] = []
                            trades_por_dia[data_trade].append(trade['Lucro'])
                    
                    # Se não conseguir agrupar por data, usa agrupamento sequencial por período
                    if not trades_por_dia:
                        # Agrupa em períodos de até 5 trades por "dia"
                        trades_por_periodo = []
                        for i in range(0, len(lucros_reais), 5):
                            periodo_lucros = lucros_reais[i:i+5]
                            trades_por_periodo.append(sum(periodo_lucros))
                        
                        datas = [f"Período {i+1}" for i in range(len(trades_por_periodo))]
                        resultados_diarios = trades_por_periodo
                    else:
                        # Ordena por data e calcula resultado diário
                        datas_ordenadas = sorted(trades_por_dia.keys())
                        datas = [data.strftime('%d/%m') if hasattr(data, 'strftime') else str(data) for data in datas_ordenadas]
                        resultados_diarios = [sum(trades_por_dia[data]) for data in datas_ordenadas]
                    
                    # Separa cores: azul para dias lucrativos, vermelho para dias com prejuízo
                    cores = ['#2980b9' if resultado > 0 else '#e74c3c' for resultado in resultados_diarios]
                    
                    # Adiciona as barras
                    fig.add_trace(go.Bar(
                        x=datas,
                        y=resultados_diarios,
                        marker_color=cores,
                        name="Resultado Diário",
                        text=[f"R$ {resultado:+.2f}" for resultado in resultados_diarios],
                        textposition="outside",
                        textfont=dict(size=10),
                        hovertemplate='<b>%{x}</b><br>' +
                                      'Resultado do Dia: R$ %{y:+,.2f}<br>' +
                                      'Trades: %{customdata}<extra></extra>',
                        customdata=[len(trades_por_dia.get(data, [])) if trades_por_dia else 5 for data in (sorted(trades_por_dia.keys()) if trades_por_dia else range(len(resultados_diarios)))]
                    ))
                    
                    # Adiciona linha de referência no zero (break-even)
                    fig.add_hline(y=0, line_dash="dash", line_color="gray", 
                                  annotation_text="Break Even", annotation_position="top right")
                    
                    # Estatísticas dos dados reais
                    dias_lucrativos = len([r for r in resultados_diarios if r > 0])
                    dias_prejuizo = len([r for r in resultados_diarios if r < 0])
                    win_rate_diario = (dias_lucrativos / len(resultados_diarios)) * 100 if resultados_diarios else 0
                    
                    fig.update_layout(
                        title="📊 Resultado Acumulado por Dia",
                        xaxis_title=f"🔵 Gain: {dias_lucrativos}  |  🔴 Loss: {dias_prejuizo}",
                        yaxis_title="Resultado Diário (R$)",
                        height=400,
                        template="plotly_white",
                        showlegend=False,
                        # Configurações do eixo X
                        xaxis=dict(
                            title_font=dict(size=12, color='white'),
                            tickfont=dict(size=10),
                            tickangle=45  # Inclina as datas para melhor visualização
                        ),
                        # Configurações do eixo Y
                        yaxis=dict(
                            title_font=dict(size=12),
                            tickfont=dict(size=10),
                            zeroline=True,
                            zerolinecolor='gray',
                            zerolinewidth=2
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Exibe métricas resumidas
                    #col1, col2, col3, col4 = st.columns(4)
                    
                    #with col1:
                        #st.metric("🔵 Dias Lucrativos", dias_lucrativos)
                    
                    #with col2:
                        #st.metric("🔴 Dias com Prejuízo", dias_prejuizo)
                    
                    #with col3:
                        #st.metric("📊 Win Rate Diário", f"{win_rate_diario:.1f}%")
                    
                    #with col4:
                        #resultado_total = sum(resultados_diarios)
                        #st.metric("💰 Resultado Total", f"R$ {resultado_total:+,.2f}")
                    
                    #st.success(f"✅ Análise baseada em {len(lucros_reais)} trades dos últimos 30 dias agrupados por dia")
                    
                    # Não mostra dados demo quando há dados reais disponíveis
                    sistema._dados_reais_carregados = True
                    return
                else:
                    st.info("📊 Poucos trades reais encontrados para análise estatística")
            else:
                st.info("📊 Nenhum trade real encontrado nos últimos 30 dias")
                
        except Exception as e:
            sistema.log(f"❌ Erro ao buscar dados reais: {str(e)}")
            st.error(f"Erro ao buscar dados reais: {str(e)}")
    
    # FALLBACK: Apenas se não houver dados reais ou MT5 desconectado
    #if sistema.mt5_connected:
        #st.warning("🔍 **Nenhum histórico real encontrado** - Exibindo exemplo de interface")
        #st.markdown("### 📊 Exemplo: Como a Distribuição Aparece")
        #st.info("💡 Execute trades reais para ver a distribuição de resultados por período")
    #else:
        #st.error("🔌 **MT5 Desconectado** - Conecte ao MetaTrader 5 para visualizar distribuição real dos resultados")
    
        
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
            dt_inicio = datetime.combine(data_inicio, datetime_time.min)
            dt_fim = datetime.combine(data_fim, datetime_time.max)
            
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
                    
                    st.success(f"✅ {len(trades_reais)} trades REAIS exibidos com estatísticas completas")
                    return  # Sai da função - dados reais exibidos com sucesso
                else:
                    st.info(f"📊 Nenhum trade REAL encontrado no período com filtro '{filtro_resultado}'")
                    return
            else:
                st.info("📊 Nenhum trade REAL encontrado no período selecionado")
                return
                
        except Exception as e:
            sistema.log(f"❌ Erro ao buscar histórico real: {str(e)}")
            st.error(f"Erro ao buscar dados reais: {str(e)}")
    
    # FALLBACK: Apenas se não houver dados reais ou MT5 desconectado
    #if sistema.mt5_connected:
        #st.warning("� **Nenhum histórico real encontrado** - Exibindo exemplo de interface")
        #st.markdown("### 📊 Exemplo: Como o Histórico Aparece")
        #st.info("💡 Execute trades reais para ver o histórico detalhado com estatísticas")
    #else:
        #st.error("🔌 **MT5 Desconectado** - Conecte ao MetaTrader 5 para visualizar histórico real")
    
    # Usa trade_history_exibicao se disponível, senão simula
    #trades_simulados = sistema.trade_history_exibicao if hasattr(sistema, 'trade_history_exibicao') else []
    #if not trades_simulados:
        #np.random.seed(42)
        #for i in range(50):
            #resultado = np.random.normal(50, 200)
            #trades_simulados.append({
                #'Ticket': f"12345{i:02d}",
                #'Par': np.random.choice(['PETR4', 'VALE3', 'ITUB4', 'BBDC4']),
                #'Tipo': np.random.choice(['COMPRA', 'VENDA']),
                #'Data': (datetime.now() - timedelta(days=np.random.randint(1, 30))).strftime('%d/%m/%Y %H:%M'),
                #'Volume': round(np.random.uniform(100, 1000), 0),
                #'Preço': f"R$ {np.random.uniform(20, 100):.2f}",
                #'Lucro': f"R$ {resultado:.2f}",
                #'Comentário': 'Trade simulado'
            #})
    #df_trades = pd.DataFrame(trades_simulados)
    
    # Aplica filtros aos dados simulados
    #if filtro_resultado == "Lucro":
        #df_trades = df_trades[df_trades['Lucro'].str.replace('R$ ', '').str.replace(',', '').astype(float) > 0]
    #elif filtro_resultado == "Prejuízo":
        #df_trades = df_trades[df_trades['Lucro'].str.replace('R$ ', '').str.replace(',', '').astype(float) < 0]
    
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
    """Renderiza aba com dados detalhados da segunda seleção - VERSÃO ESTÁVEL"""
    
    try:
        sistema = st.session_state.trading_system
        
        # Inicializa controle de debug
        if 'debug_expanded_tab3' not in st.session_state:
            st.session_state.debug_expanded_tab3 = False
        
        # DEBUG controlado pelo usuário (evita auto-refresh que causa erros DOM)
        if st.button("🔍 Debug", key="btn_debug_tab3"):
            st.session_state.debug_expanded_tab3 = not st.session_state.debug_expanded_tab3
        
        if st.session_state.debug_expanded_tab3:
            st.write("**📊 Status do Sistema:**")
            modo_str = '🚀 OTIMIZADO' if sistema.modo_otimizado else '⚙️ BÁSICO'
            mt5_str = '✅' if sistema.mt5_connected else '❌'
            running_str = '✅' if sistema.running else '❌'
            
            st.write(f"- Modo: {modo_str}")
            st.write(f"- MT5: {mt5_str}")
            st.write(f"- Sistema: {running_str}")
            
            # Dados sincronizados (proteção contra mudanças rápidas)
            if sistema.modo_otimizado:
                dados_sync = sistema.obter_dados_sincronizados()
                if dados_sync:
                    timestamp_sync = dados_sync.get('timestamp_sync', datetime.min)
                    tempo_desde_sync = (datetime.now() - timestamp_sync).total_seconds()
                    st.write(f"- Sincronização: há {tempo_desde_sync:.1f}s")
                else:
                    st.write("- Sincronização: ❌ Indisponível")
            
            # Dados locais
            sinais_count = len(sistema.sinais_ativos) if hasattr(sistema, 'sinais_ativos') and sistema.sinais_ativos else 0
            st.write(f"- Sinais locais: {sinais_count}")
            
            if hasattr(sistema, 'tabela_linha_operacao01') and isinstance(sistema.tabela_linha_operacao01, pd.DataFrame):
                st.write(f"- 2ª Seleção: {len(sistema.tabela_linha_operacao01)} pares")
            else:
                st.write("- 2ª Seleção: ❌ Vazia")
        
        # RENDERIZAÇÃO PRINCIPAL DOS DADOS (simplificada e estável)
        df_segunda = None
        source_info = "📊 Processando dados..."
        dados_reais_encontrados = False
        
        # PRIORIDADE MÁXIMA: Dados sincronizados (modo otimizado)
        if sistema.modo_otimizado:
            dados_sincronizados = sistema.obter_dados_sincronizados()
            if dados_sincronizados:
                # Tenta tabela_linha_operacao01 sincronizada
                tabela_sync_01 = dados_sincronizados.get('tabela_linha_operacao01')
                if tabela_sync_01 is not None and not tabela_sync_01.empty:
                    df_segunda = tabela_sync_01.copy()
                    source_info = f"🚀 {len(df_segunda)} pares sincronizados (2ª seleção)"
                    dados_reais_encontrados = True
                
                # Fallback: sinais_ativos sincronizados convertidos
                elif dados_sincronizados.get('sinais_ativos'):
                    sinais_sync = dados_sincronizados.get('sinais_ativos')
                    sinais_data = []
                    for sinal in sinais_sync:
                        par_original = sinal.get('par', '')
                        if '/' in par_original:
                            dependente, independente = par_original.split('/')[:2]
                        else:
                            dependente, independente = par_original, 'INDEX'
                        
                        sinais_data.append({
                            'Dependente': dependente,
                            'Independente': independente,
                            'Z-Score': sinal.get('zscore', sinal.get('Z-Score', 0)),
                            'r2': sinal.get('r2', 0.7),
                            'preco_atual': sinal.get('preco_atual', 100),
                            'sinal': sinal.get('sinal', 'NEUTRO'),
                            'status': 'SINCRONIZADO'
                        })
                    
                    if sinais_data:
                        df_segunda = pd.DataFrame(sinais_data)
                        source_info = f" {len(df_segunda)} sinais sincronizados convertidos"
                        dados_reais_encontrados = True
        
        # PRIORIDADE ALTA: Dados locais (apenas se não houver dados reais sincronizados)
        if not dados_reais_encontrados and df_segunda is None:
            # sinais_ativos locais
            if hasattr(sistema, 'sinais_ativos') and sistema.sinais_ativos:
                sinais_data = []
                for sinal in sistema.sinais_ativos:
                    par_original = sinal.get('par', '')
                    if '/' in par_original:
                        dependente, independente = par_original.split('/')[:2]
                    else:
                        dependente, independente = par_original, 'INDEX'
                    
                    sinais_data.append({
                        'Dependente': dependente,
                        'Independente': independente,
                        'Z-Score': sinal.get('zscore', sinal.get('Z-Score', 0)),
                        'r2': sinal.get('r2', 0.7),
                        'preco_atual': sinal.get('preco_atual', 100),
                        'sinal': sinal.get('sinal', 'NEUTRO'),
                        'status': 'LOCAL'
                    })
                
                if sinais_data:
                    df_segunda = pd.DataFrame(sinais_data)
                    source_info = f"📱 {len(df_segunda)} sinais locais processados"
                    dados_reais_encontrados = True
            
            # tabela_linha_operacao01 local
            elif hasattr(sistema, 'tabela_linha_operacao01') and not sistema.tabela_linha_operacao01.empty:
                df_segunda = sistema.tabela_linha_operacao01.copy()
                source_info = f"📱 {len(df_segunda)} pares da 2ª seleção local"
                dados_reais_encontrados = True
            
            # Fallback: primeira seleção filtrada
            elif hasattr(sistema, 'tabela_linha_operacao') and not sistema.tabela_linha_operacao.empty:
                df_filtrada = sistema.tabela_linha_operacao[sistema.tabela_linha_operacao['Z-Score'].abs() >= 1.5]
                if not df_filtrada.empty:
                    df_segunda = df_filtrada.copy()
                    source_info = f"📊 {len(df_segunda)} pares filtrados (1ª seleção)"
                    dados_reais_encontrados = True
        
        # RENDERIZAÇÃO DOS RESULTADOS - PRIORIZA DADOS REAIS
        if df_segunda is not None and not df_segunda.empty and dados_reais_encontrados:
            if "🚀" in source_info:
                st.success(f"✅ {source_info} - DADOS REAIS")
            else:
                st.info(f"✅ {source_info} - DADOS REAIS")
            
            # Métricas resumidas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_pl = 0
                for _, row in df_segunda.iterrows():
                    zscore = row.get('Z-Score', 0)
                    preco = row.get('preco_atual', 100)
                    if zscore <= -1.5:
                        total_pl += preco * 0.015
                    elif zscore >= 1.5:
                        total_pl += preco * 0.012
                st.metric("P&L Estimado", f"R$ +{total_pl:.2f}")
            
            with col2:
                st.metric("Pares Analisados", len(df_segunda))
            
            with col3:
                r2_medio = df_segunda['r2'].mean() if 'r2' in df_segunda.columns else 0.65
                taxa_acerto = min(95, max(50, r2_medio * 100))
                st.metric("Confiança Média", f"{taxa_acerto:.1f}%")
            
            with col4:
                tempo_medio = "4h 30m" if len(df_segunda) <= 5 else "3h 15m"
                st.metric("Tempo Estimado", tempo_medio)
            
            # Tabela principal
            st.markdown("---")
            
            # Converte para formato de exibição
            dados_exibicao = []
            for i, (_, row) in enumerate(df_segunda.iterrows()):
                dep = row.get('Dependente', 'N/A')
                ind = row.get('Independente', 'N/A')
                zscore = row.get('Z-Score', 0)
                r2 = row.get('r2', 0)
                preco = row.get('preco_atual', 100 + i*10)
                
                tipo = 'LONG' if zscore <= -1.5 else 'SHORT' if zscore >= 1.5 else 'NEUTRO'
                pl_estimado = abs(zscore) * preco * 0.008 if tipo != 'NEUTRO' else preco * 0.001
                
                dados_exibicao.append({
                    'Par': f"{dep}/{ind}",
                    'Tipo': tipo,
                    'Z-Score': f"{zscore:.3f}",
                    'R²': f"{r2:.3f}",
                    'Preço': f"R$ {preco:.2f}",
                    'P&L Est.': f"R$ {pl_estimado:+.2f}",
                    'Setor': sistema.segmentos.get(dep, 'Outros'),
                    'Status': row.get('status', 'PROCESSADO')
                })
            
            if dados_exibicao:
                df_display = pd.DataFrame(dados_exibicao)
                
                # Filtros
                col_f1, col_f2, col_f3 = st.columns(3)
                with col_f1:
                    tipos = ['Todos'] + sorted(df_display['Tipo'].unique().tolist())
                    tipo_filter = st.selectbox("Tipo", tipos, key="tipo_filter_tab3")
                
                with col_f2:
                    setores = ['Todos'] + sorted(df_display['Setor'].unique().tolist())
                    setor_filter = st.selectbox("Setor", setores, key="setor_filter_tab3")
                
                with col_f3:
                    show_advanced = st.checkbox("Detalhes Avançados", True, key="advanced_tab3")
                
                # Aplica filtros
                df_filtered = df_display.copy()
                if tipo_filter != "Todos":
                    df_filtered = df_filtered[df_filtered['Tipo'] == tipo_filter]
                if setor_filter != "Todos":
                    df_filtered = df_filtered[df_filtered['Setor'] == setor_filter]
                
                # Exibe tabela
                st.dataframe(df_filtered, use_container_width=True, hide_index=True, height=400)
                
                # Análise adicional
                if show_advanced:
                    with st.expander("📊 Análise Detalhada"):
                        analise_col1, analise_col2 = st.columns(2)
                        
                        with analise_col1:
                            st.write("**Distribuição por Tipo:**")
                            tipo_dist = df_filtered['Tipo'].value_counts()
                            for tipo, count in tipo_dist.items():
                                st.write(f"- {tipo}: {count} pares")
                        
                        with analise_col2:
                            st.write("**Distribuição por Setor:**")
                            setor_dist = df_filtered['Setor'].value_counts()
                            for setor, count in setor_dist.items():
                                st.write(f"- {setor}: {count} pares")
        else:
            # Sem dados disponíveis
            st.warning("📡 Aguardando sinais... Execute o sistema para gerar análises.")
            st.info("💡 Execute a análise completa para gerar dados da segunda seleção")
            
            # FALLBACK: Mostra dados de exemplo APENAS quando não há dados reais
            #if sistema.mt5_connected:
                #st.warning("🔍 **Nenhum par validado encontrado** - Exibindo exemplo de interface")
                #st.markdown("### 📊 Exemplo: Como os Pares Validados Aparecem")
                #pares_exemplo = [
                    #{'Par': 'PETR4/VALE3', 'Tipo': 'LONG', 'Z-Score': '-2.150', 'R²': '0.785', 'Preço': 'R$ 28.50', 'P&L Est.': 'R$ +1.20', 'Setor': 'Petróleo', 'Status': 'VALIDADO'},
                    #{'Par': 'ITUB4/BBDC4', 'Tipo': 'SHORT', 'Z-Score': '2.030', 'R²': '0.820', 'Preço': 'R$ 24.80', 'P&L Est.': 'R$ +0.95', 'Setor': 'Bancos', 'Status': 'VALIDADO'},
                    #{'Par': 'VALE3/BRAP4', 'Tipo': 'LONG', 'Z-Score': '-1.890', 'R²': '0.750', 'Preço': 'R$ 65.20', 'P&L Est.': 'R$ +2.10', 'Setor': 'Mineração', 'Status': 'VALIDADO'},
                    #{'Par': 'BBAS3/ITSA4', 'Tipo': 'SHORT', 'Z-Score': '1.780', 'R²': '0.765', 'Preço': 'R$ 45.60', 'P&L Est.': 'R$ +1.85', 'Setor': 'Bancos', 'Status': 'VALIDADO'},
                    #{'Par': 'WEGE3/RAIA3', 'Tipo': 'LONG', 'Z-Score': '-2.200', 'R²': '0.810', 'Preço': 'R$ 52.30', 'P&L Est.': 'R$ +2.50', 'Setor': 'Indústria', 'Status': 'VALIDADO'}
                #]
                
                #df_exemplo = pd.DataFrame(pares_exemplo)
                
                # Métricas do exemplo
                #col1, col2, col3, col4 = st.columns(4)
                #with col1:
                    #st.metric("P&L Estimado", "R$ +8.60", help="Exemplo - dados fictícios")
                #with col2:
                    #st.metric("Pares Analisados", "5", help="Exemplo - dados fictícios")
                #with col3:
                    #st.metric("Confiança Média", "78.2%", help="Exemplo - dados fictícios")
                #with col4:
                    #st.metric("Tempo Estimado", "3h 45m", help="Exemplo - dados fictícios")
                
                #st.markdown("---")
                #st.dataframe(df_exemplo, use_container_width=True, hide_index=True, height=300)
                #st.error("⚠️ **ATENÇÃO: Dados de exemplo/demonstração** - Execute o sistema de análise para ver pares reais")
            #else:
                #st.error("🔌 **MT5 Desconectado** - Conecte ao MetaTrader 5 para análise de pares")
            
            with st.expander("ℹ️ Sobre a Segunda Seleção"):
                st.markdown("""
                **🎯 O que é a Segunda Seleção?**
                
                A segunda seleção é um processo de refinamento que:
                
                1. **🔍 Analisa os melhores pares** da primeira seleção
                2. **📊 Aplica análise detalhada** com filtros rigorosos
                3. **💰 Calcula preços de entrada otimizados**
                4. **⚡ Prioriza por viabilidade de execução**
                
                **🔧 Para ativar:** Inicie o sistema de análise real no painel principal.
                """)
    
    except Exception as e:
        st.error(f"❌ Erro na aba Pares Validados: {str(e)}")
        st.info("💡 Tente recarregar a página ou reiniciar o sistema")

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
    tab1, tab3, tab2, tab4, tab5, tab0 = st.tabs([
        "📊 Gráficos e Análises", 
        "🎯 Pares Validados", 
        "📡 Sinais e Posições", 
        "📋 Históricos", 
        "📝 Log de Eventos",
        "🏠 Sistema"
    ])
    
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
    
    with tab0:
        # PAINEL DE MONITORAMENTO DE THREADS DO SISTEMA INTEGRADO
        st.session_state.trading_system.render_thread_monitor_panel()
    
    # Auto-refresh CONTROLADO - Remove loop infinito
    sistema = st.session_state.trading_system
    
    # Controle de refresh com session_state para evitar loops
    if 'last_refresh_attempt' not in st.session_state:
        st.session_state.last_refresh_attempt = datetime.min
        st.session_state.refresh_count = 0
    
    # Limita tentativas de refresh (máximo 3 por sessão)
    if st.session_state.refresh_count < 3:
        tempo_desde_ultimo = (datetime.now() - st.session_state.last_refresh_attempt).total_seconds()
        
        should_refresh = False
        
        if sistema.running and tempo_desde_ultimo >= 30:
            # Sistema rodando: refresh a cada 30 segundos
            should_refresh = True
            refresh_reason = "Sistema ativo"
        elif sistema.mt5_connected and tempo_desde_ultimo >= 60:
            # MT5 conectado: refresh a cada 60 segundos
            should_refresh = True
            refresh_reason = "Atualização MT5"
        
        if should_refresh:
            st.session_state.last_refresh_attempt = datetime.now()
            st.session_state.refresh_count += 1
            
            # REMOVE o time.sleep() e usa apenas st.rerun()
            st.rerun()
    else:
        # Após 5 tentativas, para o auto-refresh e informa ao usuário
        if st.session_state.refresh_count == 5:
            st.sidebar.warning("⚠️ Auto-refresh pausado. Recarregue a página se necessário.")
            st.session_state.refresh_count = 6  # Evita mostrar a mensagem repetidamente

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
        profit_atual = account_info.profit
        
        # ✅ CORREÇÃO: Usa o mesmo cálculo correto do saldo inicial
        # Aplica a mesma lógica que já funciona no lucro diário
        balance_inicial = sistema.calcular_saldo_inicial_do_dia()
        
        # Equity inicial também deve ser baseado no saldo inicial correto
        equity_inicial = balance_inicial
        
        sistema.log(f"📊 GRÁFICO EQUITY - Saldo inicial correto: R$ {balance_inicial:,.2f}")
        sistema.log(f"📊 GRÁFICO EQUITY - Balance atual: R$ {balance_atual:,.2f}")
        
        # Cria pontos da curva corrigidos
        equity_historico.append({
            'timestamp': data_inicio,
            'equity': equity_inicial,
            'balance': balance_inicial,
            'profit': 0.0
        })
        
        # ✅ CORREÇÃO: Reconstroi curva baseada nos deals fechados com saldo inicial correto
        lucro_acumulado_realizado = 0
        deals_validos = [deal for deal in deals if hasattr(deal, 'profit') and deal.profit != 0]
        
        sistema.log(f"📊 GRÁFICO EQUITY - Processando {len(deals_validos)} deals")
        
        for deal in sorted(deals_validos, key=lambda x: x.time):
            lucro_acumulado_realizado += deal.profit
            # Balance progride a partir do saldo inicial correto
            balance_no_momento = balance_inicial + lucro_acumulado_realizado
            
            equity_historico.append({
                'timestamp': datetime.fromtimestamp(deal.time),
                'equity': balance_no_momento,  # Equity = Balance quando deal é fechado
                'balance': balance_no_momento,  # Balance reflete operações fechadas
                'profit': 0.0  # Profit zerado após fechamento do trade
            })
        
        # ✅ CORREÇÃO: Ponto atual com equity e balance distintos (se houver posições abertas)
        equity_historico.append({
            'timestamp': datetime.now(),
            'equity': equity_atual,
            'balance': balance_atual,
            'profit': profit_atual
        })
        
        sistema.log(f"📊 GRÁFICO EQUITY - {len(equity_historico)} pontos gerados")
        
        return equity_historico
        
    except Exception as e:
        sistema.log(f"❌ Erro ao obter histórico de equity do MT5: {str(e)}")
        return []

if __name__ == "__main__":
    main()
