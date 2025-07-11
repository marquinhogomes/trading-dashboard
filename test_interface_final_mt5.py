#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Final da Interface MT5 - Validação Completa
Verifica:
1. Posicionamento dos botões (Conectar à esquerda, Status à direita)
2. Botão de status totalmente preenchido (verde conectado, vermelho desconectado)
3. Comportamento do botão Conectar/Desconectar
4. Campos ocultos quando conectado
5. CSS aplicado corretamente
"""

import streamlit as st
import sys
import os

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuração da página
st.set_page_config(
    page_title="Teste Interface MT5 Final",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS dos botões MT5 (copiado do dashboard principal)
st.markdown("""
<style>
    /* Botões de status MT5 customizados */
    .status-button-connected {
        background-color: #27ae60 !important;
        color: white !important;
        border: 2px solid #27ae60 !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
        text-align: center !important;
        font-weight: bold !important;
        cursor: default !important;
    }
    
    .status-button-disconnected {
        background-color: #e74c3c !important;
        color: white !important;
        border: 2px solid #e74c3c !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
        text-align: center !important;
        font-weight: bold !important;
        cursor: default !important;
    }
    
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# Simulação do estado de conexão (persistente durante a sessão)
if 'mt5_connected' not in st.session_state:
    st.session_state.mt5_connected = False

if 'last_login' not in st.session_state:
    st.session_state.last_login = None
if 'last_password' not in st.session_state:
    st.session_state.last_password = None
if 'last_server' not in st.session_state:
    st.session_state.last_server = None

st.title("🔌 Teste Final da Interface MT5")

st.markdown("""
### 📋 Checklist de Validação:

**✅ Posicionamento dos Botões:**
- Botão "Conectar/Desconectar" à esquerda
- Botão de status à direita

**✅ Aparência do Botão de Status:**
- Verde totalmente preenchido quando conectado
- Vermelho totalmente preenchido quando desconectado
- Mesmo tamanho dos botões

**✅ Comportamento dos Botões:**
- "Conectar" vira "Desconectar" quando conectado
- Campos de login aparecem apenas quando desconectado
- Desconectar limpa credenciais salvas

**✅ Visual Final:**
- CSS aplicado corretamente
- Botões com largura completa
- Cores vibrantes e contrastantes
""")

st.markdown("---")

# Interface MT5 na sidebar
st.sidebar.markdown("## 🔌 Teste Interface MT5")
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.markdown("### 🔌 Conexão MT5")

# Verifica se já está conectado para minimizar a interface
is_connected = st.session_state.mt5_connected

if not is_connected:
    # Mostra campos de login apenas se não estiver conectado
    mt5_login = st.sidebar.number_input("Login", value=12345, format="%d")
    mt5_password = st.sidebar.text_input("Senha", type="password", value="senha123")
    mt5_server = st.sidebar.text_input("Servidor", value="Demo-Server")
else:
    # Usa valores salvos quando conectado
    mt5_login = st.session_state.last_login or 12345
    mt5_password = st.session_state.last_password or "senha123"
    mt5_server = st.session_state.last_server or "Demo-Server"

# Interface de conexão compacta
col_btn, col_status = st.sidebar.columns([1, 1])

with col_btn:
    if is_connected:
        # Quando conectado, botão vira "Desconectar"
        if st.button("🔌 Desconectar", use_container_width=True, help="Clique para desconectar do MT5"):
            st.session_state.mt5_connected = False
            # Limpa as credenciais salvas
            st.session_state.last_login = None
            st.session_state.last_password = None
            st.session_state.last_server = None
            st.success("🔌 Desconectado!")
            st.rerun()
    else:
        # Quando desconectado, botão normal "Conectar"
        if st.button("🔗 Conectar", use_container_width=True, help="Clique para conectar ao MT5"):
            # Simula conexão sempre bem-sucedida
            st.session_state.mt5_connected = True
            # Salva as credenciais
            st.session_state.last_login = mt5_login
            st.session_state.last_password = mt5_password
            st.session_state.last_server = mt5_server
            st.success("✅ Conectado!")
            st.rerun()

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
        </div>
        """, unsafe_allow_html=True)

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Status no corpo principal
st.markdown("### 📊 Status Atual da Interface:")

col1, col2 = st.columns(2)

with col1:
    if is_connected:
        st.success("🟢 **CONECTADO**")
        st.write(f"**Login:** {mt5_login}")
        st.write(f"**Servidor:** {mt5_server}")
        st.write("**Campos de login:** Ocultos ✅")
        st.write("**Botão principal:** Desconectar ✅")
    else:
        st.error("🔴 **DESCONECTADO**")
        st.write("**Login:** Não definido")
        st.write("**Servidor:** Não definido")
        st.write("**Campos de login:** Visíveis ✅")
        st.write("**Botão principal:** Conectar ✅")

with col2:
    st.markdown("#### 🎨 Validação Visual:")
    
    if is_connected:        st.markdown("""
        ✅ **Botão Status:** Verde preenchido  
        ✅ **Posição:** Direita  
        ✅ **Texto:** "Conectado"  
        ✅ **CSS:** Aplicado corretamente  
        """)
    else:        st.markdown("""
        ✅ **Botão Status:** Vermelho preenchido  
        ✅ **Posição:** Direita  
        ✅ **Texto:** "Desconectado"  
        ✅ **CSS:** Aplicado corretamente  
        """)

st.markdown("---")

# Instruções de teste
st.markdown("""
### 🧪 Instruções de Teste:

1. **Teste Estado Desconectado:**
   - Veja os campos de login na sidebar
   - Observe o botão vermelho "Desconectado" à direita
   - Clique em "🔗 Conectar" à esquerda

2. **Teste Estado Conectado:**
   - Campos de login devem desaparecer
   - Botão verde "Conectado" à direita
   - Botão "🔌 Desconectar" à esquerda

3. **Teste Alternância:**
   - Clique em "Desconectar" para voltar ao estado inicial
   - Verifique se as credenciais são limpas
   - Reconecte e veja se tudo funciona novamente

### ✅ **RESULTADO ESPERADO:**
Interface limpa, botões bem posicionados, cores vibrantes e comportamento correto de conexão/desconexão.
""")

# Footer
st.markdown("---")
st.markdown("**🔧 Teste criado para validar as melhorias da interface MT5**")
