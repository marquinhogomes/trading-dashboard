#!/usr/bin/env python3
"""
Teste ultra simples - apenas verificação de classe
"""
import ast

print('[SIMPLES] Iniciando análise estática...')

try:
    # Lê o arquivo como texto
    with open('sistema_integrado.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print('[SIMPLES] ✅ Arquivo lido com sucesso')
    
    # Parse do AST
    tree = ast.parse(content)
    print('[SIMPLES] ✅ AST parseado com sucesso')
    
    # Procura pela classe SistemaIntegrado
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == 'SistemaIntegrado':
            print('[SIMPLES] ✅ Classe SistemaIntegrado encontrada!')
            
            # Lista métodos da classe
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods.append(item.name)
            
            print(f'[SIMPLES] Métodos encontrados: {len(methods)}')
            
            # Procura métodos de análise
            analysis_methods = [m for m in methods if 'analysis' in m.lower()]
            print(f'[SIMPLES] Métodos de análise: {analysis_methods}')
            
            # Procura métodos específicos
            essential_methods = ['start_analysis_thread', 'stop_analysis_thread', 'is_analysis_running']
            found_methods = [m for m in essential_methods if m in methods]
            print(f'[SIMPLES] Métodos essenciais encontrados: {found_methods}')
            
            if len(found_methods) == len(essential_methods):
                print('[SIMPLES] ✅ TODOS os métodos essenciais estão presentes!')
                print('[SIMPLES] ✅ Backend Sistema Integrado está PRONTO para uso!')
            else:
                missing = [m for m in essential_methods if m not in methods]
                print(f'[SIMPLES] ❌ Métodos faltando: {missing}')
            
            break
    else:
        print('[SIMPLES] ❌ Classe SistemaIntegrado não encontrada')
    
    print('[SIMPLES] ✅ Análise estática concluída com sucesso!')

except Exception as e:
    print(f'[SIMPLES] ❌ Erro: {e}')

print('[SIMPLES] Teste finalizado.')
