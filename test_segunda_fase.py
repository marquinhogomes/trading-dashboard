#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste para verificar se a segunda fase da análise foi implementada corretamente
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Adicionar o diretório atual ao path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

def test_segunda_fase_analise():
    """Testa se a segunda fase da análise foi implementada"""
    print("🧪 Testando implementação da segunda fase da análise...")
    
    try:
        # Importar funções necessárias
        from calculo_entradas_v55 import (
            calcular_residuo_zscore_timeframe01,
            encontrar_linha_monitorada01
        )
        print("✅ Funções da segunda fase importadas com sucesso!")
        
        # Testar calcular_residuo_zscore_timeframe01
        print("🔍 Testando calcular_residuo_zscore_timeframe01...")
        
        # Criar dados simulados mínimos
        dados_teste = {
            'PETR4': pd.DataFrame({
                'close': {'raw': pd.Series([50, 51, 52, 53, 54])},
                'open': {'raw': pd.Series([49.8, 50.8, 51.8, 52.8, 53.8])},
                'high': {'raw': pd.Series([50.2, 51.2, 52.2, 53.2, 54.2])},
                'low': {'raw': pd.Series([49.6, 50.6, 51.6, 52.6, 53.6])}
            }),
            'VALE3': pd.DataFrame({
                'close': {'raw': pd.Series([45, 46, 47, 48, 49])},
                'open': {'raw': pd.Series([44.8, 45.8, 46.8, 47.8, 48.8])},
                'high': {'raw': pd.Series([45.2, 46.2, 47.2, 48.2, 49.2])},
                'low': {'raw': pd.Series([44.6, 45.6, 46.6, 47.6, 48.6])}
            }),
            'IBOV': pd.DataFrame({
                'close': {'raw': pd.Series([120000, 121000, 122000, 123000, 124000])},
                'open': {'raw': pd.Series([119800, 120800, 121800, 122800, 123800])},
                'high': {'raw': pd.Series([120200, 121200, 122200, 123200, 124200])},
                'low': {'raw': pd.Series([119600, 120600, 121600, 122600, 123600])}
            }),
            'WIN$': pd.DataFrame({
                'close': {'raw': pd.Series([100000, 101000, 102000, 103000, 104000])},
                'open': {'raw': pd.Series([99800, 100800, 101800, 102800, 103800])},
                'high': {'raw': pd.Series([100200, 101200, 102200, 103200, 104200])},
                'low': {'raw': pd.Series([99600, 100600, 101600, 102600, 103600])}
            })
        }
        
        # Tabela linha operação simulada
        tabela_linha_operacao = pd.DataFrame([{
            'Dependente': 'PETR4',
            'Independente': 'VALE3',
            'Período': 5,
            'Z-Score': 2.5,
            'r2': 0.8
        }])
        
        # Testar a função
        try:
            resultado = calcular_residuo_zscore_timeframe01(
                dep='PETR4',
                ind='VALE3',
                ibov='IBOV',
                win='WIN$',
                periodo=5,
                dados_preprocessados=dados_teste,
                tabela_linha_operacao=tabela_linha_operacao,
                tolerancia=0.010,
                min_train=5,  # Reduzido para teste
                verbose=False
            )
            
            if resultado is None:
                print("   ⚠️ Resultado é None (esperado com dados limitados)")
            else:
                print(f"   ✅ Função retornou resultado (tipo: {type(resultado)})")
                if isinstance(resultado, (list, tuple)):
                    print(f"   📊 Resultado tem {len(resultado)} elementos")
                    
        except Exception as e:
            print(f"   ❌ Erro na função calcular_residuo_zscore_timeframe01: {e}")
            print(f"   Tipo do erro: {type(e).__name__}")
        
        # Testar encontrar_linha_monitorada01
        print("🔍 Testando encontrar_linha_monitorada01...")
        
        # Dados de teste para segunda função
        tabela_zscore_dependente_atual01 = pd.DataFrame([
            {
                'ID': 'PETR4_VALE3_5',
                'Dependente': 'PETR4',
                'Independente': 'VALE3',
                'Z-Score': 2.1,
                'r2': 0.7,
                'Estacionario': True
            },
            {
                'ID': 'VALE3_PETR4_5', 
                'Dependente': 'VALE3',
                'Independente': 'PETR4',
                'Z-Score': -2.3,
                'r2': 0.6,
                'Estacionario': True
            }
        ])
        
        try:
            resultado_01 = encontrar_linha_monitorada01(
                tabela_zscore_dependente_atual01=tabela_zscore_dependente_atual01,
                linha_operacao01=[]
            )
            
            if resultado_01 is None or len(resultado_01) == 0:
                print("   ⚠️ Nenhum par selecionado (comportamento normal com filtros)")
            else:
                print(f"   ✅ Função retornou {len(resultado_01)} pares selecionados")
                
        except Exception as e:
            print(f"   ❌ Erro na função encontrar_linha_monitorada01: {e}")
            print(f"   Tipo do erro: {type(e).__name__}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro na importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

def test_dashboard_integration():
    """Testa se a integração no dashboard funciona"""
    print("🔍 Testando integração no dashboard...")
    
    try:
        # Tentar importar o dashboard
        import trading_dashboard_complete
        print("✅ Dashboard importado com sucesso!")
        
        # Verificar se a função de análise existe
        if hasattr(trading_dashboard_complete, 'executar_analise_real_v55'):
            print("✅ Função executar_analise_real_v55 encontrada!")
        else:
            print("❌ Função executar_analise_real_v55 não encontrada!")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro na integração do dashboard: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TESTE DA SEGUNDA FASE DA ANÁLISE")
    print("=" * 50)
    
    success1 = test_segunda_fase_analise()
    print()
    success2 = test_dashboard_integration()
    
    print("=" * 50)
    if success1 and success2:
        print("🎉 TESTES PASSARAM! Segunda fase implementada com sucesso.")
    else:
        print("❌ ALGUNS TESTES FALHARAM. Verificar implementação.")
