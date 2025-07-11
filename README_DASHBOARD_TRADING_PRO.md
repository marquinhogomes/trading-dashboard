# 🏆 Dashboard Trading Professional - MT5 Real Operations

## 📋 Visão Geral

Dashboard profissional completo para operações reais de trading algorítmico com MetaTrader 5. Sistema totalmente integrado baseado no `calculo_entradas_v55.py` com interface web moderna e funcionalidades avançadas.

## ✨ Características Principais

### 🎯 Interface Profissional
- **Design Moderno**: Interface limpa e responsiva com Streamlit
- **Tema Customizado**: Cores profissionais e layout otimizado
- **Navegação Intuitiva**: Tabs organizadas e sidebar configurável
- **Auto-refresh**: Atualização automática em tempo real

### 📊 Funcionalidades Completas

#### 🔌 Conexão MT5
- Login direto na interface (usuário, senha, servidor)
- Status de conexão em tempo real
- Validação automática de credenciais
- Reconexão automática em caso de falha

#### 📈 Monitoramento em Tempo Real
- **Equity Curve**: Gráfico de equity com histórico completo
- **Posições Abertas**: Tabela com P/L atualizado automaticamente
- **Sinais Ativos**: Lista de oportunidades detectadas pelo sistema
- **Métricas Avançadas**: Win Rate, Sharpe Ratio, Drawdown

#### ⚙️ Configurações Avançadas
- **Seleção de Ativos**: Multi-select com filtro por segmento
- **Parâmetros de Trading**: Timeframe, período, limiares
- **Filtros Personalizáveis**: Cointegração, R², Beta, Z-Score
- **Perfis Salvos**: Configurações persistentes

#### 📊 Visualizações Avançadas
- Curva de equity em tempo real
- Distribuição de lucros/prejuízos
- Gráficos interativos com Plotly
- Tabelas responsivas e filtráveis

#### 🎮 Controles Operacionais
- Iniciar/Parar sistema com um clique
- Fechamento manual de posições
- Ajustes de parâmetros em tempo real
- Reset completo do sistema

#### 📤 Exportação e Relatórios
- **Excel**: Relatório completo com múltiplas abas
- **PDF**: Relatórios formatados (em desenvolvimento)
- **Logs**: Exportação de eventos do sistema
- **Histórico**: Dados históricos de trades

## 🚀 Como Usar

### 1. Instalação
```bash
# Clone ou baixe os arquivos
# Instale as dependências
pip install -r requirements_dashboard.txt
```

### 2. Execução Rápida
```bash
# Use o launcher (recomendado)
python launcher_dashboard.py

# Ou execute diretamente
streamlit run dashboard_trading_pro_real.py
```

### 3. Configuração Inicial

1. **Abra o dashboard**: http://localhost:8501
2. **Configure MT5**: Insira login, senha e servidor na sidebar
3. **Conecte**: Clique em "🔗 Conectar"
4. **Selecione Ativos**: Escolha segmentos e ativos para monitorar
5. **Ajuste Parâmetros**: Configure timeframe, limiares e filtros
6. **Inicie Sistema**: Clique em "▶️ Iniciar Sistema"

## 📱 Interface do Dashboard

### 🎛️ Sidebar (Configurações)
```
⚙️ CONFIGURAÇÕES DO SISTEMA
├── 🔌 Conexão MT5
│   ├── Login, Senha, Servidor
│   └── Status de Conexão
├── 📊 Ativos Monitorados
│   ├── Filtro por Segmento
│   ├── Seleção Multi-Ativos
│   └── Opção "Selecionar Todos"
├── 🎯 Parâmetros de Trading
│   ├── Timeframe (1min a 1dia)
│   ├── Período de Análise
│   ├── Limiar Z-Score
│   ├── Máx. Posições
│   └── Filtros Avançados
└── 🎮 Controles
    ├── Iniciar/Parar Sistema
    ├── Salvar Perfil
    └── Reset Completo
```

### 📊 Painel Principal
```
🏆 HEADER PRINCIPAL
├── Status da Conexão
├── Última Atualização
└── Botões de Exportação

📈 CARTÕES DE STATUS
├── Pares Processados
├── Posições Abertas  
├── Equity Atual
├── Lucro/Prejuízo Diário
├── Win Rate
├── Sharpe Ratio
├── Drawdown Máximo
└── Saldo Inicial vs Atual

📋 TABS PRINCIPAIS
├── 📊 Gráficos e Análises
│   ├── Curva de Equity
│   └── Distribuição P/L
├── 📡 Sinais e Posições
│   ├── Tabela de Sinais
│   └── Posições Abertas
└── 📋 Histórico e Logs
    ├── Histórico de Trades
    └── Log de Eventos
```

## 🔧 Configurações Avançadas

### ⚙️ Parâmetros Principais

