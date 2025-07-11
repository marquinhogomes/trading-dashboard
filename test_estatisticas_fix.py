#!/usr/bin/env python3
"""
Test script para validar a correção do bug das estatísticas
Testa se a função calcular_estatisticas_performance_real funciona corretamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dashboard_trading_pro_real import SistemaTradingPro

def test_estatisticas_performance():
    """Testa o cálculo de estatísticas de performance"""
    print("🧪 Testando cálculo de estatísticas de performance...")
    
    # Cria instância do sistema
    sistema = SistemaTradingPro()
    
    # Dados de teste - trades simulados
    trades_teste = [
        {'Lucro': 150.0, 'Simbolo': 'IBOV', 'Data': '2024-01-01'},
        {'Lucro': -80.0, 'Simbolo': 'PETR4', 'Data': '2024-01-02'},
        {'Lucro': 200.0, 'Simbolo': 'VALE3', 'Data': '2024-01-03'},
        {'Lucro': -50.0, 'Simbolo': 'IBOV', 'Data': '2024-01-04'},
        {'Lucro': 300.0, 'Simbolo': 'MGLU3', 'Data': '2024-01-05'},
    ]
    
    # Calcula estatísticas
    print(f"📊 Calculando estatísticas para {len(trades_teste)} trades...")
    estatisticas = sistema.calcular_estatisticas_performance_real(trades_teste)
    
    # Exibe resultados
    print("\n✅ Estatísticas calculadas:")
    print(f"   Total de Trades: {estatisticas['total_trades']}")
    print(f"   Win Rate: {estatisticas['win_rate']:.1f}%")
    print(f"   Resultado Total: R$ {estatisticas['resultado_total']:,.2f}")
    print(f"   Resultado Médio: R$ {estatisticas['resultado_medio']:,.2f}")
    print(f"   Melhor Trade: R$ {estatisticas['melhor_trade']:,.2f}")
    print(f"   Pior Trade: R$ {estatisticas['pior_trade']:,.2f}")
    print(f"   Profit Factor: {estatisticas['profit_factor']:.2f}")
    print(f"   Max Drawdown: {estatisticas['max_drawdown']:.2f}%")
    print(f"   Sharpe Ratio: {estatisticas['sharpe_ratio']:.2f}")
    
    # Validações
    assert estatisticas['total_trades'] == 5, "Total de trades incorreto"
    assert estatisticas['win_rate'] == 60.0, "Win rate incorreto"  # 3 lucros de 5 trades = 60%
    assert estatisticas['resultado_total'] == 520.0, "Resultado total incorreto"  # 150-80+200-50+300 = 520
    assert estatisticas['melhor_trade'] == 300.0, "Melhor trade incorreto"
    assert estatisticas['pior_trade'] == -80.0, "Pior trade incorreto"
    
    print("\n✅ Todas as validações passaram!")
    
def test_estatisticas_vazio():
    """Testa com lista vazia"""
    print("\n🧪 Testando com lista vazia...")
    
    sistema = SistemaTradingPro()
    estatisticas = sistema.calcular_estatisticas_performance_real([])
    
    print(f"📊 Estatísticas para lista vazia:")
    print(f"   Total de Trades: {estatisticas['total_trades']}")
    print(f"   Win Rate: {estatisticas['win_rate']:.1f}%")
    print(f"   Resultado Total: R$ {estatisticas['resultado_total']:,.2f}")
    
    assert estatisticas['total_trades'] == 0, "Total de trades deveria ser 0"
    assert estatisticas['win_rate'] == 0.0, "Win rate deveria ser 0"
    assert estatisticas['resultado_total'] == 0.0, "Resultado total deveria ser 0"
    
    print("✅ Teste com lista vazia passou!")

if __name__ == "__main__":
    print("🔧 TESTE DE CORREÇÃO: Bug das Estatísticas")
    print("="*50)
    
    try:
        test_estatisticas_performance()
        test_estatisticas_vazio()
        
        print("\n" + "="*50)
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Bug das estatísticas foi corrigido com sucesso")
        print("✅ A função calcular_estatisticas_performance_real funciona corretamente")
        print("✅ O dashboard agora pode exibir estatísticas sem erros de variável não definida")
        
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {str(e)}")
        print("🔧 Verifique a implementação da função calcular_estatisticas_performance_real")
