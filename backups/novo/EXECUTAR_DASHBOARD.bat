@echo off
echo.
echo ==========================================
echo   🏆 DASHBOARD TRADING PROFESSIONAL
echo   Sistema Completo de Trading MT5 Real
echo ==========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale Python 3.8+ primeiro.
    echo 💡 Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python encontrado!
python --version
echo.

REM Verifica se o dashboard existe
if not exist "dashboard_trading_pro_real.py" (
    echo ❌ Arquivo dashboard_trading_pro_real.py não encontrado!
    echo 💡 Certifique-se de estar no diretório correto.
    pause
    exit /b 1
)

echo ✅ Dashboard encontrado!
echo.

REM Instala dependências se necessário
if exist "requirements_dashboard.txt" (
    echo 📦 Instalando/verificando dependências essenciais...
    echo Este processo pode demorar alguns minutos...
    echo.
    
    REM Atualiza pip primeiro
    python -m pip install --upgrade pip
    
    REM Instala dependências básicas primeiro
    python -m pip install streamlit plotly pandas numpy MetaTrader5 openpyxl
    
    echo.
    echo 📦 Instalando dependências restantes...
    python -m pip install -r requirements_dashboard.txt
    echo.
) else (
    echo ⚠️  Arquivo requirements_dashboard.txt não encontrado!
    echo 📦 Instalando dependências básicas...
    python -m pip install streamlit plotly pandas numpy MetaTrader5 openpyxl
)

REM Configura codepage para UTF-8
chcp 65001 >nul

echo.
echo � Verificando instalação do Streamlit...
python -c "import streamlit; print('✅ Streamlit OK')" 2>nul
if errorlevel 1 (
    echo ❌ Erro no Streamlit! Tentando reinstalar...
    python -m pip install --upgrade streamlit
)

echo.
echo 🔍 Verificando sistema...
python verificar_dashboard.py
if errorlevel 1 (
    echo ❌ Problemas detectados no sistema!
    pause
    exit /b 1
)

echo.
echo 🚀 Iniciando Dashboard Trading Professional...
echo.
echo 📊 Dashboard será aberto automaticamente no navegador
echo 🌐 URL: http://localhost:8501
echo 🛑 Para parar: Pressione Ctrl+C nesta janela
echo.
echo ⏳ Aguarde alguns segundos para o dashboard carregar...
echo.

REM Inicia o Streamlit com configurações otimizadas
streamlit run dashboard_trading_pro_real.py --server.port 8501 --server.address localhost --browser.gatherUsageStats false --server.headless false

echo.
echo 🏁 Dashboard finalizado.
echo.
pause
