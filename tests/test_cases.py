"""
Casos de teste para validação do MVP
"""
import json
from datetime import date

# Caso 1: Timon Real (Validação Base)
CASO_TESTE_1 = {
    "nome": "Caso 1: Timon Real - Validação Base",
    "descricao": "Dados reais de Timon para validação. Valores devem bater 100% com planilha manual.",
    "inputs": {
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
    },
    "outputs_esperados": {
        "nota": "Preencher após executar na planilha manual",
        "nt7_ipca_selic": {
            "principal": 0.0,  # TODO: preencher valor real
            "honorarios": 0.0,
            "total": 0.0
        }
    }
}

# Caso 2: Honorários Percentual
CASO_TESTE_2 = {
    "nome": "Caso 2: São Luís - Honorários Percentual",
    "descricao": "Teste com honorários percentuais de 15%",
    "inputs": {
        "municipio": "SAO LUIS",
        "periodo_inicio": "2010-01-01",
        "periodo_fim": "2015-12-01",
        "ajuizamento": "2014-03-01",
        "citacao": "2015-06-01",
        "honorarios_perc": 0.15,
        "honorarios_fixo": 0.0,
        "desagio_principal": 0.1,
        "desagio_honorarios": 0.05,
        "correcao_ate": "2024-12-01"
    },
    "outputs_esperados": {
        "nota": "Preencher após executar na planilha manual"
    }
}

# Caso 3: Honorários Fixo
CASO_TESTE_3 = {
    "nome": "Caso 3: Fortaleza - Honorários Fixo",
    "descricao": "Teste com honorários fixo de R$ 5.000,00",
    "inputs": {
        "municipio": "FORTALEZA",
        "periodo_inicio": "2015-01-01",
        "periodo_fim": "2020-12-01",
        "ajuizamento": "2019-06-01",
        "citacao": "2020-03-01",
        "honorarios_perc": 0.0,
        "honorarios_fixo": 5000.0,
        "desagio_principal": 0.15,
        "desagio_honorarios": 0.15,
        "correcao_ate": "2025-01-01"
    },
    "outputs_esperados": {
        "nota": "Preencher após executar na planilha manual"
    }
}

# Caso 4: Sem Deságio
CASO_TESTE_4 = {
    "nome": "Caso 4: Recife - Sem Deságio",
    "descricao": "Teste sem aplicação de deságio",
    "inputs": {
        "municipio": "RECIFE",
        "periodo_inicio": "2018-01-01",
        "periodo_fim": "2023-12-01",
        "ajuizamento": "2022-01-01",
        "citacao": "2023-01-01",
        "honorarios_perc": 0.20,
        "honorarios_fixo": 0.0,
        "desagio_principal": 0.0,
        "desagio_honorarios": 0.0,
        "correcao_ate": "2025-01-01"
    },
    "outputs_esperados": {
        "nota": "Preencher após executar na planilha manual"
    }
}

# Caso 5: Período Curto
CASO_TESTE_5 = {
    "nome": "Caso 5: Salvador - Período Curto (6 meses)",
    "descricao": "Teste com período muito curto",
    "inputs": {
        "municipio": "SALVADOR",
        "periodo_inicio": "2024-01-01",
        "periodo_fim": "2024-06-30",
        "ajuizamento": "2024-03-01",
        "citacao": "2024-05-01",
        "honorarios_perc": 0.10,
        "honorarios_fixo": 0.0,
        "desagio_principal": 0.05,
        "desagio_honorarios": 0.05,
        "correcao_ate": "2024-12-31"
    },
    "outputs_esperados": {
        "nota": "Preencher após executar na planilha manual"
    }
}


def salvar_casos_teste():
    """Salva casos de teste em arquivo JSON"""
    casos = [
        CASO_TESTE_1,
        CASO_TESTE_2,
        CASO_TESTE_3,
        CASO_TESTE_4,
        CASO_TESTE_5
    ]
    
    with open('casos_teste.json', 'w', encoding='utf-8') as f:
        json.dump(casos, f, indent=2, ensure_ascii=False)
    
    print("✅ Casos de teste salvos em casos_teste.json")


if __name__ == "__main__":
    salvar_casos_teste()
    
    print("\n📋 CASOS DE TESTE DEFINIDOS")
    print("=" * 60)
    
    for i, caso in enumerate([CASO_TESTE_1, CASO_TESTE_2, CASO_TESTE_3, CASO_TESTE_4, CASO_TESTE_5], 1):
        print(f"\n{i}. {caso['nome']}")
        print(f"   {caso['descricao']}")
        print(f"   Município: {caso['inputs']['municipio']}")
        print(f"   Período: {caso['inputs']['periodo_inicio']} a {caso['inputs']['periodo_fim']}")
