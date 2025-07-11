#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste isolado das importações necessárias
"""

print('[ISOLADO] Testando importações básicas...')

try:
    import threading
    print('[ISOLADO] ✅ threading importado')
    
    import time
    print('[ISOLADO] ✅ time importado')
    
    import json
    print('[ISOLADO] ✅ json importado')
    
    import sys
    print('[ISOLADO] ✅ sys importado')
    
    import os
    print('[ISOLADO] ✅ os importado')
    
    import importlib.util
    print('[ISOLADO] ✅ importlib.util importado')
    
    from datetime import datetime
    print('[ISOLADO] ✅ datetime importado')
    
    import traceback
    print('[ISOLADO] ✅ traceback importado')
    
    print('[ISOLADO] ✅ Todas as importações básicas funcionam!')
    
    # Agora tenta importar o sistema_integrado
    print('[ISOLADO] Tentando importar sistema_integrado...')
    
    # Vamos tentar importar linha por linha
    with open('sistema_integrado.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f'[ISOLADO] Arquivo tem {len(lines)} linhas')
    print('[ISOLADO] Primeira linha:', lines[0].strip())
    print('[ISOLADO] Segunda linha:', lines[1].strip())
    
    # Verificar se há problemas de encoding
    problematic_lines = []
    for i, line in enumerate(lines):
        try:
            line.encode('utf-8')
        except UnicodeEncodeError as e:
            problematic_lines.append((i+1, str(e)))
    
    if problematic_lines:
        print(f'[ISOLADO] ❌ Encontradas {len(problematic_lines)} linhas com problemas de encoding')
        for line_num, error in problematic_lines[:5]:  # Mostra apenas as primeiras 5
            print(f'[ISOLADO]   Linha {line_num}: {error}')
    else:
        print('[ISOLADO] ✅ Nenhum problema de encoding encontrado')
    
    print('[ISOLADO] Teste de compilação...')
    try:
        compile(open('sistema_integrado.py', 'r', encoding='utf-8').read(), 'sistema_integrado.py', 'exec')
        print('[ISOLADO] ✅ Arquivo compila sem erros de sintaxe')
    except SyntaxError as e:
        print(f'[ISOLADO] ❌ Erro de sintaxe: {e}')
        print(f'[ISOLADO]   Linha {e.lineno}: {e.text}')
    
except Exception as e:
    print(f'[ISOLADO] ❌ Erro: {e}')
    import traceback
    traceback.print_exc()

print('[ISOLADO] Teste concluído.')
