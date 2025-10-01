#!/bin/bash
# Script de inicialização para Linux/Mac
# Uso: ./start.sh

echo ""
echo "========================================"
echo "  🚀 Calculadora Trabalhista - MVP"
echo "========================================"
echo ""

# Verificar se .env existe
if [ ! -f ".env" ]; then
    echo "⚠️  Arquivo .env não encontrado!"
    echo ""
    echo "📝 Copiando .env.example para .env..."
    cp .env.example .env
    echo ""
    echo "Configure o arquivo .env com suas credenciais:"
    echo "  - CLIENT_ID"
    echo "  - CLIENT_SECRET"
    echo "  - TENANT_ID"
    echo "  - WORKBOOK_ID"
    echo ""
    echo "Depois execute novamente: ./start.sh"
    exit 1
fi

# Verificar se venv existe
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar venv
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install -q -r requirements.txt

echo ""
echo "✅ Ambiente configurado!"
echo ""
echo "🌐 Iniciando servidor..."
echo ""
echo "Acesse: http://localhost:8000"
echo ""

# Executar aplicação
python main.py
