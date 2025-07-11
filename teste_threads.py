#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples para verificar se as threads estão funcionando
"""

import time
from sistema_integrado import SistemaIntegrado

def teste_threads():
    print("🚀 TESTE DE THREADS DO SISTEMA INTEGRADO")
    print("="*50)
    
    try:
        print("Criando instância do SistemaIntegrado...")
        sistema = SistemaIntegrado()
        print("✅ Instância criada com sucesso!")
        
        # Aguarda um pouco para as threads iniciarem
        print("Aguardando threads iniciarem...")
        time.sleep(1)
        
        # Verifica status das threads
        print("\n📊 STATUS DAS THREADS:")
        print("-"*30)
        
        threads_info = [
            ("Trading", sistema.thread_trading),
            ("Monitor", sistema.thread_monitor),
            ("Monitor Posições", sistema.thread_monitor_posicoes),
            ("Break-Even", sistema.thread_break_even),
            ("Ajustes", sistema.thread_ajustes),
            ("Ordens", sistema.thread_ordens),
        ]
        
        threads_ativas = 0
        for nome, thread in threads_info:
            if thread is not None:
                is_alive = thread.is_alive()
                status = "🟢 ATIVA" if is_alive else "🔴 INATIVA"
                thread_name = getattr(thread, 'name', 'N/A')
                print(f"{nome:<15}: {status} | Nome: {thread_name}")
                if is_alive:
                    threads_ativas += 1
            else:
                print(f"{nome:<15}: ❌ NÃO CRIADA")
        
        print(f"\n✅ RESUMO: {threads_ativas}/6 threads ativas")
        print(f"Sistema running: {'🟢' if sistema.running else '🔴'} {sistema.running}")
        
        # Mostra alguns logs recentes
        if hasattr(sistema, 'logs') and sistema.logs:
            print(f"\n📝 ÚLTIMOS LOGS ({len(sistema.logs)} total):")
            print("-"*40)
            for log in sistema.logs[-5:]:  # Últimos 5 logs
                print(f"  {log}")
        
        return threads_ativas
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return 0

if __name__ == "__main__":
    threads_ativas = teste_threads()
    print(f"\n{'✅ SUCESSO' if threads_ativas > 0 else '❌ FALHA'}: {threads_ativas}/6 threads ativas")
