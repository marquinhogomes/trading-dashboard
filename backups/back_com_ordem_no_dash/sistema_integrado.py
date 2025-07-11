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
            # Log mais detalhado do erro
            import traceback
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
        """Inicia o sistema completo com todas as threads"""
        self.log("🎯 INICIANDO SISTEMA INTEGRADO DE TRADING COM MONITORAMENTO AVANÇADO")
        self.log("=" * 80)
        self.log("Este sistema executa:")
        self.log("✅ Coleta de dados reais de pares")
        self.log("✅ Análise de cointegração")
        self.log("✅ Modelos ARIMA/GARCH")
        self.log("✅ Envio de ordens automáticas")
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
        
        # Nova thread: Break-even contínuo
        thread_break_even = threading.Thread(target=self.thread_break_even_continuo, name="BreakEvenContinuo")
        
        # Nova thread: Ajustes programados
        thread_ajustes = threading.Thread(target=self.thread_ajustes_programados, name="AjustesProgramados")
        
        # Inicia todas as threads
        thread_trading.start()
        thread_monitor.start()
        thread_monitor_posicoes.start()
        thread_break_even.start()
        thread_ajustes.start()
        
        self.log("✅ Todas as threads iniciadas - Sistema operacional!")
        self.log("🔍 Thread de monitoramento de posições: A cada 30 segundos")
        self.log("📈 Thread de break-even contínuo: A cada 10 segundos durante pregão")
        self.log("⏰ Thread de ajustes programados: Horários específicos (15:10h, 15:20h, 16:01h)")
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
                    "Ajustes": thread_ajustes.is_alive()
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
        threads = [thread_trading, thread_monitor, thread_monitor_posicoes, thread_break_even, thread_ajustes]
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
    print("Funcionalidades do bloco linhas 5779-6099:")
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
