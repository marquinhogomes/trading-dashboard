@echo off
chcp 65001 >nul
title 🚀 Dashboard Trading Pro v2.0

echo.
echo ==========================================
echo   🚀 DASHBOARD TRADING PRO v2.0
echo   🧵 Sistema com Threading Avançado
echo ==========================================
echo.

cd /d "%~dp0"

REM Verificação rápida e início
python -c "from dashboard_trading_pro_real import TradingSystemReal; print('✅ Sistema carregado')" 2>nul && (
    echo 🚀 Iniciando dashboard otimizado...
    echo 📊 Abrindo em: http://localhost:8501
    echo.
    streamlit run dashboard_trading_pro_real.py --server.port 8501 --browser.gatherUsageStats false
) || (
    echo ❌ Erro no sistema. Executando verificação...
    python verificar_dashboard.py
    pause
)

echo.
echo 🏁 Dashboard finalizado.
pause
