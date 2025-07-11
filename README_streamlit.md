# 🚀 Sistema de Trading Profissional - Streamlit

Sistema completo de trading automatizado de pares de ações com interface web profissional, baseado em análise de cointegração, modelos ARIMA/GARCH e execução automatizada via MetaTrader 5.

## 📋 Funcionalidades Principais

### 🔍 Análise Avançada
- **Análise de Cointegração**: Identifica pares de ações com relação estatística estável
- **Modelos ARIMA/GARCH**: Previsão de preços e volatilidade
- **Z-Score Analysis**: Identificação precisa de oportunidades de entrada/saída
- **Beta Rolling**: Análise de correlação dinâmica entre ativos
- **Filtros de Qualidade**: Volume, spread, liquidez e capitalização

### 🎯 Trading Automatizado
- **Execução Automática**: Envio de ordens via MetaTrader 5
- **Gestão de Risco**: Stop-loss, take-profit e controle de exposição
- **Monitoramento Real-time**: Acompanhamento de posições e P&L
- **Alerts Inteligentes**: Notificações de sinais e eventos importantes

### 📊 Interface Profissional
- **Dashboard Completo**: Métricas, gráficos e indicadores em tempo real
- **Configuração Flexível**: Parâmetros personalizáveis para todas as estratégias
- **Logs Detalhados**: Rastreamento completo de operações e eventos
- **Visualizações Avançadas**: Gráficos interativos com Plotly

## 🛠️ Instalação

### Pré-requisitos
- Python 3.8 ou superior
- MetaTrader 5 instalado e configurado
- Conexão com broker compatível com MT5

### 1. Clone o repositório
```bash
git clone <repository_url>
cd trading-system-streamlit
```

### 2. Instale as dependências
```bash
pip install -r requirements_streamlit.txt
```

### 3. Configure o MetaTrader 5
1. Abra o MetaTrader 5
2. Faça login em sua conta
3. Habilite o trading automático (Ctrl+E)
4. Permita importação de DLLs nas configurações

## 🚀 Como Usar

### 1. Executar o Sistema
```bash
streamlit run trading_system_streamlit.py
```

