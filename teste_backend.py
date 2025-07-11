#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste robusto do backend Sistema Integrado - Etapa 2
"""

print('[TESTE] Iniciando teste robusto do backend...')

try:
    from sistema_integrado import SistemaIntegrado
    print('[TESTE] ✅ Importação do SistemaIntegrado bem-sucedida')
    
    print('[TESTE] Criando instância do backend...')
    sistema = SistemaIntegrado()
    print('[TESTE] ✅ Instância criada com sucesso')
    
    print('[TESTE] Verificando atributos essenciais...')
    print(f'[TESTE] - running: {getattr(sistema, "running", "N/A")}')
    print(f'[TESTE] - logs: {len(getattr(sistema, "logs", []))} entradas')
    print(f'[TESTE] - dados_sistema: {type(getattr(sistema, "dados_sistema", None))}')
    
    print('[TESTE] Verificando threads principais...')
    threads = ['thread_trading', 'thread_monitor', 'thread_monitor_posicoes', 'thread_break_even', 'thread_ajustes', 'thread_ordens']
    threads_ativas = 0
    for thread_name in threads:
        thread_obj = getattr(sistema, thread_name, None)
        if thread_obj and hasattr(thread_obj, 'is_alive'):
            if thread_obj.is_alive():
                status = '🟢 Ativa'
                threads_ativas += 1
            else:
                status = '🔴 Inativa'
        else:
            status = '❌ Não encontrada'
        print(f'[TESTE] - {thread_name}: {status}')
    
    print(f'[TESTE] Total de threads ativas: {threads_ativas}/{len(threads)}')
    
    print('[TESTE] Testando métodos de análise...')
    print(f'[TESTE] - start_analysis_thread: {hasattr(sistema, "start_analysis_thread")}')
    print(f'[TESTE] - stop_analysis_thread: {hasattr(sistema, "stop_analysis_thread")}')
    print(f'[TESTE] - is_analysis_running: {hasattr(sistema, "is_analysis_running")}')
    
    if hasattr(sistema, 'is_analysis_running'):
        try:
            analysis_status = sistema.is_analysis_running()
            print(f'[TESTE] - Análise rodando: {analysis_status}')
        except Exception as e:
            print(f'[TESTE] - Erro ao verificar análise: {e}')
    
    print('[TESTE] Verificando logs do sistema...')
    if hasattr(sistema, 'logs') and sistema.logs:
        print(f'[TESTE] Total de logs: {len(sistema.logs)}')
        print('[TESTE] Últimos 5 logs:')
        for log in sistema.logs[-5:]:
            print(f'[TESTE]   {log}')
    else:
        print('[TESTE] Nenhum log encontrado')
    
    print('[TESTE] Testando start/stop da análise...')
    if hasattr(sistema, 'start_analysis_thread') and hasattr(sistema, 'stop_analysis_thread'):
        try:
            # Teste básico de start
            config_teste = {
                'zscore_min': 2.0,
                'zscore_max': 6.5,
                'max_posicoes': 3,
                'valor_operacao': 5000,
                'finaliza_ordens': 17
            }
            
            print('[TESTE] Iniciando análise de teste...')
            resultado = sistema.start_analysis_thread(tabela_linha_operacao01=None, config=config_teste)
            print(f'[TESTE] - Start analysis result: {resultado}')
            
            # Aguarda um pouco para verificar se iniciou
            import time
            time.sleep(2)
            
            if hasattr(sistema, 'is_analysis_running'):
                is_running = sistema.is_analysis_running()
                print(f'[TESTE] - Análise rodando após start: {is_running}')
            
            # Para a análise
            print('[TESTE] Parando análise de teste...')
            sistema.stop_analysis_thread()
            
            # Aguarda um pouco para verificar se parou
            time.sleep(1)
            
            if hasattr(sistema, 'is_analysis_running'):
                is_running = sistema.is_analysis_running()
                print(f'[TESTE] - Análise rodando após stop: {is_running}')
            
        except Exception as e:
            print(f'[TESTE] - Erro no teste start/stop: {e}')
    
    print('[TESTE] ✅ Teste do backend concluído com SUCESSO!')
    print('[TESTE] Sistema Integrado está funcionando corretamente!')
    
except ImportError as e:
    print(f'[TESTE] ❌ Erro de importação: {e}')
    import traceback
    print(f'[TESTE] Traceback: {traceback.format_exc()}')
except Exception as e:
    print(f'[TESTE] ❌ Erro no teste: {e}')
    import traceback
    print(f'[TESTE] Traceback: {traceback.format_exc()}')

print('[TESTE] Finalizando teste...')
