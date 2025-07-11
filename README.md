
# Trading Dashboard - Sistema de Trading Automatizado

## 📈 Descrição

Sistema completo de trading automatizado com dashboard interativo desenvolvido em Streamlit. O sistema monitora pares de moedas, executa análises técnicas e gerencia operações de trading em tempo real.

## 🚀 Funcionalidades

- **Dashboard Interativo**: Interface web com múltiplas abas para monitoramento
- **Análise Técnica Automatizada**: Cálculo de indicadores e sinais de trading
- **Monitoramento de Pares**: Validação e filtro de oportunidades de trading
- **Sistema de Logs**: Monitoramento detalhado de operações e decisões
- **Integração MetaTrader5**: Execução automática de ordens (local)
- **Gestão de Risco**: Controle de exposição e gerenciamento de capital
- **Parâmetros Dinâmicos**: Sistema centralizado e flexível de configuração

## 🛠️ Tecnologias Utilizadas

- **Frontend**: Streamlit
- **Backend**: Python 3.11+
- **Trading**: MetaTrader5 (desenvolvimento local)
- **Análise**: pandas, numpy, plotly
- **Deploy**: Streamlit Community Cloud

## 🌐 Acesso Online

**Dashboard disponível em**: [Link do seu deploy será exibido aqui após configuração]

## 📋 Estrutura Principal
- **calculo_entradas_v55.py**: Módulo de cálculo e lógica de trading. Parâmetros críticos centralizados em `parametros_dinamicos`.
- **dashboard_trading_pro_real.py**: Dashboard interativo para operação real, monitoramento e controle. Busca parâmetros de forma dinâmica.
- **sistema_integrado.py**: Backend integrado para execução, threading e sincronização de parâmetros.
- **app.py**: Arquivo principal para deploy no Streamlit Cloud

## 🔧 Instalação Local

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/trading-dashboard.git
cd trading-dashboard

# Instale as dependências
pip install -r requirements.txt

# Execute o dashboard
streamlit run app.py
```

## 🌐 Deploy no Streamlit Cloud

### Passo a Passo Completo:

1. **Preparar Repositório GitHub**:
   - Fork este repositório ou crie um novo
   - Faça upload de todos os arquivos do projeto
   - Certifique-se que `app.py` está na raiz

2. **Acessar Streamlit Cloud**:
   - Vá para [share.streamlit.io](https://share.streamlit.io)
   - Faça login com sua conta GitHub
   - Clique em "New app"

3. **Configurar Deploy**:
   - Repository: Selecione seu repositório
   - Branch: main (ou master)
   - Main file path: `app.py`
   - App URL: Escolha um nome único

4. **Deploy Automático**:
   - Clique em "Deploy!"
   - Aguarde o processo de instalação
   - Seu dashboard estará online em poucos minutos

## 📊 Arquivos de Deploy Criados

Todos os arquivos necessários para o deploy foram criados:

- ✅ `app.py` - Arquivo principal do Streamlit
- ✅ `requirements.txt` - Dependências otimizadas para cloud
- ✅ `.streamlit/config.toml` - Configurações do Streamlit
- ✅ `.gitignore` - Arquivos a serem ignorados no Git
- ✅ `README.md` - Documentação completa

## 🔑 Configuração

### Para Deploy no Streamlit Cloud

O sistema está configurado para funcionar no Streamlit Cloud com funcionalidades de demonstração. MetaTrader5 funciona apenas localmente.

### Configuração Local (Desenvolvimento)

Para desenvolvimento local com MT5:

```python
# config_real.py
ACCOUNT_CONFIG = {
    "account": "sua_conta",
    "password": "sua_senha", 
    "server": "seu_servidor"
}
```

## 📈 Como Usar

1. **Acesse o Dashboard**: Via link do Streamlit Cloud ou localmente
2. **Navegue pelas Abas**:
   - **Sinais**: Visualize oportunidades de trading
   - **Monitoramento**: Acompanhe análises em tempo real
   - **Configurações**: Ajuste parâmetros do sistema

3. **Modo Demo**: No Streamlit Cloud, funciona com dados simulados
4. **Monitore Logs**: Acompanhe as decisões do sistema em tempo real

## 🔧 Parâmetros Dinâmicos

Sistema centralizado de configuração sem hardcoding:
- **Período de Análise**: Timeframes configuráveis
- **Critérios de Entrada**: Z-Score, correlações, volatilidade
- **Gestão de Risco**: Stop loss, take profit, tamanho de posição
- **Filtros de Mercado**: Horários, pares permitidos, condições

## 📊 Indicadores Utilizados

- Z-Score para detecção de anomalias
- Correlações entre pares
- Médias móveis e tendências
- Volatilidade e volume
- Beta rotation para rotação setorial
- Sistema de logs detalhado para validação de pares

## 🚀 Próximos Passos para Deploy

1. **Criar Repositório GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Trading Dashboard"
   git branch -M main
   git remote add origin https://github.com/seu-usuario/trading-dashboard.git
   git push -u origin main
   ```

2. **Deploy no Streamlit Cloud**:
   - Acesse share.streamlit.io
   - Conecte com GitHub
   - Selecione o repositório
   - Configure app.py como arquivo principal
   - Deploy automático

3. **Teste e Validação**:
   - Verifique se todas as funcionalidades funcionam online
   - Teste navegação entre abas
   - Valide logs e validações de pares

## 🐛 Troubleshooting

### Problemas Comuns no Deploy

1. **Erro de Dependências**: 
   - Verificar `requirements.txt`
   - Remover pacotes incompatíveis (MT5)

