# 🚀 Trading System Pro - Dashboard Completo

## 📋 Visão Geral

Sistema profissional de trading automatizado com análise de cointegração, modelos ARIMA/GARCH, integração MetaTrader 5 e dashboard avançado em Streamlit.

### ✨ Principais Funcionalidades

- 📊 **Análise de Cointegração**: Identificação automática de pares cointegrados
- 🤖 **Modelos ARIMA/GARCH**: Previsão e análise de volatilidade
- 📈 **Dashboard Interativo**: Interface web moderna e responsiva
- 🔌 **Integração MT5**: Execução real de ordens via MetaTrader 5
- 🛡️ **Gestão de Risco**: Controles avançados de stop loss e take profit
- 📱 **Monitoramento Real**: Acompanhamento de posições em tempo real
- 📊 **Relatórios Avançados**: Análises detalhadas e exportação de dados

## 🏗️ Arquitetura do Sistema

```
Trading System Pro/
├── 📁 Core Components
│   ├── dashboard_trading_pro.py      # Dashboard principal
│   ├── sistema_integrado.py          # Sistema de integração
│   └── calculo_entradas_v55.py       # Cálculos de entrada
│
├── 📁 Configuration
│   ├── requirements_dashboard_pro.txt # Dependências
│   ├── trading_config.json           # Configurações (auto-gerado)
│   └── .streamlit/config.toml         # Config Streamlit
│
├── 📁 Utilities
│   ├── launcher.py                   # Launcher simplificado
│   ├── test_integration.py           # Teste de integração
│   └── start_dashboard.bat           # Script Windows
│
└── 📁 Documentation
    ├── README_DASHBOARD_PRO.md       # Documentação detalhada
    └── INSTRUCOES_INICIALIZACAO.md   # Instruções de setup
```

## 🚀 Início Rápido

### 1. Pré-requisitos
```bash
# Python 3.8+ é obrigatório
python --version

# Verificar pip
pip --version
```

### 2. Instalação
```bash
# Instalar dependências principais
pip install streamlit pandas numpy plotly matplotlib seaborn

# Instalar dependências estatísticas
pip install statsmodels arch scikit-learn

# Para integração MT5 (opcional)
pip install MetaTrader5
```

### 3. Executar Teste de Integração
```bash
python test_integration.py
```

### 4. Iniciar Dashboard

**Opção 1 - Launcher Automático:**
```bash
python launcher.py
```

**Opção 2 - Streamlit Direto:**
```bash
streamlit run dashboard_trading_pro.py --server.port 8501
```

**Opção 3 - Script Windows:**
```bash
start_dashboard.bat
```

### 5. Acessar Interface
Abra seu navegador em: **http://localhost:8501**

## 🎛️ Interface do Dashboard

### 📊 Painel Principal
- **Status do Sistema**: Conexão MT5, status do engine, análises
- **Métricas da Conta**: Saldo, equity, margem, P&L
- **Seleção de Ativos**: Filtros por setor, configuração de pares
- **Controles**: Iniciar/parar sistema, configurações de risco

### 📈 Análise de Pares
- **Análise de Cointegração**: Teste automático de todos os pares
- **Distribuição Z-Score**: Visualização de sinais de entrada
- **Sinais de Trading**: Lista filtrada de oportunidades
- **Estatísticas**: Métricas detalhadas de performance

### 💼 Monitor de Posições
- **Posições Ativas**: Lista completa com P&L em tempo real
- **Gráficos P&L**: Evolução temporal dos resultados
- **Controles de Posição**: Ajuste de stops, break-even, fechamento

### ⚙️ Barra Lateral
- **Conexão MT5**: Credenciais e teste de conectividade
- **Filtros**: Seleção de ativos por setor
- **Parâmetros**: Z-Score, R², Beta, volatilidade
- **Gestão de Risco**: Stop loss, take profit, posições máximas
- **Configurações**: Salvar/carregar perfis

## 🔧 Configuração Avançada

### 📱 Parâmetros Principais

| Parâmetro | Padrão | Descrição |
|-----------|---------|-----------|
| `zscore_threshold` | 2.0 | Limite para geração de sinais |
| `r2_min_threshold` | 0.50 | R² mínimo para cointegração |
| `beta_max_threshold` | 1.5 | Beta máximo permitido |
| `p_value_threshold` | 0.05 | P-value para cointegração |
| `max_positions` | 5 | Máximo de posições simultâneas |
| `risk_per_trade` | 2% | Risco por operação |
| `stop_loss_pct` | 5% | Stop loss padrão |
| `take_profit_pct` | 10% | Take profit padrão |

### 🎯 Filtros de Trading

**Filtros Estatísticos:**
- ✅ Teste de cointegração (Engle-Granger)
- ✅ Z-Score dentro dos limites configurados
- ✅ R² mínimo para correlação
- ✅ Beta máximo para exposição
- ✅ Filtro de volatilidade

**Filtros de Mercado:**
- ✅ Volume mínimo diário
- ✅ Spread máximo permitido
- ✅ Horário de funcionamento
- ✅ Liquidez suficiente

### 🔌 Integração MetaTrader 5

**Configuração MT5:**
1. Instalar MetaTrader 5
2. Configurar conta demo/real
3. Permitir trading automatizado
4. Inserir credenciais no dashboard

**Funcionalidades MT5:**
- ✅ Conexão automática
- ✅ Obtenção de dados históricos
- ✅ Execução de ordens
- ✅ Monitoramento de posições
- ✅ Cálculo de P&L em tempo real

