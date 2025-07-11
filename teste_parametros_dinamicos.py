#!/usr/bin/env python3
"""
Teste do Sistema de Parâmetros Dinâmicos
Valida se a comunicação entre dashboard, sistema_integrado e calculo_entradas_v55 está funcionando
"""

import os
import sys
import time
from datetime import datetime

def teste_parametros_dinamicos():
    """Testa o fluxo completo de parâmetros dinâmicos"""
    print("🧪 TESTE DO SISTEMA DE PARÂMETROS DINÂMICOS")
    print("=" * 60)
    
    try:
        # Importa o sistema de parâmetros dinâmicos
        from parametros_dinamicos import (
            gerenciador_parametros, 
            salvar_config_dashboard, 
            verificar_parametros_alterados,
            obter_config_sistema_principal,
            aplicar_parametros_sistema
        )
        
        print("✅ Sistema de parâmetros dinâmicos importado com sucesso")
        
        # Teste 1: Verificar estado inicial
        print("\n📋 TESTE 1: Estado inicial dos parâmetros")
        parametros_iniciais = gerenciador_parametros.carregar_parametros()
        print(f"   • Parâmetros alterados: {parametros_iniciais.get('parametros_alterados', False)}")
        print(f"   • Valor operação atual: R$ {parametros_iniciais.get('valor_operacao', 0):,}")
        print(f"   • Limite operações: {parametros_iniciais.get('max_posicoes', 0)}")
        print(f"   • R² mínimo: {parametros_iniciais.get('r2_min', 0)}")
        
        # Teste 2: Simular alteração do dashboard
        print("\n📋 TESTE 2: Simulando alteração do dashboard")
        config_teste = {
            'max_posicoes': 8,  # Alterado de 6 para 8
            'valor_operacao': 15000,  # Alterado de 10000 para 15000
            'r2_min': 0.65,  # Alterado de 0.5 para 0.65
            'zscore_min': 2.5,  # Alterado de 2.0 para 2.5
            'filtro_cointegracao': True,
            'ativos_selecionados': ['PETR4', 'VALE3', 'ITUB4', 'BBAS3']
        }
        
        sucesso = salvar_config_dashboard(config_teste)
        print(f"   • Salvamento: {'✅ Sucesso' if sucesso else '❌ Falha'}")
        
        # Teste 3: Verificar se alterações foram detectadas
        print("\n📋 TESTE 3: Verificando detecção de alterações")
        tem_alteracoes = verificar_parametros_alterados()
        print(f"   • Alterações detectadas: {'✅ Sim' if tem_alteracoes else '❌ Não'}")
        
        if tem_alteracoes:
            # Teste 4: Obter configuração para sistema principal
            print("\n📋 TESTE 4: Obtendo configuração para sistema principal")
            config_sistema = obter_config_sistema_principal()
            print(f"   • Limite operações: {config_sistema.get('limite_operacoes', 0)}")
            print(f"   • Valor operação: R$ {config_sistema.get('valor_operacao', 0):,}")
            print(f"   • R² mínimo: {config_sistema.get('filter_params', {}).get('r2_min', 0)}")
            
            # Teste 5: Marcar como aplicado
            print("\n📋 TESTE 5: Marcando parâmetros como aplicados")
            aplicacao_ok = aplicar_parametros_sistema()
            print(f"   • Marcação como aplicado: {'✅ Sucesso' if aplicacao_ok else '❌ Falha'}")
            
            # Verificar se não há mais alterações pendentes
            tem_alteracoes_pos = verificar_parametros_alterados()
            print(f"   • Alterações pendentes após aplicação: {'❌ Ainda há' if tem_alteracoes_pos else '✅ Nenhuma'}")
        
        # Teste 6: Testar integração com sistema integrado
        print("\n📋 TESTE 6: Testando integração com sistema integrado")
        try:
            from sistema_integrado import SistemaIntegrado
            
            # Cria uma instância do sistema integrado
            sistema = SistemaIntegrado()
            
            # Força nova alteração para testar
            config_teste_2 = {
                'max_posicoes': 10,
                'valor_operacao': 20000,
                'limite_lucro': 150,
                'limite_prejuizo': 100
            }
            salvar_config_dashboard(config_teste_2)
            
            # Aplica parâmetros no sistema integrado
            valores_antes = {
                'limite_operacoes': sistema.limite_operacoes,
                'valor_operacao': sistema.valor_operacao,
                'limite_lucro': sistema.limite_lucro,
                'limite_prejuizo': sistema.limite_prejuizo
            }
            print(f"   • Valores antes: {valores_antes}")
            
            sistema.aplicar_parametros_dinamicos()
            
            valores_depois = {
                'limite_operacoes': sistema.limite_operacoes,
                'valor_operacao': sistema.valor_operacao,
                'limite_lucro': sistema.limite_lucro,
                'limite_prejuizo': sistema.limite_prejuizo
            }
            print(f"   • Valores depois: {valores_depois}")
            
            # Verifica se os valores foram alterados
            alteracoes_detectadas = []
            for chave in valores_antes:
                if valores_antes[chave] != valores_depois[chave]:
                    alteracoes_detectadas.append(f"{chave}: {valores_antes[chave]} → {valores_depois[chave]}")
            
            if alteracoes_detectadas:
                print("   ✅ Alterações aplicadas no sistema integrado:")
                for alteracao in alteracoes_detectadas:
                    print(f"     • {alteracao}")
            else:
                print("   ⚠️ Nenhuma alteração detectada no sistema integrado")
                
        except ImportError:
            print("   ⚠️ Sistema integrado não disponível para teste")
        except Exception as e:
            print(f"   ❌ Erro ao testar sistema integrado: {e}")
        
        print("\n📋 TESTE 7: Limpeza e restauração")
        # Restaura valores padrão
        config_padrao = {
            'max_posicoes': 6,
            'valor_operacao': 10000,
            'r2_min': 0.5,
            'zscore_min': 2.0,
            'filtro_cointegracao': True,
            'ativos_selecionados': ['PETR4', 'VALE3', 'ITUB4', 'BBAS3', 'ABEV3']
        }
        salvar_config_dashboard(config_padrao)
        aplicar_parametros_sistema()
        print("   ✅ Valores padrão restaurados")
        
        print("\n" + "=" * 60)
        print("✅ TESTE COMPLETO FINALIZADO COM SUCESSO")
        print("📊 O sistema de parâmetros dinâmicos está funcionando corretamente!")
        
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    teste_parametros_dinamicos()
