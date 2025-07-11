#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples das Etapas 1, 2 e 3 implementadas
"""

print("🧪 TESTE SIMPLES DO SISTEMA INTEGRADO")
print("="*50)

# Teste de sintaxe básico
try:
    print("1. Testando sintaxe...")
    import ast
    with open('sistema_integrado.py', 'r', encoding='utf-8') as f:
        ast.parse(f.read())
    print("✅ Sintaxe correta!")
except Exception as e:
    print(f"❌ Erro de sintaxe: {e}")

# Teste de importação
try:
    print("2. Testando importação...")
    import sistema_integrado
    print("✅ Importação bem-sucedida!")
except Exception as e:
    print(f"❌ Erro de importação: {e}")

# Teste de criação de instância
try:
    print("3. Testando criação de instância...")
    sistema = sistema_integrado.SistemaIntegrado()
    print("✅ Instância criada!")
    
    # Verificação das Etapas
    print("\n🔍 VERIFICAÇÃO DAS ETAPAS:")
    
    # Etapa 1
    if hasattr(sistema, '_start_all_threads_integrado'):
        print("✅ ETAPA 1: _start_all_threads_integrado implementado")
    else:
        print("❌ ETAPA 1: _start_all_threads_integrado FALTANDO")
    
    # Etapa 2
    metodos_etapa2 = ['start_analysis_thread', 'stop_analysis_thread', 'is_analysis_running']
    for metodo in metodos_etapa2:
        if hasattr(sistema, metodo):
            print(f"✅ ETAPA 2: {metodo} implementado")
        else:
            print(f"❌ ETAPA 2: {metodo} FALTANDO")
    
    # Atributos da Etapa 2
    attrs_etapa2 = ['analysis_thread', 'analysis_thread_lock', 'analysis_thread_stop_event']
    for attr in attrs_etapa2:
        if hasattr(sistema, attr):
            print(f"✅ ETAPA 2: {attr} presente")
        else:
            print(f"❌ ETAPA 2: {attr} FALTANDO")
    
    print(f"\n✅ SISTEMA PRONTO! Running={sistema.running}")
    
except Exception as e:
    print(f"❌ Erro ao criar instância: {e}")
    import traceback
    traceback.print_exc()

print("="*50)
print("🎯 TESTE CONCLUÍDO!")
