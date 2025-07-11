#!/usr/bin/env python3
"""
Teste para verificar se a thread SistemaTrading está funcionando corretamente
"""

import sistema_integrado
import time

def test_sistema_trading_thread():
    """Testa se a thread SistemaTrading está funcionando"""
    print('=== TESTE DA CORREÇÃO DA THREAD SistemaTrading ===')
    
    sistema = sistema_integrado.SistemaIntegrado()
    print('✓ Sistema criado com sucesso')
    
    # Inicia as threads
    print('\n🚀 Iniciando threads...')
    resultado = sistema.iniciar_threads_apenas()
    print(f'✓ Resultado do iniciar_threads_apenas: {resultado}')
    
    # Aguarda um pouco para as threads iniciarem
    time.sleep(5)
    
    # Verifica status das threads
    print('\n=== STATUS DAS THREADS ===')
    threads_status = []
    
    # Verifica cada thread individualmente
    if hasattr(sistema, 'sistema_trading_thread') and sistema.sistema_trading_thread:
        alive = sistema.sistema_trading_thread.is_alive()
        name = sistema.sistema_trading_thread.name
        threads_status.append(('SistemaTrading', alive, name))
        print(f'✓ SistemaTrading: {"🟢 ATIVA" if alive else "🔴 PARADA"} (Nome: {name})')
    else:
        print('❌ SistemaTrading: Não encontrada')
    
    if hasattr(sistema, 'thread_monitoramento') and sistema.thread_monitoramento:
        alive = sistema.thread_monitoramento.is_alive()
        name = sistema.thread_monitoramento.name
        threads_status.append(('Monitoramento', alive, name))
        print(f'✓ Monitoramento: {"🟢 ATIVA" if alive else "🔴 PARADA"} (Nome: {name})')
    
    if hasattr(sistema, 'thread_monitoramento_posicoes') and sistema.thread_monitoramento_posicoes:
        alive = sistema.thread_monitoramento_posicoes.is_alive()
        name = sistema.thread_monitoramento_posicoes.name
        threads_status.append(('MonitoramentoPosicoes', alive, name))
        print(f'✓ MonitoramentoPosicoes: {"🟢 ATIVA" if alive else "🔴 PARADA"} (Nome: {name})')
    
    if hasattr(sistema, 'thread_break_even') and sistema.thread_break_even:
        alive = sistema.thread_break_even.is_alive()
        name = sistema.thread_break_even.name
        threads_status.append(('BreakEven', alive, name))
        print(f'✓ BreakEven: {"🟢 ATIVA" if alive else "🔴 PARADA"} (Nome: {name})')
    
    if hasattr(sistema, 'thread_ajustes_programados') and sistema.thread_ajustes_programados:
        alive = sistema.thread_ajustes_programados.is_alive()
        name = sistema.thread_ajustes_programados.name
        threads_status.append(('AjustesProgramados', alive, name))
        print(f'✓ AjustesProgramados: {"🟢 ATIVA" if alive else "🔴 PARADA"} (Nome: {name})')
    
    if hasattr(sistema, 'thread_analise_e_envio_ordens') and sistema.thread_analise_e_envio_ordens:
        alive = sistema.thread_analise_e_envio_ordens.is_alive()
        name = sistema.thread_analise_e_envio_ordens.name
        threads_status.append(('AnaliseEnvioOrdens', alive, name))
        print(f'✓ AnaliseEnvioOrdens: {"🟢 ATIVA" if alive else "🔴 PARADA"} (Nome: {name})')
    
    # Resumo
    total_threads = len(threads_status)
    threads_ativas = sum(1 for _, alive, _ in threads_status if alive)
    
    print(f'\n📊 RESUMO: {threads_ativas}/{total_threads} threads ativas')
    
    # Verifica especificamente a SistemaTrading
    sistema_trading_ativa = any(name == 'SistemaTrading' and alive for name, alive, _ in threads_status)
    
    if sistema_trading_ativa:
        print('🎉 SUCESSO: Thread SistemaTrading está funcionando corretamente!')
        print('✅ A correção do loop infinito permitiu que a thread continue executando')
    else:
        print('❌ FALHA: Thread SistemaTrading ainda não está funcionando')
    
    # Para o sistema
    print('\n🛑 Parando sistema...')
    sistema.parar_sistema()
    
    time.sleep(2)
    print('✅ Teste concluído')
    
    return sistema_trading_ativa

if __name__ == "__main__":
    test_sistema_trading_thread()
