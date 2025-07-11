#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste da Correção: Botão Vermelho Quando Sistema Parado
Demonstra que o status do sistema agora fica vermelho quando parado
"""

import streamlit as st
import sys
import os

# Configuração da página
st.set_page_config(
    page_title="Teste Status Vermelho Sistema Parado",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS atualizado (igual ao dashboard principal)
st.markdown("""
<style>
    .system-status-running {
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
    
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #dee2e6;
    }
    
    .test-highlight {
        border: 3px solid #007bff;
        background: rgba(0, 123, 255, 0.1);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Estado do sistema
if 'sistema_rodando' not in st.session_state:
    st.session_state.sistema_rodando = False

st.title("🔴 Teste: Botão Vermelho Quando Sistema Parado")

st.markdown("""
### 🎯 Correção Implementada:

**❌ PROBLEMA ANTERIOR:**
- Botão de status ficava cinza quando sistema parado
- Falta de consistência visual com outros botões

**✅ SOLUÇÃO APLICADA:**
- Botão agora fica VERMELHO quando sistema parado
- Verde quando rodando (mantido)
- Consistência com botões MT5 (verde/vermelho)
""")

st.markdown("---")

# SIDEBAR COM CONTROLES CORRIGIDOS
st.sidebar.markdown("## ⚙️ Configurações do Sistema")

st.sidebar.markdown('<div class="sidebar-section test-highlight">', unsafe_allow_html=True)
st.sidebar.markdown("### 🎮 Controles do Sistema")
st.sidebar.markdown("**🔍 TESTE: Status vermelho quando parado**")

# Interface de controle no mesmo formato MT5
is_running = st.session_state.sistema_rodando

# Interface de controle compacta
col_btn, col_status = st.sidebar.columns([1, 1])

with col_btn:
    if is_running:
        # Quando rodando, botão vira "Parar Sistema"
        if st.button("⏹️ Parar Sistema", use_container_width=True, help="Clique para parar o sistema"):
            st.session_state.sistema_rodando = False
            st.rerun()
    else:
        # Quando parado, botão normal "Iniciar Sistema"
        if st.button("▶️ Iniciar Sistema", use_container_width=True, help="Clique para iniciar o sistema"):
            st.session_state.sistema_rodando = True
            st.rerun()

with col_status:
    if is_running:
        # Botão verde quando sistema rodando
        st.markdown("""
        <div class="system-status-running">
            Rodando
        </div>
        """, unsafe_allow_html=True)
    else:
        # Botão VERMELHO quando sistema parado (CORREÇÃO!)
        st.markdown("""
        <div class="system-status-stopped">
            Parado
        </div>
        """, unsafe_allow_html=True)

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# PAINEL PRINCIPAL - VERIFICAÇÃO
st.markdown("### 🔍 Verificação da Correção")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎨 Estado Atual dos Botões:")
    
    if is_running:
        st.success("🟢 **SISTEMA RODANDO**")
        st.markdown("""
        **Botão Esquerdo:** ⏹️ Parar Sistema  
        **Botão Direito:** 🟢 Verde "Rodando"  
        
        ✅ **Comportamento:** Verde quando ativo
        """)
    else:
        st.error("🔴 **SISTEMA PARADO**")
        st.markdown("""
        **Botão Esquerdo:** ▶️ Iniciar Sistema  
        **Botão Direita:** 🔴 **VERMELHO "Parado"**  
        
        ✅ **CORREÇÃO:** Agora fica vermelho quando parado!
        """)

with col2:
    st.markdown("#### ✅ Especificações da Correção:")
    
    st.markdown("""
    **🎨 Cores dos Status:**
    
    **🟢 Sistema Rodando:**
    - Cor: Verde #27ae60
    - Texto: "Rodando"
    - Estado: Ativo
    
    **🔴 Sistema Parado:**
    - Cor: **Vermelho #e74c3c** ← CORRIGIDO!
    - Texto: "Parado"
    - Estado: Inativo
    
    **📏 Consistência Visual:**
    - Mesmo formato dos botões MT5
    - Altura uniforme: 38px
    - Largura: 50% cada coluna
    - Cores padronizadas: Verde/Vermelho
    """)

st.markdown("---")

# COMPARAÇÃO ANTES/DEPOIS
st.markdown("### 📊 Comparação Antes/Depois")

col_before, col_after = st.columns(2)

with col_before:
    st.markdown("#### ❌ ANTES (Problema)")
    st.markdown("""
    ```
    Sistema Parado:
    ┌─────────────────┬─────────────────┐
    │ ▶️ Iniciar      │  🔘 Parado     │
    │   Sistema       │   (cinza)      │
    └─────────────────┴─────────────────┘
    ```
    
    **Problemas:**
    - Cor cinza pouco destacada
    - Inconsistência visual
    - Status neutro para situação crítica
    """)

with col_after:
    st.markdown("#### ✅ DEPOIS (Corrigido)")
    st.markdown("""
    ```
    Sistema Parado:
    ┌─────────────────┬─────────────────┐
    │ ▶️ Iniciar      │  🔴 Parado     │
    │   Sistema       │  (vermelho)    │
    └─────────────────┴─────────────────┘
    ```
    
    **Melhorias:**
    - Cor vermelha chamativa
    - Consistência com outros botões
    - Status claro para situação crítica
    """)

st.markdown("---")

# INSTRUÇÕES DE TESTE
st.markdown("### 🧪 Instruções de Teste:")

st.markdown("""
1. **🔴 Observe o estado atual:**
   - Se sistema parado: botão direito deve estar VERMELHO
   - Se sistema rodando: botão direito deve estar VERDE

2. **🔄 Teste a alternância:**
   - Clique "Iniciar Sistema" → botão fica verde
   - Clique "Parar Sistema" → botão fica vermelho

3. **✅ Verifique a consistência:**
   - Cores seguem padrão: Verde=Ativo, Vermelho=Inativo
   - Tamanhos uniformes em ambos os estados
   - Visual profissional e claro

4. **🎯 Compare com MT5:**
   - Botões seguem o mesmo padrão visual
   - Cores consistentes em toda interface
""")

st.markdown("---")

# RESUMO TÉCNICO
st.markdown("### 🔧 Detalhes Técnicos da Correção:")

codigo_css = '''
/* CSS Corrigido */
.system-status-stopped {
    background-color: #e74c3c !important;  /* VERMELHO em vez de cinza */
    color: white !important;
    border: 2px solid #e74c3c !important;
    /* ... outras propriedades mantidas ... */
}
'''

st.code(codigo_css, language='css')

st.markdown("""
**📝 Alteração realizada:**
- Mudança da cor de fundo de `#6c757d` (cinza) para `#e74c3c` (vermelho)
- Mudança da cor da borda para coincidir
- Mantidas todas as outras propriedades (tamanho, alinhamento, etc.)

**🎯 Resultado:** Interface mais consistente e intuitiva!
""")

st.markdown("---")
st.markdown("**🎉 Correção aplicada com sucesso! Botão agora fica vermelho quando sistema parado.**")