2. **Erro de Imports**:
   - Verificar estrutura de arquivos
   - Confirmar que `app.py` está na raiz

3. **Dados Não Carregam**:
   - Verificar conexão de internet
   - Modo demo para cloud

### Logs e Depuração

O sistema gera logs detalhados sobre:
- Decisões de validação de pares com motivos específicos
- Critérios de entrada/saída
- Análises técnicas realizadas
- Performance das estratégias

## ⚠️ Disclaimer

Este sistema é para fins educacionais e de pesquisa. Trading envolve riscos significativos. Use por sua conta e risco. A versão online é apenas demonstrativa.

---

**Sistema pronto para deploy no GitHub + Streamlit Cloud** 🚀
- Números mágicos não críticos (apenas para documentação)

**Recomenda-se rodar este teste antes de qualquer release.**

### Como rodar o teste

```bash
python test_no_hardcoding.py
```

## Automatização da checagem em CI
A checagem de hardcoding pode ser automatizada em pipelines de integração contínua (CI), como GitHub Actions, GitLab CI, Azure DevOps, etc. Assim, toda vez que alguém faz um push ou abre um pull request, o teste é executado automaticamente e bloqueia merges caso algum hardcoding crítico seja detectado.

**Vantagens:**
- Garante que o padrão de centralização de parâmetros nunca será quebrado.
- Facilita auditoria e rastreabilidade.
- Evita regressões e erros humanos.

**Exemplo de passo em CI (GitHub Actions):**
```yaml
- name: Checagem de Hardcoding
  run: python test_no_hardcoding.py
```

## Requisitos
- Python 3.8+
- Streamlit
- MetaTrader5
- Outras dependências listadas nos scripts

## Recomendações
- Sempre documente números mágicos não críticos no código.
- Nunca faça hardcoding de parâmetros de negócio.
- Rode o teste automatizado antes de releases.
- Considere integrar a checagem ao seu pipeline de CI.

---

**Dúvidas ou sugestões:** abra uma issue ou entre em contato com o mantenedor do projeto.

---

## Glossário

### Push
"Push" é o ato de enviar (subir) suas alterações locais de código para um repositório remoto (por exemplo, no GitHub). Isso torna suas mudanças visíveis para outros colaboradores do projeto.

### Pull Request (PR)
"Pull Request" (ou PR) é uma solicitação para que suas alterações (geralmente já enviadas via push) sejam revisadas e, se aprovadas, integradas ao ramo principal (main/master) do projeto. O PR permite revisão de código, discussões e integração controlada das contribuições.

---

### 1. **Multithreading ou Processamento Assíncrono**
Utilize multithreading ou processamento assíncrono para separar as tarefas de extração/análise de dados e monitoramento. Isso permite que ambas as operações sejam executadas simultaneamente, sem que uma bloqueie a outra.

- **Multithreading**: Crie uma thread separada para a extração e análise de dados. A thread principal pode ser responsável pelo monitoramento.
- **Assíncrono**: Se você estiver usando uma linguagem que suporte programação assíncrona (como Python com `asyncio`), você pode fazer as chamadas de extração de dados de forma assíncrona.

### 2. **Divisão de Tarefas**
Divida as tarefas em partes menores e execute-as em intervalos regulares. Por exemplo, em vez de realizar uma análise completa de dados a cada execução, você pode realizar uma análise incremental ou em lotes.

### 3. **Cache de Resultados**
Implemente um sistema de cache para armazenar os resultados da análise de dados. Isso pode reduzir o tempo de espera, pois você pode usar resultados anteriores em vez de recalcular tudo a cada execução.

### 4. **Prioridade de Tarefas**
Defina prioridades para as tarefas. O monitoramento de lucros e operações abertas pode ter uma prioridade mais alta em relação à extração e análise de dados. Assim, você pode garantir que o monitoramento seja executado com mais frequência ou em primeiro lugar.

### 5. **Otimização de Código**
Revise o código responsável pela extração e análise de dados para identificar possíveis gargalos de desempenho. Otimize consultas a bancos de dados, reduza a complexidade algorítmica e elimine operações desnecessárias.

### 6. **Uso de Filas**
Implemente um sistema de filas para gerenciar as tarefas. O monitoramento pode colocar suas solicitações em uma fila, enquanto a extração e análise de dados processam suas tarefas em segundo plano.

### 7. **Monitoramento em Tempo Real**
Se possível, implemente um sistema de monitoramento em tempo real que atualize os dados conforme eles são recebidos, em vez de esperar pela conclusão da análise.

### 8. **Ajuste de Frequência**
Ajuste a frequência com que as análises são realizadas. Se a análise não precisa ser feita em tempo real, você pode programar para que ela ocorra em intervalos maiores, permitindo que o monitoramento tenha mais recursos.

### Exemplo de Implementação em Python (Assíncrono)
Abaixo, um exemplo simples usando `asyncio`:

```python
import asyncio

async def extrair_e_analisar_dados():
    while True:
        # Simula a extração e análise de dados
        print("Extraindo e analisando dados...")
        await asyncio.sleep(5)  # Simula um atraso de 5 segundos

async def monitorar_operacoes():
    while True:
        # Simula o monitoramento de operações
        print("Monitorando operações abertas...")
        await asyncio.sleep(1)  # Verifica a cada 1 segundo

async def main():
    await asyncio.gather(
        extrair_e_analisar_dados(),
        monitorar_operacoes()
    )

# Executa o loop principal
asyncio.run(main())
```

### Conclusão
Escolha a abordagem que melhor se adapta ao seu contexto e à sua aplicação. A implementação de uma ou mais dessas estratégias deve ajudar a melhorar a eficiência e a responsividade do seu sistema.