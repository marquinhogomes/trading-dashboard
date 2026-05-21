import streamlit as st
import sys
import os

# Adicionar o diretório atual ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar o dashboard principal.
# Observação: dashboard_trading_pro_real.py já executa st.set_page_config().
# Por isso, o app.py não deve chamar st.set_page_config novamente.
from dashboard_trading_pro_real import main


def adicionar_atalho_figurinhas():
    """Adiciona um atalho explícito para a página de figurinhas no menu lateral."""
    try:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### ⚽ Álbum Copa 2026")
        st.sidebar.page_link(
            "pages/Controle_Figurinhas_Copa_2026.py",
            label="Abrir Controle de Figurinhas",
            icon="⚽",
        )
    except Exception:
        # Fallback para versões/ambientes onde st.page_link não esteja disponível.
        st.sidebar.markdown("---")
        st.sidebar.markdown("### ⚽ Álbum Copa 2026")
        st.sidebar.info("Use o menu lateral do Streamlit e abra: Controle_Figurinhas_Copa_2026")


if __name__ == "__main__":
    adicionar_atalho_figurinhas()
    main()
