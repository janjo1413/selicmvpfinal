# 🌐 Integração com API do Banco Central (BACEN)

## Visão Geral

O sistema integra com a API de dados abertos do Banco Central do Brasil para obter taxas SELIC atualizadas em tempo real.

## Endpoint BACEN

- **Base URL**: `https://api.bcb.gov.br/dados/serie/bcdata.sgs`
- **Série SELIC**: `432` (Taxa de juros - Selic)
- **Formato**: JSON
- **Documentação oficial**: https://dadosabertos.bcb.gov.br/dataset/432-taxa-de-juros---selic

## Funcionalidades

### ✅ Busca Automática de Taxas

```python
from src.bacen_service import BacenService
from datetime import date

service = BacenService()

# Buscar taxas de um período
taxas = service.buscar_selic_periodo(
    data_inicio=date(2024, 1, 1),
    data_fim=date(2024, 12, 31)
)

# Resultado: [{'data': '02/01/2024', 'valor': 11.75}, ...]
```

### ✅ Cache Local Automático

- Primeira busca: consulta API e salva em `data/selic_cache.json`
- Buscas subsequentes: usa cache local (rápido e offline)
- Cache é atualizado automaticamente quando necessário

### ✅ Fallback Offline

Se a API BACEN estiver indisponível:
1. Tenta usar cache local
2. Se cache não existir, usa taxas do Excel
3. Logs informativos sobre a fonte dos dados

## Exemplo de Uso

### Verificar Disponibilidade

```python
from src.bacen_service import verificar_api_bacen

if verificar_api_bacen():
    print("✅ API BACEN disponível")
else:
    print("⚠️ API BACEN indisponível - usando cache")
```

### Buscar Taxas de um Período

```python
from src.bacen_service import obter_selic_atualizada
from datetime import date

taxas = obter_selic_atualizada(
    data_inicio=date(2020, 1, 1),
    data_fim=date(2025, 1, 1)
)

if taxas:
    print(f"✅ {len(taxas)} taxas obtidas")
    print(f"Primeira: {taxas[0]}")
    print(f"Última: {taxas[-1]}")
```

### Integração no Cálculo

O sistema automaticamente:
1. Consulta a API BACEN ao calcular
2. Usa cache se disponível
3. Retorna informações no `selic_context`:

```json
{
  "updated": true,
  "source": "API BACEN",
  "registros": 365,
  "periodo": "01/01/2024 a 31/12/2024",
  "message": "✅ 365 taxas SELIC obtidas da API BACEN"
}
```

## Cache Local

### Estrutura do Cache

Arquivo: `data/selic_cache.json`

```json
{
  "data_inicio": "2020-01-01",
  "data_fim": "2025-01-01",
  "atualizado_em": "2025-10-02T10:30:00",
  "dados": [
    {"data": "02/01/2020", "valor": 4.40},
    {"data": "03/01/2020", "valor": 4.40},
    ...
  ]
}
```

### Gerenciamento do Cache

- **Criação automática**: Na primeira busca
- **Atualização**: Quando necessário buscar período não coberto
- **Limpeza manual**: Deletar `data/selic_cache.json`

## Configuração (.env)

```env
# API BACEN
BACEN_API_BASE=https://api.bcb.gov.br/dados/serie/bcdata.sgs
BACEN_SERIE_SELIC=432
```

## Tratamento de Erros

### Timeout (>10 segundos)
```
⚠️ Timeout ao buscar SELIC (>10s)
➡️ Usa cache local automaticamente
```

### API Indisponível
```
⚠️ API BACEN indisponível
➡️ Usa cache local ou Excel
```

### Sem Dados para Período
```
⚠️ Nenhum dado SELIC retornado
➡️ Usa cache ou Excel
```

## Logs Informativos

### Sucesso (API)
```
INFO - Buscando SELIC de 01/01/2024 a 31/12/2024...
INFO - ✅ 365 taxas SELIC obtidas da API BACEN
INFO - Cache SELIC salvo: 365 registros
```

### Sucesso (Cache)
```
INFO - Dados SELIC carregados do cache (365 registros)
```

### Fallback
```
WARNING - ⚠️ API BACEN indisponível. Tentando usar cache local...
INFO - ✅ Usando cache local (1825 registros)
```

### Erro
```
ERROR - ❌ Nenhuma fonte de dados SELIC disponível
```

## Benefícios

1. **✅ Taxas Sempre Atualizadas**: Busca do BACEN em tempo real
2. **✅ Performance**: Cache local acelera consultas
3. **✅ Confiabilidade**: Fallback automático garante funcionamento
4. **✅ Transparência**: Logs mostram origem dos dados
5. **✅ Offline-First**: Funciona sem internet usando cache

## Limitações Atuais

- ⚠️ Apenas consulta taxas (não aplica no cálculo ainda)
- ⚠️ Cache não expira automaticamente
- ⚠️ Não valida integridade dos dados

## Próximos Passos (v1.3.0)

- [ ] Aplicar taxas SELIC no cálculo real
- [ ] Expiração automática de cache (30 dias)
- [ ] Validação de integridade (checksum)
- [ ] Suporte a outras séries (IPCA, TR)
- [ ] Interface para visualizar taxas

## Referências

- [API Dados Abertos BCB](https://dadosabertos.bcb.gov.br/)
- [Série 432 - Taxa SELIC](https://dadosabertos.bcb.gov.br/dataset/432-taxa-de-juros---selic)
- [Manual da API SGS](https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries)
