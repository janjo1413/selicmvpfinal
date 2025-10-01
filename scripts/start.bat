@echo offREM Verificar se planilha existREM Verificar se venv existe (naecho.
echo Acesse: http://localhost:8000
echo.

REM Voltar para raiz e executar app.py
cd ..
python app.py

pauseif not exist "..\venv" (
    echo [INFO] Criando ambiente virtual...
    cd ..
    python -m venv venv
    cd scripts
)

REM Ativar venv
echo [INFO] Ativando ambiente virtual...
call ..\venv\Scripts\activate.bat

REM Instalar dependencias (requirements na raiz)
echo [INFO] Instalando dependencias...
pip install -q -r ..\requirements.txtlativo da raiz)
if not exist "..\data\timon_01-2025.xlsx" (
    echo [ERRO] Arquivo Excel nao encontrado em data\!
    echo.
    echo Certifique-se de que 'timon_01-2025.xlsx' esta na pasta data\.
    echo.
    pause
    exit /b 1
)

echo [OK] Planilha Excel encontrada! de inicialização para Windows CMD
REM Uso: start.bat

echo.
echo ========================================
echo   Calculadora Trabalhista - MVP
echo ========================================
echo.

REM Verificar se planilha existe
if not exist "USADA -  Timon 01-2025 VERIFICAÃ_Ã_O.xlsx" (
    echo [ERRO] Arquivo Excel nao encontrado!
    echo.
    echo Certifique-se de que a planilha esta na pasta do projeto.
    echo.
    pause
    exit /b 1
)

echo [OK] Planilha Excel encontrada!
echo.

REM Verificar se .env existe (na raiz)
if not exist "..\.env" (
    echo [INFO] Criando arquivo .env...
    copy "..\.env.example" "..\.env"
    echo [OK] Arquivo .env criado!
    echo.
)

REM Verificar se venv existe
if not exist "venv" (
    echo [INFO] Criando ambiente virtual...
    python -m venv venv
)

REM Ativar venv
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instalar dependências
echo [INFO] Instalando dependencias...
pip install -q -r requirements.txt

echo.
echo [OK] Ambiente configurado!
echo.
echo [INFO] Iniciando servidor...
echo.
echo Acesse: http://localhost:8000
echo.

REM Executar aplicação
python main.py

pause
