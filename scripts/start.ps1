# Script de inicialização para Windows PowerShell
# Uso: .\start.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🚀 Calculadora Trabalhista - MVP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se planilha Excel existe
$excelFile = "USADA -  Timon 01-2025 VERIFICAÃ_Ã_O.xlsx"
if (-Not (Test-Path $excelFile)) {
    Write-Host "⚠️  Arquivo Excel não encontrado!" -ForegroundColor Yellow
    Write-Host "   Procurando: $excelFile" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Certifique-se de que a planilha está na pasta do projeto." -ForegroundColor Red
    Write-Host ""
    pause
    exit 1
}

Write-Host "✅ Planilha Excel encontrada!" -ForegroundColor Green
Write-Host ""

# Verificar se .env existe
if (-Not (Test-Path ".env")) {
    Write-Host "📝 Criando arquivo .env..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "   ✅ Arquivo .env criado!" -ForegroundColor Green
    Write-Host ""
}

# Verificar se venv existe
if (-Not (Test-Path "venv")) {
    Write-Host "📦 Criando ambiente virtual..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "   ✅ Ambiente virtual criado!" -ForegroundColor Green
    Write-Host ""
}

# Ativar venv
Write-Host "🔧 Ativando ambiente virtual..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Instalar dependências
Write-Host "📥 Instalando dependências..." -ForegroundColor Yellow
pip install -q -r requirements.txt

Write-Host ""
Write-Host "✅ Tudo pronto!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Iniciando servidor na porta 8000..." -ForegroundColor Cyan
Write-Host ""
Write-Host "   Acesse: http://localhost:8000" -ForegroundColor Green
Write-Host ""
Write-Host "   Pressione Ctrl+C para parar" -ForegroundColor Yellow
Write-Host ""

# Executar aplicação
python main.py
