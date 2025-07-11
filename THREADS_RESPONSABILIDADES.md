# 🧵 Responsabilidades das Threads do Sistema Integrado

## 📋 Visão Geral das Threads

O `sistema_integrado.py` possui **4 threads principais** que trabalham em paralelo para gerenciar diferentes aspectos do sistema de trading:

---

## 1️⃣ **Thread de Monitoramento Principal**
```python
def thread_monitoramento(self):
```

### 🎯 **Responsabilidades:**
- **Relatórios estatísticos** do sistema a cada 2 minutos
- **Monitoramento geral** da saúde do sistema
- **Contabilização** de execuções, pares processados e ordens enviadas
- **Cálculo de taxa de sucesso** das operações

### ⏰ **Frequência:** 120 segundos (2 minutos)

### 📊 **O que monitora:**
- ⚡ Número de execuções realizadas
- 📈 Quantidade de pares processados
- 📝 Total de ordens enviadas ao mercado
- 🔄 Status geral do sistema
- ⏰ Tempo desde o último ciclo
- ✅ Taxa de sucesso das operações

### 🔧 **Recuperação de erro:** 60 segundos

---

## 2️⃣ **Thread de Monitoramento de Posições**
```python
def thread_monitoramento_posicoes(self):
```

### 🎯 **Responsabilidades:**
- **Verificação contínua** de posições abertas no MT5
- **Monitoramento de ordens pendentes**
- **Identificação de pares incompletos** (quando só uma perna está aberta)
- **Conversão de ordens pendentes** para ordens a mercado quando necessário
- **Fechamento automático** de posições em situações específicas

### ⏰ **Frequência:** 30 segundos

### 📊 **O que monitora:**
- 🔍 Posições abertas com magic number do sistema
- 📋 Ordens pendentes não executadas
- 💰 Cálculo de lucros/prejuízos por magic number
- 🔄 Pares incompletos que precisam de ação
- 📈 Status de execução de ordens

### 🔧 **Recuperação de erro:** 60 segundos

---

## 3️⃣ **Thread de Análise e Envio de Ordens**
```python
def thread_analise_e_envio_ordens(self):
```

### 🎯 **Responsabilidades:**
- **Análise de oportunidades** de trading baseada em Z-Score
- **Envio automático** de ordens para o MT5
- **Validação de condições** de entrada (cointegração, R², beta, etc.)
- **Processamento de sinais** de compra e venda
- **Otimização de preços** e volumes das ordens

### ⏰ **Frequência:** 300 segundos (5 minutos)

### 📊 **O que faz:**
- 🔍 Busca operações candidatas da `linha_operacao01`
- 📈 Analisa Z-Score para determinar tipo de entrada
- 🟢 Processa entradas de COMPRA (Z-Score ≤ -2.0)
- 🔴 Processa entradas de VENDA (Z-Score ≥ 2.0)
- ⚙️ Calcula preços, volumes e stops otimizados
- ✅ Valida condições antes do envio
- 📤 Envia ordens para o MT5

### ⏰ **Horário ativo:** 9h às 15h (horário de pregão)
### 🔧 **Recuperação de erro:** 60 segundos

---

## 4️⃣ **Thread de Break-Even Contínuo**
```python
def thread_break_even_continuo(self):
```

### 🎯 **Responsabilidades:**
- **Monitoramento contínuo** de lucros das posições abertas
- **Movimentação automática** de stop-loss para break-even
- **Proteção de lucros** quando atingem thresholds específicos
- **Gestão dinâmica** de risco das posições

### ⏰ **Frequência:** 10 segundos (mais rápida para proteção em tempo real)

### 📊 **O que faz:**
- 💰 Calcula lucro percentual de cada posição
- 📈 Para IBOV: move SL quando lucro ≥ R$ 150
- 📊 Para outros ativos: move SL quando lucro ≥ 0.8%
- 🛡️ Protege lucros automaticamente
- ⚡ Age rapidamente em movimentos favoráveis

### ⏰ **Horário ativo:** 8h às 17h (janela de break-even)
### 🔧 **Recuperação de erro:** 30 segundos

---

## 5️⃣ **Thread de Ajustes Programados**
```python
def thread_ajustes_programados(self):
```

### 🎯 **Responsabilidades:**
- **Execução de rotinas** em horários específicos
- **Ajuste de posições** às 15:10h
- **Remoção de ordens pendentes** às 15:20h
- **Fechamento total** às 16:01h

### ⏰ **Frequência:** 30 segundos (verificação de horários)

### 📊 **Cronograma de execução:**
- **15:10h** - Ajuste de posições (move TP para 60% do lucro)
- **15:20h** - Remove todas as ordens pendentes
- **16:01h** - Fecha todas as posições do sistema

### 🔧 **Recuperação de erro:** 60 segundos

---

## 🔄 **Fluxo de Trabalho das Threads**

```
┌─────────────────────────────────────────────────────────────┐
│                    SISTEMA INTEGRADO                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 Thread Monitoramento (2min)                            │
│  ├── Relatórios estatísticos                              │
│  └── Saúde do sistema                                      │
│                                                             │
│  🔍 Thread Posições (30s)                                  │
│  ├── Verifica posições MT5                                │
│  ├── Monitora ordens pendentes                            │
│  └── Fecha pares incompletos                              │
│                                                             │
│  📈 Thread Análise/Ordens (5min)                          │
│  ├── Busca oportunidades                                  │
│  ├── Valida condições                                     │
│  └── Envia ordens MT5                                     │
│                                                             │
│  📊 Thread Break-Even (10s)                               │
│  ├── Monitora lucros                                      │
│  └── Move stop-loss                                       │
│                                                             │
│  ⏰ Thread Ajustes (30s)                                  │
│  ├── 15:10h - Ajusta posições                            │
│  ├── 15:20h - Remove pendentes                           │
│  └── 16:01h - Fecha tudo                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 **Comunicação entre Threads**

### 📊 **Dados Compartilhados:**
- `self.dados_sistema` - Estatísticas gerais
- `self.logs` - Sistema de logs centralizado
- `self.running` - Flag de controle global
- `self.ajustes_executados_hoje` - Controle de execuções diárias

### 🔒 **Thread Safety:**
- Cada thread opera de forma independente
- Acesso seguro ao MT5 através de imports locais
- Logs centralizados com timestamp
- Controle de estado através de flags booleanas

---

## 📈 **Vantagens da Arquitetura Multi-Thread**

1. **⚡ Responsividade:** Break-even reage em 10s
2. **🔄 Confiabilidade:** Monitoramento contínuo
3. **📊 Eficiência:** Cada thread tem função específica
4. **🛡️ Segurança:** Múltiplas camadas de proteção
5. **📋 Auditoria:** Logs detalhados de todas as operações
6. **⏰ Precisão:** Execução pontual de rotinas programadas

---

## 🚨 **Considerações Importantes**

- **MT5 obrigatório:** Threads precisam do MetaTrader 5 conectado
- **Horários específicos:** Algumas threads só operam durante pregão
- **Recuperação automática:** Sistema se recupera de erros automaticamente
- **Logs detalhados:** Toda atividade é registrada com timestamp
- **Controle granular:** Cada thread pode ser monitorada independentemente

---

*Documento gerado automaticamente - Sistema Integrado de Trading v1.0*
