# 🌐 Guia de Uso das APIs - v1.2.0

## Visão Geral

A versão 1.2.0 introduz integração completa com APIs públicas para buscar taxas atualizadas automaticamente:

- **BACEN** (Banco Central): SELIC e TR
- **IBGE** (Instituto Brasileiro de Geografia e Estatística): IPCA e IPCA-E

Todas as APIs são **gratuitas**, **públicas** e **não requerem autenticação**.

---

## 📡 APIs Integradas

### 1. BACEN - Banco Central do Brasil

**Base URL:** `https://api.bcb.gov.br/dados/serie/bcdata.sgs`

#### SELIC (Série 11)
- **Descrição:** Taxa de juros básica da economia brasileira
- **Frequência:** Diária (% ao dia)
- **Formato:** `{'data': 'DD/MM/YYYY', 'valor': '0.040168'}`
- **Documentação:** https://dadosabertos.bcb.gov.br/dataset/11-taxa-de-juros---selic

#### TR - Taxa Referencial (Série 226)
- **Descrição:** Taxa utilizada em financiamentos imobiliários e FGTS
- **Frequência:** Mensal
- **Formato:** `{'data': 'DD/MM/YYYY', 'dataFim': 'DD/MM/YYYY', 'valor': '0.0741'}`
- **Documentação:** https://dadosabertos.bcb.gov.br/dataset/226-taxa-referencial---tr

### 2. IBGE - Instituto Brasileiro de Geografia e Estatística

**Base URL:** `https://servicodados.ibge.gov.br/api/v3/agregados`

#### IPCA (Agregação 1737)
- **Descrição:** Índice Nacional de Preços ao Consumidor Amplo
- **Frequência:** Mensal
- **Formato:** `{'data': 'MM/YYYY', 'valor': 0.56}`
- **Documentação:** https://servicodados.ibge.gov.br/api/docs/agregados

#### IPCA-E - IPCA Especial (Agregação 7060)
- **Descrição:** Variação do IPCA calculada de forma especial
- **Frequência:** Mensal
- **Formato:** `{'data': 'MM/YYYY', 'valor': 0.52}`
- **Documentação:** https://servicodados.ibge.gov.br/api/docs/agregados

---

## 🛠️ Como Usar

### Exemplo 1: Buscar SELIC Atualizada

```python
from datetime import date
from src.bacen_service import BacenService

# Criar serviço
bacen = BacenService()

# Buscar taxas SELIC de out/2024 a dez/2024
taxas = bacen.buscar_selic_periodo(
    data_inicio=date(2024, 10, 1),
    data_fim=date(2024, 12, 31),
    usar_cache=True  # Usa cache local se disponível
)

# Resultado: lista de taxas diárias
# [
#   {'data': '01/10/2024', 'valor': '0.040168'},
#   {'data': '02/10/2024', 'valor': '0.040168'},
#   ...
# ]

print(f"Total de taxas: {len(taxas)}")
print(f"Primeira: {taxas[0]}")
print(f"Última: {taxas[-1]}")
```

### Exemplo 2: Buscar TR

```python
from src.bacen_service import BacenService

bacen = BacenService()

# Buscar TR do mesmo período
tr = bacen.buscar_tr_periodo(
    data_inicio=date(2024, 10, 1),
    data_fim=date(2024, 12, 31)
)

# Resultado: lista de taxas mensais
# [
#   {'data': '01/10/2024', 'dataFim': '31/10/2024', 'valor': '0.0741'},
#   {'data': '01/11/2024', 'dataFim': '30/11/2024', 'valor': '0.1012'},
#   ...
# ]
```

### Exemplo 3: Buscar IPCA e IPCA-E

```python
from src.ibge_service import IbgeService

ibge = IbgeService()

# Buscar IPCA
ipca = ibge.buscar_ipca_periodo(
    data_inicio=date(2024, 10, 1),
    data_fim=date(2024, 12, 31)
)

# Resultado: lista de taxas mensais
# [
#   {'data': '10/2024', 'valor': 0.56},
#   {'data': '11/2024', 'valor': 0.39},
#   {'data': '12/2024', 'valor': 0.52}
# ]

# Buscar IPCA-E
ipca_e = ibge.buscar_ipca_e_periodo(
    data_inicio=date(2024, 10, 1),
    data_fim=date(2024, 12, 31)
)
```

### Exemplo 4: Validar Todas as Taxas

```python
from src.taxas_completo_validator import TaxasCompletoValidator

validator = TaxasCompletoValidator()

# Validar disponibilidade para um cálculo até out/2025
resultado = validator.validar_todas(
    data_inicio=date(2020, 1, 1),
    data_fim=date(2025, 10, 1),
    verificar_apis=True  # Busca nas APIs para confirmar disponibilidade
)

# Imprimir relatório
relatorio = validator.gerar_relatorio(resultado)
print(relatorio)

# Resultado:
# ======================================================================
# VALIDAÇÃO DE TAXAS - RELATÓRIO COMPLETO
# ======================================================================
# 
# 📊 RESUMO:
#    Total de taxas: 4
#    ✅ Atualizadas: 0
#    ⚠️  Desatualizadas: 4
# 
# 📋 DETALHES POR TAXA:
# 
# ⚠️ SELIC: Excel até 01/2025, API até 10/2025. 9 meses faltando.
# ⚠️ TR: Excel até 01/2025, API até 10/2025. 9 meses faltando.
# ⚠️ IPCA: Excel até 01/2025, API até 08/2025. 9 meses faltando.
# ⚠️ IPCA-E: Excel até 01/2025, API até 08/2025. 9 meses faltando.
# 
# ======================================================================
# ⚠️ Excel desatualizado. 4/4 taxas precisam de atualização.
# ======================================================================
```

