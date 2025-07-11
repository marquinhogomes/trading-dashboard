#!/usr/bin/env python3
"""
Sistema de Verificação Simples - Como saber se o código está rodando perfeitamente
"""

import threading
import time
import json
from datetime import datetime

class VerificadorSistema:
    """Classe para verificar se o sistema está funcionando corretamente"""
    
    def __init__(self):
        self.metricas = {
            "inicio_execucao": None,
            "fim_execucao": None,
            "tempo_total": 0,
            "threads_ativas": 0,
            "operacoes_completadas": 0,
            "erros_encontrados": 0,
            "status_geral": "Iniciando..."
        }
        self.logs = []
    
    def log_evento(self, mensagem, tipo="INFO"):
        """Registra um evento no sistema"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        evento = f"[{timestamp}] {tipo}: {mensagem}"
        self.logs.append(evento)
        print(evento)
    
    def iniciar_monitoramento(self):
        """Inicia o monitoramento do sistema"""
        self.metricas["inicio_execucao"] = datetime.now()
        self.log_evento("=== SISTEMA DE VERIFICACAO INICIADO ===")
        self.log_evento(f"Horario de inicio: {self.metricas['inicio_execucao']}")
    
    def finalizar_monitoramento(self):
        """Finaliza o monitoramento e gera relatório"""
        self.metricas["fim_execucao"] = datetime.now()
        self.metricas["tempo_total"] = (self.metricas["fim_execucao"] - self.metricas["inicio_execucao"]).total_seconds()
        
        self.log_evento("=== SISTEMA DE VERIFICACAO FINALIZADO ===")
        self.log_evento(f"Horario de fim: {self.metricas['fim_execucao']}")
        self.log_evento(f"Tempo total de execucao: {self.metricas['tempo_total']:.2f} segundos")
        
        return self.gerar_relatorio_final()
    
    def registrar_thread_ativa(self):
        """Registra uma nova thread ativa"""
        self.metricas["threads_ativas"] += 1
        self.log_evento(f"Thread iniciada. Total ativo: {self.metricas['threads_ativas']}")
    
    def registrar_thread_finalizada(self):
        """Registra uma thread finalizada"""
        self.metricas["threads_ativas"] -= 1
        self.log_evento(f"Thread finalizada. Total ativo: {self.metricas['threads_ativas']}")
    
    def registrar_operacao_completa(self, descricao=""):
        """Registra uma operação completa"""
        self.metricas["operacoes_completadas"] += 1
        self.log_evento(f"Operacao completa: {descricao} (Total: {self.metricas['operacoes_completadas']})")
    
    def registrar_erro(self, erro):
        """Registra um erro encontrado"""
        self.metricas["erros_encontrados"] += 1
        self.log_evento(f"ERRO: {erro}", "ERROR")
    
    def atualizar_status(self, novo_status):
        """Atualiza o status geral do sistema"""
        self.metricas["status_geral"] = novo_status
        self.log_evento(f"Status atualizado: {novo_status}")
    
    def gerar_relatorio_final(self):
        """Gera relatório final do sistema"""
        print("\n" + "="*60)
        print("RELATORIO FINAL DE VERIFICACAO")
        print("="*60)
        
        # Determinar se o sistema funcionou perfeitamente
        sucesso_total = (
            self.metricas["erros_encontrados"] == 0 and
            self.metricas["threads_ativas"] == 0 and
            self.metricas["operacoes_completadas"] > 0
        )
        
        status_final = "SUCESSO TOTAL" if sucesso_total else "COM PROBLEMAS"
        
        print(f"Status Final: {status_final}")
        print(f"Tempo de Execucao: {self.metricas['tempo_total']:.2f}s")
        print(f"Operacoes Completadas: {self.metricas['operacoes_completadas']}")
        print(f"Erros Encontrados: {self.metricas['erros_encontrados']}")
        print(f"Threads Finalizadas Corretamente: {self.metricas['threads_ativas'] == 0}")
        
        if sucesso_total:
            print("\n✅ PARABENS! SEU CODIGO ESTA RODANDO PERFEITAMENTE!")
            print("   - Todas as operacoes foram completadas")
            print("   - Nenhum erro foi encontrado") 
            print("   - Todas as threads finalizaram corretamente")
        else:
            print("\n⚠️  ATENCAO! Foram encontrados alguns problemas:")
            if self.metricas["erros_encontrados"] > 0:
                print(f"   - {self.metricas['erros_encontrados']} erro(s) encontrado(s)")
            if self.metricas["threads_ativas"] > 0:
                print(f"   - {self.metricas['threads_ativas']} thread(s) ainda ativa(s)")
            if self.metricas["operacoes_completadas"] == 0:
                print("   - Nenhuma operacao foi completada")
        
        print("="*60)
        return {
            "sucesso_total": sucesso_total,
            "metricas": self.metricas,
            "logs": self.logs
        }

def extrair_e_analisar_dados_com_verificacao(verificador):
    """Função de extração com verificação integrada"""
    verificador.registrar_thread_ativa()
    
    try:
        verificador.log_evento("Iniciando extracao de dados...")
        verificador.atualizar_status("Extraindo dados")
        
        # Simular processamento de 5 lotes
        for i in range(1, 6):
            verificador.log_evento(f"Processando lote {i}/5...")
            time.sleep(1)  # Simular processamento
            verificador.registrar_operacao_completa(f"Lote {i} processado")
            
        verificador.log_evento("Extracao de dados concluida com sucesso!")
        verificador.atualizar_status("Extracao concluida")
        
    except Exception as e:
        verificador.registrar_erro(f"Erro na extracao: {str(e)}")
    finally:
        verificador.registrar_thread_finalizada()

def monitorar_operacoes_com_verificacao(verificador):
    """Função de monitoramento com verificação integrada"""
    verificador.registrar_thread_ativa()
    
    try:
        verificador.log_evento("Iniciando monitoramento de operacoes...")
        verificador.atualizar_status("Monitorando operacoes")
        
        # Monitorar por 10 segundos
        for i in range(1, 11):
            verificador.log_evento(f"Verificacao de monitoramento {i}/10...")
            time.sleep(1)  # Verificar a cada segundo
            verificador.registrar_operacao_completa(f"Verificacao {i}")
            
        verificador.log_evento("Monitoramento concluido com sucesso!")
        verificador.atualizar_status("Monitoramento concluido")
        
    except Exception as e:
        verificador.registrar_erro(f"Erro no monitoramento: {str(e)}")
    finally:
        verificador.registrar_thread_finalizada()

def main():
    """Função principal com verificação completa"""
    # Inicializar verificador
    verificador = VerificadorSistema()
    verificador.iniciar_monitoramento()
    
    try:
        # Criar threads
        thread_extracao = threading.Thread(
            target=extrair_e_analisar_dados_com_verificacao, 
            args=(verificador,), 
            name="ExtractionThread"
        )
        
        thread_monitoramento = threading.Thread(
            target=monitorar_operacoes_com_verificacao, 
            args=(verificador,), 
            name="MonitoringThread"
        )
        
        # Iniciar threads
        verificador.log_evento("Iniciando threads do sistema...")
        thread_extracao.start()
        thread_monitoramento.start()
        
        # Aguardar conclusão
        thread_extracao.join()
        thread_monitoramento.join()
        
        verificador.log_evento("Todas as threads finalizadas!")
        
    except Exception as e:
        verificador.registrar_erro(f"Erro critico no sistema: {str(e)}")
    
    finally:
        # Gerar relatório final
        relatorio = verificador.finalizar_monitoramento()
        
        # Salvar relatório em arquivo
        with open("relatorio_verificacao.json", "w", encoding="utf-8") as f:
            json.dump(relatorio, f, indent=2, default=str, ensure_ascii=False)
        
        verificador.log_evento("Relatorio salvo em 'relatorio_verificacao.json'")

if __name__ == "__main__":
    main()
