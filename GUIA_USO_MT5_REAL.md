# 🔗 GUIA DE USO - INTEGRAÇÃO MT5 REAL
## Dashboard de Trading Quantitativo v3.0

**Versão:** 3.0 - MT5 Real Integration  
**Data:** 19 de Junho de 2025  
**Status:** ✅ PRONTO PARA USO  

---

## 🚀 INÍCIO RÁPIDO

### **1. Pré-requisitos**
```bash
# Instalar dependências
pip install MetaTrader5 streamlit plotly pandas numpy

# Verificar instalação do MT5
python -c "import MetaTrader5 as mt5; print('MT5 OK' if mt5 else 'MT5 ERROR')"
```

### **2. Executar Dashboard**
```bash
streamlit run dashboard_trading_pro.py --server.port=8521
```

### **3. Acessar Interface**
- **URL:** http://localhost:8521
- **Login:** Usar credenciais reais da conta MT5

---

## 🔐 CONFIGURAÇÃO DE CONEXÃO MT5

### **Passo 1: Preparar MT5**
1. **Instalar MetaTrader 5** (versão atual)
2. **Habilitar trading automático** no MT5
3. **Configurar conta** (demo ou real)
4. **Anotar credenciais**: Login, Senha, Servidor

### **Passo 2: Conectar no Dashboard**
1. **Abrir sidebar** (painel esquerdo)
2. **Seção "🔐 Login MT5"**
3. **Inserir dados**:
   - **Usuário**: Número da conta MT5
   - **Senha**: Senha da conta
   - **Servidor**: Nome do servidor do broker
4. **Clicar "🚀 Conectar MT5"**

### **Passo 3: Verificar Conexão**
- ✅ **Status Verde**: "✅ MT5 Conectado"
- 💰 **Dados da Conta**: Balance, equity, margem
- 📊 **Símbolos Disponíveis**: Lista atualizada do broker

---

## 📊 FUNCIONALIDADES PRINCIPAIS

### **🎯 Monitoramento em Tempo Real**

#### **Cartões de Status (KPIs)**
- **💰 Equity Atual**: Valor total da conta
- **📈 P&L Atual**: Lucro/prejuízo em tempo real
- **💼 Posições Abertas**: Número de trades ativos
- **🔗 Status MT5**: Estado da conexão

#### **Dados de Mercado**
- **📈 Gráficos Candlestick**: OHLC em tempo real
- **🎯 Análise de Spread**: Cálculos baseados em cotações reais
- **💼 P&L das Posições**: Valores atuais de cada trade
- **🌐 Saúde da Conexão**: Latência e status

### **🔍 Análise de Símbolos**

#### **Validação Automática**
1. **Selecionar Ativos** na sidebar
2. **Verificação Automática** de disponibilidade
3. **Status em Tempo Real**:
   - ✅ **Verde**: Símbolo válido e cotações ativas
   - ⚠️ **Amarelo**: Símbolo válido mas sem tick atual
   - ❌ **Vermelho**: Símbolo inválido ou indisponível

#### **Informações Detalhadas**
- **Bid/Ask**: Cotações em tempo real
- **Spread**: Diferença em points
- **Volume**: Atividade do mercado
- **Última Atualização**: Timestamp do último tick

### **📈 Análise de Spread**

#### **Cálculo Automático**
1. **Selecionar 2+ Símbolos** na sidebar
2. **Cálculo do Spread**: Diferença entre cotações
3. **Z-Score Dinâmico**: Análise estatística baseada em histórico
4. **Sinais Automáticos**:
   - 🟢 **BUY**: Z-Score < -2.0
   - 🔴 **SELL**: Z-Score > +2.0
   - 🟡 **HOLD**: -2.0 ≤ Z-Score ≤ +2.0

#### **Gráficos Interativos**
- **Linha do Spread**: Evolução histórica
- **Thresholds**: Linhas de entrada/saída
- **Spread Atual**: Valor em tempo real
- **Sinal Atual**: Recomendação de trading

---

## ⚙️ CONFIGURAÇÕES AVANÇADAS

### **🎛️ Parâmetros de Trading**

#### **Timeframes Disponíveis**
- **M1**: 1 minuto
- **M5**: 5 minutos  
- **M15**: 15 minutos
- **M30**: 30 minutos
- **H1**: 1 hora ⭐ (recomendado)
- **H4**: 4 horas
- **D1**: 1 dia

#### **Filtros e Limites**
- **Z-Score Threshold**: Sensibilidade dos sinais (1.0 - 4.0)
- **Max Posições**: Limite de trades simultâneos
- **Risco por Trade**: Percentual de risco (0.1% - 10.0%)
- **Stop Loss**: Percentual de stop (0.5% - 20.0%)
- **Take Profit**: Percentual de target (0.5% - 20.0%)

### **📊 Filtros de Mercado**
- **Cointegração**: Análise estatística de pares
- **Volatilidade**: Filtro por volatilidade histórica
- **Volume**: Filtro por atividade de mercado
- **Spread**: Filtro por spread mínimo/máximo

---

## 🛠️ TROUBLESHOOTING

### **❌ Problemas Comuns**

