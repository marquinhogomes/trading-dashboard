#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para debugar problema da segunda seleção não aparecer no dashboard
"""

import pandas as pd
import sys
import os

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_segunda_selecao_debug():
    """Simula exatamente os dados dos logs para debugar"""
    print("🔬 DEBUG: Simulando dados da segunda seleção dos logs")
    print("=" * 70)
    
    # Dados exatos dos logs fornecidos
    sinais_logs = [
        {"par": "RAIL3", "sinal": "COMPRA", "zscore": -2.38, "beta_rotation": 0.538},
        {"par": "CSAN3", "sinal": "COMPRA", "zscore": -2.16, "beta_rotation": 0.670},
        {"par": "BRAP4", "sinal": "COMPRA", "zscore": -2.42, "beta_rotation": 0.301},
        {"par": "TIMS3", "sinal": "VENDA", "zscore": 2.26, "beta_rotation": 0.717},
        {"par": "ELET6", "sinal": "COMPRA", "zscore": -2.55, "beta_rotation": -0.649},
        {"par": "SMTO3", "sinal": "COMPRA", "zscore": -2.22, "beta_rotation": -0.498},
        {"par": "EQTL3", "sinal": "COMPRA", "zscore": -2.07, "beta_rotation": 1.405},
        {"par": "NTCO3", "sinal": "VENDA", "zscore": 2.07, "beta_rotation": 0.822},
        {"par": "WEGE3", "sinal": "COMPRA", "zscore": -2.10, "beta_rotation": -1.239}
    ]
    
    print(f"📊 DADOS DOS LOGS: {len(sinais_logs)} sinais encontrados")
    print()
    
    # Simula estrutura que deveria estar em sinais_ativos
    sinais_ativos_structure = []
    for i, sinal in enumerate(sinais_logs):
        sinal_completo = {
            'par': sinal['par'],
            'sinal': sinal['sinal'],
            'zscore': sinal['zscore'], 
            'r2': 0.65 + (i * 0.05),  # R² simulado
            'preco_atual': 30.0 + (i * 5.0),  # Preços simulados
            'preco_entrada': (30.0 + (i * 5.0)) * 0.998,  # Entrada 0.2% melhor
            'beta_rotation': sinal['beta_rotation'],
            'beta_rotation_mean': sinal['beta_rotation'] * 0.8,  # Média simulada
            'status': 'REAL',
            'timestamp': '2025-06-21 18:49:09'
        }
        sinais_ativos_structure.append(sinal_completo)
    
    print("🎯 ESTRUTURA DE sinais_ativos:")
    print("-" * 50)
    for sinal in sinais_ativos_structure[:3]:  # Mostra apenas 3 exemplos
        print(f"Par: {sinal['par']}")
        print(f"  Sinal: {sinal['sinal']}")
        print(f"  Z-Score: {sinal['zscore']}")
        print(f"  Preço: R$ {sinal['preco_atual']:.2f}")
        print(f"  Beta Rot: {sinal['beta_rotation']:.3f}")
        print()
    
    # Testa conversão para DataFrame (que a função render_segunda_selecao faz)
    print("🔄 TESTE: Conversão para DataFrame")
    print("-" * 50)
    
    # Simula exatamente o que a função render_segunda_selecao faz
    sinais_data = []
    for sinal in sinais_ativos_structure:
        sinais_data.append({
            'Dependente': sinal.get('par', '').split('/')[0] if '/' in sinal.get('par', '') else sinal.get('par', ''),
            'Independente': sinal.get('par', '').split('/')[1] if '/' in sinal.get('par', '') else '',
            'Z-Score': sinal.get('zscore', 0),
            'r2': sinal.get('r2', 0),
            'preco_atual': sinal.get('preco_atual', 100),
            'Preco_Entrada_Final': sinal.get('preco_entrada', sinal.get('preco_atual', 100)),
            'sinal': sinal.get('sinal', 'NEUTRO'),
            'beta_rotation': sinal.get('beta_rotation', 0),
            'beta_rotation_mean': sinal.get('beta_rotation_mean', 0),
            'status': sinal.get('status', 'PROCESSADO')
        })
    
    df_segunda = pd.DataFrame(sinais_data)
    print(f"✅ DataFrame criado: {len(df_segunda)} linhas")
    print("Colunas:", list(df_segunda.columns))
    print()
    print("Preview:")
    print(df_segunda[['Dependente', 'Z-Score', 'sinal', 'preco_atual']].head())
    print()
    
    # Testa conversão para formato de tabela profissional
    print("🎨 TESTE: Conversão para Formato Profissional")
    print("-" * 50)
    
    posicoes_segunda = []
    for i, (_, row) in enumerate(df_segunda.iterrows()):
        dep = row.get('Dependente', 'N/A')
        zscore = row.get('Z-Score', 0)
        preco_atual = row.get('preco_atual', 100)
        preco_entrada = row.get('Preco_Entrada_Final', preco_atual * 0.998)
        sinal_tipo = row.get('sinal', 'NEUTRO')
        
        # Converte sinal para tipo da tabela
        if sinal_tipo == 'COMPRA':
            tipo = 'LONG'
            pl_estimado = abs(zscore) * preco_atual * 0.008
        elif sinal_tipo == 'VENDA':
            tipo = 'SHORT'
            pl_estimado = zscore * preco_atual * 0.006
        else:
            tipo = 'NEUTRO'
            pl_estimado = 0
        
        pos_data = {
            'Par': f"{dep}/INDEX",  # Simplificado
            'Tipo': tipo,
            'Volume': f"{1000 + i*100:,}",
            'Preço Abertura': f"R$ {preco_entrada:.2f}",
            'Preço Atual': f"R$ {preco_atual:.2f}",
            'P&L (R$)': f"R$ {pl_estimado:+.2f}",
            'P&L (%)': f"{(pl_estimado/preco_entrada*100):+.2f}%",
            'Z-Score': f"{zscore:.3f}",
            'Sinal Original': sinal_tipo
        }
        posicoes_segunda.append(pos_data)
    
    print(f"✅ Tabela profissional: {len(posicoes_segunda)} linhas")
    print()
    print("Exemplo de linha:")
    exemplo = posicoes_segunda[0]
    for key, value in exemplo.items():
        print(f"  {key}: {value}")
    print()
    
    # Verifica problemas potenciais
    print("🔍 VERIFICAÇÃO DE PROBLEMAS POTENCIAIS:")
    print("-" * 50)
    
    problemas = []
    
    # 1. Verifica se sinais_ativos está sendo limpo incorretamente
    if len(sinais_ativos_structure) == 0:
        problemas.append("❌ sinais_ativos está vazio")
    else:
        problemas.append("✅ sinais_ativos tem dados")
    
    # 2. Verifica se DataFrame está sendo criado corretamente
    if df_segunda.empty:
        problemas.append("❌ DataFrame df_segunda está vazio")
    else:
        problemas.append("✅ DataFrame df_segunda tem dados")
    
    # 3. Verifica se colunas necessárias existem
    colunas_necessarias = ['Dependente', 'Z-Score', 'sinal', 'preco_atual']
    for col in colunas_necessarias:
        if col in df_segunda.columns:
            problemas.append(f"✅ Coluna '{col}' existe")
        else:
            problemas.append(f"❌ Coluna '{col}' FALTANDO")
    
    # 4. Verifica se conversão para tabela funciona
    if len(posicoes_segunda) == 0:
        problemas.append("❌ Conversão para tabela profissional falhou")
    else:
        problemas.append("✅ Conversão para tabela profissional funcionou")
    
    for problema in problemas:
        print(problema)
    
    print()
    print("🎯 POSSÍVEIS CAUSAS DO PROBLEMA:")
    print("-" * 50)
    print("1. ❓ sinais_ativos sendo limpo após processamento")
    print("2. ❓ Problema de timing - dados não estão disponíveis quando aba é renderizada")  
    print("3. ❓ Erro na verificação hasattr() ou empty check")
    print("4. ❓ Problema de threading - dados em thread diferente")
    print("5. ❓ Session state não sendo atualizado corretamente")
    print()
    
    # Testa o que acontece se usar estrutura real do log
    print("🧪 TESTE: Estrutura Real vs Simulada")
    print("-" * 50)
    
    # Estrutura que provavelmente está sendo criada no código real
    estrutura_real = []
    for sinal in sinais_logs:
        estrutura_real.append({
            'par': sinal['par'],
            'sinal': sinal['sinal'], 
            'zscore': sinal['zscore'],
            'r2': 0.70,  # Padrão
            'preco_atual': 35.50,  # Preço real simulado
            'segmento': 'Energia/Mineração',
            'status': 'REAL'
        })
    
    print(f"Estrutura real simulada: {len(estrutura_real)} sinais")
    print("Exemplo:", estrutura_real[0])
    print()
    
    print("✅ DEBUG CONCLUÍDO")
    print("📋 RECOMENDAÇÕES:")
    print("1. Verificar se sinais_ativos não está sendo limpo")
    print("2. Adicionar logs de debug na função render_segunda_selecao")
    print("3. Verificar timing de atualização do session state")
    print("4. Testar com dados reais no dashboard")

if __name__ == "__main__":
    test_segunda_selecao_debug()
