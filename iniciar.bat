@echo off
title Calculadora Trabalhista SELIC - MVP v1.2.0
color 0A

echo ========================================
echo   CALCULADORA TRABALHISTA SELIC MVP
echo   Versao: 1.2.0
echo ========================================
echo.
echo [*] Iniciando servidor FastAPI...
echo [*] Acesse: http://localhost:8000
echo.
echo Pressione CTRL+C para encerrar
echo ========================================
echo.

REM Inicia o servidor uvicorn
python -m uvicorn app:app --host 0.0.0.0 --port 8000

pause
