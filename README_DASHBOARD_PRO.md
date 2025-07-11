# 🚀 Trading System Pro - Dashboard Completo

## 📋 Visão Geral

Este é um sistema completo de trading profissional com foco em **pairs trading**, análise de cointegração, modelos ARIMA/GARCH e execução automatizada via MetaTrader 5. O dashboard foi desenvolvido com tecnologias modernas e interface responsiva.

## ✨ Funcionalidades Principais

### 🎯 **Core Trading**
- ✅ Análise de cointegração entre pares de ativos
- ✅ Modelos preditivos ARIMA/GARCH
- ✅ Geração automática de sinais de trading
- ✅ Integração com MetaTrader 5
- ✅ Gestão avançada de risco
- ✅ Monitor de posições em tempo real

### 📊 **Interface Moderna**
- ✅ Dashboard responsivo e intuitivo
- ✅ Gráficos interativos com Plotly
- ✅ Métricas em tempo real
- ✅ Filtros avançados por setor
- ✅ CSS profissional customizado
- ✅ Tema escuro otimizado

### ⚙️ **Configurações Avançadas**
- ✅ Parâmetros estatísticos configuráveis
- ✅ Filtros de cointegração e volatilidade
- ✅ Gestão de risco personalizável
- ✅ Auto-refresh configurável
- ✅ Salvamento/carregamento de configurações

### 📈 **Análise e Relatórios**
- ✅ Distribuição de Z-Scores
- ✅ Estatísticas de cointegração
- ✅ P&L histórico e em tempo real
- ✅ Exportação de relatórios
- ✅ Logs estruturados

## 🛠️ Instalação e Configuração

### **Pré-requisitos**
- Python 3.8+
- MetaTrader 5 (apenas Windows)
- 4GB RAM mínimo
- Conexão com internet

### **Instalação Rápida**

1. **Clonar/Baixar o projeto**
   ```bash
   # Se usando Git
   git clone <repositorio>
   cd trading-system-pro
   
   # Ou baixar e extrair os arquivos
   ```

2. **Instalar dependências**
   ```bash
   pip install -r requirements_dashboard_pro.txt
   ```

3. **Executar o dashboard**
   ```bash
   # Método 1: Launcher automático
   python launch_dashboard_pro.py
   
   # Método 2: Streamlit direto
   streamlit run dashboard_trading_pro.py
   ```

4. **Acessar via navegador**
   - URL: http://localhost:8501
   - O dashboard abrirá automaticamente

## 🎮 Como Usar

### **1. Configuração Inicial**

1. **Conectar ao MetaTrader 5** (opcional para modo simulado)
   - Abra a barra lateral esquerda
   - Vá em "🔌 Conexão MetaTrader 5"
   - Insira suas credenciais
   - Clique em "🔌 Conectar"

2. **Selecionar Ativos**
   - Use "📊 Seleção de Ativos"
   - Filtre por setor se desejar
   - Selecione os ativos desejados
   - Confirme a seleção

### **2. Análise de Pares**

1. **Configurar Parâmetros**
   - Ajuste Z-Score threshold (padrão: 2.0)
   - Configure filtros estatísticos
   - Defina período de análise
   - Escolha timeframe

2. **Executar Análise**
   - Clique em "🔍 Executar Análise"
   - Aguarde processamento
   - Visualize resultados

### **3. Monitoramento**

1. **Visualizar Sinais**
   - Veja tabela de sinais gerados
   - Filtre por tipo (BUY/SELL)
   - Analise confiança e R/R ratio

2. **Monitor de Posições**
   - Acompanhe P&L em tempo real
   - Visualize gráficos de evolução
   - Use controles de gestão

## 📊 Estrutura do Projeto

```
trading-system-pro/
├── 📄 dashboard_trading_pro.py      # Dashboard principal
├── 📄 launch_dashboard_pro.py       # Launcher automático
├── 📄 requirements_dashboard_pro.txt # Dependências
├── 📄 README_DASHBOARD_PRO.md       # Este arquivo
├── 📄 calculo_entradas_v55.py      # Sistema de análise original
├── 📄 sistema_integrado.py         # Sistema integrado com threading
└── 📄 trading_system_streamlit.py  # Sistema original Streamlit
```

## ⚙️ Configurações Avançadas

### **Parâmetros Estatísticos**
```python
zscore_threshold = 2.0          # Limite para sinais
r2_min_threshold = 0.5          # R² mínimo
beta_max_threshold = 1.5        # Beta máximo
p_value_threshold = 0.05        # P-value para cointegração
```

### **Gestão de Risco**
```python
max_positions = 5               # Máx posições simultâneas
risk_per_trade = 0.02          # 2% de risco por trade
stop_loss_pct = 0.05           # 5% stop loss
take_profit_pct = 0.10         # 10% take profit
```

### **Filtros de Mercado**
```python
min_volume = 1000000           # Volume mínimo diário
max_spread_pct = 0.01          # 1% spread máximo
enable_cointegration_filter = True
enable_volatility_filter = True
```

## 🔧 Troubleshooting

### **Problemas Comuns**

1. **MetaTrader5 não encontrado**
   ```
   ⚠️ MetaTrader5 não encontrado. Instale com: pip install MetaTrader5
   ```
   **Solução**: Instale MT5 terminal e biblioteca Python

2. **Bibliotecas estatísticas faltando**
   ```
   ⚠️ Bibliotecas estatísticas não encontradas
   ```
   **Solução**: 
   ```bash
   pip install statsmodels arch scipy
   ```

3. **Dashboard não carrega**
   - Verifique se porta 8501 está livre
   - Execute: `streamlit run dashboard_trading_pro.py --server.port=8502`

4. **Erro de dependências**
   ```bash
   pip install --upgrade pip
   pip install -r requirements_dashboard_pro.txt --force-reinstall
   ```

### **Modo Simulação**
Se MT5 não estiver disponível, o dashboard funciona em **modo simulação**:
- Dados simulados realistas
- Todas as funcionalidades de interface
- Sinais de exemplo
- P&L simulado

## 📈 Funcionalidades por Aba

### **🎯 Dashboard**
- Visão geral do sistema
- Status de conexões
- Métricas da conta
- Resumo de posições

### **📊 Seleção de Pares**
- Lista de ativos disponíveis
- Filtros por setor
- Estatísticas de seleção
- Gráfico de distribuição

### **📈 Análise**
- Resultados de cointegração
- Distribuição de Z-Scores
- Sinais de trading
- Estatísticas detalhadas

### **💼 Posições**
- Monitor em tempo real
- P&L cumulativo
- Controles de posição
- Gráficos de evolução

## 🚀 Próximas Atualizações

### **Em Desenvolvimento**
- 🔄 Integração WhatsApp/Email
- 🔄 Exportação Excel avançada
- 🔄 Backtesting histórico
- 🔄 Otimização automática
- 🔄 Dashboard mobile

### **Roadmap 2025**
- AI/ML para previsões
- Multi-broker support
- Cloud deployment
- API REST completa
- Mobile app

## 📞 Suporte

Para suporte técnico:
- 📧 Email: suporte@tradingsystempro.com
- 📱 WhatsApp: +55 (11) 99999-9999
- 🌐 Site: www.tradingsystempro.com
- 📚 Docs: docs.tradingsystempro.com

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

---

**🚀 Trading System Pro** - *Desenvolvido com ❤️ para traders profissionais*
