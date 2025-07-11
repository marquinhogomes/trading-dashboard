#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Integrado Otimizado: Versão sem espera desnecessária de minuto
Remove o aguardar_proximo_minuto() para início imediato do trading
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

class SistemaIntegradoOtimizado:
    """Sistema que integra o código original com threading e início imediato"""
    
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
        log_completo = f"[{timestamp}] {mensagem}"
        print(log_completo)
        self.logs.append(log_completo)
        
        # Mantém apenas os últimos 100 logs
        if len(self.logs) > 100:
            self.logs = self.logs[-100:]
    
    def get_dados_sistema(self):
        """Retorna dados atuais do sistema"""
        return self.dados_sistema.copy()
    
    def get_logs_recentes(self, quantidade=10):
        """Retorna os logs mais recentes"""
        return self.logs[-quantidade:] if self.logs else []
    
    def executar_sistema_original_otimizado(self):
        """Executa o sistema original sem espera desnecessária de minuto"""
        try:
            self.log("🚀 Iniciando sistema original OTIMIZADO (sem espera de minuto)")
            
            # Lê o código do calculo_entradas_v55.py
            script_path = os.path.join(os.path.dirname(__file__), "calculo_entradas_v55.py")
            
            with open(script_path, 'r', encoding='utf-8') as file:
                codigo_original = file.read()
            
            # OTIMIZAÇÃO 1: Remove a espera até o próximo minuto
            # Substitui a função aguardar_proximo_minuto para início imediato
            codigo_otimizado = codigo_original.replace(
                'def aguardar_proximo_minuto():\n    """Aguarda até o início do próximo minuto."""\n    while True:\n        # Obtém o segundo atual\n        segundo_atual = datetime.now().second\n        # Se estivermos no início de um novo minuto, saia do loop\n        if segundo_atual == 0:\n            break\n        # Aguarda 1 segundo antes de verificar novamente\n        time.sleep(1)',
                'def aguardar_proximo_minuto():\n    """OTIMIZADO: Inicia imediatamente sem esperar minuto."""\n    print("[OTIMIZADO] Iniciando trading imediatamente, sem esperar próximo minuto")\n    return  # Retorna imediatamente'
            )
            
            # OTIMIZAÇÃO 2: Remove o sleep de 2 segundos no final do loop
            codigo_otimizado = codigo_otimizado.replace(
                'time.sleep(2)',
                'time.sleep(0.1)  # OTIMIZADO: Sleep reduzido de 2s para 0.1s'
            )
            
            # OTIMIZAÇÃO 3: Substitui if __name__ == "__main__": por if True:
            codigo_otimizado = codigo_otimizado.replace(
                'if __name__ == "__main__":',
                'if True:  # OTIMIZADO: Forçar execução via sistema integrado'
            )
            
            self.log("✅ Código otimizado carregado - iniciando execução imediata")
            
            # Executa o código otimizado
            exec(codigo_otimizado, globals())
            
        except Exception as e:
            self.log(f"❌ ERRO na execução do sistema original: {str(e)}")
            self.log(f"📋 Traceback: {traceback.format_exc()}")
    
    def iniciar(self):
        """Inicia o sistema integrado otimizado"""
        if self.running:
            self.log("⚠️ Sistema já está rodando")
            return False
            
        self.running = True
        self.dados_sistema["inicio"] = datetime.now().isoformat()
        self.dados_sistema["status"] = "Iniciando"
        
        self.log("🚀 SISTEMA INTEGRADO OTIMIZADO INICIADO")
        self.log("📈 Versão com início imediato do trading (sem espera de minuto)")
        
        # Thread principal - Sistema original otimizado
        self.thread_principal = threading.Thread(
            target=self.executar_sistema_original_otimizado,
            name="Trading-Otimizado",
            daemon=True
        )
        self.thread_principal.start()
        
        self.dados_sistema["status"] = "Ativo"
        self.log("✅ Thread principal iniciada - trading começará IMEDIATAMENTE")
        
        return True
    
    def parar(self):
        """Para o sistema"""
        if not self.running:
            self.log("⚠️ Sistema já está parado")
            return False
            
        self.running = False
        self.dados_sistema["status"] = "Parando"
        
        self.log("🛑 Parando sistema integrado...")
        
        # Aguarda threads terminarem (com timeout)
        if self.thread_principal and self.thread_principal.is_alive():
            self.thread_principal.join(timeout=5)
            
        self.dados_sistema["status"] = "Parado"
        self.log("✅ Sistema parado com sucesso")
        
        return True
    
    def status_threads(self):
        """Retorna status das threads"""
        status = {
            "principal": {
                "ativa": self.thread_principal.is_alive() if self.thread_principal else False,
                "nome": self.thread_principal.name if self.thread_principal else "Não iniciada"
            },
            "sistema_rodando": self.running
        }
        return status

