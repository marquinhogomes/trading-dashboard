@echo off
echo.
echo ==========================================
echo   📦 INSTALADOR - DASHBOARD TRADING PRO
echo   Instalação de Dependências
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

echo 🔧 Atualizando pip...
python -m pip install --upgrade pip
echo.

echo 📦 Instalando dependências ESSENCIAIS (1/3)...
echo Instalando: streamlit, plotly, pandas, numpy...
python -m pip install streamlit>=1.28.0 plotly>=5.15.0 pandas>=2.0.0 numpy>=1.24.0
echo.

echo 📦 Instalando dependências de TRADING (2/3)...
echo Instalando: MetaTrader5, pytz, openpyxl...
python -m pip install MetaTrader5>=5.0.45 pytz>=2023.3 openpyxl>=3.1.2
echo.

echo 📦 Instalando dependências COMPLEMENTARES (3/3)...
echo Instalando: scipy, statsmodels, matplotlib, scikit-learn...
python -m pip install scipy>=1.10.0 statsmodels>=0.14.0 matplotlib>=3.7.1 scikit-learn>=1.3.0
echo.

echo 📦 Instalando dependências EXTRAS...
echo Instalando: seaborn, requests, colorama...
python -m pip install seaborn>=0.12.2 requests>=2.31.0 colorama>=0.4.6 python-dateutil>=2.8.2 typing-extensions>=4.7.1
echo.

echo 🔍 Verificando instalações...
echo.

python -c "import streamlit; print('✅ Streamlit:', streamlit.__version__)" 2>nul || echo "❌ Streamlit FALHOU"
python -c "import plotly; print('✅ Plotly:', plotly.__version__)" 2>nul || echo "❌ Plotly FALHOU"
python -c "import pandas; print('✅ Pandas:', pandas.__version__)" 2>nul || echo "❌ Pandas FALHOU"
python -c "import numpy; print('✅ NumPy:', numpy.__version__)" 2>nul || echo "❌ NumPy FALHOU"
python -c "import MetaTrader5; print('✅ MetaTrader5: OK')" 2>nul || echo "❌ MetaTrader5 FALHOU"
python -c "import openpyxl; print('✅ OpenPyXL: OK')" 2>nul || echo "❌ OpenPyXL FALHOU"

echo.
echo ==========================================
echo   ✅ INSTALAÇÃO CONCLUÍDA!
echo ==========================================
echo.
echo 🚀 Para executar o dashboard:
echo    1. Execute: EXECUTAR_DASHBOARD.bat
echo    2. Ou digite: streamlit run dashboard_trading_pro_real.py
echo.
echo 💡 Se houver problemas:
echo    1. Reinstale Python 3.8+
echo    2. Execute este instalador novamente
echo    3. Verifique se o MetaTrader 5 está instalado
echo.

pause
