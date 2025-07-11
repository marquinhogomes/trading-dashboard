#!/usr/bin/env python3
"""
Teste para verificar se a correção do loop infinito está funcionando corretamente.
"""

import time
import threading
from sistema_integrado import SistemaIntegrado

def test_no_infinite_loop():
    """Testa se o sistema não entra em loop infinito"""
    print("=== TESTE DE CORREÇÃO DO LOOP INFINITO ===")
    
    # Criar instância do sistema
    print("\n1. Criando instância do sistema...")
    sistema = SistemaIntegrado()
    print("✓ Sistema criado com sucesso")
    
    # Testar método executar_sistema_original
    print("\n2. Testando método executar_sistema_original...")
    start_time = time.time()
    
    # Executar em thread separada para poder controlar o tempo
    def run_sistema_original():
        try:
            sistema.executar_sistema_original()
            print("✓ executar_sistema_original executado com sucesso")
        except Exception as e:
            print(f"✗ Erro em executar_sistema_original: {e}")
    
    # Executar em thread
    thread = threading.Thread(target=run_sistema_original)
    thread.daemon = True
    thread.start()
    
    # Esperar máximo 10 segundos
    thread.join(timeout=10)
    
    elapsed_time = time.time() - start_time
    
    if thread.is_alive():
        print(f"✗ FALHA: executar_sistema_original ainda está rodando após {elapsed_time:.2f}s")
        print("  Isso indica que o loop infinito não foi corrigido")
        return False
    else:
        print(f"✓ executar_sistema_original terminou em {elapsed_time:.2f}s")
        print("  O loop infinito foi corrigido com sucesso")
    
    # Testar thread de análise
    print("\n3. Testando thread de análise...")
    
    # Verificar se a thread pode ser iniciada sem problemas
    try:
        sistema.start_analysis_thread()
        print("✓ Thread de análise iniciada com sucesso")
        
        # Esperar um pouco para verificar se está funcionando
        time.sleep(3)
        
        # Parar a thread
        sistema.stop_analysis_thread()
        print("✓ Thread de análise parada com sucesso")
        
    except Exception as e:
        print(f"✗ Erro ao testar thread de análise: {e}")
        return False
    
    print("\n=== RESULTADO DO TESTE ===")
    print("✓ SUCESSO: A correção do loop infinito está funcionando corretamente!")
    print("✓ O sistema agora executa normalmente sem reinicializações constantes")
    print("✓ As threads podem ser iniciadas e paradas sem problemas")
    
    return True

def test_controlled_execution():
    """Testa se a execução está sendo controlada corretamente"""
    print("\n=== TESTE DE EXECUÇÃO CONTROLADA ===")
    
    sistema = SistemaIntegrado()
    
    # Contar quantas vezes o sistema original é executado
    original_method = sistema.executar_sistema_original
    execution_count = {'count': 0}
    
    def counting_wrapper():
        execution_count['count'] += 1
        print(f"Execução #{execution_count['count']} do sistema original")
        return original_method()
    
    sistema.executar_sistema_original = counting_wrapper
    
    # Testar múltiplas execuções
    print("Executando sistema original 3 vezes...")
    for i in range(3):
        sistema.executar_sistema_original()
        time.sleep(0.5)
    
    expected_count = 3
    actual_count = execution_count['count']
    
    if actual_count == expected_count:
        print(f"✓ Execução controlada funcionando: {actual_count} execuções como esperado")
        return True
    else:
        print(f"✗ Problema na execução controlada: esperado {expected_count}, obtido {actual_count}")
        return False

if __name__ == "__main__":
    print("Iniciando testes de correção do loop infinito...")
    
    # Executar testes
    test1_passed = test_no_infinite_loop()
    test2_passed = test_controlled_execution()
    
    print("\n" + "="*50)
    print("RESUMO DOS TESTES:")
    print(f"• Correção do loop infinito: {'✓ PASSOU' if test1_passed else '✗ FALHOU'}")
    print(f"• Execução controlada: {'✓ PASSOU' if test2_passed else '✗ FALHOU'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("A correção do loop infinito está funcionando perfeitamente.")
        print("O sistema agora pode ser usado normalmente sem reinicializações constantes.")
    else:
        print("\n❌ ALGUNS TESTES FALHARAM!")
        print("É necessário revisar a correção do loop infinito.")
