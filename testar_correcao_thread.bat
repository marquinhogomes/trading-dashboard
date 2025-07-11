@echo off
echo ================================================================================
echo TESTE DO SISTEMA DE AUTO-RESTART - THREAD TRADING
echo ================================================================================
echo Data: %date% %time%
echo.

echo 🔧 Verificando sistema integrado...
python -c "from sistema_integrado import SistemaIntegrado; print('✅ Sistema integrado importado com sucesso')"

if %errorlevel% neq 0 (
    echo ❌ Erro ao importar sistema_integrado.py
    pause
    exit /b 1
)

echo.
echo 🧪 Executando teste de auto-restart...
echo ⏰ Este teste levará cerca de 2 minutos para demonstrar o auto-restart
echo.

python teste_auto_restart.py

echo.
echo ✅ Teste concluído!
echo.
echo 📋 RESUMO DA CORREÇÃO:
echo   - Thread Trading agora tem auto-restart automático
echo   - Sistema se recupera sozinho quando o código original falha  
echo   - Logs menos verbosos e mais informativos
echo   - Métricas de restart incluídas nos relatórios
echo.
pause
