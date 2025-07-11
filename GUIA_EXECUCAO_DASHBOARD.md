# 🚀 GUIA DE EXECUÇÃO - DASHBOARD TRADING PRO

## ⚡ Execução Rápida

### Opção 1: Usar o arquivo BAT (Mais Fácil)
```
1. PRIMEIRO: Duplo clique em INSTALAR_DEPENDENCIAS.bat
2. Aguarde instalação completa das dependências
3. DEPOIS: Duplo clique em EXECUTAR_DASHBOARD.bat
4. Dashboard abrirá automaticamente no navegador
```

### Opção 2: Linha de Comando (Manual)
```powershell
# 1. Instalar dependências essenciais
pip install streamlit plotly pandas numpy MetaTrader5 openpyxl

# 2. Executar dashboard
streamlit run dashboard_trading_pro_real.py

# 3. Abrir navegador em: http://localhost:8501
```

### Opção 3: Usando o Launcher Python
```powershell
python launcher_dashboard.py
```

### ⚠️ IMPORTANTE - Se houver ERROS:
```
1. Execute PRIMEIRO: INSTALAR_DEPENDENCIAS.bat
2. Aguarde instalação completa (pode demorar)
3. SÓ DEPOIS execute: EXECUTAR_DASHBOARD.bat
```

## 📋 Pré-requisitos

### ✅ Verificações Necessárias
- [x] Python 3.8 ou superior instalado
- [x] MetaTrader 5 instalado e funcionando
- [x] Conta de trading configurada no MT5
- [x] Conexão com internet ativa
- [x] Porta 8501 disponível

### 📦 Dependências Principais
```
streamlit >= 1.28.0
plotly >= 5.15.0
MetaTrader5 >= 5.0.45
pandas >= 2.0.0
numpy >= 1.24.0
```

## 🎯 Configuração Inicial

### 1️⃣ Primeiro Acesso
1. **Abra o dashboard**: http://localhost:8501
2. **Verifique a sidebar**: Configurações do Sistema
3. **Configure MT5**: Insira login, senha e servidor
4. **Teste Conexão**: Clique em "🔗 Conectar"

### 2️⃣ Configuração de Ativos
1. **Selecione Segmentos**: Bancos, Energia, Petróleo, etc.
2. **Escolha Ativos**: Use multi-select ou "Selecionar Todos"
3. **Confirme Seleção**: Verifique lista de ativos selecionados

### 3️⃣ Parâmetros de Trading
```
Timeframe: 15 min (recomendado)
Período: 200 (padrão)
Z-Score: 2.0 (conservador)
Max Posições: 6
```

### 4️⃣ Filtros Avançados
- ✅ Cointegração (recomendado)
- ✅ R² Mínimo (0.5)
- ✅ Beta Máximo
- ✅ Z-Score Range

## 🎮 Como Usar

### 🔄 Operação Básica
1. **Configure parâmetros** na sidebar
2. **Clique "▶️ Iniciar Sistema"**
3. **Monitore** cartões de status no topo
4. **Observe** gráficos e tabelas atualizando
5. **Use "⏹️ Parar Sistema"** quando necessário

### 📊 Navegação por Tabs

#### Tab 1: 📊 Gráficos e Análises
- **Curva de Equity**: Evolução da conta em tempo real
- **Distribuição P/L**: Histograma de resultados

#### Tab 2: 📡 Sinais e Posições  
- **Sinais Ativos**: Oportunidades detectadas pelo sistema
- **Posições Abertas**: Operações em andamento
- **Ações Rápidas**: Botões para fechar posições

#### Tab 3: 📋 Histórico e Logs
- **Histórico de Trades**: Filtros por período e resultado
- **Log de Eventos**: Mensagens do sistema em tempo real

### 🎛️ Controles Principais

| Botão | Função | Localização |
|-------|--------|-------------|
| 🔗 Conectar | Conecta ao MT5 | Sidebar |
| ▶️ Iniciar Sistema | Inicia trading | Sidebar |
| ⏹️ Parar Sistema | Para trading | Sidebar |
| ❌ Fechar [Ativo] | Fecha posição | Tab Posições |
| 💾 Salvar Perfil | Salva config | Sidebar |
| 🔄 Reset Completo | Reseta sistema | Sidebar |