#### **"MT5 não conecta"**
**Soluções:**
1. Verificar se MT5 está instalado e rodando
2. Conferir credenciais (login deve ser número)
3. Verificar nome correto do servidor
4. Testar conexão manual no MT5 primeiro
5. Verificar firewall/antivírus

#### **"Símbolos não encontrados"**
**Soluções:**
1. Verificar se símbolos estão disponíveis no broker
2. Usar nomenclatura correta (ex: EURUSD, não EUR/USD)
3. Verificar se conta tem acesso aos instrumentos
4. Tentar símbolos padrão (EURUSD, GBPUSD)

#### **"Dados não carregam"**
**Soluções:**
1. Verificar conexão com internet
2. Verificar se mercado está aberto
3. Reduzir número de símbolos monitorados
4. Aguardar alguns segundos para cache atualizar
5. Reconectar MT5

#### **"Interface lenta"**
**Soluções:**
1. Reduzir número de símbolos (máx 10)
2. Usar timeframes maiores (H1, H4)
3. Limpar cache do navegador
4. Verificar recursos do sistema
5. Fechar outros programas

### **🔧 Comandos de Diagnóstico**

#### **Teste de Conectividade**
```python
import MetaTrader5 as mt5
print("MT5 disponível:", mt5.initialize())
print("Info terminal:", mt5.terminal_info())
```

#### **Verificar Símbolos**
```python
symbols = mt5.symbols_get()
print(f"Símbolos disponíveis: {len(symbols) if symbols else 0}")
```

#### **Teste de Dados**
```python
eurusd = mt5.symbol_info_tick("EURUSD")
print("Tick EURUSD:", eurusd)
```

---

## 📊 INTERPRETAÇÃO DOS DADOS

### **🎯 Sinais de Trading**

#### **Z-Score**
- **< -2.0**: 🟢 **Sinal de COMPRA** (spread baixo)
- **> +2.0**: 🔴 **Sinal de VENDA** (spread alto)
- **-2.0 a +2.0**: 🟡 **AGUARDAR** (spread normal)

#### **Cores dos Gráficos**
- **🟢 Verde**: Valores positivos/lucro
- **🔴 Vermelho**: Valores negativos/prejuízo  
- **🟡 Amarelo**: Neutralidade/aguardar
- **🔵 Azul**: Dados históricos/referência

### **💰 Métricas da Conta**

#### **Equity vs Balance**
- **Equity**: Valor total (posições + dinheiro)
- **Balance**: Dinheiro disponível
- **P&L**: Equity - Balance

#### **Margem**
- **Margem Utilizada**: Capital comprometido
- **Margem Livre**: Capital disponível
- **Nível de Margem**: Razão Equity/Margem
  - **> 1000%**: 🟢 Saudável
  - **500-1000%**: 🟡 Atenção
  - **< 500%**: 🔴 Crítico

---

## 💡 DICAS DE USO

### **🎯 Boas Práticas**

#### **Seleção de Símbolos**
1. **Começar com 2-3 pares** para análise
2. **Usar pares correlacionados** (EUR/USD, GBP/USD)
3. **Verificar disponibilidade** antes de análise
4. **Preferir majors** para melhor liquidez

#### **Configuração de Parâmetros**
1. **Timeframe H1** para análise diária
2. **Z-Score 2.0** como padrão
3. **Risk 1%** para contas pequenas
4. **Stop/Target** 2.5%/5.0% como base

#### **Monitoramento**
1. **Verificar conexão** regularmente
2. **Acompanhar P&L** das posições
3. **Atentar para margem** disponível
4. **Observar sinais** de entrada/saída

### **⚠️ Precauções**

#### **Risk Management**
- **Nunca arriscar mais de 1-2%** por trade
- **Sempre usar stop loss**
- **Diversificar pares** para reduzir correlação
- **Monitorar exposição total**

#### **Conexão**
- **Manter MT5 aberto** durante análise
- **Verificar conexão** com broker
- **Ter plano B** para reconexão
- **Não depender 100%** de automação

---

## 📞 SUPORTE

### **🆘 Em Caso de Problemas**

#### **Suporte Técnico**
1. **Verificar logs** do sistema
2. **Testar conexão manual** no MT5
3. **Reiniciar dashboard** se necessário
4. **Documentar erro** com screenshots

#### **Reset do Sistema**
```bash
# Parar dashboard
Ctrl+C

# Limpar cache
# Reabrir navegador

# Reiniciar dashboard
streamlit run dashboard_trading_pro.py --server.port=8521
```

#### **Contato**
- **GitHub**: Reportar issues no repositório
- **Email**: Suporte técnico via email
- **Documentation**: Consultar documentação técnica

---

## 🎉 CONCLUSÃO

O Dashboard de Trading Quantitativo v3.0 com **Integração MT5 Real** oferece:

- 🔥 **Conectividade Total**: Dados diretos do MetaTrader 5
- 📊 **Análise Profissional**: Interface executiva e moderna
- ⚡ **Tempo Real**: Atualizações instantâneas
- 🛡️ **Confiabilidade**: Sistema robusto e estável
- 🎯 **Facilidade**: Interface intuitiva e documentada

**O sistema está PRONTO para uso profissional em contas reais ou demo!**

---

*Guia de Uso - Dashboard de Trading Quantitativo v3.0*  
*Atualizado em 19 de Junho de 2025*
