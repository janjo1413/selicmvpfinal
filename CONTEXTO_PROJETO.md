# CONTEXTO DO PROJETO - CALCULADORA SELIC

## RESUMO EXECUTIVO

Sistema web para cálculo de correção monetária e juros em processos judiciais, desenvolvido em Python com FastAPI. O sistema realiza cálculos complexos utilizando índices econômicos do Banco Central (SELIC, TR, IPCA, IPCA-E) e fornece resultados em múltiplas metodologias de cálculo conforme normativas do CNJ e STJ.

**Status atual**: Sistema em produção, 100% testado e validado com 30 testes automatizados.

---

## ESPECIFICAÇÕES TÉCNICAS

### Stack Tecnológica
- **Backend**: Python 3.13 + FastAPI
- **Frontend**: HTML/CSS/JavaScript vanilla
- **APIs Externas**: Banco Central do Brasil (BCB), IBGE
- **Automação**: win32com (Excel COM automation)
- **Deploy**: Heroku-ready (Procfile, runtime.txt, requirements.txt configurados)

### Arquitetura
```
Frontend (static/) 
    ↓ HTTP POST /calcular
Backend (app.py + src/)
    ↓ Validações
Serviços (bacen_service.py, ibge_service.py)
    ↓ Cache (data/cache/*.json)
APIs Externas (BCB, IBGE)
    ↓ Processamento
Calculadoras (calculator_service.py, desagio_calculator.py, honorarios_calculator.py)
    ↓ Resultado
9 cenários de cálculo retornados
```

---

## FUNCIONALIDADES PRINCIPAIS

### 1. Entrada de Dados
O usuário fornece:
- **Município**: Nome da cidade (184+ municípios mapeados no Excel template)
- **Competência**: Mês/ano de referência (formato: mm/aaaa)
- **Datas**: Data inicial e data final do período de cálculo
- **Honorários**: Percentual (0-100%) ou valor fixo em reais
- **Deságio**: Percentual (0-100%) aplicado sobre o principal

### 2. Cálculos Realizados
O sistema retorna **9 cenários diferentes**:

1. **nt7_ipca_selic**: Nota Técnica 7 STJ com IPCA + SELIC
2. **nt7_periodo_cnj**: Nota Técnica 7 STJ com períodos CNJ
3. **nt6_ipca_selic**: Nota Técnica 6 STJ com IPCA + SELIC
4. **jasa_ipca_selic**: JASA com IPCA + SELIC
5. **nt7_tr**: Nota Técnica 7 STJ com TR
6. **nt36_tr**: Nota Técnica 36 STJ com TR
7. **nt7_ipca_e**: Nota Técnica 7 STJ com IPCA-E
8. **nt36_ipca_e**: Nota Técnica 36 STJ com IPCA-E
9. **nt36_ipca_e_1pct**: Nota Técnica 36 STJ com IPCA-E + 1% a.m.

Cada cenário retorna:
- **Principal corrigido**: Valor base com correção monetária
- **Juros**: Montante de juros calculados
- **Total**: Principal + Juros
- **Honorários**: Aplicados conforme configuração
- **Total com honorários**: Valor final após aplicação de honorários

### 3. Validações Implementadas
- **Taxas completas**: Verifica se há dados do BCB/IBGE para todo período
- **Datas**: Data inicial ≤ data final
- **Percentuais**: Honorários e deságio entre 0-100%
- **Município**: Verificação de existência no template Excel
- **Competência**: Formato mm/aaaa válido

---

## ESTRUTURA DE ARQUIVOS

### Diretório `/src/` (13 arquivos)
**Serviços**:
- `bacen_service.py`: Integração com API do Banco Central (SELIC, TR)
- `ibge_service.py`: Integração com API do IBGE (IPCA, IPCA-E)
- `config.py`: Configurações globais e URLs das APIs

**Calculadoras**:
- `calculator_service.py`: Orquestrador principal dos cálculos (CalculadoraService)
- `desagio_calculator.py`: Cálculo de deságio sobre o principal
- `honorarios_calculator.py`: Cálculo de honorários advocatícios
- `excel_template_calculator.py`: Automação do cálculo via planilha Excel

**Validadores**:
- `taxas_validator.py`: Validação de disponibilidade de taxas
- `taxas_completo_validator.py`: Validação completa de período

