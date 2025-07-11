#!/usr/bin/env python3
"""
Dashboard Simplificado para Teste - Sem Auto Import
"""
import streamlit as st

# Configuração básica
st.set_page_config(
    page_title="Trading System Real - Teste",
    page_icon="📈", 
    layout="wide"
)

st.title("🎯 Sistema de Trading Real - Teste de Funcionamento")

try:
    # Teste 1: Configurações
    st.subheader("1. 📊 Configurações Reais")
    from config_real import DEPENDENTE_REAL, INDEPENDENTE_REAL, get_setores_disponiveis
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Ativos Dependentes", len(DEPENDENTE_REAL))
    with col2:
        st.metric("Ativos Independentes", len(INDEPENDENTE_REAL))
    with col3:
        st.metric("Setores", len(get_setores_disponiveis()))
    
    st.success("✅ Configurações reais carregadas com sucesso!")
    
    # Teste 2: Mostrar alguns ativos
    st.subheader("2. 📋 Ativos Configurados")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Dependentes (primeiros 10):**")
        st.write(DEPENDENTE_REAL[:10])
    
    with col2:
        st.write("**Independentes (primeiros 10):**")
        st.write(INDEPENDENTE_REAL[:10])
      # Teste 3: Módulo de integração (MANUAL)
    st.subheader("3. 🔧 Sistema de Integração")
    
    if st.button("🧪 Testar Módulo de Integração"):
        try:
            # Debug REAL_CONFIG primeiro
            st.write("**Debug REAL_CONFIG:**")
            from config_real import get_real_config_for_streamlit
            config_fonte = get_real_config_for_streamlit()
            st.write(f"- Config da fonte: {len(config_fonte)} chaves")
            st.write(f"- Chaves: {list(config_fonte.keys())}")
            st.write(f"- 'trading' presente: {'trading' in config_fonte}")
            
            # Import manual para evitar auto-inicialização problemática
            import trading_real_integration
            
            st.write("**Debug trading_real_integration:**")
            st.write(f"- HAS_REAL_CONFIG: {trading_real_integration.HAS_REAL_CONFIG}")
            st.write(f"- REAL_CONFIG existe: {hasattr(trading_real_integration, 'REAL_CONFIG')}")
            
            if hasattr(trading_real_integration, 'REAL_CONFIG') and trading_real_integration.REAL_CONFIG:
                config_tri = trading_real_integration.REAL_CONFIG
                st.write(f"- REAL_CONFIG chaves: {list(config_tri.keys())}")
                st.write(f"- 'trading' em REAL_CONFIG: {'trading' in config_tri}")
                
                if 'trading' not in config_tri:
                    st.warning("🔧 Corrigindo REAL_CONFIG...")
                    trading_real_integration.REAL_CONFIG = config_fonte
                    st.success("✅ REAL_CONFIG corrigido!")
            
            # Testar inicialização manual
            resultado = trading_real_integration.safe_auto_init()
            
            if resultado:
                st.success("✅ Módulo de integração funcionando corretamente!")
                
                # Mostrar status
                if hasattr(trading_real_integration, 'real_state'):
                    state = trading_real_integration.real_state
                    st.write(f"**Status:** {'Inicializado' if state.is_initialized else 'Não inicializado'}")
                    st.write(f"**Logs disponíveis:** {len(state.logs)}")
                    
                    if state.logs:
                        st.write("**Últimos logs:**")
                        for log in state.logs[-5:]:
                            st.text(log)
            else:
                st.warning("⚠️ Módulo de integração com problemas")
                
        except Exception as e:
            st.error(f"❌ Erro no módulo de integração: {e}")
            st.code(str(e))
      # Informações do sistema
    st.subheader("4. ℹ️ Informações do Sistema")
    try:
        from config_real import SYSTEM_INFO
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Versão:** {SYSTEM_INFO.get('version', 'N/A')}")
            st.write(f"**Fonte:** {SYSTEM_INFO.get('source_file', SYSTEM_INFO.get('source', 'N/A'))}")
        
        with col2:
            st.write(f"**Data de Extração:** {SYSTEM_INFO.get('extracted_date', 'N/A')}")
            st.write(f"**Configuração:** {SYSTEM_INFO.get('config_type', 'N/A')}")
        
        st.success("✅ Informações do sistema carregadas com sucesso!")
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar informações do sistema: {e}")
        st.write(f"Detalhes do erro: {str(e)}")
    
    # Botões de ação
    st.subheader("5. 🚀 Ações")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Dashboard Completo", type="primary"):
            st.info("🔄 Executar: streamlit run trading_dashboard_real.py")
    
    with col2:
        if st.button("🧪 Teste Completo"):
            st.info("🔄 Executar: python test_sistema_completo.py")
    
    with col3:
        if st.button("📋 Logs de Sistema"):
            st.info("📄 Verificar logs na pasta /logs/")

except Exception as e:
    st.error(f"❌ Erro ao carregar sistema: {e}")
    st.code(str(e))

st.markdown("---")
st.markdown("🎯 **Sistema de Trading Real v5.5** - Teste de Funcionamento")
