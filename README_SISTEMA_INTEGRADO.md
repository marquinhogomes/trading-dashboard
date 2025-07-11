# 🎯 SISTEMA DE TRADING INTEGRADO - GUIA RÁPIDO

## 🚀 COMO EXECUTAR

### Método 1: Launcher Automático (Recomendado)
```bash
python launcher_sistema_integrado.py
```

### Método 2: Execução Direta
```bash
streamlit run dashboard_trading_integrado.py
```

## 📋 PRÉ-REQUISITOS

- ✅ Python 3.7+
- ✅ MetaTrader 5 instalado
- ✅ Dependências: `streamlit`, `MetaTrader5`, `pandas`, `numpy`, `plotly`

## 🎯 FUNCIONALIDADES

### 🔄 Sistema Multithreaded
- **Thread Principal**: Monitoramento em tempo real
- **Thread Break-Even**: Ajuste automático de SL
- **Thread Programada**: Fechamento após 15:20h
- **Thread Controle**: Gestão de posições

### 📊 Dashboard Integrado
- **Controle MT5**: Conexão e monitoramento
- **Visualizações**: Gráficos e métricas em tempo real
- **Logs**: Sistema de logging centralizado
- **Controles**: Botões para todas as operações

### ⚡ Operações Reais
- **Sem simulação**: Todas as operações são reais no MT5
- **Break-even**: Automático quando lucro >= 50% do TP
- **Fechamento**: Posições pendentes fechadas às 15:20h
- **Gestão de risco**: Monitoramento contínuo

## 🔧 ARQUIVOS PRINCIPAIS

- **`launcher_sistema_integrado.py`** - Launcher principal
- **`dashboard_trading_integrado.py`** - Interface do sistema
- **`sistema_integrado.py`** - Core multithreaded
- **`teste_dashboard_integrado.py`** - Teste de validação

## 📞 SUPORTE

Para detalhes técnicos completos, consulte:
- `RELATORIO_FINAL_SISTEMA_COMPLETO.md`
- `RELATORIO_INTEGRACAO_COMPLETA.md`

---

**🏆 SISTEMA 100% FUNCIONAL E TESTADO!**