### Exemplo 5: Verificar Disponibilidade da API

```python
from src.bacen_service import BacenService
from src.ibge_service import IbgeService

bacen = BacenService()
ibge = IbgeService()

# Verificar se APIs estão respondendo
if bacen.verificar_disponibilidade("SELIC"):
    print("✅ API BACEN (SELIC) disponível")
else:
    print("❌ API BACEN (SELIC) indisponível - usando cache")

if ibge.verificar_disponibilidade("IPCA"):
    print("✅ API IBGE (IPCA) disponível")
else:
    print("❌ API IBGE (IPCA) indisponível - usando cache")
```

---

## 💾 Sistema de Cache

Todas as APIs usam **cache local automático**:

- **Localização:** `data/cache/`
- **Arquivos:**
  - `selic_cache.json` - Taxas SELIC
  - `tr_cache.json` - Taxas TR
  - `ipca_cache.json` - Taxas IPCA
  - `ipca_e_cache.json` - Taxas IPCA-E

### Vantagens do Cache

1. **Performance:** Evita requisições redundantes
2. **Confiabilidade:** Funciona offline se cache existe
3. **Resiliência:** Fallback automático se API falhar

### Estrutura do Cache

```json
{
  "taxa": "SELIC",
  "data_inicio": "2024-10-01",
  "data_fim": "2024-12-31",
  "atualizado_em": "2025-10-10T14:30:00",
  "dados": [
    {"data": "01/10/2024", "valor": "0.040168"},
    {"data": "02/10/2024", "valor": "0.040168"},
    ...
  ]
}
```

### Desabilitar Cache

```python
# Forçar busca na API (ignorar cache)
taxas = bacen.buscar_selic_periodo(
    data_inicio=date(2024, 10, 1),
    data_fim=date(2024, 12, 31),
    usar_cache=False  # ← Desabilita cache
)
```

---

## ⚙️ Configurações Avançadas

### Timeout Customizado

```python
# Timeout padrão: 10 segundos
bacen = BacenService()

# Timeout customizado (útil para conexões lentas)
from src.bacen_service import BacenService
service = BacenService()
service.timeout = 30  # 30 segundos
```

### Diretório de Cache Customizado

```python
from src.ibge_service import IbgeService

# Cache em diretório customizado
ibge = IbgeService(cache_dir="meu_cache/")
```

---

## 🚨 Tratamento de Erros

### Quando a API Falha

```python
taxas = bacen.buscar_selic_periodo(data_inicio, data_fim)

if taxas is None:
    print("❌ Erro: API indisponível e sem cache")
    # Usar dados do Excel como fallback
else:
    print(f"✅ Obtidas {len(taxas)} taxas")
```

### Tipos de Erro Comuns

1. **Timeout** - API demorou mais que o limite
   - Solução: Aumentar `timeout` ou verificar conexão

2. **404 Not Found** - URL incorreta ou série inexistente
   - Solução: Verificar código da série

3. **Network Error** - Sem internet
   - Solução: Usar cache local

4. **Dados vazios** - Período sem dados
   - Solução: Verificar datas (formato DD/MM/YYYY)

---

## 📊 Limitações e Restrições

### BACEN API

- **Período máximo:** 10 anos por consulta
- **Formato de data:** DD/MM/YYYY
- **Últimos registros:** Máximo 20 (`/dados/ultimos/20`)

### IBGE API

- **Formato de data:** YYYYMM (período)
- **Frequência:** Mensal (não tem dados diários)
- **Agregação:** Retorna estrutura JSON complexa (processada automaticamente)

---

## 🧪 Testando as APIs

Execute o script de teste completo:

```powershell
python teste_apis.py
```

Resultado esperado:
```
================================================================================
TESTE DAS APIs - BACEN E IBGE
================================================================================

🔵 1. Testando BACEN API - SELIC
--------------------------------------------------------------------------------
✅ API BACEN (SELIC) disponível
✅ Obtidas 63 taxas SELIC

🔵 2. Testando BACEN API - TR
--------------------------------------------------------------------------------
✅ API BACEN (TR) disponível
✅ Obtidas 94 taxas TR

🟢 3. Testando IBGE API - IPCA
--------------------------------------------------------------------------------
✅ API IBGE (IPCA) disponível
✅ Obtidas 3 taxas IPCA

🟢 4. Testando IBGE API - IPCA-E
--------------------------------------------------------------------------------
✅ API IBGE (IPCA-E) disponível
✅ Obtidas 3 taxas IPCA-E

🔍 5. Testando VALIDADOR COMPLETO
--------------------------------------------------------------------------------
⚠️ Excel desatualizado. 4/4 taxas precisam de atualização.
```

---

## 📚 Referências

- **BACEN Dados Abertos:** https://dadosabertos.bcb.gov.br/
- **IBGE APIs:** https://servicodados.ibge.gov.br/api/docs
- **Documentação SGS:** https://www3.bcb.gov.br/sgspub/

---

## ✅ Próximos Passos (v1.3.0)

1. Integrar APIs no fluxo de cálculo (substituir valores fixos do Excel)
2. Atualização automática de planilha Excel com dados das APIs
3. Interface web para visualizar status das taxas
4. Alertas quando taxas ficarem desatualizadas
5. Logs detalhados de uso das APIs

---

**Documentação criada em:** 10/10/2025  
**Versão:** 1.2.0  
**Autor:** Sistema de Cálculo Trabalhista
