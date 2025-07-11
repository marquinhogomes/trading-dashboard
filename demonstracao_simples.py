#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demonstracao da correcao da linha verde do grafico
"""

def demonstrar_correcao():
    print("=" * 60)
    print("CORRECAO DA LINHA VERDE DO GRAFICO DE EQUITY")
    print("=" * 60)
    
    # Dados simulados
    balance_atual = 9987.00
    equity_atual = 10012.00
    
    # Deals fechados do dia
    deals = [50.00, -83.00, 20.00]  # Total: -13.00
    lucro_total = sum(deals)
    
    print(f"Balance atual (MT5): R$ {balance_atual:,.2f}")
    print(f"Equity atual (MT5):  R$ {equity_atual:,.2f}")
    print(f"Deals fechados:      {deals}")
    print(f"Total dos deals:     R$ {lucro_total:+,.2f}")
    
    # Calculo do saldo inicial CORRETO
    saldo_inicial = balance_atual - lucro_total
    
    print(f"\nCALCULO SALDO INICIAL:")
    print(f"saldo_inicial = balance_atual - lucro_total_dia")
    print(f"saldo_inicial = {balance_atual:,.2f} - ({lucro_total:+,.2f})")
    print(f"saldo_inicial = R$ {saldo_inicial:,.2f}")
    
    print(f"\nLINHA VERDE (BALANCE) NO GRAFICO:")
    print(f"Inicio:  R$ {saldo_inicial:,.2f}")
    print(f"Final:   R$ {balance_atual:,.2f}")
    print(f"Variacao: R$ {balance_atual - saldo_inicial:+,.2f}")
    
    print(f"\nLUCRO DIARIO:")
    lucro_diario = equity_atual - saldo_inicial
    print(f"lucro_diario = equity_atual - saldo_inicial")
    print(f"lucro_diario = {equity_atual:,.2f} - {saldo_inicial:,.2f}")
    print(f"lucro_diario = R$ {lucro_diario:+,.2f}")
    
    print(f"\nVALIDACOES:")
    print(f"Diferenca balance:  R$ {balance_atual - saldo_inicial:+,.2f}")
    print(f"Total dos deals:    R$ {lucro_total:+,.2f}")
    print(f"Confere? {abs((balance_atual - saldo_inicial) - lucro_total) < 0.01}")
    
    print(f"\nRESUMO DA CORRECAO:")
    print(f"- Saldo inicial calculado corretamente: R$ {saldo_inicial:,.2f}")
    print(f"- Linha verde mostra evolucao das operacoes fechadas")
    print(f"- Lucro diario inclui posicoes abertas: R$ {lucro_diario:+,.2f}")
    print("- Grafico agora reflete a realidade!")

if __name__ == "__main__":
    demonstrar_correcao()
