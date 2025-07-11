#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Específico de Keras - Verifica se o Keras está funcionando
"""

def testar_keras():
    """Testa todas as formas possíveis de importar Keras"""
    print("🧠 TESTANDO KERAS...")
    
    # Método 1: Keras independente
    try:
        import keras
        print(f"✅ Keras independente: {keras.__version__}")
        return True, keras
    except ImportError:
        print("⚠️  Keras independente não encontrado")
    
    # Método 2: Keras do TensorFlow
    try:
        import tensorflow as tf
        from tensorflow import keras
        print(f"✅ TensorFlow: {tf.__version__}")
        print(f"✅ Keras do TensorFlow: {keras.__version__}")
        return True, keras
    except ImportError as e:
        print(f"❌ TensorFlow/Keras falhou: {e}")
        return False, None

def testar_funcionalidades_keras(keras):
    """Testa funcionalidades básicas do Keras"""
    if keras is None:
        print("❌ Keras não disponível para testes")
        return False
    
    try:
        # Teste básico de criação de modelo
        from keras.models import Sequential
        from keras.layers import Dense
        
        model = Sequential([
            Dense(10, activation='relu', input_shape=(5,)),
            Dense(1, activation='sigmoid')
        ])
        
        print("✅ Criação de modelo Sequential funcionando")
        
        # Teste de métricas
        mse = keras.metrics.MeanSquaredError()
        print("✅ Métricas do Keras funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nas funcionalidades Keras: {e}")
        return False

def main():
    print("🎯 TESTE ESPECÍFICO DE KERAS")
    print("=" * 40)
    
    sucesso_import, keras_module = testar_keras()
    
    if sucesso_import:
        sucesso_funcional = testar_funcionalidades_keras(keras_module)
        
        if sucesso_funcional:
            print("\n🎉 KERAS TOTALMENTE FUNCIONAL!")
            print("✅ Modelos de IA podem ser carregados")
        else:
            print("\n⚠️  KERAS PARCIALMENTE FUNCIONAL")
            print("✅ Importação OK, mas funcionalidades limitadas")
    else:
        print("\n❌ KERAS NÃO DISPONÍVEL")
        print("📋 Sistema continuará sem funcionalidades de IA")
    
    print("=" * 40)

if __name__ == "__main__":
    main()