**Modelos**:
- `models.py`: Pydantic models para validação de entrada/saída
- `main.py`: Ponto de entrada alternativo

### Diretório `/tests/` (5 arquivos)
- `test_api.py`: Testes de endpoints da API
- `test_cases.py`: Casos de teste específicos
- `test_hello.py`: Teste básico de health check
- `test_honorarios_calculator.py`: Testes da calculadora de honorários
- `test_integracao_excel_vs_site.py`: Testes de integração Excel vs API

### Diretório `/static/` (3 arquivos)
- `index.html`: Interface web do usuário
- `script.js`: Lógica de frontend e comunicação com API
- `styles.css`: Estilização da interface

### Diretório `/data/`
- `timon_01-2025.xlsx`: Template Excel com 184 municípios e fórmulas de cálculo
- `/cache/*.json`: Cache de índices econômicos (selic_cache.json, tr_cache.json, ipca_cache.json, ipca_e_cache.json)
- `/output/`: Arquivos de saída dos testes (CSV e XLSX)

### Arquivos Raiz (2 scripts)
- `app.py`: Aplicação FastAPI principal
- `bateria_testes_completa.py`: Script de testes automatizados (30 testes)

### Documentação
- `README.md`: Documentação geral do projeto
- `ARQUIVOS_PARA_IA.md`: Guia para contexto de IA
- `CHANGELOG.md`: Histórico de mudanças
- `RELATORIO_FINAL_TESTES.md`: Relatório completo dos testes de validação
- `docs/GUIA_RAPIDO_v1.2.0.md`: Guia rápido de uso
- `docs/ARCHITECTURE.md`: Arquitetura detalhada
- `docs/GUIA_APIS.md`: Documentação das APIs externas

---

## FLUXO DE CÁLCULO DETALHADO

### Passo 1: Recepção de Dados
```python
# Endpoint: POST /calcular
{
    "municipio": "TIMON",
    "competencia": "01/2025",
    "data_inicio": "2020-01-01",
    "data_fim": "2024-12-31",
    "honorarios_percentual": 30.0,
    "desagio_percentual": 0.0
}
```

### Passo 2: Validações
1. `taxas_completo_validator.py`: Verifica disponibilidade de todas as taxas (SELIC, TR, IPCA, IPCA-E) para o período
2. Validação de formato de datas e competência
3. Validação de município no template Excel

### Passo 3: Busca de Índices (com cache)
- **BacenService**: Busca SELIC e TR via API do BCB
- **IbgeService**: Busca IPCA e IPCA-E via API do IBGE
- Cache local em JSON para otimização (atualização diária)

### Passo 4: Cálculo Excel (Referência)
- `excel_template_calculator.py` abre `data/timon_01-2025.xlsx`
- Preenche células com dados do usuário
- Excel recalcula automaticamente usando fórmulas complexas
- Extrai valores calculados para validação

### Passo 5: Cálculos Python (9 cenários)
- `CalculadoraService` orquestra todos os cálculos
- Aplica metodologias: NT7, NT6, NT36, JASA
- Aplica índices: IPCA+SELIC, TR, IPCA-E, IPCA-E+1%
- `DesagioCalculator`: Reduz principal se deságio > 0
- `HonorariosCalculator`: Aplica honorários sobre total

### Passo 6: Retorno de Resultados
```json
{
    "nt7_ipca_selic": {
        "principal": 158570032.07,
        "juros": 95142288.84,
        "total": 253712320.91,
        "honorarios": 76113696.27,
        "total_com_honorarios": 329826017.18
    },
    // ... mais 8 cenários
}
```

---

## VALIDAÇÃO E TESTES

### Bateria de Testes Automatizada
**Arquivo**: `bateria_testes_completa.py`

**Configuração**:
- 10 municípios testados: TIMON, FORTALEZA, SAO LUIS, TERESINA, CAMPO MAIOR, PARNAIBA, PICOS, FLORIANO, CAXIAS, BACABAL
- 3 cenários de entrada por município:
  1. Sem honorários
  2. Com honorários 30%
  3. Sem deságio
- 9 cenários de cálculo por teste
- **Total**: 30 testes × 9 cenários = 270 validações

**Metodologia**:
1. Calcula via Excel (win32com)
2. Calcula via API (requests)
3. Compara valores: diferença deve ser < R$ 0.01 (1 centavo)
4. Gera relatório JSON e Markdown

