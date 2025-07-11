@echo off
echo Iniciando Trading System Pro Dashboard...
echo.

:: Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado. Instale Python primeiro.
    pause
    exit /b 1
)

:: Verificar se Streamlit esta instalado
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Instalando Streamlit...
    pip install streamlit
)

:: Verificar se outras dependencias estao instaladas
python -c "import pandas, numpy, plotly" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install pandas numpy plotly matplotlib seaborn statsmodels
)

echo Todas as dependencias estao instaladas!
echo.
echo Iniciando dashboard na porta 8501...
echo Acesse: http://localhost:8501
echo.
echo Para parar o dashboard, pressione Ctrl+C
echo.

:: Iniciar o dashboard
streamlit run dashboard_trading_pro.py --server.port 8501 --server.headless true

pause
