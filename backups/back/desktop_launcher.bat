@echo off
chcp 65001 >nul
title 🚀 Trading Dashboard - Desktop Launcher

REM Vai para o diretório do dashboard
cd /d "c:\Users\marqu\OneDrive\leag_o1_omni\leag_o1_omni-folder"

echo.
echo 🚀 DASHBOARD TRADING PRO v2.0
echo 🧵 Iniciando sistema com threading...
echo.

REM Verifica se está no diretório correto
if not exist "dashboard_trading_pro_real.py" (
    echo ❌ Dashboard não encontrado neste local!
    echo 💡 Ajuste o caminho no arquivo desktop_launcher.bat
    pause
    exit /b 1
)

echo ✅ Dashboard localizado
echo 🔍 Verificando sistema...

REM Teste rápido
python -c "import streamlit; print('✅ Streamlit OK')" 2>nul || (
    echo 📦 Instalando Streamlit...
    python -m pip install streamlit
)

echo 🚀 Iniciando...
echo 📊 URL: http://localhost:8501

timeout /t 2 /nobreak >nul

REM Inicia o dashboard
streamlit run dashboard_trading_pro_real.py --server.port 8501 --browser.gatherUsageStats false

pause
