#!/usr/bin/env python3
"""
Teste do Sistema de Auto-Restart da Thread Trading
==================================================

Este script testa o novo sistema de auto-restart da thread Trading
no sistema_integrado.py, verificando se funciona corretamente quando
o sistema original termina ou falha.

Teste: 2025-01-20
Status: Verificação do Auto-Restart
"""

import os
import sys
import time
import threading
from datetime import datetime
import tempfile
import shutil

def criar_calculo_entradas_teste():
    """Cria um arquivo calculo_entradas_v55.py de teste que termina rapidamente"""
    codigo_teste = '''
# Arquivo de teste para verificar auto-restart
import time
import random
from datetime import datetime

print(f"[TESTE] Sistema de teste iniciado às {datetime.now().strftime('%H:%M:%S')}")

# Simula execução do sistema por alguns segundos
for i in range(3):
    print(f"[TESTE] Ciclo {i+1}/3 - {datetime.now().strftime('%H:%M:%S')}")
    time.sleep(2)

# Simula término inesperado (como acontece no sistema real)
if random.choice([True, False]):
    print("[TESTE] Simulando término natural do sistema")
else:
    print("[TESTE] Simulando erro no sistema")
    raise Exception("Erro simulado para teste de restart")

print(f"[TESTE] Sistema de teste finalizado às {datetime.now().strftime('%H:%M:%S')}")
'''
    
    with open('calculo_entradas_v55.py', 'w', encoding='utf-8') as f:
        f.write(codigo_teste)
    
    print("✅ Arquivo calculo_entradas_v55.py de teste criado")

def fazer_backup_original():
    """Faz backup do arquivo original se existir"""
    if os.path.exists('calculo_entradas_v55.py'):
        backup_name = f'calculo_entradas_v55_backup_{int(time.time())}.py'
        shutil.copy2('calculo_entradas_v55.py', backup_name)
        print(f"✅ Backup do arquivo original criado: {backup_name}")
        return backup_name
    return None

def restaurar_backup(backup_name):
    """Restaura o arquivo original do backup"""
    if backup_name and os.path.exists(backup_name):
        shutil.copy2(backup_name, 'calculo_entradas_v55.py')
        os.remove(backup_name)
        print(f"✅ Arquivo original restaurado do backup")
    else:
        # Remove o arquivo de teste
        if os.path.exists('calculo_entradas_v55.py'):
            os.remove('calculo_entradas_v55.py')
            print("✅ Arquivo de teste removido")

def teste_auto_restart():
    """Testa o sistema de auto-restart"""
    print("=" * 80)
    print("🧪 TESTE DO SISTEMA DE AUTO-RESTART DA THREAD TRADING")
    print("=" * 80)
    print(f"📅 Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Faz backup do arquivo original
    backup_name = fazer_backup_original()
    
    try:
        # Cria arquivo de teste
        criar_calculo_entradas_teste()
        
        # Importa e testa o sistema integrado
        print("📥 Importando sistema_integrado...")
        from sistema_integrado import SistemaIntegrado
        
        # Cria instância do sistema
        print("🚀 Criando instância do sistema...")
        sistema = SistemaIntegrado()
        
        # Configura para teste (reduz tempos)
        print("⚙️ Configurando para teste rápido...")
        
        # Inicia o sistema em thread separada
        print("▶️ Iniciando sistema em thread de teste...")
        thread_sistema = threading.Thread(target=sistema.iniciar_sistema, name="TesteSistema")
        thread_sistema.daemon = True
        thread_sistema.start()
        
        # Monitora por 2 minutos para ver múltiplos restarts
        print("👀 Monitorando sistema por 2 minutos para observar restarts...")
        print("   (O sistema de teste deve reiniciar várias vezes)")
        print()
        
        inicio_teste = time.time()
        restart_count_anterior = 0
        
        for i in range(24):  # 24 * 5s = 2 minutos
            time.sleep(5)
            
            # Verifica quantos restarts ocorreram
            restart_count_atual = sistema.dados_sistema['thread_restarts']['trading']
            
            if restart_count_atual > restart_count_anterior:
                print(f"🔄 RESTART DETECTADO: Thread Trading reiniciou ({restart_count_atual} restarts total)")
                restart_count_anterior = restart_count_atual
            
            # Status das threads
            if hasattr(sistema, 'thread_principal') and sistema.thread_principal:
                status = "🟢 Ativo" if sistema.running else "🔴 Parado"
                print(f"📊 Status sistema: {status} | Restarts: {restart_count_atual} | Tempo: {i*5}s")
            
            if restart_count_atual >= 3:
                print("✅ Teste bem-sucedido: Sistema reiniciou múltiplas vezes conforme esperado")
                break
        
        # Para o sistema
        print()
        print("🛑 Parando sistema de teste...")
        sistema.parar_sistema()
        
        # Aguarda finalização
        time.sleep(5)
        
        # Relatório final
        print()
        print("=" * 80)
        print("📊 RELATÓRIO FINAL DO TESTE")
        print("=" * 80)
        print(f"⏰ Duração do teste: {time.time() - inicio_teste:.1f}s")
        print(f"🔄 Total de restarts: {sistema.dados_sistema['thread_restarts']['trading']}")
        
        if sistema.dados_sistema['thread_restarts']['ultimo_restart']:
            ultimo = sistema.dados_sistema['thread_restarts']['ultimo_restart']
            print(f"🕒 Último restart: {ultimo.strftime('%H:%M:%S')}")
        
        print(f"📝 Total de logs: {len(sistema.logs)}")
        
        # Verifica se o teste foi bem-sucedido
        if sistema.dados_sistema['thread_restarts']['trading'] >= 2:
            print("✅ TESTE PASSOU: Sistema de auto-restart funcionando corretamente")
            resultado = True
        else:
            print("❌ TESTE FALHOU: Sistema não reiniciou conforme esperado")
            resultado = False
        
        print()
        print("📋 Últimos 10 logs do sistema:")
        for log in sistema.logs[-10:]:
            print(f"   {log}")
            
        return resultado
        
    except Exception as e:
        print(f"❌ ERRO durante o teste: {str(e)}")
        return False
        
    finally:
        # Restaura backup
        restaurar_backup(backup_name)
        print()
        print("🧹 Limpeza concluída")

if __name__ == "__main__":
    print("🧪 Iniciando teste de auto-restart do sistema de trading...")
    print()
    
    try:
        sucesso = teste_auto_restart()
        
        print()
        print("=" * 80)
        if sucesso:
            print("🎉 TESTE CONCLUÍDO COM SUCESSO!")
            print("   O sistema de auto-restart está funcionando corretamente.")
            print("   A thread Trading será reiniciada automaticamente quando necessário.")
        else:
            print("⚠️ TESTE APRESENTOU PROBLEMAS")
            print("   Verifique os logs acima para mais detalhes.")
        
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n🛑 Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado no teste: {str(e)}")
