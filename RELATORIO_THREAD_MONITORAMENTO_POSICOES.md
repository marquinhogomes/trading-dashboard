# Relatório: Thread de Monitoramento de Posições

## 📋 Resumo
Implementada thread específica para monitoramento de posições baseada no bloco do `calculo_entradas_v55.py` no sistema integrado.

## 🎯 Objetivo
Adicionar monitoramento ativo e contínuo de posições abertas, incluindo:
- Detecção de pernas órfãs (apenas uma posição do par aberta)
- Conversão automática de ordens pendentes para ordens a mercado
- Fechamento automático de posições remanescentes
- Controle de limites de lucro/prejuízo por magic

## 🔄 Mudanças Implementadas

### 1. Nova Thread Adicionada
**Função:** `thread_monitoramento_posicoes()`
**Frequência:** A cada 30 segundos
**Funcionalidades:**
- Monitoramento real com MT5 (se disponível)
- Modo simulado para demonstração
- Logs detalhados de todas as ações

### 2. Funcionalidades Implementadas

#### 🔍 Monitoramento Real (`executar_monitoramento_real`)
```python
# Obtém posições e ordens do MT5
posicoes_abertas = mt5.positions_get()
posicoes_pendentes = mt5.orders_get()

# Filtra por magic number específico
magics_abertas = set(p.magic for p in posicoes_abertas 
                    if magic_comeca_com(p.magic, prefixo_script))
```

#### 📊 Detecção de Pernas Órfãs
- Identifica quando apenas uma posição do par está aberta
- Programa fechamento automático da perna remanescente
- Logs detalhados para rastreabilidade

#### 🔄 Conversão de Ordens Pendentes
- Detecta ordens pendentes do independente quando dependente está aberto
- Cancela ordem pendente automaticamente
- Envia nova ordem a mercado para completar o par

#### 💰 Controle de Lucros/Prejuízos
- Calcula P&L por magic number
- Verifica limites configuráveis (ex: +1200 / -500)
- Alertas automáticos quando limites são atingidos

### 3. Modo Simulado (`executar_monitoramento_simulado`)
- Demonstra funcionalidades sem MT5
- Posições fictícias para teste
- Logs informativos para validação

### 4. Funções Auxiliares

#### `obter_pares_configurados(magic)`
- Mapeia magic numbers para pares de ativos
- Estrutura adaptável conforme configuração

#### `programar_fechamento_posicao(magic, ativo)`
- Interface para fechamento de posições
- Integração com sistema de orders

#### `converter_ordem_pendente_para_mercado(...)`
- Cancela ordens pendentes
- Envia ordens a mercado
- Logs detalhados do processo

#### `calcular_lucros_por_magic(...)`
- Soma P&L por magic number
- Verifica limites de risco
- Alertas de controle

## 🧵 Integração no Sistema

### Inicialização Atualizada
```python
# Thread principal do sistema de trading
thread_trading = threading.Thread(target=self.executar_sistema_original, name="SistemaTrading")

# Thread de monitoramento geral
thread_monitor = threading.Thread(target=self.thread_monitoramento, name="Monitoramento")

# Thread de monitoramento de posições (NOVA)
thread_monitor_posicoes = threading.Thread(target=self.thread_monitoramento_posicoes, name="MonitoramentoPosicoes")
```

### Verificação de Threads
- Monitora se todas as threads estão executando
- Alertas automáticos se alguma thread parar
- Logs de status contínuos

## 📊 Exemplo de Saída

```
🔍 INICIANDO: Thread de monitoramento de posições
✅ MetaTrader5 importado com sucesso
🔍 VERIFICAÇÃO DE POSIÇÕES E ORDENS PENDENTES
📊 Número de operações em aberto: 3
⚠️ Magic 101: Apenas uma perna aberta (PETR4)
📌 Magic=101: ativo dependente (PETR4) já foi fechado.
   🔄 Programando fechamento da perna remanescente (VALE3)...
🔄 Magic=102: Dependente aberto, convertendo ordem pendente do independente para mercado
💰 ANÁLISE DE LUCROS/PREJUÍZOS POR MAGIC:
   Magic 101: 🟢 R$ +234.50
   Magic 102: 🔴 R$ -89.30
   Magic 103: 🟢 R$ +567.80
```

## ✅ Benefícios

### 🛡️ Gestão de Risco Automatizada
- Controle contínuo de posições
- Fechamento automático de exposições órfãs
- Limites de P&L por operação

### ⚡ Resposta Rápida
- Monitoramento a cada 30 segundos
- Conversão imediata de ordens pendentes
- Redução de slippage

### 📋 Transparência Total
- Logs detalhados de todas as ações
- Rastreabilidade completa
- Histórico de decisões automáticas

### 🔧 Flexibilidade
- Configuração de magic numbers adaptável
- Limites personalizáveis
- Modo simulado para testes

## 🧪 Status
- ✅ Thread implementada
- ✅ Integração no sistema principal
- ✅ Modo real e simulado
- ✅ Logs detalhados
- ✅ Sintaxe validada (sem erros)
- 🔄 Pronto para testes em produção

## 📁 Arquivos Modificados
- `sistema_integrado.py` - Nova thread de monitoramento de posições

---
**Data:** 2025-06-23  
**Status:** Concluído  
**Thread:** `MonitoramentoPosicoes` ativa no sistema integrado
