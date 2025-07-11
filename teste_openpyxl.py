#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de OpenPyXL - Verifica se o módulo está funcionando
"""

def testar_openpyxl():
    """Testa o módulo openpyxl"""
    print("📊 TESTANDO OPENPYXL...")
    
    try:
        import openpyxl
        print(f"✅ OpenPyXL {openpyxl.__version__}: Importação OK")
        
        # Teste de funcionalidade básica
        import pandas as pd
        import os
        
        # Cria dados de teste
        dados_teste = pd.DataFrame({
            'Par': ['PETR4 x VALE3', 'BBDC4 x ITUB4'],
            'Preco': [25.50, 32.10],
            'Volume': [1000, 1500],
            'Status': ['Compra', 'Venda']
        })
        
        # Teste de escrita Excel
        arquivo_teste = 'teste_openpyxl.xlsx'
        
        with pd.ExcelWriter(arquivo_teste, engine='openpyxl') as writer:
            dados_teste.to_excel(writer, sheet_name='Teste', index=False)
        
        print("✅ Escrita de arquivo Excel: OK")
        
        # Teste de leitura Excel
        dados_lidos = pd.read_excel(arquivo_teste, sheet_name='Teste')
        print(f"✅ Leitura de arquivo Excel: OK ({len(dados_lidos)} linhas)")
        
        # Limpa arquivo de teste
        if os.path.exists(arquivo_teste):
            os.remove(arquivo_teste)
            print("✅ Limpeza de arquivos: OK")
        
        return True
        
    except ImportError as e:
        print(f"❌ OpenPyXL não encontrado: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro no teste OpenPyXL: {e}")
        return False

def testar_fallback_csv():
    """Testa o fallback para CSV"""
    print("\n📄 TESTANDO FALLBACK CSV...")
    
    try:
        import pandas as pd
        import os
        
        # Cria dados de teste
        dados_teste = pd.DataFrame({
            'Par': ['ABEV3 x PETR4', 'BBAS3 x ITUB4'],
            'Preco': [15.25, 28.90],
            'Volume': [800, 1200],
            'Status': ['Venda', 'Compra']
        })
        
        # Teste de escrita CSV
        arquivo_csv = 'teste_fallback.csv'
        dados_teste.to_csv(arquivo_csv, index=False)
        print("✅ Escrita de arquivo CSV: OK")
        
        # Teste de leitura CSV
        dados_lidos = pd.read_csv(arquivo_csv)
        print(f"✅ Leitura de arquivo CSV: OK ({len(dados_lidos)} linhas)")
        
        # Limpa arquivo de teste
        if os.path.exists(arquivo_csv):
            os.remove(arquivo_csv)
            print("✅ Limpeza de arquivos CSV: OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste CSV: {e}")
        return False

def main():
    print("🎯 TESTE DE SUPORTE A EXCEL/CSV")
    print("=" * 40)
    
    sucesso_openpyxl = testar_openpyxl()
    sucesso_csv = testar_fallback_csv()
    
    print("\n" + "=" * 40)
    if sucesso_openpyxl:
        print("🎉 OPENPYXL TOTALMENTE FUNCIONAL!")
        print("✅ Sistema pode salvar arquivos Excel")
    elif sucesso_csv:
        print("⚠️  OPENPYXL NÃO DISPONÍVEL")
        print("✅ Fallback CSV funcionando")
    else:
        print("❌ PROBLEMAS COM EXPORT DE DADOS")
    print("=" * 40)

if __name__ == "__main__":
    main()
