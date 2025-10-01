"""
Script para testar a API com casos de teste
Uso: python test_api.py
"""
import requests
import json
import time
from datetime import datetime

API_BASE_URL = "http://localhost:8000"

# Caso de teste 1 - Timon Real
CASO_TESTE_1 = {
    "municipio": "TIMON",
    "periodo_inicio": "2000-01-01",
    "periodo_fim": "2006-12-01",
    "ajuizamento": "2005-05-01",
    "citacao": "2006-06-01",
    "honorarios_perc": 0.0,
    "honorarios_fixo": 0.0,
    "desagio_principal": 0.2,
    "desagio_honorarios": 0.2,
    "correcao_ate": "2025-01-01"
}


def testar_health_check():
    """Testa endpoint de health check"""
    print("\n🔍 Testando Health Check...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        response.raise_for_status()
        data = response.json()
        print(f"✅ API Online - Status: {data['status']}")
        print(f"   Versão: {data['version']}")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def testar_calculo(caso_teste, nome_caso="Teste"):
    """Testa endpoint de cálculo"""
    print(f"\n🧮 Testando Cálculo - {nome_caso}")
    print(f"   Município: {caso_teste['municipio']}")
    print(f"   Período: {caso_teste['periodo_inicio']} a {caso_teste['periodo_fim']}")
    
    try:
        inicio = time.time()
        
        response = requests.post(
            f"{API_BASE_URL}/api/calcular",
            json=caso_teste,
            timeout=120
        )
        
        tempo_decorrido = time.time() - inicio
        
        response.raise_for_status()
        resultado = response.json()
        
        print(f"✅ Cálculo concluído em {tempo_decorrido:.2f}s")
        print(f"   Run ID: {resultado['run_id']}")
        print(f"   Tempo de execução: {resultado['execution_time_ms']}ms")
        print(f"\n📊 Resultados:")
        
        # Exibir alguns cenários
        cenarios_exibir = ['nt7_ipca_selic', 'nt7_periodo_cnj', 'nt7_tr']
        
        for cenario_key in cenarios_exibir:
            if cenario_key in resultado['outputs']:
                cenario = resultado['outputs'][cenario_key]
                print(f"\n   {cenario_key.upper()}:")
                print(f"   • Principal: R$ {cenario['principal']:,.2f}")
                print(f"   • Honorários: R$ {cenario['honorarios']:,.2f}")
                print(f"   • Total: R$ {cenario['total']:,.2f}")
        
        # Salvar resultado completo
        nome_arquivo = f"resultado_{resultado['run_id'][:8]}.json"
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Resultado completo salvo em: {nome_arquivo}")
        
        return resultado
        
    except requests.exceptions.Timeout:
        print(f"❌ Timeout após 120 segundos")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"❌ Erro HTTP {e.response.status_code}:")
        try:
            error_data = e.response.json()
            print(f"   {error_data.get('detail', str(e))}")
        except:
            print(f"   {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None


def testar_rate_limit():
    """Testa rate limiting"""
    print("\n⏱️  Testando Rate Limiting (10 req/min)...")
    
    sucesso = 0
    bloqueado = 0
    
    for i in range(12):
        try:
            response = requests.get(f"{API_BASE_URL}/")
            if response.status_code == 200:
                sucesso += 1
            elif response.status_code == 429:
                bloqueado += 1
                print(f"   Requisição {i+1}: Bloqueada (429)")
        except Exception as e:
            print(f"   Requisição {i+1}: Erro - {e}")
    
    print(f"\n   Sucesso: {sucesso}/12")
    print(f"   Bloqueadas: {bloqueado}/12")
    
    if bloqueado >= 2:
        print("✅ Rate limiting funcionando")
    else:
        print("⚠️  Rate limiting pode não estar funcionando corretamente")


def menu_interativo():
    """Menu interativo para testes"""
    print("\n" + "="*60)
    print("🧪 TESTE DA API - CALCULADORA TRABALHISTA")
    print("="*60)
    
    while True:
        print("\n📋 Opções:")
        print("1. Health Check")
        print("2. Testar Cálculo (Caso Timon)")
        print("3. Testar Rate Limiting")
        print("4. Executar Todos os Testes")
        print("5. Sair")
        
        opcao = input("\nEscolha uma opção (1-5): ").strip()
        
        if opcao == "1":
            testar_health_check()
        elif opcao == "2":
            testar_calculo(CASO_TESTE_1, "Timon Real")
        elif opcao == "3":
            testar_rate_limit()
        elif opcao == "4":
            print("\n🚀 Executando todos os testes...\n")
            if testar_health_check():
                testar_calculo(CASO_TESTE_1, "Timon Real")
                testar_rate_limit()
        elif opcao == "5":
            print("\n👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")


if __name__ == "__main__":
    # Verificar se API está online
    print("\n🔌 Verificando conexão com API...")
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ API está online!")
            menu_interativo()
        else:
            print("❌ API retornou status inesperado")
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar à API")
        print(f"   Verifique se a API está rodando em {API_BASE_URL}")
        print("\n   Para iniciar a API, execute:")
        print("   python main.py")
    except Exception as e:
        print(f"❌ Erro: {e}")
