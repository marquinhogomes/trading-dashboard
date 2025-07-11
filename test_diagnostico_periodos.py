#!/usr/bin/env python3
"""
Script de teste para diagnóstico da transmissão de configuração
de múltiplos períodos entre interface e lógica de análise.
"""

def test_config_transmission():
    """Testa transmissão completa da configuração"""
    print("🔍 DIAGNÓSTICO: Transmissão de Configuração de Períodos")
    print("=" * 60)
    
    print("\n📋 1. TESTE DA INTERFACE (render_sidebar)")
    
    # Simula a interface do sidebar
    print("Interface do sidebar:")
    usar_multiplos_periodos_radio = "Múltiplos Períodos"  # Default (index=1)
    periodo_analise_slider = 250  # Valor padrão quando oculto
    
    print(f"   - Radio button: '{usar_multiplos_periodos_radio}'")
    print(f"   - Slider valor (quando oculto): {periodo_analise_slider}")
    
    # Simula criação do config
    config = {
        'periodo_analise': periodo_analise_slider,
        'usar_multiplos_periodos': usar_multiplos_periodos_radio == "Múltiplos Períodos",
        'ativos_selecionados': ['PETR4', 'VALE3'],
        'timeframe': '1 dia'
    }
    
    print(f"   - Config gerado: usar_multiplos_periodos = {config['usar_multiplos_periodos']}")
    print(f"   - Config gerado: periodo_analise = {config['periodo_analise']}")
    
    print("\n🔄 2. TESTE DA FUNÇÃO ANÁLISE (executar_analise_real)")
    
    # Simula lógica da função executar_analise_real
    usar_multiplos_periodos = config.get('usar_multiplos_periodos', True)
    periodo_unico = config.get('periodo_analise', 250)
    
    print(f"   - Valor recebido usar_multiplos_periodos: {usar_multiplos_periodos}")
    print(f"   - Valor recebido periodo_unico: {periodo_unico}")
    
    if usar_multiplos_periodos:
        periodos_analise = [70, 100, 120, 140, 160, 180, 200, 220, 240, 250]
        modo = "Múltiplos períodos canônicos"
    else:
        periodos_analise = [periodo_unico]
        modo = "Período único"
    
    print(f"   - Modo detectado: {modo}")
    print(f"   - Períodos finais: {periodos_analise}")
    
    print("\n✅ 3. VALIDAÇÃO")
    esperado_multiplos = True
    esperado_periodos = [70, 100, 120, 140, 160, 180, 200, 220, 240, 250]
    
    resultado_correto = (
        usar_multiplos_periodos == esperado_multiplos and
        periodos_analise == esperado_periodos
    )
    
    if resultado_correto:
        print("✅ CORRETO: Múltiplos períodos sendo aplicados corretamente")
        return True
    else:
        print("❌ PROBLEMA: Múltiplos períodos NÃO sendo aplicados")
        print(f"   Esperado usar_multiplos_periodos: {esperado_multiplos}")
        print(f"   Recebido usar_multiplos_periodos: {usar_multiplos_periodos}")
        print(f"   Esperado períodos: {esperado_periodos}")
        print(f"   Recebido períodos: {periodos_analise}")
        return False

def test_config_transmission_periodo_unico():
    """Testa transmissão para período único"""
    print("\n🔍 DIAGNÓSTICO: Período Único")
    print("=" * 40)
    
    # Simula seleção de período único
    usar_multiplos_periodos_radio = "Período Único"
    periodo_analise_slider = 95  # Valor do slider quando visível
    
    config = {
        'periodo_analise': periodo_analise_slider,
        'usar_multiplos_periodos': usar_multiplos_periodos_radio == "Múltiplos Períodos",
        'ativos_selecionados': ['PETR4', 'VALE3'],
        'timeframe': '1 dia'
    }
    
    print(f"   - Radio button: '{usar_multiplos_periodos_radio}'")
    print(f"   - Config usar_multiplos_periodos: {config['usar_multiplos_periodos']}")
    
    # Simula lógica
    usar_multiplos_periodos = config.get('usar_multiplos_periodos', True)
    periodo_unico = config.get('periodo_analise', 250)
    
    if usar_multiplos_periodos:
        periodos_analise = [70, 100, 120, 140, 160, 180, 200, 220, 240, 250]
        modo = "Múltiplos períodos canônicos"
    else:
        periodos_analise = [periodo_unico]
        modo = "Período único"
    
    print(f"   - Períodos finais: {periodos_analise}")
    print(f"   - Modo: {modo}")
    
    esperado = [95]
    correto = periodos_analise == esperado
    print(f"   - ✅ Correto: {correto}")
    
    return correto

def test_debug_logs():
    """Sugere logs para debug no dashboard real"""
    print("\n🐛 SUGESTÕES PARA DEBUG NO DASHBOARD REAL:")
    print("=" * 50)
    
    print("""
📝 Adicione estes logs na função executar_analise_real para debug:

1. Logo após receber o config:
   self.log(f"🔧 DEBUG: Config recebido - usar_multiplos_periodos: {config.get('usar_multiplos_periodos')}")
   self.log(f"🔧 DEBUG: Config recebido - periodo_analise: {config.get('periodo_analise')}")

2. Logo após definir periodos_analise:
   self.log(f"🔧 DEBUG: usar_multiplos_periodos processado: {usar_multiplos_periodos}")
   self.log(f"🔧 DEBUG: periodos_analise final: {periodos_analise}")
   self.log(f"🔧 DEBUG: Quantidade de períodos: {len(periodos_analise)}")

3. No loop de análise, para confirmar quantos períodos são processados:
   for i, periodo_atual in enumerate(periodos_analise):
       self.log(f"🔧 DEBUG: Processando período {i+1}/{len(periodos_analise)}: {periodo_atual}")
       # ... resto do loop
    """)

if __name__ == "__main__":
    print("🔍 DIAGNÓSTICO COMPLETO: MÚLTIPLOS PERÍODOS")
    print("=" * 60)
    
    # Testa múltiplos períodos
    resultado_multiplos = test_config_transmission()
    
    # Testa período único
    resultado_unico = test_config_transmission_periodo_unico()
    
    # Debug suggestions
    test_debug_logs()
    
    print("\n📊 RESUMO DO DIAGNÓSTICO:")
    print(f"✅ Múltiplos períodos: {'OK' if resultado_multiplos else 'PROBLEMA'}")
    print(f"✅ Período único: {'OK' if resultado_unico else 'PROBLEMA'}")
    
    if resultado_multiplos and resultado_unico:
        print("\n🎉 RESULTADO: Lógica da configuração está CORRETA")
        print("📋 Se múltiplos períodos não estão sendo usados, o problema pode ser:")
        print("   1. Na interface do dashboard (config não sendo criado correto)")
        print("   2. Na transmissão entre sidebar e sistema")
        print("   3. Logs não estão sendo exibidos")
        print("\n💡 SOLUÇÃO: Adicione logs de debug conforme sugerido acima")
    else:
        print("\n❌ RESULTADO: Há problemas na lógica")
        print("💡 SOLUÇÃO: Revisar e corrigir a lógica de configuração")
