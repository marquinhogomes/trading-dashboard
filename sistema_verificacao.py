#!/usr/bin/env python3
"""
Sistema de Verificação e Monitoramento - Versão Avançada
"""

import threading
import time
import logging
import json
import psutil
import os
from datetime import datetime
from pathlib import Path

# Configuração de logging
def setup_logging():
    """Configura sistema de logging detalhado"""
    log_dir = Path("data/logs")
    
    # Criar diretório se não existir
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        # Se falhar, usar diretório atual
        log_dir = Path(".")
    
    # Configurar formato de log
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s"
    
    # Configurar múltiplos handlers
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_dir / f"sistema_{datetime.now().strftime('%Y%m%d')}.log"),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger("SistemaTrading")

class MonitorSistema:
    """Classe para monitorar a saúde do sistema"""
    
    def __init__(self):
        self.logger = logging.getLogger("MonitorSistema")
        self.status = {
            "thread_extracao": {"status": "stopped", "last_heartbeat": None, "errors": 0},
            "thread_monitoramento": {"status": "stopped", "last_heartbeat": None, "errors": 0},
            "sistema_geral": {"start_time": datetime.now(), "uptime": 0, "memory_usage": 0}
        }
        self.running = False
    
    def start_monitoring(self):
        """Inicia o monitoramento do sistema"""
        self.running = True
        monitor_thread = threading.Thread(target=self._monitor_loop, name="SystemMonitor")
        monitor_thread.daemon = True
        monitor_thread.start()
        self.logger.info("Sistema de monitoramento iniciado")
    
    def stop_monitoring(self):
        """Para o monitoramento do sistema"""
        self.running = False
        self.logger.info("Sistema de monitoramento parado")
    
    def update_thread_status(self, thread_name, status, error=None):
        """Atualiza o status de uma thread"""
        if thread_name in self.status:
            self.status[thread_name]["status"] = status
            self.status[thread_name]["last_heartbeat"] = datetime.now()
            if error:
                self.status[thread_name]["errors"] += 1
                self.logger.error(f"Erro em {thread_name}: {error}")
    
    def _monitor_loop(self):
        """Loop principal de monitoramento"""
        while self.running:
            try:
                # Atualizar informações do sistema
                process = psutil.Process()
                self.status["sistema_geral"]["uptime"] = (datetime.now() - self.status["sistema_geral"]["start_time"]).total_seconds()
                self.status["sistema_geral"]["memory_usage"] = process.memory_info().rss / 1024 / 1024  # MB
                
                # Verificar saúde das threads
                self._check_thread_health()
                
                # Log de status geral a cada 30 segundos
                if int(time.time()) % 30 == 0:
                    self._log_system_status()
                
                time.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Erro no monitoramento: {e}")
                time.sleep(5)
    
    def _check_thread_health(self):
        """Verifica a saúde das threads"""
        now = datetime.now()
        
        for thread_name, info in self.status.items():
            if thread_name == "sistema_geral":
                continue
                
            if info["last_heartbeat"]:
                time_since_heartbeat = (now - info["last_heartbeat"]).total_seconds()
                
                # Thread morta se não houver heartbeat por mais de 60 segundos
                if time_since_heartbeat > 60 and info["status"] == "running":
                    info["status"] = "error"
                    self.logger.warning(f"Thread {thread_name} pode estar travada (último heartbeat: {time_since_heartbeat:.1f}s)")
    
    def _log_system_status(self):
        """Registra o status completo do sistema"""
        self.logger.info("=" * 60)
        self.logger.info("STATUS DO SISTEMA")
        self.logger.info(f"Uptime: {self.status['sistema_geral']['uptime']:.1f}s")
        self.logger.info(f"Memória: {self.status['sistema_geral']['memory_usage']:.1f}MB")
        
        for thread_name, info in self.status.items():
            if thread_name == "sistema_geral":
                continue
            self.logger.info(f"{thread_name}: {info['status']} (erros: {info['errors']})")
        self.logger.info("=" * 60)
    
    def get_status_report(self):
        """Retorna relatório completo do sistema"""
        return json.dumps(self.status, default=str, indent=2)

