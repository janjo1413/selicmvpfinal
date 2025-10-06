"""
Script de Comparação Automática - Site vs Planilha
Executa cálculo e compara com valores esperados
"""

import requests
import json
from datetime import date

# Valores esperados da PLANILHA TIMON (com deságio 20%)
VALORES_ESPERADOS_TIMON = {
    "nt7_ipca_selic": 158570032.07,
    "nt7_periodo_cnj": 182188802.72,
    "nt6_ipca_selic": 195182330.06,
    "jasa_ipca_selic": 194285738.57,
    "nt7_tr": 109937284.97,
    "nt36_tr": 135988890.88,
    "nt7_ipca_e": 136226336.92,
    "nt36_ipca_e": 255795585.87,
    "nt36_ipca_e_1pct": 351225928.23,
}

# Valores esperados da PLANILHA FORTALEZA (com deságio 20%)
VALORES_ESPERADOS_FORTALEZA = {
    "nt7_ipca_selic": 1204809414.31,
    "nt7_periodo_cnj": 1384394741.52,
    "nt6_ipca_selic": 1510232527.50,
    "jasa_ipca_selic": 1502881002.96,
}

def comparar_valores(municipio, valores_site, valores_esperados, tolerancia=0.01):
    """
    Compara valores do site com valores esperados
    tolerancia: % máxima de diferença aceitável (0.01 = 0.01%)
    """
    print("=" * 80)
    print(f"📊 COMPARAÇÃO: {municipio}")
    print("=" * 80)
    print()
    
    diferencas = []
    passou = True
    
    for cenario, valor_esperado in valores_esperados.items():
        if cenario not in valores_site:
            print(f"❌ {cenario}: NÃO ENCONTRADO no site")
            passou = False
            continue
        
        valor_site = valores_site[cenario]['principal']
        diferenca = valor_site - valor_esperado
        percentual = abs(diferenca / valor_esperado * 100) if valor_esperado != 0 else 0
        
        status = "✅" if percentual < tolerancia else "❌"
        
        print(f"{status} {cenario}:")
        print(f"   Esperado:  R$ {valor_esperado:>20,.2f}")
        print(f"   Site:      R$ {valor_site:>20,.2f}")
        print(f"   Diferença: R$ {diferenca:>20,.2f} ({percentual:.4f}%)")
        print()
        
        if percentual >= tolerancia:
            passou = False
            diferencas.append((cenario, percentual))
    
    print("=" * 80)
    if passou:
        print("🎉 TODOS OS TESTES PASSARAM!")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM:")
        for cenario, perc in diferencas:
            print(f"   - {cenario}: {perc:.4f}% de diferença")
    print("=" * 80)
    
    return passou

def testar_municipio(municipio, valores_esperados):
    """Executa cálculo via API e compara"""
    print()
    print("🔄 Executando cálculo no servidor...")
    print(f"   Município: {municipio}")
    print()
    
    # Payload
    payload = {
        "municipio": municipio,
        "periodo_inicio": "2000-01-01",
        "periodo_fim": "2006-12-01",
        "ajuizamento": "2005-05-01",
        "citacao": "2006-06-01",
        "honorarios_perc": 10.0,
        "honorarios_fixo": 5000.0,
        "desagio_principal": 20.0,
        "desagio_honorarios": 20.0,
        "correcao_ate": "2025-01-01"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/calcular",
            json=payload,
            timeout=300  # 5 minutos
        )
        
        if response.status_code != 200:
            print(f"❌ Erro na API: {response.status_code}")
            print(response.text)
            return False
        
        resultado = response.json()
        
        print(f"✅ Cálculo concluído em {resultado['execution_time_ms']/1000:.1f}s")
        print()
        
        # Comparar
        passou = comparar_valores(municipio, resultado['outputs'], valores_esperados)
        
        # Mostrar arquivos gerados
        print()
        print(f"📁 Arquivos gerados:")
        print(f"   Excel: {resultado['excel_output_path']}")
        print(f"   CSV:   {resultado.get('csv_output_path', 'N/A')}")
        
        return passou
        
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT: Cálculo demorou mais de 5 minutos")
        return False
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

if __name__ == "__main__":
    print("=" * 80)
    print("🧪 TESTE AUTOMÁTICO: Site vs Planilha")
    print("=" * 80)
    
    # Teste 1: TIMON
    print("\n" + "🏛️ " * 20)
    passou_timon = testar_municipio("TIMON", VALORES_ESPERADOS_TIMON)
    
    # Teste 2: FORTALEZA
    print("\n" + "🏛️ " * 20)
    passou_fortaleza = testar_municipio("FORTALEZA", VALORES_ESPERADOS_FORTALEZA)
    
    # Resumo final
    print()
    print("=" * 80)
    print("📊 RESUMO FINAL")
    print("=" * 80)
    print(f"TIMON:     {'✅ PASSOU' if passou_timon else '❌ FALHOU'}")
    print(f"FORTALEZA: {'✅ PASSOU' if passou_fortaleza else '❌ FALHOU'}")
    print("=" * 80)
    
    if passou_timon and passou_fortaleza:
        print()
        print("🎉🎉🎉 SISTEMA VALIDADO! 🎉🎉🎉")
        print("Todos os cálculos estão corretos!")
    else:
        print()
        print("⚠️ SISTEMA PRECISA DE AJUSTES")
        print("Alguns valores estão diferentes da planilha")
