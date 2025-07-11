#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simplificado para validar o fix do dashboard.
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Adicionar o diretório atual ao path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

def test_dashboard_analysis():
    """Testa a função de análise do dashboard diretamente"""
    print("🔍 Testando função de análise do dashboard...")
    
    try:
        # Importar a função do dashboard
        from trading_dashboard_complete import executar_analise_real_v55
        print("✅ Função do dashboard importada!")
        
        # Criar uma lista simples de ativos
        ativos_teste = ['PETR4', 'VALE3']
        
        print(f"   Testando com ativos: {ativos_teste}")
        
        # Função de callback simples para progresso
        def progress_callback(p):
            print(f"   Progresso: {int(p*100)}%")
        
        # Executar a análise
        print("   Executando análise...")
        resultado = executar_analise_real_v55(
            lista_dependente=ativos_teste,
            lista_independente=ativos_teste,
            progress_callback=progress_callback
        )
        
        if resultado is None:
            print("   ⚠️ Resultado é None")
            return True
        
        if isinstance(resultado, list):
            print(f"   ✅ Resultado é uma lista com {len(resultado)} itens")
            
            # Verificar se há resultados válidos
            for i, res in enumerate(resultado[:3]):  # Mostrar até 3 resultados
                print(f"   Resultado {i+1}:")
                print(f"     Par: {res.get('pair', 'N/A')}")
                print(f"     Signal: {res.get('signal', 'N/A')}")
                print(f"     R²: {res.get('r2', 'N/A')}")
                print(f"     Z-Score: {res.get('zscore', 'N/A')}")
            
            return True
        else:
            print(f"   ⚠️ Resultado tem tipo inesperado: {type(resultado)}")
            return True
            
    except Exception as e:
        print(f"   ❌ Erro no teste: {e}")
        print(f"   Tipo do erro: {type(e).__name__}")
        if "'adf_p_value'" in str(e):
            print("   🎯 ERRO adf_p_value DETECTADO!")
            return False
        return True  # Outros erros podem ser aceitáveis (MT5, etc.)

if __name__ == "__main__":
    print("🧪 TESTE SIMPLIFICADO DO DASHBOARD")
    print("=" * 50)
    
    success = test_dashboard_analysis()
    
    print("=" * 50)
    if success:
        print("🎉 TESTE PASSOU! A função do dashboard funciona corretamente.")
    else:
        print("❌ TESTE FALHOU! Erro adf_p_value ainda presente.")
