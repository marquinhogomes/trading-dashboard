#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Integrado: calculo_entradas_v55.py com Threading e Monitoramento
Este sistema combina o código original com threading para visualização completa
Versão corrigida - apenas operações reais
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
            # Executa o código original
            exec(codigo, globals())
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
            self.log("⚠️ MetaTrader5 não disponível - sistema não pode operar")
            return
        
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
                            # Fecha a posição órfã diretamente
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

                        # Prepara requisição de fechamento (sem comment para evitar erro)
                        request = {
                            "action": mt5.TRADE_ACTION_DEAL,
                            "symbol": symbol,
                            "volume": volume,
                            "type": order_type,
                            "position": posicao.ticket,
                            "price": price,
                            "magic": posicao.magic,
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

                        # Prepara requisição de cancelamento (sem comment para evitar erro)
                        request = {
                            "action": mt5.TRADE_ACTION_REMOVE,
                            "order": ordem.ticket,
                            "symbol": symbol,
                            "magic": ordem.magic,
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

                # Prepara ordem a mercado (sem comment para evitar erro)
                ordem_mercado = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": independe_atual,
                    "volume": volume,
                    "type": tipo_ordem,
                    "price": preco,
                    "magic": magic,
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
        import MetaTrader5 as mt5
        
        self.log("💰 ANÁLISE DE LUCROS/PREJUÍZOS POR MAGIC:")
        
        for magic in magics_abertas:
            lucro_prejuizo = 0.00
            
            # Calcula lucro/prejuízo para cada posição do magic
            for posicao in posicoes_abertas:
                if posicao.magic == magic:
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

    def iniciar_sistema(self):
        """Inicia o sistema completo com todas as threads"""
        self.log("🎯 SISTEMA INTEGRADO DE TRADING - OPERAÇÕES REAIS")
        self.log("=" * 80)
        self.log("Este sistema executa:")
        self.log("✅ Monitoramento de posições reais")
        self.log("✅ Identificação automática de pares")
        self.log("✅ Fechamento de posições órfãs")
        self.log("✅ Conversão de ordens pendentes")
        self.log("✅ Análise de lucros/prejuízos")
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
        
        # Inicia todas as threads
        thread_trading.start()
        thread_monitor.start()
        thread_monitor_posicoes.start()
        
        self.log("✅ Todas as threads iniciadas - Sistema operacional!")
        self.log("🔍 Thread de monitoramento de posições: A cada 30 segundos")
        self.log("💡 Pressione Ctrl+C para parar o sistema")
        
        try:
            # Aguarda interrupção
            while self.running:
                time.sleep(5)
                
                # Verifica se threads estão vivas
                threads_status = {
                    "Trading": thread_trading.is_alive(),
                    "Monitoramento": thread_monitor.is_alive(),
                    "Posições": thread_monitor_posicoes.is_alive()
                }
                
                for nome, status in threads_status.items():
                    if not status:
                        self.log(f"⚠️ AVISO: Thread {nome} parou")
        
        except KeyboardInterrupt:
            self.log("🛑 INTERRUPÇÃO: Parando sistema...")
            self.parar_sistema()
            
        # Aguarda threads finalizarem
        threads = [thread_trading, thread_monitor, thread_monitor_posicoes]
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
                    "apenas_operacoes_reais": True
                }
            }
            
            arquivo = f"relatorio_sistema_real_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(relatorio, f, indent=2, ensure_ascii=False, default=str)
            
            self.log(f"💾 RELATÓRIO: Salvo em {arquivo}")
        except Exception as e:
            self.log(f"❌ ERRO ao salvar relatório: {str(e)}")

def main():
    """Função principal"""
    # Configure o terminal para UTF-8 no Windows
    if os.name == 'nt':  # Windows
        os.system('chcp 65001 > nul')  # UTF-8 code page
    
    print("🎯 SISTEMA INTEGRADO DE TRADING - OPERAÇÕES REAIS")
    print("Monitoramento de posições reais do MetaTrader5")
    print("Funcionalidades:")
    print("  📊 Identificação automática de pares")
    print("  🔄 Fechamento de posições órfãs")
    print("  💱 Conversão de ordens pendentes")
    print("  💰 Análise de lucros/prejuízos")
    print("=" * 80)
    
    sistema = SistemaIntegrado()
    sistema.iniciar_sistema()

if __name__ == "__main__":
    main()