def main():
    """Função principal de teste do sistema otimizado"""
    print("=" * 70)
    print("SISTEMA INTEGRADO OTIMIZADO - INÍCIO IMEDIATO DO TRADING")
    print("=" * 70)
    
    sistema = SistemaIntegradoOtimizado()
    
    try:
        # Inicia o sistema
        print("▶️ Iniciando sistema otimizado...")
        inicio_sistema = time.time()
        
        sucesso = sistema.iniciar()
        if not sucesso:
            print("❌ Falha ao iniciar sistema")
            return
        
        tempo_inicio = time.time() - inicio_sistema
        print(f"✅ Sistema iniciado em {tempo_inicio:.2f} segundos")
        
        # Monitora por 2 minutos para ver se o trading realmente inicia
        print("\n📊 Monitorando sistema por 2 minutos...")
        tempo_monitoramento = 120  # 2 minutos
        inicio_monitoramento = time.time()
        
        while (time.time() - inicio_monitoramento) < tempo_monitoramento:
            # Mostra status a cada 10 segundos
            time.sleep(10)
            
            tempo_decorrido = int(time.time() - inicio_monitoramento)
            dados = sistema.get_dados_sistema()
            threads = sistema.status_threads()
            
            print(f"\n⏱️ Tempo: {tempo_decorrido}s | Status: {dados['status']}")
            print(f"📈 Execuções: {dados['execucoes']} | Pares: {dados['pares_processados']}")
            print(f"🧵 Thread principal: {'✅ Ativa' if threads['principal']['ativa'] else '❌ Inativa'}")
            
            # Mostra logs recentes
            logs_recentes = sistema.get_logs_recentes(3)
            if logs_recentes:
                print("📝 Logs recentes:")
                for log in logs_recentes:
                    print(f"   {log}")
        
        print(f"\n✅ Monitoramento concluído após {tempo_monitoramento} segundos")
        
        # Relatório final
        dados_finais = sistema.get_dados_sistema()
        print("\n" + "=" * 70)
        print("RELATÓRIO FINAL - SISTEMA OTIMIZADO")
        print("=" * 70)
        print(f"⏱️ Tempo total de execução: {tempo_monitoramento} segundos")
        print(f"📈 Execuções realizadas: {dados_finais['execucoes']}")
        print(f"🔄 Pares processados: {dados_finais['pares_processados']}")
        print(f"📊 Ordens enviadas: {dados_finais['ordens_enviadas']}")
        print(f"🟢 Status final: {dados_finais['status']}")
        
        if dados_finais['execucoes'] > 0:
            print("\n✅ SUCESSO: Trading iniciou e está processando!")
        else:
            print("\n⚠️ ATENÇÃO: Trading ainda não processou execuções")
            print("   Pode estar aguardando condições de mercado ou horário específico")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print(f"📋 Traceback: {traceback.format_exc()}")
    finally:
        # Para o sistema
        print("\n🛑 Parando sistema...")
        sistema.parar()
        print("✅ Sistema parado com sucesso")

if __name__ == "__main__":
    main()
