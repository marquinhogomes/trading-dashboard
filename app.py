import streamlit as st
import sys
import os

# Adicionar o diretório atual ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar o dashboard principal
from dashboard_trading_pro_real import main

if __name__ == "__main__":
    # Configurar a página
    st.set_page_config(
        page_title="Trading Dashboard",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Executar o dashboard
    main()
