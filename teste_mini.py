print("Testando métodos...")
from sistema_integrado import SistemaIntegrado
sistema = SistemaIntegrado()
print("start_analysis_thread:", hasattr(sistema, 'start_analysis_thread'))
print("stop_analysis_thread:", hasattr(sistema, 'stop_analysis_thread'))
print("is_analysis_running:", hasattr(sistema, 'is_analysis_running'))
print("Teste concluído!")