## 📤 Exportação de Dados

### 📊 Relatório Excel
1. **Clique "📊 Exportar Excel"** no topo
2. **Aguarde geração** do arquivo
3. **Download automático** será oferecido
4. **Arquivo inclui**:
   - Resumo geral
   - Posições abertas
   - Sinais detectados
   - Equity histórico
   - Logs completos

### 📋 Dados Inclusos
- **Métricas financeiras** (P/L, equity, drawdown)
- **Histórico completo** de trades
- **Análises estatísticas** (win rate, sharpe)
- **Logs detalhados** de eventos
- **Configurações utilizadas**

## 🔍 Monitoramento

### 📈 Cartões de Status (Auto-atualizados)
- **Pares Processados**: Total de análises
- **Posições Abertas**: Operações ativas
- **Equity Atual**: Valor da conta
- **P/L Diário**: Resultado do dia
- **Win Rate**: Taxa de acerto
- **Sharpe Ratio**: Qualidade dos retornos
- **Drawdown**: Perda máxima
- **Última Atualização**: Timestamp

### 🎯 Métricas Chave
```
✅ Verde: Valores positivos/normais
🟡 Amarelo: Atenção necessária  
🔴 Vermelho: Valores negativos/críticos
```

## ⚠️ Troubleshooting

### ❌ Problemas Comuns

**Dashboard não abre:**
```powershell
# Verifique Python
python --version

# Instale dependências
pip install -r requirements_dashboard.txt

# Tente porta alternativa
streamlit run dashboard_trading_pro_real.py --server.port 8502
```

**Erro de conexão MT5:**
```
1. Abra MT5 manualmente
2. Faça login na conta
3. Verifique servidor/dados
4. Tente reconectar no dashboard
```

**Dados não atualizam:**
```
1. Verifique se sistema está iniciado
2. Observe logs na Tab 3
3. Confirme conexão MT5 ativa
4. Aguarde 1-2 ciclos (1-2 minutos)
```

**Performance lenta:**
```
1. Reduza número de ativos
2. Aumente intervalo de execução
3. Feche outras aplicações
4. Use filtros para reduzir processamento
```

### 🔧 Comandos de Diagnóstico
```powershell
# Verificar instalação
python -c "import streamlit; print('OK')"

# Testar MT5
python -c "import MetaTrader5; print('OK')"

# Verificar porta
netstat -an | findstr 8501
```

## 🎯 Dicas de Uso

### 💡 Melhores Práticas
1. **Inicie com poucos ativos** para teste
2. **Use filtros conservadores** inicialmente
3. **Monitore logs** regularmente
4. **Exporte dados** periodicamente
5. **Teste em conta demo** primeiro

### ⚡ Otimização
- **Filtros ativos**: Reduzem processamento
- **Período menor**: Execução mais rápida
- **Menos ativos**: Maior performance
- **Auto-refresh**: Apenas quando necessário

### 🛡️ Segurança
- **Nunca compartilhe** credenciais MT5
- **Use senhas fortes** na conta
- **Monitore posições** regularmente
- **Mantenha logs** para auditoria

## 📞 Suporte Rápido

### 🆘 Se algo der errado:
1. **Pare o sistema** (⏹️ Parar Sistema)
2. **Verifique logs** (Tab 3 - Histórico e Logs)
3. **Teste conexão MT5** (🔗 Conectar)
4. **Reinicie dashboard** se necessário

### 📋 Informações Úteis
- **URL Dashboard**: http://localhost:8501
- **Logs Completos**: Visíveis na Tab 3
- **Configuração**: Salva automaticamente
- **Dados**: Exportáveis em Excel

---

## 🎉 Pronto para Usar!

**Seu dashboard profissional está configurado e pronto para trading real com MT5!**

🚀 **Execute agora**: `EXECUTAR_DASHBOARD.bat` ou `streamlit run dashboard_trading_pro_real.py`
