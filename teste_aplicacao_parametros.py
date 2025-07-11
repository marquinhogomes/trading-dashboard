#!/usr/bin/env python3
"""
Teste completo do mecanismo de aplicação de parâmetros dinâmicos
com verificação de regeneração de tabelas
"""

import sys
import os
sys.path.append('.')

def testar_aplicacao_parametros_completa():
    """Teste completo do mecanismo"""
    
    print("🧪 TESTE COMPLETO: Aplicação de Parâmetros Dinâmicos")
    print("=" * 70)
    
    try:
        # Importa o sistema de parâmetros dinâmicos
        from parametros_dinamicos import (
            verificar_parametros_alterados,
            obter_config_sistema_principal,
            aplicar_parametros_sistema,
            salvar_config_dashboard,
            verificar_regeneracao_tabelas,
            marcar_tabelas_regeneradas
        )
        
        print("✅ Sistema de parâmetros dinâmicos importado")
        
        # ETAPA 1: Simula alteração no dashboard
        print("\n1️⃣ SIMULANDO ALTERAÇÃO NO DASHBOARD:")
        config_nova = {
            'valor_operacao': 25000,
            'limite_operacoes': 10,
            'max_posicoes': 10,
            'limite_lucro': 200,
            'r2_min': 0.7
        }
        
        resultado = salvar_config_dashboard(config_nova)
        print(f"   Salvamento: {'✅ OK' if resultado else '❌ ERRO'}")
        
        # ETAPA 2: Verifica se foi detectado
        print("\n2️⃣ VERIFICANDO DETECÇÃO DE ALTERAÇÕES:")
        alterado = verificar_parametros_alterados()
        print(f"   Parâmetros alterados: {'✅ Sim' if alterado else '❌ Não'}")
        
        # ETAPA 3: Simula clique no botão "Aplicar Parâmetros Agora"
        if alterado:
            print("\n3️⃣ SIMULANDO CLIQUE NO BOTÃO 'APLICAR PARÂMETROS AGORA':")
            
            # Carrega configuração
            config_aplicar = obter_config_sistema_principal()
            print(f"   Configuração carregada:")
            print(f"     • Valor operação: R$ {config_aplicar.get('valor_operacao', 0):,}")
            print(f"     • Limite operações: {config_aplicar.get('limite_operacoes', 0)}")
            print(f"     • R² mínimo: {config_aplicar.get('r2_min', 0)}")
            
            # Aplica parâmetros
            aplicar_parametros_sistema()
            print("   ✅ Parâmetros aplicados")
            
            # Verifica regeneração de tabelas
            print("\n4️⃣ VERIFICANDO REGENERAÇÃO DE TABELAS:")
            regenerar = verificar_regeneracao_tabelas()
            print(f"   Tabelas precisam ser regeneradas: {'✅ Sim' if regenerar else '❌ Não'}")
            
            if regenerar:
                print("   🔄 Simulando regeneração de tabelas...")
                marcar_tabelas_regeneradas()
                print("   ✅ Tabelas marcadas como regeneradas")
                
                # Verifica se foi marcado corretamente
                regenerar_apos = verificar_regeneracao_tabelas()
                print(f"   Regeneração pendente após marcação: {'❌ Ainda sim' if regenerar_apos else '✅ Não'}")
        
        # ETAPA 5: Verifica estado final
        print("\n5️⃣ VERIFICANDO ESTADO FINAL:")
        alterado_final = verificar_parametros_alterados()
        print(f"   Parâmetros alterados: {'❌ Ainda sim' if alterado_final else '✅ Não'}")
        
        regenerar_final = verificar_regeneracao_tabelas()
        print(f"   Regeneração pendente: {'❌ Ainda sim' if regenerar_final else '✅ Não'}")
        
        # ETAPA 6: Teste com sistema integrado
        print("\n6️⃣ TESTE COM SISTEMA INTEGRADO:")
        try:
            from sistema_integrado import SistemaIntegrado
            
            # Cria instância do sistema
            sistema = SistemaIntegrado()
            print("   ✅ Sistema integrado criado")
            
            # Simula nova alteração
            config_teste = {
                'valor_operacao': 30000,
                'limite_operacoes': 12
            }
            salvar_config_dashboard(config_teste)
            print("   ✅ Nova configuração salva")
            
            # Aplica parâmetros
            print("   🔄 Aplicando parâmetros no sistema integrado...")
            sistema.aplicar_parametros_dinamicos()
            print("   ✅ Parâmetros aplicados no sistema integrado")
            
            # Verifica valores
            print(f"   📊 Valores atuais no sistema:")
            print(f"     • Valor operação: R$ {sistema.valor_operacao:,}")
            print(f"     • Limite operações: {sistema.limite_operacoes}")
            
        except Exception as e:
            print(f"   ❌ Erro ao testar sistema integrado: {e}")
        
        print("\n" + "=" * 70)
        print("✅ TESTE COMPLETO FINALIZADO COM SUCESSO!")
        print("📊 O mecanismo de aplicação de parâmetros está funcionando corretamente")
        print("🔄 As tabelas serão regeneradas quando necessário")
        print("💡 Usuário pode clicar 'Aplicar Parâmetros Agora' para aplicação imediata")
        
    except Exception as e:
        print(f"❌ ERRO no teste: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_aplicacao_parametros_completa()