### 2. Configurar Conexão
1. Acesse a aplicação no navegador (normalmente http://localhost:8501)
2. Na barra lateral, configure a conexão com o MT5
3. Insira suas credenciais (login, senha, servidor) ou deixe em branco para usar a conta ativa

### 3. Configurar Parâmetros
- **Timeframe**: Escolha o período de análise (M1 a D1)
- **Pares**: Selecione os ativos para análise
- **Z-Score**: Configure o limiar para sinais (padrão: 2.0)
- **Gestão de Risco**: Defina stop-loss, take-profit e exposição máxima

### 4. Iniciar Trading
1. Configure todos os parâmetros desejados
2. Clique em "Iniciar" na barra lateral
3. Monitor o dashboard para acompanhar resultados
4. Use "Parar" para interromper o sistema

## 📱 Interface do Usuário

### 🎯 Dashboard
- **Métricas Principais**: Saldo, trades, taxa de acerto, drawdown
- **Performance**: Curva de equity e estatísticas
- **Melhores/Piores Trades**: Análise de resultados

### 📊 Seleção de Pares
- **Lista Personalizável**: Adicione/remova pares
- **Filtros por Setor**: Organize por categoria
- **Validação Automática**: Verifica disponibilidade dos símbolos

### 📈 Análise
- **Resultados em Tempo Real**: Pares analisados, cointegração, sinais
- **Gráficos Interativos**: Distribuição de Z-Scores
- **Tabela de Sinais**: Oportunidades identificadas com confiança

### 💼 Monitoramento de Posições
- **Posições Ativas**: Status, P&L, Z-Score atual
- **Controles**: Fechar posições, configurar alertas
- **Histórico**: Evolução do P&L ao longo do tempo

### 📝 Logs do Sistema
- **Filtros Avançados**: Por nível, origem e período
- **Exportação**: Salve logs para análise externa
- **Tempo Real**: Atualizações automáticas

## ⚙️ Configurações Avançadas

### 📋 Arquivo config.py
Personalize configurações detalhadas:
- Parâmetros de conexão MT5
- Limites de risco e exposição
- Configurações de modelos
- Filtros de qualidade
- Notificações e alertas

### 🎨 Personalização Visual
- Temas e cores customizáveis
- Layout responsivo
- Gráficos interativos
- Métricas personalizáveis

### 🔔 Sistema de Alertas
Configure notificações para:
- Novos sinais de trading
- Execução de ordens
- Níveis de stop-loss/take-profit
- Problemas de conexão
- Limites de risco atingidos

## 📊 Estratégias Implementadas

### 🔗 Pairs Trading
- Identificação de pares cointegrados
- Cálculo de spread e normalização
- Sinais baseados em reversão à média
- Gestão dinâmica de posições

### 📈 Mean Reversion
- Z-Score como indicador principal
- Filtros de volatilidade
- Confirmação por múltiplos timeframes
- Exit strategies otimizadas

### 🛡️ Risk Management
- Position sizing baseado em volatilidade
- Correlação entre posições
- Drawdown máximo
- Stop-loss dinâmico

## 🔧 Troubleshooting

### Problemas de Conexão MT5
```python
# Verificar status da conexão
import MetaTrader5 as mt5
print(mt5.initialize())
print(mt5.account_info())
```

### Erro de Importação
```bash
# Reinstalar dependências
pip install --upgrade -r requirements_streamlit.txt
```

### Performance Lenta
- Reduza o número de pares analisados
- Aumente o intervalo de atualização
- Use timeframes maiores (H1, H4, D1)

### Logs de Debug
Habilite logs detalhados em `config.py`:
```python
LOGGING_CONFIG = {
    'level': 'DEBUG',
    # ...
}
```

## 📈 Métricas e KPIs

### Performance
- **Sharpe Ratio**: Retorno ajustado ao risco
- **Sortino Ratio**: Downside deviation
- **Maximum Drawdown**: Maior perda consecutiva
- **Win Rate**: Taxa de trades vencedores
- **Profit Factor**: Lucros / Prejuízos

### Operacionais
- **Average Trade**: Resultado médio por trade
- **Holding Period**: Tempo médio de posição
- **Turnover**: Frequência de negociação
- **Slippage**: Diferença entre preço esperado/executado

## 🔐 Segurança

### Proteção de Dados
- Credenciais criptografadas
- Logs de auditoria
- Session timeout
- Backup automático

### Controles de Risco
- Limites de exposição
- Validação de ordens
- Emergency stop
- Monitoramento contínuo

## 🤝 Contribuição

### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Abra um Pull Request

### Reportar Bugs
- Use a seção Issues do GitHub
- Inclua logs detalhados
- Descreva os passos para reproduzir
- Informe versões do Python e dependências

## 📞 Suporte

### Documentação
- Consulte este README
- Veja comentários no código
- Arquivo `config.py` com todas as opções

### Comunidade
- GitHub Issues para bugs
- Discussions para dúvidas
- Wiki para tutoriais avançados

## ⚠️ Disclaimer

**AVISO IMPORTANTE**: Este sistema é fornecido apenas para fins educacionais e de pesquisa. Trading automatizado envolve riscos significativos e pode resultar em perdas substanciais. Sempre:

- Teste em conta demo primeiro
- Use apenas capital que pode perder
- Monitore o sistema regularmente
- Entenda completamente os riscos
- Consulte um consultor financeiro se necessário

O uso deste sistema é de sua inteira responsabilidade. Os desenvolvedores não se responsabilizam por perdas financeiras.

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

**Desenvolvido para trading profissional** | **Version 1.0.0** | **2025**
