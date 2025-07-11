# 📊 Mapeamento de Tempos de Atualização - Sistema de Trading

Este documento mapeia todos os intervalos de atualização automática das threads, da página Streamlit e outras funções relevantes no sistema de trading.

## 📈 Dashboard Streamlit (dashboard_trading_pro_real.py)

### 🔄 Auto-Refresh da Interface - ✅ CORRIGIDO
- **Status**: ✅ Funcionando corretamente após correções
- **Problema Identificado**: Inicialização dupla de variáveis de estado causando conflitos
- **Solução Aplicada**: 
  - Centralizada inicialização no início do arquivo
  - Removida reinicialização na sidebar
  - Adicionado debug melhorado
  - Implementado fallback para casos extremos

### 📊 Configurações Atuais:
- **Intervalo Padrão**: 30 segundos
- **Intervalo Configurável**: 10 a 300 segundos (via slider na sidebar)
- **Controle**: Checkbox para ativar/desativar
- **Status**: Indicador visual no canto superior direito da tela
- **Debug**: Painel de debug disponível quando ativado
- **Fallback**: Auto-refresh forçado se não executar em 5s extras

### 🔧 Melhorias Implementadas:
- **Debug Console**: Mostra estado atual do auto-refresh
- **Timing Preciso**: Cálculo mais preciso do tempo decorrido
- **Logs Detalhados**: Print statements para debug no console
- **Teste Manual**: Botão para testar auto-refresh imediatamente
- **Fallback Safety**: Execução forçada se timing falhar

### 🎮 Controles da Sidebar
- **Localização**: Linhas 3470-3500 (atualizado)
- **Funcionalidades**:
  - Checkbox: "Atualização Automática"
  - Slider: "Intervalo (segundos)" (10-300s, padrão 30s)
  - Status: Próxima atualização em Xs
  - Debug: Painel detalhado quando habilitado
  - Teste: Botão para forçar atualização

---

## 🔧 Problemas Identificados e Soluções

### ❌ Problema: Auto-Refresh não funcionava
**Causa Raiz:**
- Inicialização dupla de `st.session_state` (linhas 53-60 e 3433-3437)
- Conflito entre valores iniciais e valores da sidebar
- Timing impreciso entre verificações

**Soluções Aplicadas:**
1. **Centralização**: Inicialização única no início do arquivo
2. **Debug**: Adicionado console de debug detalhado
3. **Fallback**: Sistema de fallback para casos extremos
4. **Timing**: Cálculo mais preciso do tempo decorrido
5. **Teste**: Botão manual para testar funcionalidade

### ✅ Status Atual: FUNCIONANDO
- Auto-refresh operacional com debug
- Indicadores visuais atualizados
- Fallback implementado para segurança
- Console de debug disponível

---

## 🧵 Sistema Integrado (sistema_integrado.py)

### 📊 Thread de Monitoramento Principal
- **Função**: `thread_monitoramento()`
- **Intervalo**: 120 segundos (2 minutos)
- **Localização**: Linha 230
- **Código**: `time.sleep(120)  # A cada 2 minutos`
- **Erro**: 60 segundos de espera em caso de exceção (linha 234)
- **Funcionalidades**:
  - Relatório de execuções
  - Contagem de pares processados
  - Contagem de ordens enviadas
  - Taxa de sucesso do sistema

### 🔍 Thread de Monitoramento de Posições
- **Função**: `thread_monitoramento_posicoes()`
- **Intervalo**: 30 segundos
- **Localização**: Linhas 263-264
- **Código**: `for i in range(30): time.sleep(1)`
- **Erro**: 60 segundos de espera em caso de exceção (linha 267)
- **Funcionalidades**:
  - Verificação de posições MT5
  - Monitoramento de ordens pendentes
  - Execução de monitoramento real

### 📈 Thread de Análise e Envio de Ordens
- **Função**: `thread_analise_e_envio_ordens()`
- **Intervalo**: 300 segundos (5 minutos)
- **Localização**: Linhas 360-364
- **Código**: `for i in range(300): time.sleep(1)`
- **Erro**: 60 segundos de espera em caso de exceção (linha 364)
- **Restrição**: Apenas durante horário de operações (9h às 15h)
- **Funcionalidades**:
  - Análise de oportunidades
  - Envio de ordens ao MT5
  - Processamento de sinais

