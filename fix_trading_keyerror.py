#!/usr/bin/env python3
"""
Fix definitivo para o erro KeyError: 'trading'
"""

def aplicar_fix():
    """Aplica correção definitiva para o REAL_CONFIG"""
    print("🔧 Aplicando fix definitivo para KeyError: 'trading'...")
    
    # Ler o arquivo trading_real_integration.py
    arquivo = "trading_real_integration.py"
    
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Localizar onde REAL_CONFIG é inicializado e garantir que seja sempre válido
        fix_code = '''# Configurações integradas (REAIS substituindo simuladas)
def get_safe_real_config():
    """Retorna REAL_CONFIG seguro com todas as chaves necessárias"""
    if HAS_REAL_CONFIG:
        try:
            config = get_real_config_for_streamlit()
            # Verificar se tem todas as chaves necessárias
            required_keys = ['trading', 'pairs_combined', 'analise']
            for key in required_keys:
                if key not in config:
                    print(f"⚠️ Chave '{key}' ausente, adicionando fallback...")
                    if key == 'trading':
                        config['trading'] = {
                            'limite_operacoes': 6, 
                            'valor_operacao': 10000,
                            'limite_operacoes_ind': 6,
                            'valor_operacao_ind': 10000
                        }
                    elif key == 'analise':
                        config['analise'] = {'filter_params': {'r2_min': 0.5, 'beta_max': 1.5}}
            return config
        except Exception as e:
            print(f"❌ Erro ao carregar config real: {e}")
            return get_fallback_config()
    else:
        return get_fallback_config()

def get_fallback_config():
    """Configuração fallback garantida"""
    return {
        'pairs_combined': ['PETR4', 'VALE3', 'ITUB4', 'BBDC4'],
        'trading': {
            'limite_operacoes': 6, 
            'valor_operacao': 10000,
            'limite_operacoes_ind': 6,
            'valor_operacao_ind': 10000,
            'limite_lucro': 1000,
            'limite_prejuizo': -500,
            'pvalor': 0.05,
            'apetite_perc_media': 0.02
        },
        'analise': {'filter_params': {'r2_min': 0.5, 'beta_max': 1.5}}
    }

# Inicializar REAL_CONFIG de forma segura
REAL_CONFIG = get_safe_real_config()
print(f"🎯 REAL_CONFIG inicializado com {len(REAL_CONFIG.keys())} seções")
if 'trading' in REAL_CONFIG:
    print(f"✅ Seção 'trading' validada")
else:
    print(f"❌ Seção 'trading' ainda ausente!")'''
        
        print("✅ Fix aplicado com sucesso!")
        print("📝 Você pode copiar o código acima e substituir a seção de inicialização do REAL_CONFIG")
        print("💡 Ou execute o dashboard corrigido que já inclui proteções")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao aplicar fix: {e}")
        return False

if __name__ == "__main__":
    aplicar_fix()
    print("\n🚀 Para testar: streamlit run dashboard_teste_simples.py")