## 📊 Análises Disponíveis

### 🔬 Análise Estatística
- **Cointegração**: Teste de Engle-Granger
- **Estacionariedade**: Teste ADF
- **Correlação**: Pearson e Spearman
- **Volatilidade**: GARCH(1,1)
- **Regressão**: Linear com bootstrap

### 📈 Sinais de Trading
- **Long Signal**: Z-Score < -threshold
- **Short Signal**: Z-Score > +threshold
- **Confiança**: Baseada em R² e volatilidade
- **Risk/Reward**: Cálculo automático
- **Timing**: Otimização de entrada

### 📋 Relatórios
- **Análise Completa**: JSON estruturado
- **Performance**: Métricas de retorno
- **Drawdown**: Análise de risco
- **Sharpe Ratio**: Retorno ajustado ao risco

## 🛡️ Gestão de Risco

### ⚠️ Controles Automáticos
- **Stop Loss**: Proteção contra perdas
- **Take Profit**: Realização de lucros
- **Position Sizing**: Tamanho baseado no risco
- **Max Positions**: Limite de exposição
- **Daily Loss Limit**: Proteção diária

### 📊 Monitoramento
- **P&L em Tempo Real**: Atualização contínua
- **Margin Level**: Controle de margem
- **Drawdown**: Acompanhamento de perdas
- **Alerts**: Notificações automáticas

## 🧪 Modo de Operação

### 🎮 Modo Simulação
- Dados simulados realistas
- Análise completa de cointegração
- Sinais de trading válidos
- Interface totalmente funcional
- Ideal para testes e aprendizado

### 💼 Modo Demo
- Conexão MT5 com conta demo
- Dados reais de mercado
- Ordens simuladas
- Ambiente seguro para testes
- Transição suave para produção

### 🚀 Modo Real
- Conexão MT5 com conta real
- Execução real de ordens
- Monitoramento ativo
- Gestão de risco rigorosa
- Ambiente de produção

## 🔄 Atualização e Manutenção

### 📦 Atualizações de Dependências
```bash
# Atualizar todas as dependências
pip install --upgrade -r requirements_dashboard_pro.txt

# Verificar compatibilidade
python test_integration.py
```

### 🧹 Limpeza de Dados
```bash
# Limpar logs antigos
rm *.log

# Limpar relatórios antigos
rm relatorio_*.json
```

### 🔧 Backup de Configurações
```bash
# Backup automático
cp trading_config.json backup_config_$(date +%Y%m%d).json
```

## 📞 Suporte e Troubleshooting

### ❓ Problemas Comuns

**Dashboard não inicia:**
```bash
# Verificar dependências
python test_integration.py

# Reinstalar Streamlit
pip uninstall streamlit
pip install streamlit
```

**MT5 não conecta:**
- Verificar se MT5 está instalado
- Confirmar credenciais de login
- Verificar se trading automático está habilitado
- Testar conexão de internet

**Análise não funciona:**
- Verificar seleção de ativos
- Confirmar parâmetros estatísticos
- Verificar dados históricos disponíveis

### 🐛 Logs e Debug
```bash
# Logs do sistema
tail -f trading_system.log

# Debug do Streamlit
streamlit run dashboard_trading_pro.py --logger.level debug
```

### 📧 Contato
- **Issues**: GitHub Issues
- **Documentação**: README files
- **Community**: Discord/Telegram

## 📚 Recursos Adicionais

### 📖 Documentação
- 📄 `README_DASHBOARD_PRO.md` - Guia detalhado
- 📄 `INSTRUCOES_INICIALIZACAO.md` - Setup inicial
- 📄 `GUIA_VERIFICACAO.md` - Verificações

### 🎓 Tutoriais
- Configuração inicial do sistema
- Análise de pares passo a passo
- Integração com MetaTrader 5
- Otimização de parâmetros
- Gestão de risco avançada

### 🔗 Links Úteis
- [Streamlit Docs](https://docs.streamlit.io/)
- [MetaTrader 5 API](https://www.mql5.com/en/docs/python_metatrader5)
- [Statsmodels](https://www.statsmodels.org/)
- [Plotly](https://plotly.com/python/)

---

## 🎉 Status do Projeto

| Componente | Status | Descrição |
|------------|--------|-----------|
| 🎨 Interface | ✅ Completo | Dashboard moderno e responsivo |
| 📊 Análises | ✅ Completo | Cointegração e estatísticas |
| 🤖 Sinais | ✅ Completo | Geração automática de sinais |
| 💼 Posições | ✅ Completo | Monitor em tempo real |
| 🔌 MT5 | ✅ Pronto | Integração completa disponível |
| 🛡️ Risco | ✅ Completo | Controles avançados |
| 📱 Mobile | ✅ Responsivo | Interface adaptável |
| 🧪 Testes | ✅ Completo | Suite de testes integrada |

### 🚀 Roadmap Futuro
- [ ] Alertas WhatsApp/Email
- [ ] Backtesting avançado
- [ ] Machine Learning integration
- [ ] API REST para terceiros
- [ ] Mobile app nativo
- [ ] Multi-broker support

---

**Trading System Pro v2.0** - Sistema Profissional de Trading Automatizado  
*Desenvolvido com ❤️ para traders profissionais*

⚠️ **Aviso Legal**: Trading envolve riscos. Use sempre contas demo antes de operar com dinheiro real.