### 📊 Thread de Break-Even Contínuo
- **Função**: `thread_break_even_continuo()`
- **Intervalo**: 10 segundos
- **Localização**: Linhas 1396-1400
- **Código**: `for i in range(10): time.sleep(1)`
- **Erro**: 30 segundos de espera em caso de exceção (linha 1400)
- **Restrição**: Apenas durante janela de break-even (8h às 17h)
- **Funcionalidades**:
  - Monitoramento contínuo de lucros
  - Movimentação automática de stop-loss
  - Proteção de capital

---

## ⚠️ Tempos de Erro e Recuperação

### 🔄 Recuperação de Erros
- **Thread Principal**: 60 segundos
- **Thread Posições**: 60 segundos
- **Thread Ordens**: 60 segundos
- **Thread Break-Even**: 30 segundos
- **Dashboard**: Não aplicável (recarrega imediatamente)

### 🕐 Janelas de Operação
- **Análise e Envio**: 9h às 15h
- **Break-Even**: 8h às 17h
- **Monitoramento**: 24h (sempre ativo)
- **Dashboard**: 24h (sempre ativo)

---

## 📊 Outros Tempos Relevantes

### 🚀 Execução de Análise Manual
- **Intervalo Padrão**: 60 segundos (config.intervalo_execucao)
- **Localização**: Linha 2288 do dashboard
- **Código**: `time.sleep(intervalo)`

### 🔧 Verificador Simples
- **Processamento**: 1 segundo (linha 128)
- **Verificação**: 1 segundo por ciclo (linha 150)

### 🔄 Auto-Restart do Sistema
- **Aguardo**: 5 segundos após falha (linha 1902)
- **Código**: `time.sleep(5)`

---

## 📋 Resumo dos Intervalos

| Componente | Intervalo | Configurável | Localização |
|------------|-----------|-------------|-------------|
| Dashboard Auto-Refresh | 30s (10-300s) | ✅ Sim | Sidebar |
| Thread Monitoramento | 120s | ❌ Não | sistema_integrado.py |
| Thread Posições | 30s | ❌ Não | sistema_integrado.py |
| Thread Análise/Ordens | 300s | ❌ Não | sistema_integrado.py |
| Thread Break-Even | 10s | ❌ Não | sistema_integrado.py |
| Recuperação de Erro | 30-60s | ❌ Não | Várias |

---

## 🎯 Recomendações de Otimização

### ⚡ Performance
- Dashboard: 30s é adequado para monitoramento em tempo real
- Posições: 30s permite resposta rápida a mudanças
- Break-Even: 10s garante proteção eficaz do capital
- Análise: 5min evita overtrading

### 🔧 Configurações Avançadas
- Para day trading: reduzir break-even para 5s
- Para swing trading: aumentar análise para 10min
- Para conservador: aumentar dashboard para 60s
- Para agressivo: reduzir posições para 15s

### 📊 Monitoramento
- Todos os tempos são logados no sistema
- Indicadores visuais mostram status em tempo real
- Controles na sidebar permitem ajustes rápidos
- Sistema se recupera automaticamente de erros

---

## 🔍 Como Modificar os Tempos

### 📈 Dashboard (Streamlit)
```python
# Arquivo: dashboard_trading_pro_real.py
# Linhas: 3440-3460
auto_refresh_interval = st.sidebar.slider(
    "Intervalo (segundos)", 
    10, 300, 30, 10  # min, max, padrão, step
)
```

### 🧵 Threads do Sistema
```python
# Arquivo: sistema_integrado.py
# Monitoramento: linha 230
time.sleep(120)  # Alterar para novo valor

# Posições: linha 263
for i in range(30):  # Alterar 30 para novo valor
    time.sleep(1)

# Análise: linha 360
for i in range(300):  # Alterar 300 para novo valor
    time.sleep(1)

# Break-Even: linha 1396
for i in range(10):  # Alterar 10 para novo valor
    time.sleep(1)
```

---

*📅 Documento atualizado em: 2025-07-03*  
*🔄 Versão: 1.1 - Auto-refresh corrigido*  
*👨‍💻 Sistema: Trading Dashboard Pro*
