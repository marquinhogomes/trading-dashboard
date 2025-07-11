import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Teste Header", 
    page_icon="📊",
    layout="wide"
)

# Teste apenas do header
st.markdown("""
<div style="background: #0d1117; padding: 2rem; border-radius: 12px; margin-bottom: 1.5rem;">
    <h1 style="color: #ffd700; margin: 0;">📊 Trading Quantitativo</h1>
    <h2 style="color: #8b949e; margin: 0; font-size: 1rem;">Dashboard de Operações</h2>
    <p style="color: #8b949e;">Última Atualização: {}</p>
</div>
""".format(datetime.now().strftime('%d/%m/%Y %H:%M:%S')), unsafe_allow_html=True)

# Teste de métricas simples
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Ativos", "25", delta="5")

with col2:
    st.metric("Posições", "3", delta="1")

with col3:
    st.metric("Equity", "USD 125,000", delta="2.3%")

with col4:
    st.metric("P&L", "USD +2,300", delta="1.8%")

st.write("✅ Se você está vendo os cards acima, o problema está em outra parte do código!")
