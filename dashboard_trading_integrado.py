#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard Trading Integrado - Unificação dos Três Sistemas
Integra: sistema_integrado.py + dashboard_trading_pro_real.py + calculo_entradas_v55.py
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

# Import do sistema integrado
try:
    from sistema_integrado import SistemaIntegrado
    SISTEMA_INTEGRADO_DISPONIVEL = True
except ImportError:
    SISTEMA_INTEGRADO_DISPONIVEL = False
    print("⚠️ Sistema integrado não disponível")

# Imports do sistema original
import sys
sys.path.append('.')

# Configuração da página
st.set_page_config(
    page_title="Trading Dashboard Integrado - Sistema Completo",
    page_icon="🎯",
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
    
    .thread-status {
        background: #ecf0f1;
        padding: 0.5rem;
        border-radius: 6px;
        margin: 0.2rem 0;
        border-left: 3px solid #3498db;
    }
    
    .log-container {
        background: #2c3e50;
        color: #ecf0f1;
        padding: 1rem;
        border-radius: 8px;
        height: 400px;
        overflow-y: auto;
        font-family: 'Courier New', monospace;
        font-size: 0.8rem;
    }
    
    .integration-badge {
        background: linear-gradient(45deg, #e74c3c, #f39c12);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class DashboardTradingIntegrado:
    """Dashboard integrado que unifica todos os sistemas"""
    
    def __init__(self):
        # Sistema integrado principal
        if SISTEMA_INTEGRADO_DISPONIVEL:
            self.sistema_principal = SistemaIntegrado()
            self.integracao_ativa = True
        else:
            self.sistema_principal = None
            self.integracao_ativa = False
        
        # Dados compartilhados entre todos os sistemas
        self.dados_unificados = {
            "sistema_integrado_rodando": False,
            "dashboard_ativo": True,
            "threads_status": {},
            "ultima_sincronizacao": None,
            "posicoes_unificadas": [],
            "equity_historico": [],
            "logs_unificados": [],
            "mt5_conectado": False
        }
        
        # Configurações do sistema original (herdadas)
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
        
    def log_unificado(self, mensagem: str, origem: str = "Dashboard"):
        """Sistema de log unificado para todos os componentes"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        evento = f"[{timestamp}] [{origem}] {mensagem}"
        self.dados_unificados["logs_unificados"].append(evento)
        print(evento)
        
        # Mantém apenas os últimos 1000 logs para performance
        if len(self.dados_unificados["logs_unificados"]) > 1000:
            self.dados_unificados["logs_unificados"] = self.dados_unificados["logs_unificados"][-1000:]
    
    def conectar_mt5(self) -> bool:
        """Conecta ao MT5 de forma unificada"""
        try:
            if not mt5.initialize():
                self.log_unificado("❌ Falha ao inicializar MT5", "MT5")
                return False
            
            # Verifica informações da conta
            account_info = mt5.account_info()
            if account_info is None:
                self.log_unificado("❌ Falha ao obter informações da conta", "MT5")
                return False
            
            self.dados_unificados["mt5_conectado"] = True
            self.log_unificado(f"✅ MT5 conectado - Conta: {account_info.login}", "MT5")
            return True
            
        except Exception as e:
            self.log_unificado(f"❌ Erro na conexão MT5: {str(e)}", "MT5")
            self.dados_unificados["mt5_conectado"] = False
            return False
    
    def iniciar_sistema_integrado(self):
        """Inicia o sistema integrado completo"""
        if not self.integracao_ativa:
            self.log_unificado("❌ Sistema integrado não disponível", "Sistema")
            return False
        
        if self.dados_unificados["sistema_integrado_rodando"]:
            self.log_unificado("⚠️ Sistema integrado já está rodando", "Sistema")
            return False
        
        try:
            # Inicia o sistema integrado em thread separada
            thread_sistema = threading.Thread(
                target=self._executar_sistema_integrado,
                daemon=True,
                name="SistemaIntegrado"
            )
            thread_sistema.start()
            
            self.dados_unificados["sistema_integrado_rodando"] = True
            self.log_unificado("✅ Sistema integrado iniciado com sucesso", "Sistema")
            return True
            
        except Exception as e:
            self.log_unificado(f"❌ Erro ao iniciar sistema integrado: {str(e)}", "Sistema")
            return False
    
    def _executar_sistema_integrado(self):
        """Executa o sistema integrado em thread dedicada"""
        try:
            self.log_unificado("🚀 Iniciando sistema integrado completo...", "Sistema")
            self.sistema_principal.iniciar_sistema()
        except Exception as e:
            self.log_unificado(f"❌ Erro na execução do sistema integrado: {str(e)}", "Sistema")
            self.dados_unificados["sistema_integrado_rodando"] = False
    
    def parar_sistema_integrado(self):
        """Para o sistema integrado"""
        if not self.integracao_ativa or not self.dados_unificados["sistema_integrado_rodando"]:
            return False
        
        try:
            self.sistema_principal.parar_sistema()
            self.dados_unificados["sistema_integrado_rodando"] = False
            self.log_unificado("🛑 Sistema integrado parado", "Sistema")
            return True
        except Exception as e:
            self.log_unificado(f"❌ Erro ao parar sistema integrado: {str(e)}", "Sistema")
            return False
    
    def obter_status_threads(self) -> Dict:
        """Obtém status detalhado de todas as threads"""
        if not self.integracao_ativa or not self.dados_unificados["sistema_integrado_rodando"]:
            return {"erro": "Sistema não disponível"}
        
        try:
            # Obtém informações das threads do sistema integrado
            threads_ativas = []
            for thread in threading.enumerate():
                if thread.name in ["SistemaTrading", "Monitoramento", "MonitoramentoPosicoes", 
                                 "BreakEvenContinuo", "AjustesProgramados"]:
                    threads_ativas.append({
                        "nome": thread.name,
                        "ativo": thread.is_alive(),
                        "daemon": thread.daemon
                    })
            
            return {
                "threads_sistema": threads_ativas,
                "total_threads": len(threads_ativas),
                "sistema_principal_rodando": self.dados_unificados["sistema_integrado_rodando"]
            }
        except Exception as e:
            return {"erro": str(e)}
    
    def obter_posicoes_unificadas(self) -> List[Dict]:
        """Obtém posições de forma unificada"""
        if not self.dados_unificados["mt5_conectado"]:
            return []
        
        try:
            posicoes = mt5.positions_get()
            if not posicoes:
                return []
            
            posicoes_formatadas = []
            for pos in posicoes:
                posicoes_formatadas.append({
                    'ticket': pos.ticket,
                    'symbol': pos.symbol,
                    'type': 'Compra' if pos.type == 0 else 'Venda',
                    'volume': pos.volume,
                    'price_open': pos.price_open,
                    'price_current': pos.price_current,
                    'profit': pos.profit,
                    'magic': pos.magic,
                    'time': datetime.fromtimestamp(pos.time)
                })
            
            self.dados_unificados["posicoes_unificadas"] = posicoes_formatadas
            return posicoes_formatadas
            
        except Exception as e:
            self.log_unificado(f"❌ Erro ao obter posições: {str(e)}", "MT5")
            return []
    
    def sincronizar_logs(self):
        """Sincroniza logs do sistema integrado com o dashboard"""
        if self.integracao_ativa and self.sistema_principal:
            try:
                # Obtém logs do sistema integrado
                logs_sistema = getattr(self.sistema_principal, 'logs', [])
                
                # Adiciona aos logs unificados se houver novos
                for log in logs_sistema[-10:]:  # Últimos 10 logs
                    if log not in [l for l in self.dados_unificados["logs_unificados"] if "[Sistema]" in l]:
                        self.dados_unificados["logs_unificados"].append(log.replace("[", "[Sistema] ["))
                
                self.dados_unificados["ultima_sincronizacao"] = datetime.now()
                
            except Exception as e:
                self.log_unificado(f"❌ Erro na sincronização de logs: {str(e)}", "Sync")

# Inicializa sistema global unificado
if 'dashboard_integrado' not in st.session_state:
    st.session_state.dashboard_integrado = DashboardTradingIntegrado()

def render_header():
    """Renderiza header principal integrado"""
    
    st.markdown('<div class="integration-badge">🎯 SISTEMA TOTALMENTE INTEGRADO</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    dashboard = st.session_state.dashboard_integrado
    
    with col1:
        if dashboard.integracao_ativa:
            status_integracao = "✅ INTEGRADO"
            color = "🟢"
        else:
            status_integracao = "❌ NÃO INTEGRADO"
            color = "🔴"
        
        st.markdown(f"""
        **🔗 Status de Integração**
        **{color} {status_integracao}**
        """)
    
    with col2:
        mt5_status = "CONECTADO" if dashboard.dados_unificados["mt5_conectado"] else "DESCONECTADO"
        color_mt5 = "🟢" if dashboard.dados_unificados["mt5_conectado"] else "🔴"
        st.markdown(f"""
        **📡 MetaTrader 5**
        **{color_mt5} {mt5_status}**
        """)
    
    with col3:
        sistema_status = "RODANDO" if dashboard.dados_unificados["sistema_integrado_rodando"] else "PARADO"
        color_sistema = "🟢" if dashboard.dados_unificados["sistema_integrado_rodando"] else "🔴"
        st.markdown(f"""
        **🚀 Sistema Integrado**
        **{color_sistema} {sistema_status}**
        """)
    
    with col4:
        posicoes_count = len(dashboard.dados_unificados["posicoes_unificadas"])
        st.markdown(f"""
        **📊 Posições Ativas**
        **📈 {posicoes_count} posições**
        """)
    
    st.markdown("---")

def render_controles_integrados():
    """Renderiza controles unificados do sistema"""
    
    st.markdown("## 🎮 Controles do Sistema Integrado")
    
    dashboard = st.session_state.dashboard_integrado
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔌 Conectar MT5", disabled=dashboard.dados_unificados["mt5_conectado"]):
            if dashboard.conectar_mt5():
                st.success("✅ MT5 conectado com sucesso!")
                st.rerun()
            else:
                st.error("❌ Falha na conexão MT5")
    
    with col2:
        if dashboard.integracao_ativa:
            if not dashboard.dados_unificados["sistema_integrado_rodando"]:
                if st.button("🚀 Iniciar Sistema Completo"):
                    if dashboard.iniciar_sistema_integrado():
                        st.success("✅ Sistema integrado iniciado!")
                        st.rerun()
                    else:
                        st.error("❌ Falha ao iniciar sistema")
            else:
                if st.button("🛑 Parar Sistema"):
                    if dashboard.parar_sistema_integrado():
                        st.success("🛑 Sistema parado")
                        st.rerun()
        else:
            st.button("❌ Sistema Não Disponível", disabled=True)
    
    with col3:
        if st.button("🔄 Sincronizar Dados"):
            dashboard.sincronizar_logs()
            dashboard.obter_posicoes_unificadas()
            st.success("✅ Dados sincronizados!")

def render_status_threads():
    """Renderiza status detalhado das threads"""
    
    st.markdown("## 🧵 Status das Threads")
    
    dashboard = st.session_state.dashboard_integrado
    status_threads = dashboard.obter_status_threads()
    
    if "erro" in status_threads:
        st.warning(f"⚠️ {status_threads['erro']}")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total de Threads", status_threads.get("total_threads", 0))
    
    with col2:
        sistema_ativo = status_threads.get("sistema_principal_rodando", False)
        status_cor = "🟢" if sistema_ativo else "🔴"
        st.metric("Sistema Principal", f"{status_cor} {'Ativo' if sistema_ativo else 'Inativo'}")
    
    # Detalhes das threads
    threads_info = status_threads.get("threads_sistema", [])
    if threads_info:
        st.markdown("### 📋 Detalhes das Threads:")
        
        for thread in threads_info:
            status_icon = "🟢" if thread["ativo"] else "🔴"
            daemon_info = "(Daemon)" if thread["daemon"] else ""
            
            st.markdown(f"""
            <div class="thread-status">
                <strong>{status_icon} {thread['nome']}</strong> {daemon_info}
                <br><small>Status: {'Ativo' if thread['ativo'] else 'Inativo'}</small>
            </div>
            """, unsafe_allow_html=True)

def render_posicoes_unificadas():
    """Renderiza tabela de posições unificada"""
    
    st.markdown("## 📊 Posições Unificadas")
    
    dashboard = st.session_state.dashboard_integrado
    posicoes = dashboard.obter_posicoes_unificadas()
    
    if not posicoes:
        st.info("📋 Nenhuma posição aberta no momento")
        return
    
    df_posicoes = pd.DataFrame(posicoes)
    
    # Formatação da tabela
    df_display = df_posicoes.copy()
    df_display['Lucro/Prejuízo'] = df_display['profit'].apply(
        lambda x: f"{'🟢' if x >= 0 else '🔴'} R$ {x:.2f}"
    )
    
    # Colunas para exibição
    colunas_exibir = ['ticket', 'symbol', 'type', 'volume', 'price_open', 
                     'price_current', 'Lucro/Prejuízo', 'magic']
    
    st.dataframe(df_display[colunas_exibir], use_container_width=True)
    
    # Métricas resumo
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Posições", len(posicoes))
    
    with col2:
        lucro_total = sum([p['profit'] for p in posicoes])
        st.metric("P&L Total", f"R$ {lucro_total:.2f}")
    
    with col3:
        posicoes_positivas = len([p for p in posicoes if p['profit'] > 0])
        st.metric("Posições Positivas", posicoes_positivas)
    
    with col4:
        posicoes_negativas = len([p for p in posicoes if p['profit'] < 0])
        st.metric("Posições Negativas", posicoes_negativas)

def render_logs_unificados():
    """Renderiza logs unificados de todos os sistemas"""
    
    st.markdown("## 📝 Logs Unificados")
    
    dashboard = st.session_state.dashboard_integrado
    logs = dashboard.dados_unificados["logs_unificados"]
    
    if not logs:
        st.info("📋 Nenhum log disponível")
        return
    
    # Exibe os últimos 50 logs
    logs_recentes = logs[-50:] if len(logs) > 50 else logs
    logs_text = "\n".join(reversed(logs_recentes))
    
    st.markdown(f"""
    <div class="log-container">
        <pre>{logs_text}</pre>
    </div>
    """, unsafe_allow_html=True)
    
    # Botão para limpar logs
    if st.button("🗑️ Limpar Logs"):
        dashboard.dados_unificados["logs_unificados"] = []
        st.rerun()

def main():
    """Função principal do dashboard integrado"""
    
    st.title("🎯 Dashboard Trading Integrado")
    st.markdown("**Sistema completo unificando: sistema_integrado.py + dashboard_trading_pro_real.py + calculo_entradas_v55.py**")
    
    # Header com status
    render_header()
    
    # Abas do sistema
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎮 Controles", 
        "🧵 Threads", 
        "📊 Posições", 
        "📝 Logs", 
        "📋 Relatórios"
    ])
    
    with tab1:
        render_controles_integrados()
    
    with tab2:
        render_status_threads()
    
    with tab3:
        render_posicoes_unificadas()
    
    with tab4:
        render_logs_unificados()
    
    with tab5:
        st.markdown("## 📋 Relatórios")
        st.info("🚧 Seção de relatórios em desenvolvimento...")
        
        dashboard = st.session_state.dashboard_integrado
        
        if dashboard.dados_unificados["ultima_sincronizacao"]:
            st.success(f"✅ Última sincronização: {dashboard.dados_unificados['ultima_sincronizacao'].strftime('%H:%M:%S')}")
        
        # Informações de integração
        st.markdown("### 🔗 Status de Integração")
        
        if dashboard.integracao_ativa:
            st.success("✅ Integração total ativa - Todos os sistemas funcionando harmoniosamente")
            
            if dashboard.sistema_principal:
                st.markdown("**Funcionalidades integradas:**")
                st.markdown("""
                - ✅ Sistema de trading principal (calculo_entradas_v55.py)
                - ✅ Monitoramento de posições em tempo real
                - ✅ Break-even contínuo durante pregão
                - ✅ Ajustes programados (15:10h, 15:20h, 16:01h)
                - ✅ Gestão automática de Stop Loss e Take Profit
                - ✅ Remoção automática de ordens pendentes
                - ✅ Dashboard visual em tempo real
                """)
        else:
            st.error("❌ Integração não disponível - Execute com o sistema_integrado.py disponível")

if __name__ == "__main__":
    main()
