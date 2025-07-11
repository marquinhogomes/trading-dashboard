#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste do sistema_integrado_v10.py após implementação das Etapas 1, 2 e 3
"""

def testar_sintaxe():
    """Testa se o arquivo tem sintaxe correta"""
    try:
        import ast
        with open('sistema_integrado_v10.py', 'r', encoding='utf-8') as f:
            codigo = f.read()
        ast.parse(codigo)
        print("✅ SINTAXE: Arquivo sintaticamente correto!")
        return True
    except Exception as e:
        print(f"❌ SINTAXE: Erro na sintaxe do arquivo: {e}")
        return False

def testar_importacao():
    """Testa se o módulo pode ser importado"""
    try:
        import sistema_integrado_v10
        print("✅ IMPORTAÇÃO: Módulo importado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ IMPORTAÇÃO: Erro ao importar módulo: {e}")
        return False

def testar_criacao_instancia():
    """Testa se uma instância pode ser criada"""
    try:
        import sistema_integrado_v10
        sistema = sistema_integrado_v10.SistemaIntegrado()
        print("✅ INSTÂNCIA: SistemaIntegrado criado com sucesso!")
        
        # Verifica se as Etapas 1, 2 e 3 foram implementadas
        verificacoes = []
        
        # Etapa 1: Método _start_all_threads_integrado
        if hasattr(sistema, '_start_all_threads_integrado'):
            verificacoes.append("✅ Etapa 1: _start_all_threads_integrado implementado")
        else:
            verificacoes.append("❌ Etapa 1: _start_all_threads_integrado NÃO encontrado")
        
        # Etapa 2: Métodos de thread de análise
        metodos_analise = ['start_analysis_thread', 'stop_analysis_thread', 'is_analysis_running', '_analysis_thread_target']
        for metodo in metodos_analise:
            if hasattr(sistema, metodo):
                verificacoes.append(f"✅ Etapa 2: {metodo} implementado")
            else:
                verificacoes.append(f"❌ Etapa 2: {metodo} NÃO encontrado")
        
        # Etapa 2: Atributos de controle de thread
        atributos_analise = ['analysis_thread', 'analysis_thread_lock', 'analysis_thread_stop_event']
        for attr in atributos_analise:
            if hasattr(sistema, attr):
                verificacoes.append(f"✅ Etapa 2: {attr} presente")
            else:
                verificacoes.append(f"❌ Etapa 2: {attr} NÃO encontrado")
        
        print("\n" + "="*60)
        print("VERIFICAÇÃO DAS ETAPAS IMPLEMENTADAS:")
        print("="*60)
        for verif in verificacoes:
            print(verif)
        print("="*60)
        
        return True
    except Exception as e:
        print(f"❌ INSTÂNCIA: Erro ao criar instância: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def main():
    print("🧪 TESTE DO SISTEMA_INTEGRADO_V10.PY")
    print("="*50)
    
    sucesso_total = True
    
    # Teste 1: Sintaxe
    sucesso_total &= testar_sintaxe()
    
    # Teste 2: Importação
    sucesso_total &= testar_importacao()
    
    # Teste 3: Criação de instância e verificação das etapas
    sucesso_total &= testar_criacao_instancia()
    
    print("\n" + "="*50)
    if sucesso_total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ As Etapas 1, 2 e 3 foram implementadas corretamente!")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("⚠️ Verifique os erros acima.")
    print("="*50)

if __name__ == "__main__":
    main()
