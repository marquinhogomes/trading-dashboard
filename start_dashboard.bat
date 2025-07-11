@echo off
chcp 65001 >nul
title Dashboard Trading Pro - Threading v2.0

REM Muda para o diretório do dashboard
cd /d "%~dp0"

echo.
echo ==========================================
echo   🚀 DASHBOARD TRADING PRO v2.0
echo   Sistema com Threading Avançado
echo ==========================================
echo.
echo 🔧 Preparando ambiente...

REM Verifica Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo.
    echo 💡 Instale Python 3.8+ primeiro:
    echo    https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

REM Instala dependências básicas rapidamente
echo 📦 Verificando dependências essenciais...
python -c "import streamlit, plotly, pandas, numpy, MetaTrader5" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Instalando dependências básicas...
    python -m pip install --quiet streamlit plotly pandas numpy MetaTrader5
)

echo ✅ Dependências OK
echo.

REM Verificação rápida do sistema
echo 🔍 Verificação rápida...
python -c "from dashboard_trading_pro_real import TradingSystemReal; print('✅ Sistema OK')" 2>nul
if errorlevel 1 (
    echo ❌ Problema no dashboard - executando verificação completa...
    python verificar_dashboard.py
    pause
    exit /b 1
)

echo ✅ Dashboard pronto
echo.

echo 🚀 INICIANDO SISTEMA OTIMIZADO...
echo.
echo 🧵 Threading avançado: ATIVADO
echo 📊 Interface web: http://localhost:8501
echo 🛑 Para parar: Feche esta janela ou Ctrl+C
echo.

REM Aguarda um pouco para o usuário ler
timeout /t 3 /nobreak >nul

REM Inicia o dashboard
streamlit run dashboard_trading_pro_real.py --server.port 8501 --browser.gatherUsageStats false

echo.
echo 🏁 Dashboard encerrado.
pause
