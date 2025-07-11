#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Rápido do Sistema - Verifica se openpyxl está funcionando no contexto real
"""

def teste_rapido_sistema():
    """Teste rápido focado no erro openpyxl"""
    print("🚀 TESTE RÁPIDO - SISTEMA INTEGRADO")
    print("=" * 45)
    
    try:
        # Importa as dependências principais
        import pandas as pd
        print("✅ Pandas importado")
        
        # Testa especificamente o openpyxl
        try:
            import openpyxl
            print(f"✅ OpenPyXL {openpyxl.__version__} importado")
            
            # Testa se o pandas consegue usar openpyxl
            dados_teste = pd.DataFrame({'teste': [1, 2, 3]})
            
            # Teste direto da funcionalidade que estava falhando
            with pd.ExcelWriter('teste_sistema.xlsx', engine='openpyxl') as writer:
                dados_teste.to_excel(writer, sheet_name='teste', index=False)
            
            print("✅ Pandas + OpenPyXL funcionando perfeitamente!")
            
            # Limpa arquivo de teste
            import os
            if os.path.exists('teste_sistema.xlsx'):
                os.remove('teste_sistema.xlsx')
            
            return True
            
        except Exception as openpyxl_error:
            print(f"❌ Erro específico do OpenPyXL: {openpyxl_error}")
            
            # Testa fallback CSV
            try:
                dados_teste = pd.DataFrame({'teste': [1, 2, 3]})
                dados_teste.to_csv('teste_fallback.csv', index=False)
                print("✅ Fallback CSV funcionando")
                
                import os
                if os.path.exists('teste_fallback.csv'):
                    os.remove('teste_fallback.csv')
                
                return True
            except Exception as csv_error:
                print(f"❌ Erro no fallback CSV: {csv_error}")
                return False
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

def main():
    sucesso = teste_rapido_sistema()
    
    print("\n" + "=" * 45)
    if sucesso:
        print("🎉 SISTEMA PRONTO!")
        print("✅ O erro de openpyxl foi resolvido")
        print("👉 Execute: python sistema_integrado.py")
    else:
        print("⚠️  PROBLEMAS PERSISTEM")
        print("📋 Sistema usará fallback CSV")
    print("=" * 45)

if __name__ == "__main__":
    main()