**Resultados**:
- **Taxa de sucesso**: 100% (30/30 testes aprovados)
- **Tempo médio**: ~5 minutos por teste
- **Tempo total**: ~2h30min
- **Tolerância**: Diferença máxima < R$ 0.01

### Documentação de Testes
- `RELATORIO_FINAL_TESTES.md`: Relatório completo com matriz de testes
- `relatorio_testes.json`: Resultados em formato JSON

---

## INTEGRAÇÕES COM APIs EXTERNAS

### 1. Banco Central do Brasil (BCB)
**URL Base**: `https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados`

**Séries Utilizadas**:
- **SELIC** (código 4390): Taxa SELIC diária
- **TR** (código 226): Taxa Referencial mensal

**Cache**: `data/cache/selic_cache.json`, `data/cache/tr_cache.json`

**Exemplo de requisição**:
```python
# SELIC de 01/01/2020 a 31/12/2024
url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4390/dados?formato=json&dataInicial=01/01/2020&dataFinal=31/12/2024"
```

### 2. IBGE - Sidra
**URL Base**: `https://servicodados.ibge.gov.br/api/v3/agregados/{codigo}/periodos/{periodo}/variaveis/63`

**Índices Utilizados**:
- **IPCA** (código 1737): Índice Nacional de Preços ao Consumidor Amplo
- **IPCA-E** (código 7060): IPCA Especial

**Cache**: `data/cache/ipca_cache.json`, `data/cache/ipca_e_cache.json`

**Exemplo de requisição**:
```python
# IPCA de janeiro/2020 a dezembro/2024
url = "https://servicodados.ibge.gov.br/api/v3/agregados/1737/periodos/202001|202002|...|202412/variaveis/63"
```

**Tratamento de Cache**:
- Cache atualizado diariamente
- Se índice não encontrado no cache, busca na API
- Cache persistido em JSON local

---

## REGRAS DE NEGÓCIO ESPECÍFICAS

### 1. Honorários Advocatícios
- **Entrada**: Percentual (0-100%) ou valor fixo
- **Base de cálculo**: Total (principal corrigido + juros)
- **Fórmula**: `honorarios = total * (percentual / 100)`
- **Aplicação**: Sobre cada um dos 9 cenários de cálculo

### 2. Deságio
- **Entrada**: Percentual (0-100%)
- **Base de cálculo**: Principal original
- **Fórmula**: `principal_com_desagio = principal * (1 - desagio/100)`
- **Aplicação**: Antes do cálculo de correção e juros

### 3. Metodologias de Cálculo

**Nota Técnica 7 (NT7)**:
- Correção monetária pelo IPCA
- Juros pelo SELIC
- Período: Data início até data fim

**Nota Técnica 6 (NT6)**:
- Similar à NT7 com ajustes específicos

**Nota Técnica 36 (NT36)**:
- Correção pela TR ou IPCA-E
- Opção com juros de 1% a.m. adicional

**JASA**:
- Metodologia específica com IPCA + SELIC

---

## AMBIENTE E DEPLOY

### Variáveis de Ambiente
Não requer variáveis de ambiente (APIs públicas sem autenticação).

### Dependências Principais
```txt
fastapi==0.115.4
uvicorn==0.32.0
requests==2.32.3
openpyxl==3.1.5
python-multipart==0.0.17
pydantic==2.9.2
pywin32==308  # Apenas para ambiente Windows (testes Excel)
```

### Deploy Heroku
```bash
# Arquivos configurados:
- Procfile: web: uvicorn app:app --host 0.0.0.0 --port $PORT
- runtime.txt: python-3.13.0
- requirements.txt: Todas as dependências listadas
```

### Execução Local
```powershell
# Instalar dependências
pip install -r requirements.txt

# Iniciar servidor
python app.py
# ou
uvicorn app:app --reload

# Acessar interface
http://localhost:8000
```

### Testes
```powershell
# Testes unitários
pytest

# Bateria completa (requer Excel instalado)
python bateria_testes_completa.py
```

---

## DADOS IMPORTANTES

### Template Excel (timon_01-2025.xlsx)
- **184+ municípios**: Mapeados na planilha com códigos e nomes
- **Fórmulas complexas**: Cálculos de correção e juros implementados no Excel
- **Automação**: win32com para manipular e extrair valores
- **Localização**: `data/timon_01-2025.xlsx`

