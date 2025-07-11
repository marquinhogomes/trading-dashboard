#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste: Verificar símbolos disponíveis no MT5
"""

import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

def testar_simbolos_mt5():
    """Testa quais símbolos estão disponíveis no MT5"""
    
    # Inicializa MT5
    if not mt5.initialize():
        print("❌ Falha ao inicializar MT5")
        return
    
    print("✅ MT5 inicializado com sucesso")
    
    # Lista de símbolos para testar
    simbolos_teste = [
        'IBOV', 'IBOVESPA', 'BVSP',
        'ABEV3', 'BBAS3', 'BBDC4', 'VALE3', 'PETR4', 'ITUB4',
        'MGLU3', 'WEGE3', 'RENT3', 'RAIL3'
    ]
    
    print(f"\n🔍 Testando {len(simbolos_teste)} símbolos...")
    print("=" * 60)
    
    simbolos_encontrados = []
    simbolos_nao_encontrados = []
    
    for simbolo in simbolos_teste:
        try:
            # Verifica se o símbolo existe
            symbol_info = mt5.symbol_info(simbolo)
            
            if symbol_info is not None:
                print(f"✅ {simbolo}: {symbol_info.description}")
                
                # Testa obter dados históricos
                rates = mt5.copy_rates_from_pos(simbolo, mt5.TIMEFRAME_D1, 0, 10)
                
                if rates is not None and len(rates) > 0:
                    print(f"   📊 Dados históricos: {len(rates)} registros disponíveis")
                    simbolos_encontrados.append({
                        'simbolo': simbolo,
                        'descricao': symbol_info.description,
                        'registros': len(rates)
                    })
                else:
                    print(f"   ❌ Sem dados históricos")
                    
            else:
                print(f"❌ {simbolo}: Não encontrado")
                simbolos_nao_encontrados.append(simbolo)
                
        except Exception as e:
            print(f"❌ {simbolo}: Erro - {str(e)}")
            simbolos_nao_encontrados.append(simbolo)
    
    print("\n" + "=" * 60)
    print(f"📊 RESUMO:")
    print(f"✅ Símbolos encontrados: {len(simbolos_encontrados)}")
    print(f"❌ Símbolos não encontrados: {len(simbolos_nao_encontrados)}")
    
    if simbolos_encontrados:
        print(f"\n✅ SÍMBOLOS VÁLIDOS PARA USO:")
        for item in simbolos_encontrados:
            print(f"   - {item['simbolo']}: {item['descricao']} ({item['registros']} registros)")
    
    if simbolos_nao_encontrados:
        print(f"\n❌ SÍMBOLOS NÃO ENCONTRADOS:")
        for simbolo in simbolos_nao_encontrados:
            print(f"   - {simbolo}")
    
    # Testa buscar símbolos que contenham determinadas strings
    print(f"\n🔍 Buscando símbolos disponíveis no broker...")
    
    try:
        # Obtém todos os símbolos disponíveis
        all_symbols = mt5.symbols_get()
        
        if all_symbols:
            print(f"📊 Total de símbolos disponíveis no broker: {len(all_symbols)}")
            
            # Filtra símbolos brasileiros (que contenham números)
            simbolos_br = []
            for symbol in all_symbols:
                name = symbol.name
                if any(char.isdigit() for char in name) and len(name) <= 6:
                    simbolos_br.append({
                        'name': name,
                        'description': symbol.description
                    })
            
            print(f"📈 Símbolos brasileiros encontrados: {len(simbolos_br)}")
            
            # Mostra os primeiros 20
            print(f"\n📋 Primeiros 20 símbolos brasileiros:")
            for i, symbol in enumerate(simbolos_br[:20]):
                print(f"   {i+1:2d}. {symbol['name']}: {symbol['description']}")
                
            if len(simbolos_br) > 20:
                print(f"   ... e mais {len(simbolos_br) - 20} símbolos")
        
    except Exception as e:
        print(f"❌ Erro ao buscar símbolos: {str(e)}")
    
    # Finaliza MT5
    mt5.shutdown()
    print(f"\n🔌 MT5 desconectado")

if __name__ == "__main__":
    testar_simbolos_mt5()
