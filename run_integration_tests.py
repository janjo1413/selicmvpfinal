"""
Script para rodar testes de integração com o servidor já rodando
Execute com: python run_integration_tests.py
"""
import subprocess
import sys
import time
import requests

def check_server():
    """Verifica se servidor está rodando"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("="*70)
    print("🧪 TESTES DE INTEGRAÇÃO - Excel vs Site")
    print("="*70)
    print()
    
    # Verificar se servidor está rodando
    print("🔍 Verificando servidor...")
    if not check_server():
        print("❌ ERRO: Servidor não está rodando!")
        print()
        print("Por favor, inicie o servidor em outro terminal:")
        print("  python app.py")
        print()
        return 1
    
    print("✅ Servidor está rodando em http://localhost:8000")
    print()
    print("⏳ Aguarde... os testes podem demorar ~2-3 minutos")
    print()
    
    # Rodar pytest
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/test_integracao_excel_vs_site.py",
        "-v", "-s",
        "--log-cli-level=INFO",
        "--tb=short"
    ]
    
    result = subprocess.run(cmd)
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
