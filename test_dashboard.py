#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples para verificar se o dashboard está funcionando
"""

import sys
import os

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("🔍 Verificando imports...")
    
    # Testar imports básicos
    import streamlit as st
    print("✅ Streamlit OK")
    
    import pandas as pd
    print("✅ Pandas OK")
    
    import plotly.graph_objects as go
    print("✅ Plotly OK")
    
    # Testar import do dashboard
    import trading_dashboard_fixed
    print("✅ Dashboard importado com sucesso!")
    
    print("\n🎯 Tudo pronto! O dashboard pode ser executado.")
    print("📋 Para iniciar, execute:")
    print("   streamlit run trading_dashboard_fixed.py")
    
except ImportError as e:
    print(f"❌ Erro de import: {e}")
    print("🔧 Instale as dependências com: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