### Cache de Índices
- **Formato**: JSON com estrutura `{"data": valor}`
- **Atualização**: Diária via APIs externas
- **Localização**: `data/cache/*.json`
- **Tipos**: selic_cache.json, tr_cache.json, ipca_cache.json, ipca_e_cache.json

### Saída de Testes
- **Formato**: CSV e XLSX
- **Localização**: `data/output/`
- **Nomenclatura**: `{MUNICIPIO}_{hash}_{timestamp}.{extensao}`

---

## OBSERVAÇÕES IMPORTANTES

### 1. Precisão de Cálculos
- **Tolerância**: Diferença máxima de R$ 0.01 entre Excel e API
- **Arredondamento**: 2 casas decimais para valores monetários
- **Validação**: 270 validações (30 testes × 9 cenários) com 100% de aprovação

### 2. Performance
- **Cache**: Reduz chamadas às APIs externas
- **Tempo de resposta**: ~2-5 segundos por cálculo completo
- **Testes**: ~5 minutos por teste individual

### 3. Limitações Conhecidas
- **Excel**: Requer Windows + Excel instalado para testes automatizados
- **APIs**: Dependência de disponibilidade das APIs do BCB e IBGE
- **Dados históricos**: APIs podem ter limitações de período disponível

### 4. Segurança
- APIs públicas sem autenticação requerida
- Sem armazenamento de dados sensíveis
- Validação de entrada via Pydantic

---

## CONTATO E MANUTENÇÃO

**Versão atual**: 1.2.0  
**Última atualização**: Outubro 2025  
**Status**: Produção, 100% validado  
**Repositório**: selicmvpfinal (GitHub: janjo1413)

### Histórico de Limpeza
- **37 arquivos temporários removidos** (scripts de debug e validação)
- **20 arquivos Python essenciais** mantidos
- **Estrutura otimizada** para produção

---

## PROMPT DE CONTEXTUALIZAÇÃO PARA CHAT

```
Você está trabalhando no projeto "CALCULADORA SELIC", um sistema web FastAPI para cálculo de correção monetária e juros em processos judiciais.

TECNOLOGIAS:
- Python 3.13 + FastAPI
- Frontend: HTML/CSS/JavaScript vanilla
- APIs: Banco Central (SELIC, TR), IBGE (IPCA, IPCA-E)
- Automação: win32com para Excel

ESTRUTURA:
- src/ (13 arquivos): Serviços, calculadoras, validadores
- tests/ (5 arquivos): Testes unitários e integração
- static/ (3 arquivos): Interface web
- data/: Template Excel (184 municípios), cache de índices

FUNCIONALIDADE PRINCIPAL:
Sistema recebe município, competência, datas, honorários e deságio, e retorna 9 cenários de cálculo diferentes (NT7, NT6, NT36, JASA com variações de índices: IPCA+SELIC, TR, IPCA-E).

CÁLCULOS:
1. Busca índices econômicos (BCB e IBGE com cache)
2. Calcula via Excel (referência) usando win32com
3. Calcula via Python (9 cenários)
4. Valida: diferença deve ser < R$ 0.01

VALIDAÇÃO:
- 30 testes automatizados (10 municípios × 3 cenários)
- 270 validações totais (30 testes × 9 cenários de cálculo)
- 100% de aprovação em todos os testes
- Relatório completo: RELATORIO_FINAL_TESTES.md

STATUS ATUAL:
✅ Sistema em produção
✅ 100% testado e validado
✅ Estrutura limpa (37 arquivos temporários removidos)
✅ 20 arquivos Python essenciais mantidos
✅ Deploy Heroku configurado

ARQUIVOS PRINCIPAIS:
- app.py: API FastAPI
- src/calculator_service.py: Orquestrador de cálculos
- src/bacen_service.py: Integração BCB
- src/ibge_service.py: Integração IBGE
- bateria_testes_completa.py: Testes automatizados
- data/timon_01-2025.xlsx: Template com 184 municípios

DOCUMENTAÇÃO:
- README.md: Visão geral
- docs/GUIA_RAPIDO_v1.2.0.md: Guia de uso
- docs/ARCHITECTURE.md: Arquitetura
- RELATORIO_FINAL_TESTES.md: Validação completa

Versão: 1.2.0 | Última atualização: Outubro 2025
```

---

**FIM DO CONTEXTO**
