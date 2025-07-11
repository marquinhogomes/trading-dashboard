#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Integrado: calculo_entradas_v55.py com Threading e Monitoramento
Este sistema combina o código original com threading para visualização completa
"""

import threading
import time
import json
import sys
import os
from datetime import datetime
import traceback

# Importa todo o código original
sys.path.append('.')

class SistemaIntegrado:
    """Sistema que integra o código original com threading"""
    def __init__(self):
        # Segmentos dos ativos (copiado do dashboard)
        self.segmentos = {
            'ABEV3': 'Bebidas', 'ALOS3': 'Saúde', 'ASAI3': 'Varejo Alimentar',
            'BBAS3': 'Bancos', 'BBDC4': 'Bancos', 'BBSE3': 'Seguros',
            'BPAC11': 'Bancos', 'BRAP4': 'Holding', 'BRFS3': 'Alimentos',
            'BRKM5': 'Química', 'CPFE3': 'Energia', 'CPLE6': 'Energia',
            'CSAN3': 'Energia', 'CSNA3': 'Siderurgia','CYRE3': 'Construção',
            'ELET3': 'Energia', 'ELET6': 'Energia', 'EMBR3': 'Aeroespacial',
            'ENEV3': 'Energia', 'ENGI11': 'Energia', 'EQTL3': 'Energia', 
            'EZTC3': 'Construção', 'FLRY3': 'Saúde', 'GOAU4': 'Siderurgia',
            'HYPE3': 'Farmacêutica','IGTI11': 'Financeiro','IRBR3': 'Seguros', 
            'ITSA4': 'Financeiro', 'ITUB4': 'Bancos', 'KLBN11': 'Papel e Celulose',
            'MRFG3': 'Alimentos', 'NATU3': 'Higiene/Beleza','PETR3': 'Petróleo',
            'PETR4': 'Petróleo', 'PETZ3': 'Varejo', 'PRIO3': 'Petróleo',
            'RAIL3': 'Logística', 'RADL3': 'Varejo', 'RECV3': 'Petróleo',
            'RENT3': 'Locação', 'RDOR3': 'Saúde', 'SANB11': 'Bancos',
            'SLCE3': 'Agro', 'SMTO3': 'Agro', 'SUZB3': 'Papel e Celulose',
            'TAEE11': 'Energia', 'TIMS3': 'Telecom', 'TOTS3': 'Tecnologia',
            'UGPA3': 'Distribuição','VALE3': 'Mineração','VBBR3': 'Transporte',
            'VIVT3': 'Telecom', 'WEGE3': 'Industrial','YDUQ3': 'Educação'
        }
        # Listas de dependentes e independentes (copiado do dashboard)
        self.dependente = [
            'ABEV3', 'ALOS3', 'ASAI3','BBAS3', 'BBDC4', 'BBSE3', 'BPAC11', 'BRAP4', 'BRFS3', 'BRKM5', 'CPFE3', 'CPLE6', 'CSAN3','CSNA3', 'CYRE3', 'ELET3', 'ELET6', 'EMBR3', 'ENEV3', 'ENGI11', 'EQTL3', 'EZTC3', 'FLRY3', 'GOAU4', 'HYPE3', 'IGTI11', 'IRBR3', 'ITSA4', 'ITUB4', 'KLBN11', 'MRFG3', 'NATU3', 'PETR3', 'PETR4', 'PETZ3', 'PRIO3', 'RAIL3', 'RADL3', 'RECV3', 'RENT3', 'RDOR3', 'SANB11', 'SLCE3', 'SMTO3', 'SUZB3', 'TAEE11', 'TIMS3', 'TOTS3', 'UGPA3', 'VALE3', 'VBBR3', 'VIVT3', 'WEGE3', 'YDUQ3'
        ]
        self.independente = self.dependente.copy()

        # Centralização de parâmetros do sistema (valores padrão conforme calculo_entradas_v55.py)
        self.prefixo = "2"
        self.limite_operacoes = 6
        self.indep_limite_operacoes = 6
        self.valor_operacao = 10000
        self.valor_operacao_ind = 5000
        self.limite_lucro = 120
        self.limite_prejuizo = 120
        self.pvalor = 0.05
        self.apetite_perc_media = 1.0
        self.finaliza_ordens = 23
        self.ajusta_ordens = 23
        self.ajusta_ordens_minuto = 10
        self.horario_ajuste_stops = 23
        self.horario_remove_pendentes = 23
        self.horario_fechamento_total = 23
        self.JANELA_ANALISE_POSICOES = (0, 23)
        self.JANELA_NOVAS_OPERACOES = (0, 23)
        self.JANELA_AJUSTES_DINAMICOS = (0, 23)
        self.JANELA_BREAK_EVEN = (0, 23)
        self.desvio_gain_compra = 1.012
        self.desvio_loss_compra = 0.988
        self.desvio_gain_venda = 0.988
        self.desvio_loss_venda = 1.012
        self.desvio_gain_compra_ind = 1.03
        self.desvio_loss_compra_ind = 0.97
        self.desvio_gain_venda_ind = 0.97
        self.desvio_loss_venda_ind = 1.03

        self.running = False
        self.thread_principal = None
        self.dados_sistema = {
            "execucoes": 0,
            "pares_processados": 0,
            "ordens_enviadas": 0,
            "inicio": None,
            "ultimo_ciclo": None,
            "status": "Desconectado"
        }
        self.logs = []
        
        # Controles para as novas threads
        self.stops_ja_ajustados = set()
        self.ajustes_executados_hoje = set()
        
        # Configurações horário
        self.JANELA_BREAK_EVEN = (8, 17)  # 8h-17h: Break-even automático
        self.horario_ajuste_stops = 15    # 15h - Ajustar stops
        self.ajusta_ordens_minuto = 10    # 15:10h - Minuto para ajustes
        self.horario_remove_pendentes = 15 # 15h - Remover ordens pendentes (15:20h)
        self.horario_fechamento_total = 16 # 16h - Fechamento forçado (16:01h)
        self.prefixo = "2"                # Prefixo do magic number
    
    def log(self, mensagem):
        """Log com timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        evento = f"[{timestamp}] {mensagem}"
        self.logs.append(evento)
        print(evento)
    
    def executar_sistema_original(self):
        """Executa o sistema original em thread separada"""
        self.log("INICIANDO: Sistema Original de Trading")
        
        try:
            # Tenta ler o arquivo original com diferentes encodings
            codigo = None
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    with open('calculo_entradas_v55.py', 'r', encoding=encoding) as f:
                        codigo = f.read()
                    self.log(f"✅ Arquivo lido com encoding: {encoding}")
                    break
                except UnicodeDecodeError:
                    continue
                except FileNotFoundError:
                    self.log("❌ Arquivo calculo_entradas_v55.py não encontrado")
                    raise
            
            if codigo is None:
                raise UnicodeDecodeError("Não foi possível ler o arquivo com nenhum encoding")
            
            # Remove caracteres problemáticos se necessário
            codigo = codigo.replace('\x92', "'").replace('\x96', '-').replace('\x91', "'")
            
            # Modifica o código para executar o main automaticamente
            # Substitui a condição if __name__ == "__main__": por uma execução direta
            codigo_modificado = codigo.replace(
                'if __name__ == "__main__":',
                '# Executado pelo sistema_integrado.py\nif True:'
            )
            
            # Executa o código original modificado
            exec(codigo_modificado, globals())
            self.log("✅ Sistema original executado com sucesso")
                
        except FileNotFoundError:
            self.log("❌ ERRO: Arquivo calculo_entradas_v55.py não encontrado")
            self.log("   📋 Sistema funcionará apenas com monitoramento de posições reais")
        except UnicodeDecodeError as e:
            self.log("❌ ERRO: Problema de encoding no arquivo original")
            self.log(f"   📋 Detalhes: {str(e)}")
            self.log("   📋 Sistema funcionará apenas com monitoramento de posições reais")
        except Exception as e:
            self.log(f"❌ ERRO: Falha na execução: {str(e)}")
            self.log("   📋 Sistema funcionará apenas com monitoramento de posições reais")
                        
            self.log(f"   📋 Traceback: {traceback.format_exc()}")
            
    def thread_monitoramento(self):
        """Thread de monitoramento do sistema"""
        self.log("📊 INICIANDO: Thread de monitoramento")
        
        while self.running:
            try:
                # Relatório a cada 2 minutos
                self.log("📋 RELATÓRIO DE MONITORAMENTO:")
                self.log(f"   ⚡ Execuções: {self.dados_sistema['execucoes']}")
                self.log(f"   📈 Pares processados: {self.dados_sistema['pares_processados']}")
                self.log(f"   📝 Ordens enviadas: {self.dados_sistema['ordens_enviadas']}")
                self.log(f"   🔄 Status: {self.dados_sistema['status']}")
                
                if self.dados_sistema['ultimo_ciclo']:
                    tempo_ultimo = (datetime.now() - self.dados_sistema['ultimo_ciclo']).seconds
                    self.log(f"   ⏰ Último ciclo: {tempo_ultimo}s atrás")
                
                # Simula checagem de saúde do sistema
                if self.dados_sistema['execucoes'] > 0:
                    taxa_sucesso = (self.dados_sistema['pares_processados'] / 
                                   (self.dados_sistema['execucoes'] * 5)) * 100
                    self.log(f"   ✅ Taxa de sucesso: {taxa_sucesso:.1f}%")
                
                time.sleep(120)  # A cada 2 minutos
                
            except Exception as e:
                self.log(f"❌ ERRO no monitoramento: {str(e)}")
                time.sleep(60)
    
    def thread_monitoramento_posicoes(self):
        """Thread específica para monitoramento de posições - baseada no bloco do calculo_entradas_v55.py"""
        self.log("🔍 INICIANDO: Thread de monitoramento de posições")
        
        # Importações necessárias para MT5 (se disponível)
        try:
            import MetaTrader5 as mt5
            mt5_disponivel = True
            self.log("✅ MetaTrader5 importado com sucesso")
        except ImportError:
            mt5_disponivel = False
            self.log("⚠️ MetaTrader5 não disponível - executando em modo simulado")
        
        while self.running:
            try:
                self.log("🔍 VERIFICAÇÃO DE POSIÇÕES E ORDENS PENDENTES")
                if mt5_disponivel:
                    # Executa monitoramento real com MT5
                    self.executar_monitoramento_real()
                else:
                    # MT5 não disponível - apenas aguarda
                    self.log("⚠️ MetaTrader5 não disponível - aguardando conexão...")
                
                # Aguarda próximo ciclo (30 segundos para monitoramento mais frequente)
                for i in range(30):
                    if not self.running:
                        break
                    time.sleep(1)
                
            except Exception as e:
                self.log(f"❌ ERRO no monitoramento de posições: {str(e)}")
                time.sleep(60)

    def obter_pares_configurados(self):
        """Obtém pares configurados analisando posições reais do MT5"""
        try:
            import MetaTrader5 as mt5
            
            # Primeiro tenta acessar a variável global 'pares' do código original
            if 'pares' in globals() and globals()['pares']:
                self.log("✅ Usando variável 'pares' do sistema original")
                return globals()['pares']
            
            # Se não encontrou, analisa posições reais do MT5 para inferir pares
            self.log("📋 Analisando posições reais do MT5 para identificar pares...")
            pares_inferidos = {}
            
            # Obtém todas as posições abertas
            posicoes_abertas = mt5.positions_get()
            
            if posicoes_abertas:
                # Agrupa posições por magic number
                magics_posicoes = {}
                for pos in posicoes_abertas:
                    if str(pos.magic).startswith(self.prefixo):
                        magic = pos.magic
                        if magic not in magics_posicoes:
                            magics_posicoes[magic] = []
                        magics_posicoes[magic].append(pos.symbol)
                
                # Para cada magic, identifica os pares (se houver múltiplas posições)
                for magic, symbols in magics_posicoes.items():
                    unique_symbols = list(set(symbols))  # Remove duplicatas
                    
                    if len(unique_symbols) == 2:
                        # Par completo identificado
                        pares_inferidos[magic] = (unique_symbols[0], unique_symbols[1])
                        self.log(f"📌 Par completo identificado - Magic {magic}: {unique_symbols[0]} / {unique_symbols[1]}")
                    elif len(unique_symbols) == 1:
                        # Apenas uma perna, tenta inferir o par baseado no histórico do sistema original
                        # Para posições órfãs, marca como None para fechamento
                        self.log(f"⚠️ Posição órfã detectada - Magic {magic}: {unique_symbols[0]} (será fechada)")
                        pares_inferidos[magic] = (unique_symbols[0], None)
            
            # Também verifica ordens pendentes para completar informações
            ordens_pendentes = mt5.orders_get()
            if ordens_pendentes:
                for ordem in ordens_pendentes:
                    if str(ordem.magic).startswith(self.prefixo):
                        magic = ordem.magic
                        
                        # Se já temos posição aberta para este magic, complementa com ordem pendente
                        if magic in pares_inferidos and pares_inferidos[magic][1] is None:
                            posicao_atual = pares_inferidos[magic][0]
                            if ordem.symbol != posicao_atual:
                                pares_inferidos[magic] = (posicao_atual, ordem.symbol)
                                self.log(f"📌 Par completado com ordem pendente - Magic {magic}: {posicao_atual} / {ordem.symbol}")
            
            if pares_inferidos:
                self.log(f"✅ {len(pares_inferidos)} pares identificados das posições reais")
                return pares_inferidos
            else:
                self.log("📋 Nenhuma posição do sistema encontrada no MT5")
                return {}
            
        except Exception as e:
            self.log(f"❌ Erro ao obter pares configurados: {str(e)}")
            return {}

    def thread_analise_e_envio_ordens(self):
        """Thread dedicada para análise e envio de ordens baseada no calculo_entradas_v55.py"""
        self.log("📊 INICIANDO: Thread de Análise e Envio de Ordens")
        
        try:
            import MetaTrader5 as mt5
            mt5_disponivel = True
        except ImportError:
            mt5_disponivel = False
            self.log("❌ MetaTrader5 não disponível para análise de ordens")
            return
        
        while self.running:
            try:
                current_hour = datetime.now().hour
                current_minute = datetime.now().minute
                
                # Executa análise apenas durante horário de operações (ajuste conforme necessário)
                if 9 <= current_hour < 15:  # 9h às 15h
                    self.executar_analise_e_envio_ordens()
                
                # Aguarda próximo ciclo (5 minutos para análise de ordens)
                for i in range(300):  # 5 minutos
                    if not self.running:
                        break
                    time.sleep(1)
                
            except Exception as e:
                self.log(f"❌ ERRO na análise e envio de ordens: {str(e)}")
                time.sleep(60)

    # ===== MÉTODOS AUXILIARES PARA ANÁLISE E ENVIO DE ORDENS =====
    
    def obter_operacoes_candidatas(self):
        """
        Obtém operações candidatas da linha_operacao01 (dados já filtrados).
        NÃO usa simulação - apenas dados reais do sistema original.
        """
        try:
            self.log("🔍 BUSCANDO: Operações candidatas da linha_operacao01")
            
            # OPÇÃO 1: Extração direta da variável global linha_operacao01
            if 'linha_operacao01' in globals() and globals()['linha_operacao01']:
                operacoes = globals()['linha_operacao01']
                self.log(f"✅ Extraído {len(operacoes)} operações da linha_operacao01 global")
                return operacoes
            
            # OPÇÃO 2: Verificar outras variáveis globais do sistema original
            variaveis_verificar = [
                'tabela_linha_operacao01',
                'resultados_zscore_dependente_atual01'
            ]
            
            for var_nome in variaveis_verificar:
                if var_nome in globals() and globals()[var_nome]:
                    dados = globals()[var_nome]
                    
                    # Se for DataFrame pandas, converte para lista de dicts
                    if hasattr(dados, 'to_dict'):
                        operacoes = dados.to_dict('records')
                        self.log(f"✅ Extraído {len(operacoes)} operações de {var_nome} (DataFrame)")
                        return operacoes
                    
                    # Se já for lista de dicionários
                    elif isinstance(dados, list) and len(dados) > 0:
                        self.log(f"✅ Extraído {len(dados)} operações de {var_nome} (Lista)")
                        return dados
            
            # OPÇÃO 3: Tentar importar diretamente do arquivo original
            try:
                # Importa o módulo original para acessar suas variáveis
                import importlib.util
                spec = importlib.util.spec_from_file_location("calculo_entradas", "calculo_entradas_v55.py")
                if spec and spec.loader:
                    modulo_original = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(modulo_original)
                    
                    if hasattr(modulo_original, 'linha_operacao01') and modulo_original.linha_operacao01:
                        operacoes = modulo_original.linha_operacao01
                        self.log(f"✅ Extraído {len(operacoes)} operações do módulo original")
                        return operacoes
                        
            except Exception as e:
                self.log(f"⚠️ Não foi possível importar do módulo original: {str(e)}")
            
            # Se chegou aqui, não encontrou dados
            self.log("❌ NENHUMA operação candidata encontrada")
            self.log("   📋 Verifique se o sistema original está executando e gerando linha_operacao01")
            return []
            
        except Exception as e:
            self.log(f"❌ ERRO ao obter operações candidatas: {str(e)}")
            return []

    def executar_analise_e_envio_ordens(self, tabela_linha_operacao01=None, config=None):
        """
        Executa análise e envio de ordens, aceitando DataFrame e config externos (dashboard) ou usando lógica interna se não fornecidos.
        """
        import MetaTrader5 as mt5
        try:
            # Se argumentos não forem fornecidos, usa lógica antiga (autônoma)
            if tabela_linha_operacao01 is None or config is None:
                current_hour = datetime.now().hour
                finaliza_ordens = 15
                limite_operacoes = 10
                valor_operacao = 1000.0
                prefixo = getattr(self, 'prefixo', '2')
                if current_hour >= finaliza_ordens:
                    self.log(f"⏰ Fora do horário de envio de ordens (limite: {finaliza_ordens}h)")
                    return
                linha_operacao01 = self.obter_operacoes_candidatas()
                if not linha_operacao01:
                    self.log("📋 Nenhuma operação candidata encontrada")
                    return
                self.log(f"📊 Analisando {len(linha_operacao01)} operações candidatas")
                for linha_selecionada in linha_operacao01:
                    if not self.running:
                        break
                    depende_atual = linha_selecionada.get('Dependente')
                    independe_atual = linha_selecionada.get('Independente')
                    if not depende_atual or not independe_atual:
                        continue
                    if self.verificar_operacao_aberta([depende_atual]):
                        self.log(f"⚠️ Já existe posição aberta para {depende_atual}")
                        continue
                    qtd_op_script = self.contar_operacoes_por_prefixo(prefixo)
                    if qtd_op_script >= limite_operacoes:
                        self.log(f"⚠️ Limite de operações atingido: {qtd_op_script}/{limite_operacoes}")
                        continue
                    # ... aqui seguiria lógica de envio ...
                return
            # Se argumentos externos forem fornecidos (dashboard):
            # Espera-se que tabela_linha_operacao01 seja um DataFrame e config um dict
            if tabela_linha_operacao01 is not None and config is not None:
                # Replicar lógica do dashboard: para cada linha do DataFrame, processa ordem
                if tabela_linha_operacao01.empty:
                    self.log("⚠️ Nenhum par disponível para envio de ordens (via dashboard)")
                    return
                self.log("🚀 INICIANDO ENVIO AUTOMÁTICO DE ORDENS (via dashboard)")
                self.log("="*60)
                current_hour = datetime.now().hour
                finaliza_ordens = 24
                limite_operacoes = config.get('max_posicoes', 6)
                valor_operacao = 10000
                prefixo = "2"
                ordens_enviadas = 0
                max_ordens_por_ciclo = 3
                self.log(f"⚙️ Configurações: max_ordens={max_ordens_por_ciclo}, valor_op=R${valor_operacao:,}")
                if current_hour < finaliza_ordens:
                    for index, linha_selecionada in tabela_linha_operacao01.iterrows():
                        try:
                            if ordens_enviadas >= max_ordens_por_ciclo:
                                self.log(f"🚫 Limite de {max_ordens_por_ciclo} ordens por ciclo atingido")
                                break
                            depende_atual = linha_selecionada['Dependente']
                            independe_atual = linha_selecionada['Independente']
                            self.log(f"📊 Processando par: {depende_atual} x {independe_atual}")
                            zscore_hoje = linha_selecionada.get('Z-Score', 0)
                            beta_hoje = linha_selecionada.get('beta', 1)
                            r2_hoje = linha_selecionada.get('r2', 0)
                            self.log(f"📈 Z-Score: {zscore_hoje:.2f}, Beta: {beta_hoje:.3f}, R²: {r2_hoje:.3f}")
                            colunas_disponiveis = list(linha_selecionada.keys())
                            self.log(f"🔧 DEBUG: Colunas disponíveis na linha: {colunas_disponiveis[:10]}...")
                            if self.verificar_operacao_aberta([depende_atual]):
                                self.log(f"[ATENÇÃO] Já existe uma posição aberta para {depende_atual}")
                                continue
                            if zscore_hoje is None:
                                self.log(f"[AVISO] Z-Score inválido para {depende_atual} - pulando")
                                continue
                            # Aplica condições de entrada baseadas no Z-Score
                            if zscore_hoje is not None and -6.5 < zscore_hoje < -2.0:
                                self.log(f"🟢 PROCESSANDO COMPRA {depende_atual} + VENDA {independe_atual}")
                                self.processar_entrada_compra(linha_selecionada, valor_operacao)
                                ordens_enviadas += 1
                            elif zscore_hoje is not None and 2.0 < zscore_hoje < 6.5:
                                self.log(f"🔴 PROCESSANDO VENDA {depende_atual} + COMPRA {independe_atual}")
                                self.processar_entrada_venda(linha_selecionada, valor_operacao)
                                ordens_enviadas += 1
                            else:
                                self.log(f"⚠️ Z-Score {zscore_hoje:.2f} fora da faixa de operação para {depende_atual}")
                        except Exception as e:
                            self.log(f"❌ Erro ao processar linha {index}: {str(e)}")
                            continue
                self.log(f"✅ ENVIO AUTOMÁTICO CONCLUÍDO: {ordens_enviadas} ordens enviadas (via dashboard)")
                self.log("="*60)
        except Exception as e:
            self.log(f"❌ Erro geral no envio automático: {str(e)}")

    def processar_entrada_compra(self, linha_selecionada, valor_operacao):
        """Processa entrada de compra (DEP) + venda (IND)"""
        import MetaTrader5 as mt5
        
        try:
            depende_atual = linha_selecionada['Dependente']
            independe_atual = linha_selecionada['Independente']
            zscore_hoje = linha_selecionada['Z-Score']
            beta_hoje = linha_selecionada.get('beta', 1.0)
            r2_hoje = linha_selecionada.get('r2', 0.5)
            correlacao_hoje = linha_selecionada.get('correlacao', 0.5)
            magic_id = linha_selecionada.get('ID', int(time.time()))
            
            self.log(f"🟢 PROCESSANDO COMPRA: {depende_atual} | Z-Score: {zscore_hoje:.2f}")
            
            # Executa centro de comando de otimização (se disponível)
            resultado_otimizacao = self.executar_centro_comando_otimizacao(linha_selecionada)
            
            # Obtém preços e volumes otimizados
            price_dep_compra = self.obter_preco_compra_dependente(linha_selecionada, resultado_otimizacao)
            price_ind_venda = self.obter_preco_venda_independente(linha_selecionada, resultado_otimizacao)
            
            # Calcula stops
            stop_gain, stop_loss = self.calcular_stops_compra(linha_selecionada, resultado_otimizacao)
            stop_gain_ind, stop_loss_ind = self.calcular_stops_venda_independente(linha_selecionada)
            
            # Calcula volumes
            qtd_arredondada_dep = self.calcular_volume_dependente(price_dep_compra, stop_gain, valor_operacao, resultado_otimizacao)
            qtd_arredondada_ind = self.calcular_volume_independente(qtd_arredondada_dep, beta_hoje, resultado_otimizacao)
            
            # Validações finais
            if not self.validar_entrada_compra(linha_selecionada, price_dep_compra, stop_gain, resultado_otimizacao):
                return
            
            # Envia ordens
            sucesso = self.enviar_ordens_compra(
                depende_atual, independe_atual, magic_id,
                price_dep_compra, price_ind_venda,
                qtd_arredondada_dep, qtd_arredondada_ind,
                stop_gain, stop_loss, stop_gain_ind, stop_loss_ind,
                zscore_hoje, r2_hoje, beta_hoje, correlacao_hoje
            )
            
            if sucesso:
                self.log(f"✅ Ordens de compra enviadas com sucesso para {depende_atual}")
                self.salvar_detalhes_operacao(linha_selecionada, 'COMPRA', resultado_otimizacao)
            
        except Exception as e:
            self.log(f"❌ ERRO ao processar entrada de compra: {str(e)}")

    def processar_entrada_venda(self, linha_selecionada, valor_operacao):
        """Processa entrada de venda (DEP) + compra (IND)"""
        import MetaTrader5 as mt5
        
        try:
            depende_atual = linha_selecionada['Dependente']
            independe_atual = linha_selecionada['Independente']
            zscore_hoje = linha_selecionada['Z-Score']
            beta_hoje = linha_selecionada.get('beta', 1.0)
            r2_hoje = linha_selecionada.get('r2', 0.5)
            correlacao_hoje = linha_selecionada.get('correlacao', 0.5)
            magic_id = linha_selecionada.get('ID', int(time.time()))
            
            self.log(f"🔴 PROCESSANDO VENDA: {depende_atual} | Z-Score: {zscore_hoje:.2f}")
            
            # Executa centro de comando de otimização (se disponível)
            resultado_otimizacao = self.executar_centro_comando_otimizacao(linha_selecionada)
            
            # Obtém preços e volumes otimizados
            price_dep_venda = self.obter_preco_venda_dependente(linha_selecionada, resultado_otimizacao)
            price_ind_compra = self.obter_preco_compra_independente(linha_selecionada, resultado_otimizacao)
            
            # Calcula stops
            stop_gain, stop_loss = self.calcular_stops_venda(linha_selecionada, resultado_otimizacao)
            stop_gain_ind, stop_loss_ind = self.calcular_stops_compra_independente(linha_selecionada)
            
            # Calcula volumes
            qtd_arredondada_dep = self.calcular_volume_dependente(price_dep_venda, stop_gain, valor_operacao, resultado_otimizacao)
            qtd_arredondada_ind = self.calcular_volume_independente(qtd_arredondada_dep, beta_hoje, resultado_otimizacao)
            
            # Validações finais
            if not self.validar_entrada_venda(linha_selecionada, price_dep_venda, stop_gain, resultado_otimizacao):
                return
            
            # Envia ordens
            sucesso = self.enviar_ordens_venda(
                depende_atual, independe_atual, magic_id,
                price_dep_venda, price_ind_compra,
                qtd_arredondada_dep, qtd_arredondada_ind,
                stop_gain, stop_loss, stop_gain_ind, stop_loss_ind,
                zscore_hoje, r2_hoje, beta_hoje, correlacao_hoje
            )
            
            if sucesso:
                self.log(f"✅ Ordens de venda enviadas com sucesso para {depende_atual}")
                self.salvar_detalhes_operacao(linha_selecionada, 'VENDA', resultado_otimizacao)
            
        except Exception as e:
            self.log(f"❌ ERRO ao processar entrada de venda: {str(e)}")

    
    def executar_centro_comando_otimizacao(self, linha_selecionada):
        """Executa centro de comando de otimização (versão simplificada)"""
        try:
            # Versão simplificada do centro de comando
            resultado = {
                'entrada_otimizada': linha_selecionada.get('preco_atual', 25.0),
                'saida_otimizada': linha_selecionada.get('spread_compra_gain', 26.0),
                'fator_volume': 1.0,
                'fator_stop': 1.0,
                'fator_confianca': 0.7,
                'qualidade_sinal': 'MODERADA',
                'metodo_entrada': 'spreads_sistema',
                'alertas': ['Sistema operando normalmente'],
                'recomendacao_final': '✅ ENTRADA APROVADA'
            }
            
            # Ajustes baseados no Z-Score
            zscore = linha_selecionada.get('Z-Score', 0)
            if abs(zscore) > 3.0:
                resultado['fator_confianca'] = 0.9
                resultado['qualidade_sinal'] = 'ALTA'
            elif abs(zscore) < 2.0:
                resultado['fator_confianca'] = 0.4
                resultado['qualidade_sinal'] = 'BAIXA'
            
            return resultado
            
        except Exception as e:
            self.log(f"❌ ERRO no centro de comando: {str(e)}")
            return {'fator_volume': 1.0, 'fator_stop': 1.0, 'fator_confianca': 0.5}

    def obter_preco_compra_dependente(self, linha_selecionada, resultado_otimizacao):
        """Obtém preço de compra do dependente"""
        if resultado_otimizacao and resultado_otimizacao.get('entrada_otimizada'):
            return round(resultado_otimizacao['entrada_otimizada'], 2)
        return round(linha_selecionada.get('spread_compra', linha_selecionada.get('preco_atual', 25.0)), 2)

    def obter_preco_venda_dependente(self, linha_selecionada, resultado_otimizacao):
        """Obtém preço de venda do dependente"""
        if resultado_otimizacao and resultado_otimizacao.get('entrada_otimizada'):
            return round(resultado_otimizacao['entrada_otimizada'], 2)
        return round(linha_selecionada.get('spread_venda', linha_selecionada.get('preco_atual', 25.0)), 2)

    def obter_preco_venda_independente(self, linha_selecionada, resultado_otimizacao=None):
        """Obtém preço de venda do independente"""
        return round(linha_selecionada.get('indep_spread_venda', 85.0), 2)

    def obter_preco_compra_independente(self, linha_selecionada, resultado_otimizacao=None):
        """Obtém preço de compra do independente"""
        return round(linha_selecionada.get('indep_spread_compra', 85.0), 2)

    def calcular_stops_compra(self, linha_selecionada, resultado_otimizacao):
        """Calcula stops para compra do dependente"""
        if resultado_otimizacao and resultado_otimizacao.get('saida_otimizada'):
            stop_gain = round(resultado_otimizacao['saida_otimizada'], 2)
        else:
            stop_gain = round(linha_selecionada.get('spread_compra_gain', 26.0), 2)
        
        stop_loss = round(linha_selecionada.get('spread_compra_loss', 24.0), 2)
        return stop_gain, stop_loss

    def calcular_stops_venda(self, linha_selecionada, resultado_otimizacao):
        """Calcula stops para venda do dependente"""
        if resultado_otimizacao and resultado_otimizacao.get('saida_otimizada'):
            stop_gain = round(resultado_otimizacao['saida_otimizada'], 2)
        else:
            stop_gain = round(linha_selecionada.get('spread_venda_gain', 24.0), 2)
        
        stop_loss = round(linha_selecionada.get('spread_venda_loss', 26.0), 2)
        return stop_gain, stop_loss

    def calcular_stops_venda_independente(self, linha_selecionada):
        """Calcula stops para venda do independente"""
        stop_gain = round(linha_selecionada.get('indep_spread_venda_gain', 84.0), 2)
        stop_loss = round(linha_selecionada.get('indep_spread_venda_loss', 86.0), 2)
        return stop_gain, stop_loss

    def calcular_stops_compra_independente(self, linha_selecionada):
        """Calcula stops para compra do independente"""
        stop_gain = round(linha_selecionada.get('indep_spread_compra_gain', 86.0), 2)
        stop_loss = round(linha_selecionada.get('indep_spread_compra_loss', 84.0), 2)
        return stop_gain, stop_loss

    def calcular_volume_dependente(self, preco_entrada, stop_gain, valor_operacao, resultado_otimizacao):
        """Calcula volume para o ativo dependente"""
        try:
            lucro_estimado = stop_gain - preco_entrada
            lucro_estimado = max(lucro_estimado, 0.01)  # Evita divisão por zero
            
            qtd_calculada = valor_operacao / (preco_entrada + lucro_estimado)
            
            # Aplica fator de otimização
            if resultado_otimizacao:
                qtd_calculada *= resultado_otimizacao.get('fator_volume', 1.0)
            
            return max(round(qtd_calculada, -2), 100)  # Mínimo 100 ações
            
        except Exception as e:
            self.log(f"❌ ERRO ao calcular volume dependente: {str(e)}")
            return 100

    def calcular_volume_independente(self, qtd_dependente, beta, resultado_otimizacao):
        """Calcula volume para o ativo independente"""
        try:
            qtd_independente = qtd_dependente * abs(beta)
            
            # Aplica fator de otimização
            if resultado_otimizacao:
                qtd_independente *= resultado_otimizacao.get('fator_volume', 1.0)
            
            return max(round(qtd_independente, -2), 100)  # Mínimo 100 ações
            
        except Exception as e:
            self.log(f"❌ ERRO ao calcular volume independente: {str(e)}")
            return 100

    def validar_entrada_compra(self, linha_selecionada, price_dep_compra, stop_gain, resultado_otimizacao):
        """Valida condições para entrada de compra"""
        try:
            # Validações extraídas do código original
            depende_atual = linha_selecionada['Dependente']
            pred_resid = float(linha_selecionada.get('pred_resid', 0.0))
            resid_atual = float(linha_selecionada.get('resid_atual', 0.0))
            preco_atual = float(linha_selecionada.get('preco_atual', 0.0))
            min_dist_acao_dep = stop_gain * 0.99

            # Verifica se já existe ordem de compra
            existe_ordem_compra = self.verificar_operacao_aberta_tipo(depende_atual, 'buy')
            if existe_ordem_compra:
                self.log(f"⚠️ Já existe ordem de compra para {depende_atual}")
                return False

            # Validação de previsão
            if not (pred_resid > resid_atual):
                self.log(f"⚠️ Condição de previsão não atendida para {depende_atual} | pred_resid={pred_resid} <= resid_atual={resid_atual}")
                return False

            # Validação de distância mínima
            if not (price_dep_compra < min_dist_acao_dep):
                self.log(f"⚠️ Preço não atingiu distância mínima para {depende_atual} | price_dep_compra={price_dep_compra} >= min_dist_acao_dep={min_dist_acao_dep}")
                return False

            # Validação de preço atual
            if not (price_dep_compra < preco_atual):
                self.log(f"⚠️ Preço de entrada não é favorável para {depende_atual} | price_dep_compra={price_dep_compra} >= preco_atual={preco_atual}")
                return False

            # Validação de confiança
            if resultado_otimizacao:
                fator_confianca = resultado_otimizacao.get('fator_confianca', 0.0)
                if fator_confianca < 0.4:
                    self.log(f"⚠️ Nível de confiança muito baixo: {fator_confianca:.2f} para {depende_atual}")
                    return False

            return True

        except Exception as e:
            self.log(f"❌ ERRO na validação de compra: {str(e)}")
            return False

    def validar_entrada_venda(self, linha_selecionada, price_dep_venda, stop_gain, resultado_otimizacao):
        """Valida condições para entrada de venda"""
        try:
            # Validações extraídas do código original
            depende_atual = linha_selecionada['Dependente']
            pred_resid = float(linha_selecionada.get('pred_resid', 0.0))
            resid_atual = float(linha_selecionada.get('resid_atual', 0.0))
            preco_atual = float(linha_selecionada.get('preco_atual', 0.0))
            min_dist_acao_dep = stop_gain * 1.01

            # Verifica se já existe ordem de venda
            existe_ordem_venda = self.verificar_operacao_aberta_tipo(depende_atual, 'sell')
            if existe_ordem_venda:
                self.log(f"⚠️ Já existe ordem de venda para {depende_atual}")
                return False

            # Validação de previsão
            if not (pred_resid < resid_atual):
                self.log(f"⚠️ Condição de previsão não atendida para {depende_atual} | pred_resid={pred_resid} >= resid_atual={resid_atual}")
                return False

            # Validação de distância mínima
            if not (price_dep_venda > min_dist_acao_dep):
                self.log(f"⚠️ Preço não atingiu distância mínima para {depende_atual} | price_dep_venda={price_dep_venda} <= min_dist_acao_dep={min_dist_acao_dep}")
                return False

            # Validação de preço atual
            if not (price_dep_venda > preco_atual):
                self.log(f"⚠️ Preço de entrada não é favorável para {depende_atual} | price_dep_venda={price_dep_venda} <= preco_atual={preco_atual}")
                return False

            # Validação de confiança
            if resultado_otimizacao:
                fator_confianca = resultado_otimizacao.get('fator_confianca', 0.0)
                if fator_confianca < 0.4:
                    self.log(f"⚠️ Nível de confiança muito baixo: {fator_confianca:.2f} para {depende_atual}")
                    return False

            return True

        except Exception as e:
            self.log(f"❌ ERRO na validação de venda: {str(e)}")
            return False

    def enviar_ordens_compra(self, depende_atual, independe_atual, magic_id, 
                           price_dep_compra, price_ind_venda,
                           qtd_dep, qtd_ind, stop_gain_dep, stop_loss_dep, 
                           stop_gain_ind, stop_loss_ind,
                           zscore, r2, beta, correlacao):
        """Envia ordens de compra (DEP) + venda (IND)"""
        import MetaTrader5 as mt5
        
        try:
            # Ordem de compra do dependente
            ordem_compra_dep = {
                "action": mt5.TRADE_ACTION_PENDING,
                "symbol": depende_atual,
                "volume": qtd_dep,
                "type": mt5.ORDER_TYPE_BUY_LIMIT,
                "price": price_dep_compra,
                "tp": stop_gain_dep,
                "sl": stop_loss_dep,
                "magic": magic_id,
                "comment": f"SisDep_Z{zscore:.1f}_R{r2:.2f}",
                "type_time": mt5.ORDER_TIME_DAY,
                "type_filling": mt5.ORDER_FILLING_RETURN,
            }
            
            # Ordem de venda do independente
            ordem_venda_ind = {
                "action": mt5.TRADE_ACTION_PENDING,
                "symbol": independe_atual,
                "volume": qtd_ind,
                "type": mt5.ORDER_TYPE_SELL_LIMIT,
                "price": price_ind_venda,
                "tp": stop_gain_ind,
                "sl": stop_loss_ind,
                "magic": magic_id,
                "comment": f"SisInd_B{beta:.2f}_C{correlacao:.2f}",
                "type_time": mt5.ORDER_TIME_DAY,
                "type_filling": mt5.ORDER_FILLING_RETURN,
            }
            
            # Envia ordem do dependente
            result_dep = mt5.order_send(ordem_compra_dep)
            self.log(f"📤 Ordem COMPRA {depende_atual} enviada")
            
            if result_dep is None:
                self.log(f"❌ Erro: result_dep retornou None - {mt5.last_error()}")
                return False
            
            if result_dep.retcode != mt5.TRADE_RETCODE_DONE:
                self.log(f"❌ Falha na ordem {depende_atual}: retcode {result_dep.retcode}")
                return False
            
            # Envia ordem do independente
            result_ind = mt5.order_send(ordem_venda_ind)
            self.log(f"📤 Ordem VENDA {independe_atual} enviada")
            
            if result_ind is None:
                self.log(f"❌ Erro: result_ind retornou None - {mt5.last_error()}")
                return False
            
            if result_ind.retcode != mt5.TRADE_RETCODE_DONE:
                self.log(f"❌ Falha na ordem {independe_atual}: retcode {result_ind.retcode}")
                return False
            
            self.log(f"✅ Par enviado com sucesso: {depende_atual} / {independe_atual}")
            return True
            
        except Exception as e:
            self.log(f"❌ ERRO ao enviar ordens de compra: {str(e)}")
            return False

    def enviar_ordens_venda(self, depende_atual, independe_atual, magic_id,
                          price_dep_venda, price_ind_compra,
                          qtd_dep, qtd_ind, stop_gain_dep, stop_loss_dep,
                          stop_gain_ind, stop_loss_ind,
                          zscore, r2, beta, correlacao):
        """Envia ordens de venda (DEP) + compra (IND)"""
        import MetaTrader5 as mt5
        
        try:
            # Ordem de venda do dependente
            ordem_venda_dep = {
                "action": mt5.TRADE_ACTION_PENDING,
                "symbol": depende_atual,
                "volume": qtd_dep,
                "type": mt5.ORDER_TYPE_SELL_LIMIT,
                "price": price_dep_venda,
                "tp": stop_gain_dep,
                "sl": stop_loss_dep,
                "magic": magic_id,
                "comment": f"SisDep_Z{zscore:.1f}_R{r2:.2f}",
                "type_time": mt5.ORDER_TIME_DAY,
                "type_filling": mt5.ORDER_FILLING_RETURN,
            }
            
            # Ordem de compra do independente
            ordem_compra_ind = {
                "action": mt5.TRADE_ACTION_PENDING,
                "symbol": independe_atual,
                "volume": qtd_ind,
                "type": mt5.ORDER_TYPE_BUY_LIMIT,
                "price": price_ind_compra,
                "tp": stop_gain_ind,
                "sl": stop_loss_ind,
                "magic": magic_id,
                "comment": f"SisInd_B{beta:.2f}_C{correlacao:.2f}",
                "type_time": mt5.ORDER_TIME_DAY,
                "type_filling": mt5.ORDER_FILLING_RETURN,
            }
            
            # Envia ordem do dependente
            result_dep = mt5.order_send(ordem_venda_dep)
            self.log(f"📤 Ordem VENDA {depende_atual} enviada")
            
            if result_dep is None:
                self.log(f"❌ Erro: result_dep retornou None - {mt5.last_error()}")
                return False
            
            if result_dep.retcode != mt5.TRADE_RETCODE_DONE:
                self.log(f"❌ Falha na ordem {depende_atual}: retcode {result_dep.retcode}")
                return False
            
            # Envia ordem do independente
            result_ind = mt5.order_send(ordem_compra_ind)
            self.log(f"📤 Ordem COMPRA {independe_atual} enviada")
            
            if result_ind is None:
                self.log(f"❌ Erro: result_ind retornou None - {mt5.last_error()}")
                return False
            
            if result_ind.retcode != mt5.TRADE_RETCODE_DONE:
                self.log(f"❌ Falha na ordem {independe_atual}: retcode {result_ind.retcode}")
                return False
            
            self.log(f"✅ Par enviado com sucesso: {depende_atual} / {independe_atual}")
            return True
            
        except Exception as e:
            self.log(f"❌ ERRO ao enviar ordens de venda: {str(e)}")
            return False

    def verificar_operacao_aberta(self, ativos):
        """Verifica se existe operação aberta para os ativos"""
        import MetaTrader5 as mt5
        
        try:
            posicoes = mt5.positions_get()
            if not posicoes:
                return False
            
            # Filtra apenas posições do sistema atual
            for pos in posicoes:
                if (str(pos.magic).startswith(self.prefixo) and 
                    pos.symbol in ativos):
                    return True
            
            return False
            
        except Exception as e:
            self.log(f"❌ ERRO ao verificar operação aberta: {str(e)}")
            return False

    def verificar_operacao_aberta_tipo(self, ativo, tipo):
        """Verifica se existe operação aberta de um tipo específico para o ativo"""
        import MetaTrader5 as mt5
        
        try:
            posicoes = mt5.positions_get(symbol=ativo)
            if not posicoes:
                return False
            
            tipo_mt5 = mt5.POSITION_TYPE_BUY if tipo.lower() == 'buy' else mt5.POSITION_TYPE_SELL
            
            # Filtra apenas posições do sistema atual
            for pos in posicoes:
                if (str(pos.magic).startswith(self.prefixo) and 
                    pos.type == tipo_mt5):
                    return True
            
            return False
            
        except Exception as e:
            self.log(f"❌ ERRO ao verificar operação aberta por tipo: {str(e)}")
            return False

    def contar_operacoes_por_prefixo(self, prefixo):
        """Conta operações abertas com o prefixo especificado"""
        import MetaTrader5 as mt5
        
        try:
            posicoes = mt5.positions_get()
            if not posicoes:
                return 0
            
            count = 0
            for pos in posicoes:
                if str(pos.magic).startswith(str(prefixo)):
                    count += 1
            
            return count
            
        except Exception as e:
            self.log(f"❌ ERRO ao contar operações: {str(e)}")
            return 0

    def salvar_detalhes_operacao(self, linha_selecionada, tipo_operacao, resultado_otimizacao):
        """Salva detalhes da operação executada"""
        try:
            detalhes = {
                'timestamp': datetime.now().isoformat(),
                'tipo_operacao': tipo_operacao,
                'dependente': linha_selecionada.get('Dependente'),
                'independente': linha_selecionada.get('Independente'),
                'zscore': linha_selecionada.get('Z-Score'),
                'beta': linha_selecionada.get('beta'),
                'r2': linha_selecionada.get('r2'),
                'correlacao': linha_selecionada.get('correlacao'),
                'magic_id': linha_selecionada.get('ID'),
                'qualidade_sinal': resultado_otimizacao.get('qualidade_sinal', 'N/A') if resultado_otimizacao else 'N/A',
                'fator_confianca': resultado_otimizacao.get('fator_confianca', 0.0) if resultado_otimizacao else 0.0
            }
            
            # Adiciona aos dados do sistema
            self.dados_sistema["ordens_enviadas"] += 1
            
            # Aqui você pode salvar em arquivo JSON, banco de dados, etc.
            self.log(f"💾 Detalhes da operação {tipo_operacao} salvos")
            
        except Exception as e:
            self.log(f"❌ ERRO ao salvar detalhes da operação: {str(e)}")

    def executar_monitoramento_real(self):
        """Executa monitoramento real de posições com MT5"""
        import MetaTrader5 as mt5
        
        try:
            # Obtém posições e ordens pendentes
            posicoes_abertas = mt5.positions_get()
            posicoes_pendentes = mt5.orders_get()
            
            if posicoes_abertas is not None and len(posicoes_abertas) > 0:
                self.log(f"📊 Número de operações em aberto: {len(posicoes_abertas)}")
                
                # Prefixo do script (configurável)
                prefixo_script = self.prefixo  # Usa o prefixo da configuração da classe
                
                # Filtra apenas as posições com magic prefixo específico
                def magic_comeca_com(magic, prefixo):
                    return str(magic).startswith(prefixo)
                
                magics_abertas = set(p.magic for p in posicoes_abertas if magic_comeca_com(p.magic, prefixo_script))
                
                for magic in magics_abertas:
                    pos_magic = [p for p in posicoes_abertas if p.magic == magic]
                    
                    # Se apenas uma perna do par está aberta
                    if len(pos_magic) == 1:
                        posicao = pos_magic[0]
                        ativo_aberto = posicao.symbol
                        
                        self.log(f"⚠️ Magic {magic}: Apenas uma perna aberta ({ativo_aberto})")
                        
                        # Busca o par configurado
                        pares = self.obter_pares_configurados()
                        depende_atual, independe_atual = pares.get(magic, (None, None))
                        
                        if depende_atual is None or independe_atual is None:
                            self.log(f"[AVISO] Par de ativos não encontrado para magic {magic}. Fechando posição órfã...")
                            # Em modo fallback, fecha a posição órfã diretamente
                            self.programar_fechamento_posicao(magic, posicoes_abertas, posicoes_pendentes)
                            continue
                        
                        # Se o ativo aberto NÃO for o dependente, fecha o restante (independente)
                        if ativo_aberto != depende_atual:
                            self.log(f"📌 Magic={magic}: ativo dependente ({depende_atual}) já foi fechado.")
                            self.log(f"   Fechando perna remanescente ({ativo_aberto})...")
                            self.programar_fechamento_posicao(magic, posicoes_abertas, posicoes_pendentes)
                        
                        # Se o ativo aberto É o dependente, verifica ordens pendentes do independente
                        elif ativo_aberto == depende_atual:
                            ordens_pendentes_indep = [o for o in posicoes_pendentes 
                                                    if o.symbol == independe_atual and o.magic == magic] if posicoes_pendentes else []
                            
                            if ordens_pendentes_indep:
                                self.log(f"🔄 Magic={magic}: Dependente aberto, convertendo ordem pendente do independente para mercado")
                                self.converter_ordem_pendente_para_mercado(magic, posicao, ordens_pendentes_indep, independe_atual)
                
                # Calcula lucros/prejuízos por magic
                self.calcular_lucros_por_magic(magics_abertas, posicoes_abertas)
            else:
                self.log("✅ Nenhuma posição aberta no momento")
                
        except Exception as e:
            self.log(f"❌ ERRO no monitoramento real: {str(e)}")
       
    def programar_fechamento_posicao(self, magic, posicoes_abertas, posicoes_pendentes=None):
        """Programa fechamento de posição - implementação real baseada no calculo_entradas_v55.py"""
        import MetaTrader5 as mt5
        
        self.log(f"🔄 Executando fechamento para Magic {magic}")
        
        try:
            # FECHA POSIÇÕES ABERTAS (baseado na função fechar_posicoes do calculo_entradas_v55.py)
            if posicoes_abertas:
                for posicao in posicoes_abertas:
                    if posicao.magic == magic:
                        symbol = posicao.symbol
                        type_pos = posicao.type
                        volume = posicao.volume

                        # Determina tipo de ordem para fechamento
                        if type_pos == mt5.POSITION_TYPE_BUY:
                            price = mt5.symbol_info_tick(symbol).bid
                            order_type = mt5.ORDER_TYPE_SELL
                        else:
                            price = mt5.symbol_info_tick(symbol).ask
                            order_type = mt5.ORDER_TYPE_BUY

                        # Prepara requisição de fechamento
                        request = {
                            "action": mt5.TRADE_ACTION_DEAL,
                            "symbol": symbol,
                            "volume": volume,
                            "type": order_type,
                            "position": posicao.ticket,
                            "price": price,
                            "magic": posicao.magic,
                            "comment": "Fechar posição_s_i",
                            "type_time": mt5.ORDER_TIME_GTC,
                            "type_filling": mt5.ORDER_FILLING_IOC,
                        }
                        
                        # Executa fechamento
                        result = mt5.order_send(request)
                        if result is None:
                            self.log(f"❌ [ERRO] order_send retornou None ao fechar posição ticket={posicao.ticket}")
                            self.log(f"   Último erro: {mt5.last_error()}")
                        elif result.retcode != mt5.TRADE_RETCODE_DONE:
                            self.log(f"❌ Erro ao fechar posição {posicao.ticket}, retcode={result.retcode}")
                        else:
                            self.log(f"✅ Posição ticket={posicao.ticket} ({symbol}) fechada com sucesso")

            # CANCELA ORDENS PENDENTES (baseado na função fechar_posicoes do calculo_entradas_v55.py)
            if posicoes_pendentes:
                for ordem in posicoes_pendentes:
                    if ordem.magic == magic:
                        symbol = ordem.symbol
                        # Prepara requisição de cancelamento
                        request = {
                            "action": mt5.TRADE_ACTION_REMOVE,
                            "order": ordem.ticket,
                            "symbol": symbol,
                            "magic": ordem.magic,
                            "comment": "Cancelar ordem pend_s_i",
                            "type_time": mt5.ORDER_TIME_GTC,
                            "type_filling": mt5.ORDER_FILLING_IOC,
                        }
                        
                        # Executa cancelamento
                        result = mt5.order_send(request)
                        if result is None:
                            self.log(f"❌ [ERRO] order_send retornou None ao cancelar ordem pendente={ordem.ticket}")
                            self.log(f"   Último erro: {mt5.last_error()}")
                        elif result.retcode != mt5.TRADE_RETCODE_DONE:
                            self.log(f"❌ Erro ao cancelar ordem pendente {ordem.ticket}, retcode={result.retcode}")
                        else:
                            self.log(f"✅ Ordem pendente ticket={ordem.ticket} ({symbol}) cancelada com sucesso")
                            
        except Exception as e:
            self.log(f"❌ ERRO no fechamento de posições: {str(e)}")
    
    def converter_ordem_pendente_para_mercado(self, magic, posicao, ordens_pendentes, independe_atual):
        """Converte ordem pendente para ordem a mercado - implementação real baseada no calculo_entradas_v55.py"""
        import MetaTrader5 as mt5
        
        self.log(f"🔄 Convertendo ordem pendente para mercado: {independe_atual} (Magic {magic})")
        
        try:
            for ordem in ordens_pendentes:
                # 1. CANCELA A ORDEM PENDENTE
                cancel_request = {
                    "action": mt5.TRADE_ACTION_REMOVE,
                    "order": ordem.ticket,
                }
                result_cancel = mt5.order_send(cancel_request)
                
                if result_cancel and result_cancel.retcode == mt5.TRADE_RETCODE_DONE:
                    self.log(f"✅ [OK] Ordem pendente do independente ({independe_atual}) cancelada para magic {magic}")
                else:
                    self.log(f"❌ [ERRO] Falha ao cancelar ordem pendente do independente ({independe_atual}) para magic {magic}")
                    continue

                # 2. ENVIA ORDEM A MERCADO PARA O INDEPENDENTE
                symbol_info_tick = mt5.symbol_info_tick(independe_atual)
                if not symbol_info_tick:
                    self.log(f"❌ [ERRO] Não foi possível obter cotação para {independe_atual}")
                    continue

                # Determina tipo de ordem baseado na posição do dependente
                # Se dependente está comprado, independente deve ser vendido (estratégia de pair trading)
                tipo_ordem = mt5.ORDER_TYPE_SELL if posicao.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
                preco = symbol_info_tick.bid if tipo_ordem == mt5.ORDER_TYPE_SELL else symbol_info_tick.ask
                volume = posicao.volume  # Usa mesmo volume da posição dependente
                # Prepara ordem a mercado
                ordem_mercado = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": independe_atual,
                    "volume": volume,
                    "type": tipo_ordem,
                    "price": preco,
                    "magic": magic,
                    "comment": "AutoMarketIndep_s_i",
                    "type_time": mt5.ORDER_TIME_DAY,
                    "type_filling": mt5.ORDER_FILLING_RETURN,
                }
                
                # Executa ordem a mercado
                result_envio = mt5.order_send(ordem_mercado)
                if result_envio and result_envio.retcode == mt5.TRADE_RETCODE_DONE:
                    self.log(f"✅ [OK] Ordem a mercado enviada para o independente ({independe_atual}) do magic {magic}")
                else:
                    retcode = getattr(result_envio, 'retcode', None) if result_envio else None
                    self.log(f"❌ [ERRO] Falha ao enviar ordem a mercado para o independente ({independe_atual}) do magic {magic}. Retcode: {retcode}")
                    
        except Exception as e:
            self.log(f"❌ ERRO na conversão de ordem pendente: {str(e)}")
    
    def calcular_lucros_por_magic(self, magics_abertas, posicoes_abertas):
        """Calcula lucros/prejuízos por magic - baseado na função calcular_lucro_prejuizo_por_magic do calculo_entradas_v55.py"""
        self.log("💰 ANÁLISE DE LUCROS/PREJUÍZOS POR MAGIC:")
        
        for magic in magics_abertas:
            lucro_prejuizo = 0.00
            
            # Calcula lucro/prejuízo para cada posição do magic
            for posicao in posicoes_abertas:
                if posicao.magic == magic:
                    import MetaTrader5 as mt5
                    
                    symbol = posicao.symbol
                    type_pos = posicao.type
                    volume = posicao.volume
                    open_price = posicao.price_open
                    close_price = posicao.price_current if posicao.price_current else mt5.symbol_info_tick(symbol).bid
                    
                    # Calcula P&L baseado no tipo de posição
                    if type_pos == mt5.POSITION_TYPE_BUY:
                        lucro_prejuizo += (close_price - open_price) * volume
                    else:
                        lucro_prejuizo += (open_price - close_price) * volume
            
            status = "🟢" if lucro_prejuizo > 0 else "🔴" if lucro_prejuizo < 0 else "⚪"
            self.log(f"   Magic {magic}: {status} R$ {lucro_prejuizo:+.2f}")
            
            # Verifica limites (configuráveis)
            limite_lucro = 120.0
            limite_prejuizo = 120.0
            
            if lucro_prejuizo >= limite_lucro:
                self.log(f"   🚨 LIMITE MÁXIMO ATINGIDO: Magic {magic} (R$ {lucro_prejuizo:.2f})")
                # Aqui poderia chamar fechamento automático se necessário
                self.programar_fechamento_posicao(magic, posicoes_abertas)
            elif lucro_prejuizo <= -limite_prejuizo:
                self.log(f"   🚨 LIMITE DE PREJUÍZO ATINGIDO: Magic {magic} (R$ {lucro_prejuizo:.2f})")
                # Aqui poderia chamar fechamento automático se necessário
                self.programar_fechamento_posicao(magic, posicoes_abertas)

    def thread_break_even_continuo(self):
        """Thread para monitoramento contínuo de break-even durante pregão"""
        self.log("📈 INICIANDO: Thread de Break-Even Contínuo")
        
        try:
            import MetaTrader5 as mt5
            mt5_disponivel = True
        except ImportError:
            mt5_disponivel = False
            self.log("⚠️ MetaTrader5 não disponível para break-even")
            return
        
        while self.running:
            try:
                current_hour = datetime.now().hour
                
                # Break-even contínuo durante janela de pregão
                if self.JANELA_BREAK_EVEN[0] <= current_hour < self.JANELA_BREAK_EVEN[1]:
                    self.executar_break_even_continuo()
                
                # Aguarda 10 segundos para próxima verificação
                for i in range(10):
                    if not self.running:
                        break
                    time.sleep(1)
                
            except Exception as e:
                self.log(f"❌ ERRO no break-even contínuo: {str(e)}")
                time.sleep(30)
    
    def executar_break_even_continuo(self):
        """Executa break-even contínuo baseado no bloco do calculo_entradas_v55.py"""
        import MetaTrader5 as mt5
        
        try:
            posicoes_abertas = mt5.positions_get()
            if not posicoes_abertas:
                return
            
            for pos in posicoes_abertas:
                # Filtra apenas posições do sistema atual
                if not str(pos.magic).startswith(self.prefixo):
                    continue
                    
                ticket = pos.ticket
                symbol = pos.symbol.upper()
                tipo = pos.type
                preco_abertura = pos.price_open
                sl_atual = pos.sl

                # Anti-duplo-ajuste e ignora pos sem SL
                if ticket in self.stops_ja_ajustados or sl_atual <= 0:
                    continue

                tick = mt5.symbol_info_tick(symbol)
                if not tick:
                    continue

                # 1) Calcula lucro em pontos
                if tipo == mt5.POSITION_TYPE_BUY:
                    atual = tick.bid
                    lucro_pontos = atual - preco_abertura
                else:
                    atual = tick.ask
                    lucro_pontos = preco_abertura - atual

                # 2) Escolhe divisor e thresholds por símbolo
                if symbol == 'WINM25':  # Mini índice
                    lucro_pct = lucro_pontos / 5
                    thr_breakeven = 150   # move SL
                    thr_close = 300       # fecha
                else:
                    # Padrão genérico para ações
                    lucro_pct = (lucro_pontos / preco_abertura) * 100
                    thr_breakeven = 0.8   # 0.8% genérico
                    thr_close = 1.2       # 1.2% genérico

                # 3) Aplica regras de break-even
                if lucro_pct >= thr_breakeven:
                    self.log(f"📈 {symbol} lucro {lucro_pct:.2f}%, movendo SL breakeven (ticket {ticket})")
                    self.mover_stop_loss_para_break_even(pos, preco_abertura)
                    self.stops_ja_ajustados.add(ticket)

                if lucro_pct >= thr_close:
                    self.log(f"💰 {symbol} lucro {lucro_pct:.2f}%, fechando posição (ticket {ticket})")
                    self.fechar_posicao_especifica(pos)
                    self.stops_ja_ajustados.add(ticket)
                    
        except Exception as e:
            self.log(f"❌ ERRO no break-even contínuo: {str(e)}")

    def thread_ajustes_programados(self):
        """Thread para ajustes programados em horários específicos"""
        self.log("⏰ INICIANDO: Thread de Ajustes Programados")
        
        try:
            import MetaTrader5 as mt5
            mt5_disponivel = True
        except ImportError:
            mt5_disponivel = False
            self.log("⚠️ MetaTrader5 não disponível para ajustes programados")
            return
        
        while self.running:
            try:
                current_hour = datetime.now().hour
                current_minute = datetime.now().minute
                data_hoje = datetime.now().strftime('%Y-%m-%d')
                
                # 1. Ajuste de posições às 15:10h
                if (current_hour == self.horario_ajuste_stops and 
                    current_minute >= self.ajusta_ordens_minuto and 
                    f"ajuste_posicoes_{data_hoje}" not in self.ajustes_executados_hoje):
                    
                    self.executar_ajuste_posicoes_15h10()
                    self.ajustes_executados_hoje.add(f"ajuste_posicoes_{data_hoje}")
                  # 2. Remoção de ordens pendentes às 15:20h
                if (current_hour >= self.horario_remove_pendentes and 
                    current_minute >= 20 and 
                    f"remove_pendentes_{data_hoje}" not in self.ajustes_executados_hoje):
                    
                    self.executar_remocao_pendentes()
                    self.ajustes_executados_hoje.add(f"remove_pendentes_{data_hoje}")
                
                # 3. Fechamento total às 16:01h
                if (current_hour >= self.horario_fechamento_total and 
                    current_minute >= 1 and 
                    f"fechamento_total_{data_hoje}" not in self.ajustes_executados_hoje):
                    
                    self.executar_fechamento_total()
                    self.ajustes_executados_hoje.add(f"fechamento_total_{data_hoje}")
                
                # Aguarda 30 segundos para próxima verificação
                for i in range(30):
                    if not self.running:
                        break
                    time.sleep(1)
                
            except Exception as e:
                self.log(f"❌ ERRO nos ajustes programados: {str(e)}")
                time.sleep(60)

    def executar_ajuste_posicoes_15h10(self):
        """Executa ajuste de posições às 15:10h baseado no calculo_entradas_v55.py"""
        import MetaTrader5 as mt5
        
        current_hour = datetime.now().hour
        current_minute = datetime.now().minute
        
        self.log(f"🔧 INICIANDO AJUSTE DE POSIÇÕES ÀS {current_hour:02d}:{current_minute:02d}")
        
        try:
            posicoes_abertas = mt5.positions_get()
            if not posicoes_abertas:
                self.log("📋 Nenhuma posição aberta encontrada")
                return
            
            # Filtrar apenas posições do sistema atual
            posicoes_sistema = [pos for pos in posicoes_abertas 
                              if str(pos.magic).startswith(self.prefixo)]
            
            if not posicoes_sistema:
                self.log("📋 Nenhuma posição do sistema encontrada para ajustar")
                return
            
            self.log(f"📊 Encontradas {len(posicoes_sistema)} posições do sistema para ajustar")
            
            for pos in posicoes_sistema:
                self.processar_ajuste_posicao(pos)
                
            self.log(f"✅ AJUSTE DE POSIÇÕES CONCLUÍDO ÀS {current_hour:02d}:{current_minute:02d}")
            
        except Exception as e:
            self.log(f"❌ ERRO no ajuste de posições: {str(e)}")

    def processar_ajuste_posicao(self, pos):
        """Processa ajuste individual de uma posição"""
        import MetaTrader5 as mt5
        
        try:
            ticket_posicao = pos.ticket
            symbol = pos.symbol
            tipo_posicao = pos.type
            preco_abertura = pos.price_open
            stop_loss_atual = pos.sl
            stop_gain_atual = pos.tp

            self.log(f"🔍 Analisando posição: {symbol} (Ticket: {ticket_posicao})")

            # Se já ajustamos antes
            if ticket_posicao in self.stops_ja_ajustados:
                self.log(f"⏭️ Ticket {ticket_posicao} já foi ajustado hoje - pulando")
                return

            # Ignora posições sem SL ou TP
            if stop_loss_atual <= 0 or stop_gain_atual <= 0:
                self.log(f"⚠️ Posição {ticket_posicao} sem SL/TP configurado - pulando")
                return

            # Calcular lucro atual em %
            symbol_info_tick = mt5.symbol_info_tick(symbol)
            if not symbol_info_tick:
                self.log(f"❌ Erro ao obter TICK para {symbol} - pulando")
                return

            if tipo_posicao == mt5.POSITION_TYPE_BUY:
                current_price = symbol_info_tick.bid
                profit_points = current_price - preco_abertura
            else:
                current_price = symbol_info_tick.ask
                profit_points = preco_abertura - current_price

            profit_percent = (profit_points / preco_abertura) * 100
            self.log(f"💰 Ticket={ticket_posicao}, Lucro atual = {profit_percent:.2f}%")

            # Aplicar regras de ajuste
            if profit_percent > 25:
                # Fechar posição com lucro > 25%
                self.log(f"🎯 Lucro > 25% em {symbol}, fechando posição (ticket={ticket_posicao})")
                self.fechar_posicao_especifica(pos)
                self.stops_ja_ajustados.add(ticket_posicao)
                
            elif 15 <= profit_percent <= 24:
                # Mover SL para break-even (lucro entre 15% e 24%)
                self.log(f"📈 Lucro entre 15% e 24% em {symbol}, movendo SL para break even")
                self.mover_stop_loss_para_break_even(pos, preco_abertura)
                self.stops_ja_ajustados.add(ticket_posicao)
                
            else:
                # Ajustar TP para 60% da distância original
                self.ajustar_tp_60_porcento(pos, symbol_info_tick)
                
        except Exception as e:
            self.log(f"❌ Erro ao processar ajuste da posição {pos.ticket}: {str(e)}")

    def ajustar_tp_60_porcento(self, pos, symbol_info_tick):
        """Ajusta TP para 60% da distância original"""
        import MetaTrader5 as mt5
        
        try:
            ticket_posicao = pos.ticket
            symbol = pos.symbol
            tipo_posicao = pos.type
            preco_abertura = pos.price_open
            stop_loss_atual = pos.sl
            stop_gain_atual = pos.tp
            
            self.log(f"🔧 Ajustando TP para 60% da distância original em {symbol}")
            
            # Calcula nova distância de TP (60% da original)
            distancia_tp = abs(stop_gain_atual - preco_abertura)
            nova_distancia_tp = distancia_tp * 0.6

            # Calcula novo TP
            if tipo_posicao == mt5.POSITION_TYPE_BUY:
                novo_sl = stop_loss_atual
                novo_tp = preco_abertura + nova_distancia_tp
            else:
                novo_sl = stop_loss_atual
                novo_tp = preco_abertura - nova_distancia_tp

            # Ajustar para respeitar stops level
            symbol_info = mt5.symbol_info(symbol)
            if not symbol_info:
                self.log(f"⚠️ Não foi possível obter informações do símbolo {symbol}")
                return

            digits = symbol_info.digits
            stops_level_points = symbol_info.trade_stops_level
            ponto = symbol_info.point
            distancia_minima = stops_level_points * ponto

            # Ajusta TP conforme distância mínima
            current_ask = symbol_info_tick.ask
            current_bid = symbol_info_tick.bid

            if tipo_posicao == mt5.POSITION_TYPE_BUY:
                if novo_tp < current_ask + distancia_minima:
                    novo_tp = current_ask + distancia_minima
                if novo_tp <= novo_sl:
                    novo_tp = max(novo_tp, novo_sl + distancia_minima)
            else:
                if novo_tp > current_bid - distancia_minima:
                    novo_tp = current_bid - distancia_minima
                if novo_tp >= novo_sl:
                    novo_tp = min(novo_tp, novo_sl - distancia_minima)

            novo_tp = round(novo_tp, digits)
            novo_sl = round(novo_sl, digits)
            # Enviar modificação
            request_modificacao = {
                "action": mt5.TRADE_ACTION_SLTP,
                "position": ticket_posicao,
                "symbol": symbol,
                "sl": novo_sl,
                "tp": novo_tp,
                "magic": pos.magic,
                "comment": "TP_ajust_15h_s_i",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK,
            }

            result_mod = mt5.order_send(request_modificacao)
            
            if result_mod and result_mod.retcode == mt5.TRADE_RETCODE_DONE:
                self.log(f"✅ Ticket {ticket_posicao} ({symbol}): TP ajustado com sucesso")
                self.log(f"   TP atual: {stop_gain_atual} → Novo TP: {novo_tp}")
                self.stops_ja_ajustados.add(ticket_posicao)
            else:
                retcode = result_mod.retcode if result_mod else "None"
                self.log(f"❌ Falha ao modificar TP do ticket {ticket_posicao}, retcode: {retcode}")
                
        except Exception as e:
            self.log(f"❌ Erro ao ajustar TP: {str(e)}")

    def executar_remocao_pendentes(self):
        """Remove ordens pendentes às 15:20h"""
        import MetaTrader5 as mt5
        
        current_hour = datetime.now().hour
        current_minute = datetime.now().minute
        
        self.log(f"🗑️ REMOVENDO ORDENS PENDENTES ÀS {current_hour:02d}:{current_minute:02d}")
        
        try:
            posicoes_pendentes = mt5.orders_get()
            if not posicoes_pendentes:
                self.log("📋 Nenhuma ordem pendente encontrada")
                return
            
            # Filtrar apenas ordens do sistema atual
            ordens_sistema = [ordem for ordem in posicoes_pendentes 
                            if str(ordem.magic).startswith(self.prefixo)]
            
            if not ordens_sistema:
                self.log("📋 Nenhuma ordem pendente do sistema encontrada")
                return
            
            self.log(f"📋 Encontradas {len(ordens_sistema)} ordens pendentes do sistema")
            
            # Usar função existente para fechar apenas ordens pendentes
            self.fechar_posicoes_pendentes_sistema(ordens_sistema)
            
            self.log(f"✅ REMOÇÃO DE ORDENS PENDENTES CONCLUÍDA")
            
        except Exception as e:
            self.log(f"❌ ERRO na remoção de ordens pendentes: {str(e)}")

    def executar_fechamento_total(self):
        """Executa fechamento total às 16:01h"""
        import MetaTrader5 as mt5
        
        current_hour = datetime.now().hour
        current_minute = datetime.now().minute
        
        self.log(f"🔒 FECHAMENTO TOTAL DO DIA ÀS {current_hour:02d}:{current_minute:02d}")
        
        try:
            posicoes_abertas = mt5.positions_get()
            posicoes_pendentes = mt5.orders_get()
            
            # Filtrar apenas posições/ordens do sistema atual
            posicoes_sistema = [pos for pos in (posicoes_abertas or []) 
                              if str(pos.magic).startswith(self.prefixo)]
            ordens_sistema = [ordem for ordem in (posicoes_pendentes or []) 
                            if str(ordem.magic).startswith(self.prefixo)]
            
            if posicoes_sistema or ordens_sistema:
                self.log(f"📊 Fechando {len(posicoes_sistema)} posições e {len(ordens_sistema)} ordens")
                
                # Fechar todas as posições e ordens do sistema
                for pos in posicoes_sistema:
                    self.fechar_posicao_especifica(pos)
                
                for ordem in ordens_sistema:
                    self.cancelar_ordem_pendente(ordem)
                    
                self.log("✅ Fechamento total concluído")
            else:
                self.log("📋 Nenhuma posição/ordem do sistema para fechar")
                
        except Exception as e:
            self.log(f"❌ ERRO no fechamento total: {str(e)}")

    def mover_stop_loss_para_break_even(self, pos, preco_abertura):
        """Move stop loss para break even"""
        import MetaTrader5 as mt5
        
        try:
            request = {
                "action": mt5.TRADE_ACTION_SLTP,
                "position": pos.ticket,
                "symbol": pos.symbol,
                "sl": round(preco_abertura, mt5.symbol_info(pos.symbol).digits),
                "tp": pos.tp,  # Mantém TP atual
                "magic": pos.magic,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK,
            }
            
            result = mt5.order_send(request)
            if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                self.log(f"✅ Stop Loss movido para break-even: ticket {pos.ticket}")
            else:
                retcode = result.retcode if result else "None"
                self.log(f"❌ Falha ao mover SL para break-even: ticket {pos.ticket}, retcode: {retcode}")
        except Exception as e:
            self.log(f"❌ Erro ao mover SL para break-even: {str(e)}")

    def fechar_posicao_especifica(self, pos):
        """Fecha uma posição específica"""
        import MetaTrader5 as mt5
        
        try:
            if pos.type == mt5.POSITION_TYPE_BUY:
                price = mt5.symbol_info_tick(pos.symbol).bid
                order_type = mt5.ORDER_TYPE_SELL
            else:
                price = mt5.symbol_info_tick(pos.symbol).ask
                order_type = mt5.ORDER_TYPE_BUY
                
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": order_type,
                "position": pos.ticket,
                "price": price,
                "magic": pos.magic,
                "comment": "Fechamento_s_i",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            result = mt5.order_send(request)
            if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                self.log(f"✅ Posição fechada: ticket {pos.ticket} ({pos.symbol})")
            else:
                retcode = result.retcode if result else "None"
                self.log(f"❌ Falha ao fechar posição: ticket {pos.ticket}, retcode: {retcode}")
                
        except Exception as e:
            self.log(f"❌ Erro ao fechar posição específica: {str(e)}")

    def cancelar_ordem_pendente(self, ordem):
        """Cancela uma ordem pendente específica"""
        import MetaTrader5 as mt5
        
        try:
            request = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": ordem.ticket,
                "symbol": ordem.symbol,
                "magic": ordem.magic,
                "comment": "Cancelamento_s_i",
            }
            
            result = mt5.order_send(request)
            if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                self.log(f"✅ Ordem pendente cancelada: ticket {ordem.ticket} ({ordem.symbol})")
            else:
                retcode = result.retcode if result else "None"
                self.log(f"❌ Falha ao cancelar ordem: ticket {ordem.ticket}, retcode: {retcode}")
                
        except Exception as e:
            self.log(f"❌ Erro ao cancelar ordem pendente: {str(e)}")

    def fechar_posicoes_pendentes_sistema(self, ordens_sistema):
        """Fecha apenas ordens pendentes do sistema"""
        for ordem in ordens_sistema:
            self.cancelar_ordem_pendente(ordem)

    def iniciar_sistema(self):
        """Inicia o sistema completo com todas as threads (ATUALIZADO)"""
        self.log("🎯 INICIANDO SISTEMA INTEGRADO DE TRADING COM ANÁLISE E ENVIO DE ORDENS")
        self.log("=" * 80)
        self.log("Este sistema executa:")
        self.log("✅ Coleta de dados reais de pares")
        self.log("✅ Análise de cointegração")
        self.log("✅ Modelos ARIMA/GARCH")
        self.log("✅ Envio de ordens automáticas")  # NOVO
        self.log("✅ Monitoramento de posições em tempo real")
        self.log("✅ Break-even contínuo durante pregão")
        self.log("✅ Ajustes programados (15:10h, 15:20h, 16:01h)")
        self.log("✅ Gestão de risco integrada")
        self.log("=" * 80)
        
        self.running = True
        self.dados_sistema["inicio"] = datetime.now()
        self.dados_sistema["status"] = "Iniciando"
        
        # Thread principal do sistema de trading
        thread_trading = threading.Thread(target=self.executar_sistema_original, name="SistemaTrading")
        
        # Thread de monitoramento geral
        thread_monitor = threading.Thread(target=self.thread_monitoramento, name="Monitoramento")
        
        # Thread de monitoramento de posições (pernas órfãs, conversões)
        thread_monitor_posicoes = threading.Thread(target=self.thread_monitoramento_posicoes, name="MonitoramentoPosicoes")
        
        # Thread: Break-even contínuo
        thread_break_even = threading.Thread(target=self.thread_break_even_continuo, name="BreakEvenContinuo")
        
        # Thread: Ajustes programados
        thread_ajustes = threading.Thread(target=self.thread_ajustes_programados, name="AjustesProgramados")
        
        # NOVA Thread: Análise e envio de ordens
        thread_ordens = threading.Thread(target=self.thread_analise_e_envio_ordens, name="AnaliseEnvioOrdens")
        
        # Inicia todas as threads
        thread_trading.start()
        thread_monitor.start()
        thread_monitor_posicoes.start()
        thread_break_even.start()
        thread_ajustes.start()
        thread_ordens.start()  # NOVA thread
        
        self.log("✅ Todas as threads iniciadas - Sistema operacional!")
        self.log("🔍 Thread de monitoramento de posições: A cada 30 segundos")
        self.log("📈 Thread de break-even contínuo: A cada 10 segundos durante pregão")
        self.log("⏰ Thread de ajustes programados: Horários específicos (15:10h, 15:20h, 16:01h)")
        self.log("📊 Thread de análise e envio de ordens: A cada 5 minutos durante pregão")  # NOVA
        self.log("💡 Pressione Ctrl+C para parar o sistema")
        
        try:
            # Aguarda interrupção
            while self.running:
                time.sleep(5)
                
                # Verifica se threads estão vivas
                threads_status = {
                    "Trading": thread_trading.is_alive(),
                    "Monitoramento": thread_monitor.is_alive(),
                    "Posições": thread_monitor_posicoes.is_alive(),
                    "Break-Even": thread_break_even.is_alive(),
                    "Ajustes": thread_ajustes.is_alive(),
                    "Ordens": thread_ordens.is_alive()  # NOVA thread
                }
                
                # Log apenas quando uma thread para pela primeira vez
                for nome, status in threads_status.items():
                    if not status:
                        # Verifica se já logamos este problema
                        if not hasattr(self, '_threads_paradas'):
                            self._threads_paradas = set()
                        
                        if nome not in self._threads_paradas:
                            self.log(f"⚠️ AVISO: Thread {nome} parou")
                            self._threads_paradas.add(nome)
                    else:
                        # Thread voltou a funcionar
                        if hasattr(self, '_threads_paradas') and nome in self._threads_paradas:
                            self.log(f"✅ Thread {nome} reativada")
                            self._threads_paradas.remove(nome)
        
        except KeyboardInterrupt:
            self.log("🛑 INTERRUPÇÃO: Parando sistema...")
            self.parar_sistema()
            
        # Aguarda threads finalizarem
        threads = [thread_trading, thread_monitor, thread_monitor_posicoes, 
                  thread_break_even, thread_ajustes, thread_ordens]  # ATUALIZADO
        for thread in threads:
            thread.join(timeout=10)
        
        self.log("🏁 SISTEMA FINALIZADO")

    def parar_sistema(self):
        """Para o sistema"""
        self.running = False
        self.dados_sistema["status"] = "Parando"
        
        # Salva relatório final
        self.salvar_relatorio()
    
    def salvar_relatorio(self):
        """Salva relatório final"""
        try:
            relatorio = {
                "resumo": self.dados_sistema,
                "duracao_total": str(datetime.now() - self.dados_sistema["inicio"]) if self.dados_sistema["inicio"] else "N/A",
                "log_completo": self.logs,
                "timestamp_relatorio": datetime.now().isoformat(),
                "configuracoes": {
                    "prefixo_magic": self.prefixo,
                    "janela_break_even": self.JANELA_BREAK_EVEN,
                    "horarios_ajuste": {
                        "ajuste_posicoes": f"{self.horario_ajuste_stops}:{self.ajusta_ordens_minuto:02d}",
                        "remove_pendentes": f"{self.horario_remove_pendentes}:20",
                        "fechamento_total": f"{self.horario_fechamento_total}:01"
                    }
                },
                "stops_ajustados": list(self.stops_ja_ajustados),
                "ajustes_executados": list(self.ajustes_executados_hoje)
            }
            
            arquivo = f"relatorio_integrado_avancado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(relatorio, f, indent=2, ensure_ascii=False, default=str)
            
            self.log(f"💾 RELATÓRIO AVANÇADO: Salvo em {arquivo}")
        except Exception as e:
            self.log(f"❌ ERRO ao salvar relatório: {str(e)}")

def main():
    """Função principal"""
    # Configure o terminal para UTF-8 no Windows
    if os.name == 'nt':  # Windows
        os.system('chcp 65001 > nul')  # UTF-8 code page
    
    print("🎯 SISTEMA INTEGRADO DE TRADING AVANÇADO")
    print("Incorpora o código completo calculo_entradas_v55.py com threading avançado")
    print("  📈 Break-even contínuo durante pregão")
    print("  ⏰ Ajustes programados em horários específicos")
    print("  🔧 Gestão automática de Stop Loss e Take Profit")
    print("  🗑️ Remoção automática de ordens pendentes")
    print("  🔒 Fechamento total do dia")
    print("=" * 80)
    
    sistema = SistemaIntegrado()
    sistema.iniciar_sistema()

if __name__ == "__main__":
    main()
