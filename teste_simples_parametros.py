#!/usr/bin/env python3
"""
Teste simples do sistema de parâmetros dinâmicos
"""

print("🧪 Iniciando teste simples...")

try:
    import parametros_dinamicos
    print("✅ parametros_dinamicos importado")
    
    # Testa carregamento
    params = parametros_dinamicos.carregar_config_dinamica()
    print(f"✅ Parâmetros carregados: {len(params)} chaves")
    
    # Testa salvamento
    config_teste = {
        'max_posicoes': 7,
        'valor_operacao': 12000,
        'r2_min': 0.6
    }
    
    resultado = parametros_dinamicos.salvar_config_dashboard(config_teste)
    print(f"✅ Salvamento: {resultado}")
    
    # Testa verificação
    alterado = parametros_dinamicos.verificar_parametros_alterados()
    print(f"✅ Alterações detectadas: {alterado}")
    
    print("✅ Teste concluído com sucesso!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