class ExtractorDados:
    """Classe responsável pela extração de dados"""
    
    def __init__(self, monitor):
        self.logger = logging.getLogger("ExtractorDados")
        self.monitor = monitor
        self.running = False
        self.dados_processados = 0
    
    def start(self):
        """Inicia o processo de extração"""
        self.running = True
        self.monitor.update_thread_status("thread_extracao", "starting")
        
        try:
            self.monitor.update_thread_status("thread_extracao", "running")
            self.logger.info("🚀 Iniciando extração e análise de dados...")
            
            for i in range(10):  # Simular 10 ciclos de processamento
                if not self.running:
                    break
                
                # Simular processamento
                self.logger.info(f"📊 Processando lote {i+1}/10...")
                
                # Simular tempo de processamento variável
                processing_time = 2 + (i * 0.5)  # De 2 a 6.5 segundos
                time.sleep(processing_time)
                
                self.dados_processados += 1
                
                # Heartbeat para o monitor
                self.monitor.update_thread_status("thread_extracao", "running")
                
                # Log de progresso
                self.logger.info(f"✅ Lote {i+1} processado com sucesso (tempo: {processing_time:.1f}s)")
            
            self.monitor.update_thread_status("thread_extracao", "completed")
            self.logger.info(f"🎉 Extração concluída! Total de lotes processados: {self.dados_processados}")
            
        except Exception as e:
            self.monitor.update_thread_status("thread_extracao", "error", str(e))
            self.logger.error(f"❌ Erro na extração: {e}")
        finally:
            self.running = False
    
    def stop(self):
        """Para o processo de extração"""
        self.running = False
        self.logger.info("🛑 Parando extração de dados...")

class MonitorOperacoes:
    """Classe responsável pelo monitoramento de operações"""
    
    def __init__(self, monitor):
        self.logger = logging.getLogger("MonitorOperacoes")
        self.monitor = monitor
        self.running = False
        self.operacoes_monitoradas = 0
        self.alertas_gerados = 0
    
    def start(self):
        """Inicia o monitoramento de operações"""
        self.running = True
        self.monitor.update_thread_status("thread_monitoramento", "starting")
        
        try:
            self.monitor.update_thread_status("thread_monitoramento", "running")
            self.logger.info("👁️ Iniciando monitoramento de operações...")
            
            while self.running:
                # Simular verificação de operações
                self.operacoes_monitoradas += 1
                
                # Simular geração de alertas ocasionais
                if self.operacoes_monitoradas % 7 == 0:  # A cada 7 verificações
                    self.alertas_gerados += 1
                    self.logger.warning(f"⚠️ Alerta #{self.alertas_gerados}: Operação requer atenção!")
                
                self.logger.info(f"👀 Verificação #{self.operacoes_monitoradas} - Sistema OK")
                
                # Heartbeat para o monitor
                self.monitor.update_thread_status("thread_monitoramento", "running")
                
                time.sleep(1.5)  # Verificar a cada 1.5 segundos
            
            self.monitor.update_thread_status("thread_monitoramento", "completed")
            self.logger.info(f"🏁 Monitoramento concluído! Operações verificadas: {self.operacoes_monitoradas}")
            
        except Exception as e:
            self.monitor.update_thread_status("thread_monitoramento", "error", str(e))
            self.logger.error(f"❌ Erro no monitoramento: {e}")
        finally:
            self.running = False
    
    def stop(self):
        """Para o monitoramento"""
        self.running = False
        self.logger.info("🛑 Parando monitoramento de operações...")

def main():
    """Função principal com verificação completa"""
    # Configurar logging
    logger = setup_logging()
    logger.info("🎯 INICIANDO SISTEMA DE TRADING AVANÇADO")
    logger.info("=" * 80)
    
    # Inicializar monitor do sistema
    monitor = MonitorSistema()
    monitor.start_monitoring()
    
    # Inicializar componentes
    extractor = ExtractorDados(monitor)
    monitor_ops = MonitorOperacoes(extractor.monitor)
    
    try:
        # Criar e iniciar threads
        thread_extracao = threading.Thread(target=extractor.start, name="DataExtractionThread")
        thread_monitoramento = threading.Thread(target=monitor_ops.start, name="OperationsMonitorThread")
        
        logger.info("🚀 Iniciando threads do sistema...")
        thread_extracao.start()
        thread_monitoramento.start()
        
        # Aguardar conclusão da extração (thread com duração definida)
        thread_extracao.join()
        
        # Parar monitoramento após extração
        monitor_ops.stop()
        thread_monitoramento.join(timeout=5)  # Aguardar até 5 segundos
        
        # Relatório final
        logger.info("📊 RELATÓRIO FINAL DO SISTEMA")
        logger.info("=" * 80)
        logger.info(f"✅ Dados processados: {extractor.dados_processados}")
        logger.info(f"✅ Operações monitoradas: {monitor_ops.operacoes_monitoradas}")
        logger.info(f"⚠️ Alertas gerados: {monitor_ops.alertas_gerados}")
        
        # Status detalhado
        logger.info("\n📋 STATUS DETALHADO:")
        print(monitor.get_status_report())
        
        logger.info("🎉 SISTEMA EXECUTADO COM SUCESSO!")
        
    except KeyboardInterrupt:
        logger.info("🛑 Interrupção detectada, parando sistema...")
        extractor.stop()
        monitor_ops.stop()
    except Exception as e:
        logger.error(f"❌ Erro crítico no sistema: {e}")
    finally:
        monitor.stop_monitoring()
        logger.info("🔚 Sistema finalizado")

if __name__ == "__main__":
    main()