| Parâmetro | Descrição | Valores |
|-----------|-----------|---------|
| **Timeframe** | Intervalo de análise | 1min, 5min, 15min, 30min, 1h, 4h, 1d |
| **Período** | Janela de dados históricos | 50-300 períodos |
| **Z-Score** | Limiar para sinais | 0.5-3.0 |
| **Max Posições** | Limite de posições simultâneas | 1-20 |
| **R² Mínimo** | Qualidade mínima do modelo | 0.1-0.9 |

### 🎛️ Filtros Disponíveis

- **Cointegração**: Testa cointegração entre pares
- **R² Mínimo**: Filtra por qualidade do modelo
- **Beta Máximo**: Limita exposição ao mercado
- **Z-Score Range**: Define faixa de operação

## 📊 Métricas e Indicadores

### 📈 Métricas Financeiras
- **Equity**: Valor total da conta em tempo real
- **P/L Diário**: Lucro/prejuízo do dia atual
- **Drawdown**: Perda máxima desde o pico
- **Win Rate**: Percentual de trades lucrativos
- **Sharpe Ratio**: Relação risco/retorno

### 🎯 Métricas Operacionais  
- **Pares Processados**: Total de análises realizadas
- **Posições Abertas**: Número de operações ativas
- **Sinais Detectados**: Oportunidades identificadas
- **Taxa de Execução**: Sucesso nas ordens

## 📤 Exportação de Dados

### 📊 Relatório Excel
Arquivo completo com múltiplas abas:
- **Resumo**: Métricas gerais do sistema
- **Posições Abertas**: Detalhes das operações ativas
- **Sinais**: Lista de oportunidades detectadas
- **Equity Histórico**: Evolução da conta
- **Logs**: Eventos do sistema

### 📋 Funcionalidades de Export
- Download automático de arquivos
- Nomenclatura com timestamp
- Dados formatados e organizados
- Compatibilidade com Excel/LibreOffice

## 🛡️ Segurança e Validações

### 🔒 Segurança
- Senhas mascaradas na interface
- Validação de credenciais MT5
- Logs de segurança
- Timeout automático

### ✅ Validações
- Verificação de conexão contínua
- Validação de parâmetros
- Controle de limites de operação
- Monitoramento de erros

## 🐛 Troubleshooting

### ❌ Problemas Comuns

**Erro de Conexão MT5:**
```
❌ SOLUÇÃO:
1. Verifique se o MT5 está instalado
2. Confirme login, senha e servidor
3. Teste conexão manual no MT5
4. Verifique firewall/antivírus
```

**Dashboard não carrega:**
```
❌ SOLUÇÃO:
1. Execute: pip install -r requirements_dashboard.txt
2. Use Python 3.8+ 
3. Verifique porta 8501 livre
4. Execute launcher_dashboard.py
```

**Dados não atualizam:**
```
❌ SOLUÇÃO:
1. Verifique conexão MT5
2. Confirme se sistema está iniciado
3. Aguarde 1-2 ciclos de execução
4. Verifique logs de erro
```

## 🔄 Auto-Refresh e Performance

### ⚡ Otimizações
- Auto-refresh inteligente (apenas quando sistema ativo)
- Cache de dados para performance
- Limitação de logs (últimos 1000)
- Threading para não bloquear interface

### 🎛️ Configurações de Performance
- Intervalo de execução configurável
- Limite de posições simultâneas
- Filtros para reduzir processamento
- Logs rotativos automáticos

## 📋 Logs e Monitoramento

### 📝 Tipos de Log
- **INFO**: Operações normais
- **SUCCESS**: Operações bem-sucedidas  
- **WARNING**: Alertas importantes
- **ERROR**: Erros e falhas

### 🔍 Monitoramento
- Status de conexão em tempo real
- Heartbeat do sistema
- Métricas de performance
- Alertas automáticos

## 🎯 Roadmap / Melhorias Futuras

### 🚧 Em Desenvolvimento
- [ ] Relatórios PDF automáticos
- [ ] Alertas por email/WhatsApp
- [ ] Dashboard mobile responsivo
- [ ] Backtesting integrado
- [ ] API REST para integrações

### 💡 Funcionalidades Planejadas
- [ ] Multi-conta MT5
- [ ] Análise de sentimento
- [ ] Machine Learning avançado
- [ ] Gestão de carteira
- [ ] Análise de risco avançada

## 📞 Suporte

Para dúvidas, problemas ou sugestões:
1. Verifique este README
2. Consulte os logs do sistema
3. Teste com configurações padrão
4. Documente erros específicos

---

## 🏆 Características Técnicas

- **Framework**: Streamlit + Plotly
- **Trading**: MetaTrader 5 API
- **Análise**: Pandas, NumPy, SciPy
- **Machine Learning**: TensorFlow, Scikit-learn
- **Threading**: Execução assíncrona
- **Export**: Excel, PDF (em desenvolvimento)

---

**Dashboard Trading Professional** - Sistema completo e profissional para trading algorítmico real com MT5. Interface moderna, funcionalidades avançadas e monitoramento em tempo real.

🚀 **Comece agora**: `python launcher_dashboard.py`
