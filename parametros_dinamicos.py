#!/usr/bin/env python3
"""
Sistema de Comunicação entre Módulos - Parâmetros Dinâmicos
Permite compartilhamento de configurações entre dashboard, sistema_integrado e calculo_entradas_v55
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
import pandas as pd
import shutil

class ParametrosDinamicos:
    """
    Gerenciador centralizado de parâmetros dinâmicos do sistema de trading.
    Permite comunicação entre dashboard, sistema_integrado e calculo_entradas_v55.
    """
    
    def __init__(self, arquivo_config="config_dinamica.json"):
        self.arquivo_config = arquivo_config
        self.parametros_padrao = {
            # Parâmetros de análise
            'ativos_selecionados': ['PETR4', 'VALE3', 'ITUB4', 'BBAS3', 'ABEV3'],
            'timeframe': "1 dia",
            'periodo_analise': [70, 100, 120, 140, 160, 180, 200, 220, 240, 250],
            'usar_multiplos_periodos': True,
            
            # Filtros técnicos
            'zscore_min': 2.0,
            'zscore_max': 6.5,
            'r2_min': 0.5,
            'beta_max': 1.5,
            'adf_p_value_max': 0.05,
            'coint_pvalue_max': 0.05,
            
            # Filtros habilitados
            'filtro_cointegracao': True,
            'filtro_r2': True,
            'filtro_beta': True,
            'filtro_zscore': True,
            
            # Limites operacionais
            'max_posicoes': 6,
            'valor_operacao': 10000,
            'valor_operacao_ind': 10000,
            'limite_lucro': 120,
            'limite_prejuizo': 120,
            
            # Horários
            'finaliza_ordens': 15,
            'intervalo_execucao': 60,
            
            # Spreads (mantém compatibilidade com calculo_entradas_v55)
            'desvio_gain_compra': 1.012,
            'desvio_loss_compra': 0.988,
            'desvio_gain_venda': 0.988,
            'desvio_loss_venda': 1.012,
            'desvio_gain_compra_ind': 1.03,
            'desvio_loss_compra_ind': 0.97,
            'desvio_gain_venda_ind': 0.97,
            'desvio_loss_venda_ind': 1.03,
            
            # Controle de estado
            'parametros_alterados': False,
            'timestamp_alteracao': None,
            'origem_alteracao': 'sistema'
        }
        
        # Cria arquivo de configuração se não existir
        self.inicializar_config()
    
    def inicializar_config(self):
        """Inicializa arquivo de configuração com valores padrão se não existir"""
        if not os.path.exists(self.arquivo_config):
            self.salvar_parametros(self.parametros_padrao)
            print(f"[CONFIG] Arquivo de configuração criado: {self.arquivo_config}")
    
    def carregar_parametros(self) -> Dict[str, Any]:
        """Carrega parâmetros do arquivo JSON"""
        try:
            if os.path.exists(self.arquivo_config):
                with open(self.arquivo_config, 'r', encoding='utf-8') as f:
                    parametros = json.load(f)
                # Mescla com padrões para garantir que todas as chaves existam
                parametros_completos = self.parametros_padrao.copy()
                parametros_completos.update(parametros)
                return parametros_completos
            else:
                return self.parametros_padrao.copy()
        except Exception as e:
            print(f"[ERRO] Falha ao carregar parâmetros: {e}")
            return self.parametros_padrao.copy()
    
    def salvar_parametros(self, parametros: Dict[str, Any], origem: str = 'sistema'):
        """Salva parâmetros no arquivo JSON"""
        try:
            # Atualiza timestamp e origem
            parametros['timestamp_alteracao'] = datetime.now().isoformat()
            parametros['origem_alteracao'] = origem
            parametros['parametros_alterados'] = True
            
            with open(self.arquivo_config, 'w', encoding='utf-8') as f:
                json.dump(parametros, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"[CONFIG] Parâmetros salvos por '{origem}' em {parametros['timestamp_alteracao']}")
            return True
        except Exception as e:
            print(f"[ERRO] Falha ao salvar parâmetros: {e}")
            return False
    
    def atualizar_parametros_dashboard(self, config_dashboard: Dict[str, Any]) -> bool:
        """
        Atualiza parâmetros vindos do dashboard e marca como alterados
        """
        try:
            parametros_atuais = self.carregar_parametros()
            
            # Mapeia chaves do dashboard para chaves do sistema
            mapeamento = {
                'ativos_selecionados': 'ativos_selecionados',
                'periodo_analise': 'periodo_analise',
                'zscore_min': 'zscore_min',
                'zscore_max': 'zscore_max',
                'r2_min': 'r2_min',
                'beta_max': 'beta_max',
                'coint_pvalue_max': 'coint_pvalue_max',
                'max_posicoes': 'max_posicoes',
                'valor_operacao': 'valor_operacao',
                'filtro_cointegracao': 'filtro_cointegracao',
                'filtro_r2': 'filtro_r2',
                'filtro_beta': 'filtro_beta',
                'filtro_zscore': 'filtro_zscore'
            }
            
            # Atualiza apenas parâmetros que existem no dashboard
            alteracoes = []
            for chave_dash, chave_sistema in mapeamento.items():
                if chave_dash in config_dashboard:
                    valor_antigo = parametros_atuais.get(chave_sistema)
                    valor_novo = config_dashboard[chave_dash]
                    
                    if valor_antigo != valor_novo:
                        parametros_atuais[chave_sistema] = valor_novo
                        alteracoes.append(f"{chave_sistema}: {valor_antigo} → {valor_novo}")
            
            if alteracoes:
                print(f"[CONFIG] Parâmetros alterados pelo dashboard:")
                for alteracao in alteracoes:
                    print(f"   • {alteracao}")
                
                return self.salvar_parametros(parametros_atuais, 'dashboard')
            else:
                print(f"[CONFIG] Nenhuma alteração detectada nos parâmetros")
                return True
                
        except Exception as e:
            print(f"[ERRO] Falha ao atualizar parâmetros do dashboard: {e}")
            return False
    
    def verificar_alteracoes(self) -> bool:
        """Verifica se existem parâmetros alterados pendentes"""
        parametros = self.carregar_parametros()
        return parametros.get('parametros_alterados', False)
    
    def marcar_como_aplicado(self) -> bool:
        """Marca parâmetros como aplicados pelo sistema principal"""
        try:
            parametros = self.carregar_parametros()
            parametros['parametros_alterados'] = False
            parametros['timestamp_aplicacao'] = datetime.now().isoformat()
            parametros['forcar_regeneracao_tabelas'] = True  # NOVO: Flag para forçar regeneração
            
            with open(self.arquivo_config, 'w', encoding='utf-8') as f:
                json.dump(parametros, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"[CONFIG] Parâmetros marcados como aplicados pelo sistema principal")
            print(f"[CONFIG] Flag de regeneração de tabelas ativado")
            return True
        except Exception as e:
            print(f"[ERRO] Falha ao marcar parâmetros como aplicados: {e}")
            return False
    
    def verificar_regeneracao_tabelas(self) -> bool:
        """Verifica se as tabelas precisam ser regeneradas devido a alteração de parâmetros"""
        parametros = self.carregar_parametros()
        return parametros.get('forcar_regeneracao_tabelas', False)
    
    def marcar_tabelas_regeneradas(self) -> bool:
        """Marca que as tabelas foram regeneradas com os novos parâmetros"""
        try:
            parametros = self.carregar_parametros()
            parametros['forcar_regeneracao_tabelas'] = False
            parametros['timestamp_tabelas_regeneradas'] = datetime.now().isoformat()
            
            with open(self.arquivo_config, 'w', encoding='utf-8') as f:
                json.dump(parametros, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"[CONFIG] Tabelas marcadas como regeneradas")
            return True
        except Exception as e:
            print(f"[ERRO] Falha ao marcar tabelas como regeneradas: {e}")
            return False
    
    def obter_status_parametros(self) -> Dict[str, Any]:
        """Retorna status completo dos parâmetros para o dashboard"""
        parametros = self.carregar_parametros()
        return {
            'parametros_alterados': parametros.get('parametros_alterados', False),
            'forcar_regeneracao_tabelas': parametros.get('forcar_regeneracao_tabelas', False),
            'timestamp_alteracao': parametros.get('timestamp_alteracao'),
            'timestamp_aplicacao': parametros.get('timestamp_aplicacao'),
            'timestamp_tabelas_regeneradas': parametros.get('timestamp_tabelas_regeneradas'),
            'origem_alteracao': parametros.get('origem_alteracao', 'sistema')
        }
    
    def obter_parametros_sistema_principal(self) -> Dict[str, Any]:
        """
        Retorna parâmetros formatados para uso no calculo_entradas_v55.py
        """
        parametros = self.carregar_parametros()
        
        # Formata para compatibilidade com calculo_entradas_v55.py
        config_sistema = {
            # Variáveis globais
            'periodo': parametros.get('periodo_analise', [70, 100, 120, 140, 160, 180, 200, 220, 240, 250]),
            'limite_operacoes': parametros.get('max_posicoes', 6),
            'valor_operacao': parametros.get('valor_operacao', 10000),
            'valor_operacao_ind': parametros.get('valor_operacao_ind', 10000),
            'limite_lucro': parametros.get('limite_lucro', 120),
            'limite_prejuizo': parametros.get('limite_prejuizo', 120),
            'pvalor': parametros.get('coint_pvalue_max', 0.05),
            'finaliza_ordens': parametros.get('finaliza_ordens', 15),
            
            # Spreads
            'desvio_gain_compra': parametros.get('desvio_gain_compra', 1.012),
            'desvio_loss_compra': parametros.get('desvio_loss_compra', 0.988),
            'desvio_gain_venda': parametros.get('desvio_gain_venda', 0.988),
            'desvio_loss_venda': parametros.get('desvio_loss_venda', 1.012),
            'desvio_gain_compra_ind': parametros.get('desvio_gain_compra_ind', 1.03),
            'desvio_loss_compra_ind': parametros.get('desvio_loss_compra_ind', 0.97),
            'desvio_gain_venda_ind': parametros.get('desvio_gain_venda_ind', 0.97),
            'desvio_loss_venda_ind': parametros.get('desvio_loss_venda_ind', 1.03),
            
            # Filtros
            'filter_params': {
                'r2_min': parametros.get('r2_min', 0.5),
                'beta_max': parametros.get('beta_max', 1.5),
                'coef_var_max': 5000.0,
                'adf_p_value_max': parametros.get('adf_p_value_max', 0.05),
                'use_coint_test': parametros.get('filtro_cointegracao', True),
                'use_adf_critical': False,
                'enable_cointegration_filter': parametros.get('filtro_cointegracao', True)
            }
        }
        
        return config_sistema

# Instância global do gerenciador
gerenciador_parametros = ParametrosDinamicos()

def carregar_config_dinamica():
    """Função helper para carregar configuração dinâmica"""
    return gerenciador_parametros.carregar_parametros()

def salvar_config_dashboard(config_dashboard):
    """Função helper para salvar configuração do dashboard"""
    return gerenciador_parametros.atualizar_parametros_dashboard(config_dashboard)

def verificar_parametros_alterados():
    """Função helper para verificar se há parâmetros alterados"""
    return gerenciador_parametros.verificar_alteracoes()

def aplicar_parametros_sistema():
    """Função helper para marcar parâmetros como aplicados"""
    return gerenciador_parametros.marcar_como_aplicado()

def obter_config_sistema_principal():
    """Função helper para obter configuração do sistema principal"""
    return gerenciador_parametros.obter_parametros_sistema_principal()

def verificar_regeneracao_tabelas():
    """Função helper para verificar se as tabelas precisam ser regeneradas"""
    return gerenciador_parametros.verificar_regeneracao_tabelas()

def marcar_tabelas_regeneradas():
    """Função helper para marcar que as tabelas foram regeneradas"""
    return gerenciador_parametros.marcar_tabelas_regeneradas()
