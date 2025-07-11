#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste: Verificar seção Ativos Monitorados com defaults e separadores
"""

import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Teste Ativos Monitorados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS básico
st.markdown("""
<style>
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# Dados de exemplo (similar ao sistema real)
segmentos_mock = {
    'ABEV3': 'Bebidas', 'ALOS3': 'Saúde', 'ASAI3': 'Varejo Alimentar',
    'BBAS3': 'Bancos', 'BBDC4': 'Bancos', 'BBSE3': 'Seguros',
    'BPAC11': 'Bancos', 'BRAP4': 'Holding', 'BRFS3': 'Alimentos',
    'BRKM5': 'Química', 'CPFE3': 'Energia', 'CPLE6': 'Energia',
    'CSNA3': 'Siderurgia','CYRE3': 'Construção','ELET3': 'Energia',
    'ELET6': 'Energia', 'EMBR3': 'Aeroespacial','ENEV3': 'Energia',
    'ENGI11': 'Energia', 'EQTL3': 'Energia', 'EZTC3': 'Construção',
    'FLRY3': 'Saúde', 'GOAU4': 'Siderurgia','HYPE3': 'Farmacêutica',
    'IGTI11': 'Financeiro','IRBR3': 'Seguros', 'ITSA4': 'Financeiro',
    'ITUB4': 'Bancos', 'KLBN11': 'Papel e Celulose',
    'MRFG3': 'Alimentos', 'NTCO3': 'Higiene/Beleza','PETR3': 'Petróleo',
    'PETR4': 'Petróleo', 'PETZ3': 'Varejo', 'PRIO3': 'Petróleo',
    'RAIL3': 'Logística', 'RADL3': 'Varejo', 'RECV3': 'Petróleo',
    'RENT3': 'Locação', 'RDOR3': 'Saúde', 'SANB11': 'Bancos',
    'SLCE3': 'Agro', 'SMTO3': 'Agro', 'SUZB3': 'Papel e Celulose',
    'TAEE11': 'Energia', 'TIMS3': 'Telecom', 'TOTS3': 'Tecnologia',
    'UGPA3': 'Distribuição','VALE3': 'Mineração','VBBR3': 'Transporte',
    'VIVT3': 'Telecom', 'WEGE3': 'Industrial','YDUQ3': 'Educação'
}

# Título principal
st.title("🧪 Teste: Ativos Monitorados - Defaults e Separadores")

# Sidebar com a nova estrutura
with st.sidebar:
    st.header("Teste da Nova Estrutura")
    
    # ==================== SEÇÃO: ATIVOS MONITORADOS ====================
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 📊 Ativos Monitorados")
    
    # Filtro por segmento
    segmentos_disponiveis = list(set(segmentos_mock.values()))
    segmentos_disponiveis.sort()  # Ordena alfabeticamente
    
    # Opção de selecionar todos os segmentos (PADRÃO: MARCADO)
    selecionar_todos_segmentos = st.checkbox("Selecionar Todos os Segmentos", value=True)
    
    if selecionar_todos_segmentos:
        segmentos_selecionados = segmentos_disponiveis
    else:
        segmentos_selecionados = st.multiselect(
            "Segmentos", 
            segmentos_disponiveis,
            default=segmentos_disponiveis[:5]
        )
    
    # Linha cinza separadora
    st.markdown("---")
    
    # Ativos por segmento selecionado
    ativos_filtrados = [
        ativo for ativo, segmento in segmentos_mock.items()
        if segmento in segmentos_selecionados
    ]
    
    # Opção de selecionar todos os ativos (PADRÃO: MARCADO)
    selecionar_todos_ativos = st.checkbox("Selecionar Todos os Ativos", value=True)
    
    if selecionar_todos_ativos:
        ativos_selecionados = ativos_filtrados
    else:
        ativos_selecionados = st.multiselect(
            "Ativos Específicos",
            ativos_filtrados,
            default=ativos_filtrados[:10] if ativos_filtrados else []
        )
    
    # Linha cinza separadora
    st.markdown("---")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Informações de debug
    st.subheader("Debug Info")
    st.write(f"Segmentos selecionados: {len(segmentos_selecionados)}")
    st.write(f"Ativos filtrados: {len(ativos_filtrados)}")
    st.write(f"Ativos finais: {len(ativos_selecionados)}")

# Área principal
col1, col2 = st.columns(2)

with col1:
    st.write("## ✅ Verificações Implementadas")
    st.success("✅ Checkbox 'Todos os Segmentos' marcado por padrão")
    st.success("✅ Checkbox 'Todos os Ativos' marcado por padrão")
    st.success("✅ Linha cinza após segmentos")
    st.success("✅ Linha cinza após ativos")
    st.success("✅ Campos de entrada substituídos por separadores")

with col2:
    st.write("## 📊 Resultados Atuais")
    st.info(f"**Segmentos Disponíveis:** {len(segmentos_disponiveis)}")
    st.info(f"**Segmentos Selecionados:** {len(segmentos_selecionados)}")
    st.info(f"**Ativos Filtrados:** {len(ativos_filtrados)}")
    st.info(f"**Ativos Selecionados:** {len(ativos_selecionados)}")

# Tabela de segmentos
st.write("### 📈 Segmentos e Ativos")

if segmentos_selecionados:
    for segmento in segmentos_selecionados[:5]:  # Mostra apenas os primeiros 5
        ativos_do_segmento = [ativo for ativo, seg in segmentos_mock.items() if seg == segmento]
        st.write(f"**{segmento}:** {', '.join(ativos_do_segmento)}")

# Lista de ativos selecionados
if ativos_selecionados:
    st.write("### 🎯 Ativos Finais Selecionados")
    
    # Agrupa por segmento
    ativos_por_segmento = {}
    for ativo in ativos_selecionados[:20]:  # Mostra apenas os primeiros 20
        segmento = segmentos_mock[ativo]
        if segmento not in ativos_por_segmento:
            ativos_por_segmento[segmento] = []
        ativos_por_segmento[segmento].append(ativo)
    
    for segmento, ativos in ativos_por_segmento.items():
        st.write(f"**{segmento}:** {', '.join(ativos)}")

# Status final
st.write("### ✅ Status da Implementação")

col1, col2, col3 = st.columns(3)

with col1:
    if selecionar_todos_segmentos:
        st.success("✅ Todos segmentos selecionados")
    else:
        st.warning("⚠️ Seleção manual de segmentos")

with col2:
    if selecionar_todos_ativos:
        st.success("✅ Todos ativos selecionados")
    else:
        st.warning("⚠️ Seleção manual de ativos")

with col3:
    st.metric("Total Ativos", len(ativos_selecionados))

st.write("---")
st.write("**Teste concluído!** A nova estrutura substitui os campos de entrada por separadores visuais e define defaults corretos.")
