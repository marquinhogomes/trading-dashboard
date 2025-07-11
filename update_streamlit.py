#!/usr/bin/env python3
"""
Script para atualizar as chamadas de função no Streamlit para usar o sistema real
"""

import re

# Ler o arquivo
with open('trading_system_streamlit.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Substituições necessárias
substituicoes = [
    # Funções que mudaram de nome
    (r'get_system_status\(\)', 'get_real_system_status()'),
    (r'analyze_real_pairs\(([^)]*)\)', r'get_real_analysis_data()'),
    (r'get_real_logs\(([^)]*)\)', r'real_state.logs[-\1:] if real_state.logs else []'),
    
    # Funções que não existem mais
    (r'start_real_monitoring\(\)', 'real_state.is_running = True'),
    (r'stop_real_monitoring\(\)', 'real_state.is_running = False'),
    
    # Variáveis que mudaram
    (r'HAS_ORIGINAL_CODE', 'HAS_REAL_SYSTEM'),
    (r'ORIGINAL_FUNCTIONS\.get\([^)]*\)', 'None'),
]

# Aplicar substituições
for padrao, substituto in substituicoes:
    content = re.sub(padrao, substituto, content)

# Salvar arquivo atualizado
with open('trading_system_streamlit_updated.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Arquivo atualizado salvo como trading_system_streamlit_updated.py")
print("📝 Substituições aplicadas:")
for padrao, substituto in substituicoes:
    count = len(re.findall(padrao, content))
    if count > 0:
        print(f"   - {padrao} -> {substituto} ({count} ocorrências)")
