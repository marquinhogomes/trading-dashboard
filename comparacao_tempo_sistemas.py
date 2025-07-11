#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demonstração da diferença de tempo entre sistema original e otimizado
"""

import time
from datetime import datetime
import sys
import os

def teste_sistema_original():
    """Simula o comportamento do sistema original com aguardar_proximo_minuto"""
    print("🔄 SISTEMA ORIGINAL - Com espera até próximo minuto")
    print(f"Início: {datetime.now().strftime('%H:%M:%S')}")
    
    inicio = time.time()
    
    # Simula aguardar_proximo_minuto()
    print("⏳ Aguardando próximo minuto...")
    while True:
        segundo_atual = datetime.now().second
        if segundo_atual == 0:
            break
        time.sleep(1)
    
    tempo_espera = time.time() - inicio
    print(f"✅ Trading iniciou após {tempo_espera:.2f} segundos")
    print(f"Fim: {datetime.now().strftime('%H:%M:%S')}")
    
    return tempo_espera

def teste_sistema_otimizado():
    """Simula o comportamento do sistema otimizado sem espera"""
    print("\n🚀 SISTEMA OTIMIZADO - Início imediato")
    print(f"Início: {datetime.now().strftime('%H:%M:%S')}")
    
    inicio = time.time()
    
    # Sistema otimizado: início imediato
    print("🚀 Iniciando trading imediatamente, sem esperar próximo minuto")
    time.sleep(0.1)  # Simula apenas o tempo de processamento
    
    tempo_inicio = time.time() - inicio
    print(f"✅ Trading iniciou após {tempo_inicio:.2f} segundos")
    print(f"Fim: {datetime.now().strftime('%H:%M:%S')}")
    
    return tempo_inicio

def main():
    print("=" * 60)
    print("COMPARAÇÃO: SISTEMA ORIGINAL vs OTIMIZADO")
    print("=" * 60)
    
    # Teste 1: Sistema original
    tempo_original = teste_sistema_original()
    
    # Pequena pausa
    time.sleep(2)
    
    # Teste 2: Sistema otimizado
    tempo_otimizado = teste_sistema_otimizado()
    
    # Análise
    print("\n" + "=" * 60)
    print("ANÁLISE COMPARATIVA")
    print("=" * 60)
    
    print(f"⏰ Sistema Original: {tempo_original:.2f} segundos")
    print(f"🚀 Sistema Otimizado: {tempo_otimizado:.2f} segundos")
    
    economia = tempo_original - tempo_otimizado
    percentual = (economia / tempo_original) * 100 if tempo_original > 0 else 0
    
    print(f"\n💰 ECONOMIA DE TEMPO:")
    print(f"   • Redução: {economia:.2f} segundos")
    print(f"   • Percentual: {percentual:.1f}%")
    
    print(f"\n📊 CONCLUSÕES:")
    if economia > 30:
        print(f"   ✅ Otimização SIGNIFICATIVA - Economia > 30s")
    elif economia > 10:
        print(f"   ✅ Otimização MODERADA - Economia > 10s")
    else:
        print(f"   ⚠️ Otimização MÍNIMA - Economia < 10s")
    
    print(f"   • O sistema otimizado elimina a espera desnecessária")
    print(f"   • Trading inicia imediatamente quando o sistema é iniciado")
    print(f"   • Ideal para horários de pregão ativo")
    
    # Recomendações baseadas no horário atual
    now = datetime.now()
    if 8 <= now.hour < 17:  # Horário de pregão
        print(f"\n🎯 RECOMENDAÇÃO ATUAL:")
        print(f"   • Horário: {now.strftime('%H:%M')} (PREGÃO ATIVO)")
        print(f"   • Use o SISTEMA OTIMIZADO para início imediato")
        print(f"   • Economia estimada: ~{economia:.0f} segundos")
    else:
        print(f"\n🎯 RECOMENDAÇÃO ATUAL:")
        print(f"   • Horário: {now.strftime('%H:%M')} (FORA DO PREGÃO)")
        print(f"   • Sistema hiberna até 08:00 independente da otimização")
        print(f"   • Otimização será efetiva no próximo pregão")

if __name__ == "__main__":
    main()
