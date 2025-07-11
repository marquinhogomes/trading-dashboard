@echo off
chcp 65001 >nul
echo.
echo ==========================================
echo   🚀 DASHBOARD TRADING PRO - THREADING
echo   Sistema Otimizado com Threading Avançado
echo   Versão: 2.0 - Performance Maximizada
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
    python -m pip install streamlit plotly pandas numpy MetaTrader5 openpyxl statsmodels scipy pytz arch
    
    echo.
    echo 📦 Instalando dependências restantes...
    python -m pip install -r requirements_dashboard.txt
    echo.
) else (
    echo ⚠️  Arquivo requirements_dashboard.txt não encontrado!
    echo 📦 Instalando dependências básicas...
    python -m pip install streamlit plotly pandas numpy MetaTrader5 openpyxl statsmodels scipy pytz arch
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
echo 🔍 Verificando sistema otimizado...
python verificar_dashboard.py
if errorlevel 1 (
    echo ❌ Problemas detectados no sistema!
    echo 💡 Verifique os logs acima para mais detalhes
    pause
    exit /b 1
) else (
    echo ✅ Sistema verificado - Threading avançado funcionando!
)

echo.
echo 🚀 Iniciando Dashboard Trading Pro - Versão Threading...
echo.
echo 📊 Dashboard otimizado será aberto automaticamente no navegador
echo 🧵 Threading avançado: Sistema integrado carregado
echo 🌐 URL: http://localhost:8501
echo 🛑 Para parar: Pressione Ctrl+C nesta janela
echo.
echo ⚡ Sistema com threading para performance máxima
echo 📈 Monitoramento em tempo real ativado
echo 🔄 Break-even e ajustes automáticos funcionando
echo.
echo ⏳ Aguarde alguns segundos para o dashboard carregar...
echo.

REM ========================
REM Verifica se a porta 8501 está livre antes de iniciar o Streamlit
REM ========================
set PORTA_PADRAO=8501
set PORTA=%PORTA_PADRAO%

REM Tenta detectar se a porta está ocupada (Windows)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%PORTA% ^| findstr LISTENING') do set PID_OCUPADO=%%a

if defined PID_OCUPADO (
    echo ❌ A porta %PORTA% ja esta em uso pelo processo PID: %PID_OCUPADO%.
    echo.
    echo 💡 Feche o processo antigo para liberar a porta OU escolha uma porta alternativa.
    echo Para matar o processo manualmente, execute: taskkill /PID %PID_OCUPADO% /F
    echo.
    set /p PORTA="Digite uma porta alternativa (ex: 8502) ou pressione Enter para abortar: "
    if "%PORTA%"=="" (
        echo Operacao abortada pelo usuario.
        pause
        exit /b 1
    )
    REM Verifica novamente se a nova porta esta livre
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%PORTA% ^| findstr LISTENING') do set PID_OCUPADO2=%%a
    if defined PID_OCUPADO2 (
        echo ❌ A porta %PORTA% tambem esta ocupada. Tente outra porta.
        pause
        exit /b 1
    )
)

echo.
echo 🚀 Iniciando Dashboard Trading Pro na porta %PORTA%...
echo.
streamlit run dashboard_trading_pro_real.py --server.port %PORTA% --server.address localhost --browser.gatherUsageStats false --server.headless false --runner.magicEnabled false

echo.
echo 🏁 Dashboard Threading Pro finalizado.
echo 📈 Obrigado por usar o sistema otimizado!
echo.
pause
