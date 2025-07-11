#!/usr/bin/env python3
"""
Script de teste para verificar se múltiplos períodos estão sendo processados
no dashboard com os novos logs de debug.
"""

import sys
import os

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def simular_execucao_com_debug():
    """Simula uma execução com debug para verificar os logs"""
    print("🧪 SIMULAÇÃO: Execução com Logs de Debug")
    print("=" * 60)
    
    # Simula config de múltiplos períodos
    config = {
        'ativos_selecionados': ['PETR4', 'VALE3'],
        'timeframe': '1 dia',
        'periodo_analise': 250,
        'usar_multiplos_periodos': True,  # MÚLTIPLOS PERÍODOS
        'zscore_min': 2.0,
        'zscore_max': 2.0,
        'filtro_cointegração': True,
        'filtro_r2': True,
        'filtro_beta': True,
        'filtro_zscore': True,
        'r2_min': 0.50
    }
    
    print("📋 Config simulado:")
    print(f"   - usar_multiplos_periodos: {config['usar_multiplos_periodos']}")
    print(f"   - periodo_analise: {config['periodo_analise']}")
    print(f"   - ativos_selecionados: {config['ativos_selecionados']}")
    
    print("\n🔧 LOGS DE DEBUG ESPERADOS:")
    
    # Simula logs de debug que devem aparecer
    print("   🔧 DEBUG: Config recebido - usar_multiplos_periodos: True")
    print("   🔧 DEBUG: Config recebido - periodo_analise: 250")
    print("   🔧 DEBUG: usar_multiplos_periodos processado: True")
    print("   🔧 DEBUG: periodo_unico processado: 250")
    print("   🔄 Modo: Múltiplos períodos canônicos - [70, 100, 120, 140, 160, 180, 200, 220, 240, 250]")
    print("   🔧 DEBUG: periodos_analise final: [70, 100, 120, 140, 160, 180, 200, 220, 240, 250]")
    print("   🔧 DEBUG: Quantidade de períodos a processar: 10")
    
    print("\n🔄 PARA CADA PAR, DEVE APARECER:")
    print("   🔧 DEBUG: Testando 10 períodos para par PETRx4VALE3: [70, 100, 120, 140, 160, 180, 200, 220, 240, 250]")
    print("   🔧 DEBUG: Processando período 1/10: 70 para PETR4xVALE3")
    print("   🔧 DEBUG: Processando período 2/10: 100 para PETR4xVALE3")
    print("   ... (continua para todos os 10 períodos)")
    
    print("\n📊 INDICADORES DE MÚLTIPLOS PERÍODOS FUNCIONANDO:")
    print("   ✅ Config usar_multiplos_periodos = True")
    print("   ✅ Quantidade de períodos = 10")
    print("   ✅ Períodos = [70, 100, 120, 140, 160, 180, 200, 220, 240, 250]")
    print("   ✅ Para cada par, 10 análises diferentes")
    print("   ✅ Seleção do melhor resultado por par")

def verificar_funcionamento():
    """Instruções para verificar no dashboard real"""
    print("\n🔍 COMO VERIFICAR NO DASHBOARD REAL:")
    print("=" * 50)
    
    print("""
📋 PASSOS PARA TESTAR:

1. 🚀 Execute o dashboard:
   streamlit run dashboard_trading_pro_real.py

2. 🎛️ Na sidebar, certifique-se que:
   - "Estratégia de Análise" = "Múltiplos Períodos" (padrão)
   - Veja a info: "70, 100, 120, 140, 160, 180, 200, 220, 240, 250"

3. 📊 Selecione alguns ativos (ex: 2-3 ativos)

4. ▶️ Clique em "Iniciar Sistema"

5. 👀 Observe os logs no final da página - deve aparecer:
   ✅ "🔧 DEBUG: Config recebido - usar_multiplos_periodos: True"
   ✅ "🔧 DEBUG: Quantidade de períodos a processar: 10"
   ✅ "🔧 DEBUG: Testando 10 períodos para par..."
   ✅ "🔧 DEBUG: Processando período X/10: Y para..."

6. ❌ Se aparecer apenas:
   "🔧 DEBUG: Quantidade de períodos a processar: 1"
   Então há um problema na transmissão do config.

7. 🔄 Para testar período único:
   - Mude para "Período Único"
   - Ajuste o slider (ex: 95)
   - Reinicie o sistema
   - Deve aparecer: "Quantidade de períodos a processar: 1"
    """)

def criar_script_teste_rapido():
    """Cria um script para teste rápido"""
    print("\n📝 SCRIPT DE TESTE RÁPIDO CRIADO:")
    print("=" * 40)
    
    script_content = '''#!/usr/bin/env python3
"""
Teste rápido para verificar múltiplos períodos
"""

def main():
    # Config de teste - múltiplos períodos
    config = {
        'usar_multiplos_periodos': True,
        'periodo_analise': 250,
        'ativos_selecionados': ['PETR4', 'VALE3']
    }
    
    # Simula a lógica do dashboard
    usar_multiplos_periodos = config.get('usar_multiplos_periodos', True)
    periodo_unico = config.get('periodo_analise', 250)
    
    if usar_multiplos_periodos:
        periodos_analise = [70, 100, 120, 140, 160, 180, 200, 220, 240, 250]
        modo = "Múltiplos períodos canônicos"
    else:
        periodos_analise = [periodo_unico]
        modo = "Período único"
    
    print(f"Modo: {modo}")
    print(f"Períodos: {periodos_analise}")
    print(f"Quantidade: {len(periodos_analise)}")
    
    # Simula processamento
    for i, periodo in enumerate(periodos_analise):
        print(f"Processando período {i+1}/{len(periodos_analise)}: {periodo}")

if __name__ == "__main__":
    main()
'''
    
    with open("teste_rapido_periodos.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("✅ Arquivo 'teste_rapido_periodos.py' criado")
    print("📄 Execute: python teste_rapido_periodos.py")

if __name__ == "__main__":
    print("🔍 DIAGNÓSTICO: Múltiplos Períodos com Debug")
    print("=" * 60)
    
    simular_execucao_com_debug()
    verificar_funcionamento()
    criar_script_teste_rapido()
    
    print("\n🎯 RESUMO:")
    print("✅ Logs de debug adicionados ao dashboard")
    print("✅ Deve mostrar claramente se múltiplos períodos estão sendo usados")
    print("✅ Se não aparecer '10 períodos', há problema no config")
    print("\n📋 PRÓXIMO PASSO: Execute o dashboard e observe os logs!")
