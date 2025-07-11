#!/usr/bin/env python3
"""
Script para testar apenas a função de gráfico de resultado acumulado
"""

import streamlit as st
import sys
import os

# Adiciona o diretório atual ao path para importar o dashboard
sys.path.append(os.getcwd())

# Configura página
st.set_page_config(
    page_title="Debug - Gráfico Resultado", 
    page_icon="🔍",
    layout="wide"
)

# Importa e inicializa o sistema
from dashboard_trading_pro_real import TradingSystemReal, render_profit_distribution

# Inicializa sistema na sessão se não existir
if 'trading_system' not in st.session_state:
    st.session_state.trading_system = TradingSystemReal()

st.title("🔍 Debug - Gráfico de Resultado Acumulado por Dia")

# Status da conexão MT5
sistema = st.session_state.trading_system

col1, col2 = st.columns(2)
with col1:
    if st.button("🔌 Conectar MT5"):
        if sistema.conectar_mt5():
            st.success("✅ MT5 conectado com sucesso!")
            st.rerun()
        else:
            st.error("❌ Falha ao conectar MT5")

with col2:
    status = "✅ Conectado" if sistema.mt5_connected else "❌ Desconectado"
    st.write(f"**Status MT5:** {status}")

st.markdown("---")

# Testa a função do gráfico
st.markdown("## 📊 Teste da Função de Gráfico")

try:
    render_profit_distribution()
except Exception as e:
    st.error(f"❌ Erro na função render_profit_distribution: {str(e)}")
    st.exception(e)
