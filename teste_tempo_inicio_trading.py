#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar quanto tempo demora para o trading de zscores iniciar
após o sistema integrado ser iniciado.
"""

import time
import threading
from datetime import datetime
import sys
import os

# Adiciona o diretório atual ao path para importar módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def teste_aguardar_proximo_minuto():
    """Testa a função aguardar_proximo_minuto para ver quanto tempo ela demora."""
    print(f"[TESTE] Iniciando teste de aguardar_proximo_minuto às {datetime.now().strftime('%H:%M:%S')}")
    
    def aguardar_proximo_minuto():
        """Aguarda até o início do próximo minuto."""
        inicio = time.time()
        while True:
            # Obtém o segundo atual
            segundo_atual = datetime.now().second
            # Se estivermos no início de um novo minuto, saia do loop
            if segundo_atual == 0:
                break
            # Aguarda 1 segundo antes de verificar novamente
            time.sleep(1)
        
        fim = time.time()
        tempo_espera = fim - inicio
        print(f"[TESTE] aguardar_proximo_minuto() demorou {tempo_espera:.2f} segundos")
        return tempo_espera
    
    return aguardar_proximo_minuto()

def teste_simulacao_horario_app():
    """Testa o comportamento do sistema em diferentes horários."""
    print(f"\n[TESTE] Simulando verificações de horário...")
    
    # Configurações do sistema (copiadas do calculo_entradas_v55.py)
    inicia_app = 8
    finaliza_app = 24
    inicia_pregao = 8
    finaliza_pregao = 17
    
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    
    print(f"Horário atual: {current_hour:02d}:{current_minute:02d}")
    print(f"Horário de funcionamento do app: {inicia_app}h - {finaliza_app}h")
    print(f"Horário de pregão: {inicia_pregao}h - {finaliza_pregao}h")
    
    if inicia_app <= current_hour < finaliza_app:
        print("✅ Sistema DENTRO do horário de funcionamento do app")
        
        if inicia_pregao <= current_hour < finaliza_pregao:
            print("✅ Sistema DENTRO do horário de pregão - TRADING ATIVO")
        else:
            print("⚠️ Sistema FORA do horário de pregão - TRADING INATIVO")
    else:
        print("❌ Sistema FORA do horário de funcionamento - HIBERNANDO")
        tempo_hibernacao = 900  # 15 minutos
        print(f"Tempo de hibernação: {tempo_hibernacao} segundos ({tempo_hibernacao/60:.1f} minutos)")

def teste_sistema_integrado_rapido():
    """Testa se o sistema integrado consegue executar o calculo_entradas_v55.py rapidamente."""
    print(f"\n[TESTE] Testando execução do sistema integrado...")
    
    try:
        import sistema_integrado
        print("✅ Módulo sistema_integrado importado com sucesso")
        
        # Verifica se as classes estão disponíveis
        if hasattr(sistema_integrado, 'SistemaIntegrado'):
            print("✅ Classe SistemaIntegrado encontrada")
            
            # Cria uma instância para teste
            sistema = sistema_integrado.SistemaIntegrado()
            print(f"✅ Instância criada. Estado inicial: {sistema.sistema_ativo}")
            
            # Verifica se o método de execução está disponível
            if hasattr(sistema, 'executar_sistema_original'):
                print("✅ Método executar_sistema_original encontrado")
                print("ℹ️ O sistema pode executar o calculo_entradas_v55.py")
            else:
                print("❌ Método executar_sistema_original não encontrado")
                
        else:
            print("❌ Classe SistemaIntegrado não encontrada")
            
    except ImportError as e:
        print(f"❌ Erro ao importar sistema_integrado: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def main():
    """Função principal de teste."""
    print("=" * 60)
    print("TESTE DE TEMPO DE INÍCIO DO TRADING DE ZSCORES")
    print("=" * 60)
    
    # Teste 1: Tempo de espera até próximo minuto
    print("\n1. TESTE: Tempo de espera até próximo minuto")
    tempo_espera = teste_aguardar_proximo_minuto()
    
    # Teste 2: Verificação de horários
    print("\n2. TESTE: Verificação de horários de funcionamento")
    teste_simulacao_horario_app()
    
    # Teste 3: Sistema integrado
    print("\n3. TESTE: Sistema integrado")
    teste_sistema_integrado_rapido()
    
    # Análise final
    print("\n" + "=" * 60)
    print("ANÁLISE DOS TEMPOS DE INÍCIO")
    print("=" * 60)
    
    print(f"📊 RESUMO:")
    print(f"   • Tempo até próximo minuto: {tempo_espera:.2f}s (máximo: 60s)")
    print(f"   • Horário atual: {datetime.now().strftime('%H:%M:%S')}")
    
    now = datetime.now()
    inicia_app = 8
    finaliza_app = 24
    inicia_pregao = 8
    finaliza_pregao = 17
    
    if inicia_app <= now.hour < finaliza_app:
        if inicia_pregao <= now.hour < finaliza_pregao:
            print(f"   • Status: TRADING ATIVO ✅")
            print(f"   • Tempo estimado para início: {tempo_espera:.2f}s")
        else:
            print(f"   • Status: FORA DO HORÁRIO DE PREGÃO ⚠️")
            print(f"   • Próximo pregão: {inicia_pregao}:00 de amanhã")
    else:
        print(f"   • Status: SISTEMA HIBERNANDO ❌")
        print(f"   • Próximo funcionamento: {inicia_app}:00")
    
    print("\n🔍 CONCLUSÕES:")
    print("   1. O sistema espera até o próximo minuto para iniciar")
    print("   2. Após iniciar, verifica horários de funcionamento")
    print("   3. Se dentro do horário de pregão, inicia trading imediatamente")
    print("   4. Se fora do horário, hiberna por 15 minutos")
    
    print(f"\n⏱️ TEMPO TOTAL ESTIMADO PARA INÍCIO DO TRADING:")
    if inicia_pregao <= now.hour < finaliza_pregao:
        print(f"   • Dentro do pregão: {tempo_espera:.2f}s + ~5s (processamento)")
        print(f"   • TOTAL: ~{tempo_espera + 5:.0f} segundos")
    else:
        print(f"   • Fora do pregão: Hibernando até {inicia_pregao}:00")

if __name__ == "__main__":
    main()
