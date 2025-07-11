#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Inicialização do Dashboard
"""

import streamlit as st

def test_basic_dashboard():
    """Testa se o dashboard básico funciona"""
    
    st.title("🧪 Teste de Inicialização")
    st.write("Se você está vendo essa mensagem, o Streamlit está funcionando!")
    
    # Teste de imports críticos
    try:
        import pandas as pd
        st.success("✅ Pandas importado com sucesso")
    except Exception as e:
        st.error(f"❌ Erro ao importar pandas: {e}")
    
    try:
        import plotly.graph_objects as go
        st.success("✅ Plotly importado com sucesso")
    except Exception as e:
        st.error(f"❌ Erro ao importar plotly: {e}")
    
    try:
        import MetaTrader5 as mt5
        st.success("✅ MetaTrader5 importado com sucesso")
    except Exception as e:
        st.error(f"❌ Erro ao importar MT5: {e}")
    
    # Teste de importação do dashboard principal
    try:
        from dashboard_trading_pro_real import TradingSystemReal, render_header
        st.success("✅ Dashboard principal importado com sucesso")
        
        # Testa criação do sistema
        sistema = TradingSystemReal()
        st.success("✅ TradingSystemReal criado com sucesso")
        
        # Testa render do header
        st.markdown("---")
        st.markdown("### Teste do Header:")
        render_header()
        
    except Exception as e:
        st.error(f"❌ Erro ao importar dashboard: {e}")
        st.code(str(e))

if __name__ == "__main__":
    test_basic_dashboard()
