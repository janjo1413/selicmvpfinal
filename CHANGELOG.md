# 📝 Changelog

Todas as mudanças notáveis serão documentadas neste arquivo.

---

## [1.2.0] - 2025-10-10 🚀 **IMPLEMENTAÇÃO COMPLETA DAS APIs**

### ✨ Adicionado

#### 🌐 Integração Completa com APIs Públicas
- **API BACEN (Banco Central)**: Busca SELIC e TR atualizadas automaticamente
  - ✅ SELIC (série 11) - Taxa de juros básica
  - ✅ TR (série 226) - Taxa Referencial
  - ✅ Novo módulo: `src/bacen_service.py`
  - ✅ Suporte a ambas as taxas com métodos específicos:
    - `buscar_selic_periodo()` - Taxas SELIC diárias
    - `buscar_tr_periodo()` - Taxas TR mensais
  - ✅ Cache local em `data/cache/selic_cache.json` e `tr_cache.json`
  - ✅ Fallback automático (API → Cache → Excel)

- **API IBGE (Instituto Brasileiro de Geografia e Estatística)**: Busca IPCA e IPCA-E
  - ✅ IPCA (agregação 1737) - Índice de inflação oficial
  - ✅ IPCA-E (agregação 7060) - IPCA Especial
  - ✅ Novo módulo: `src/ibge_service.py`
  - ✅ Métodos específicos:
    - `buscar_ipca_periodo()` - Taxas IPCA mensais
    - `buscar_ipca_e_periodo()` - Taxas IPCA-E mensais
  - ✅ Cache local em `data/cache/ipca_cache.json` e `ipca_e_cache.json`
  - ✅ Processamento automático da estrutura JSON complexa do IBGE

#### 🔍 Validador Completo de Taxas
- **TaxasCompletoValidator**: Verifica disponibilidade das 4 taxas essenciais
  - ✅ Novo módulo: `src/taxas_completo_validator.py`
  - ✅ Valida SELIC, TR, IPCA e IPCA-E simultaneamente
  - ✅ Compara última atualização do Excel (jan/2025) com data do cálculo
  - ✅ Busca nas APIs para confirmar disponibilidade real
  - ✅ Gera relatório detalhado:
    - Total de taxas verificadas
    - Quantas estão atualizadas
    - Quantas precisam atualização
    - Meses faltando por taxa
  - ✅ Identifica qual fonte tem dados (Excel vs API)

#### 💰 Deságio do Principal
- **Implementado cálculo de desconto sobre valor principal**
  - ✅ Aplica deságio ANTES de calcular honorários (ordem correta)
  - ✅ Suporta percentuais de 0% a 100%
  - ✅ Logs detalhados mostrando valor bruto, deságio e líquido
  - ✅ Novo módulo: `src/desagio_calculator.py`

#### ✅ Verificação Automática
- **Script para validar cálculos com casos reais**
  - ✅ Compara resultados do sistema com planilha Excel
  - ✅ Suporta múltiplos municípios e cenários
  - ✅ Margem de erro configurável (padrão: 0.01%)
  - ✅ Relatório detalhado de divergências
  - ✅ Novo arquivo: `verificacao_automatica.py`

#### 🧪 Script de Teste das APIs
- **Novo arquivo: `teste_apis.py`**
  - ✅ Testa integração com todas as 4 APIs
  - ✅ Verifica disponibilidade de cada serviço
  - ✅ Busca dados de teste (out-dez/2024)
  - ✅ Valida estrutura das respostas
  - ✅ Gera relatório completo de validação

### 🐛 Corrigido
- **Deságio do Principal não aplicado**: Agora aplica desconto corretamente
- **Ordem de cálculo**: Deságio → Honorários → Total (sequência correta)
- **Bug openpyxl**: Valores calculados retornavam 0 - agora lê valores brutos (linhas ímpares)
- **URL BACEN incorreta**: Corrigida para formato `bcdata.sgs.{codigo}/dados`

### 🚀 Melhorias
- **Logs aprimorados**: Informações detalhadas sobre deságio e taxas (todas as 4)
- **Transparência**: Sistema informa origem dos dados (API/Cache/Excel) para cada taxa
- **Confiabilidade**: Funciona 100% offline usando cache local
- **Performance**: Cache reduz requisições desnecessárias
- **Resiliência**: Fallback em 3 níveis (API → Cache → Excel)

### 📚 Documentação
- **Novo: `docs/GUIA_APIS.md`** - Guia completo de uso das APIs
  - Exemplos práticos de cada API
  - Estrutura do cache explicada
  - Tratamento de erros
  - Limitações e restrições
  - Configurações avançadas
- Novo: `docs/BACEN_INTEGRATION.md` - Guia da integração BACEN
- Novo: `docs/VERIFICACAO_AUTOMATICA.md` - Como usar verificação automática
- Atualizado: `README.md` - Novas funcionalidades documentadas

### 🔧 Técnico
- **6 novos módulos Python**:
  1. `src/desagio_calculator.py` - Cálculo de deságio
  2. `src/bacen_service.py` - Cliente API BACEN (SELIC + TR)
  3. `src/ibge_service.py` - Cliente API IBGE (IPCA + IPCA-E)
  4. `src/taxas_completo_validator.py` - Validador das 4 taxas
  5. `verificacao_automatica.py` - Verificação automática
  6. `teste_apis.py` - Suite de testes das APIs

- **Arquitetura modular**:
  - Cada serviço (BACEN/IBGE) independente
  - Cache separado por taxa
  - Validador agnóstico de fonte de dados
  
- **Integração não-bloqueante**: APIs não impedem cálculo se falharem
- **Cache inteligente**: Verifica período solicitado antes de buscar API

### ⚠️ Notas Importantes
- API BACEN requer conexão internet na primeira execução
- Cache local permite funcionamento 100% offline
- Valores de deságio são aplicados em cascata (Principal → Honorários)

---

## [1.1.0] - 2025-10-01 🎉

### ✨ Adicionado
- **Cálculo de honorários em Python**: Honorários agora calculam corretamente e dinamicamente
  - ✅ Suporte a honorários percentuais (% sobre principal)
  - ✅ Suporte a honorários fixos (valor em R$)
  - ✅ Aplicação de deságio nos honorários
  - ✅ Cálculo automático de total (principal + honorários)
  - ✅ Prioridade: percentual sobrescreve fixo quando ambos informados

### 🐛 Corrigido
- **Honorários zerados (bug crítico v1.0.0)**: Agora calcula corretamente usando Python
- **Total incorreto**: Soma correta de principal + honorários líquidos
- **Deságio não aplicado**: Deságio de honorários agora funciona

### 🚀 Melhorias
- **Performance**: Leitura otimizada do Excel (lê apenas coluna D - Principal)
- **Logs aprimorados**: Debug detalhado do cálculo de honorários
- **Testes unitários**: 11 testes cobrindo todos os casos de uso

### 🔧 Técnico
- Novo módulo: `src/honorarios_calculator.py` (79 linhas)
- Refatoração: `calculator_service.py` integrado com `HonorariosCalculator`
- Testes: `tests/test_honorarios_calculator.py` (141 linhas, 11 casos)
- Arquitetura híbrida: Excel para valores principais, Python para honorários

### 📊 Cobertura de Testes
```
test_honorarios_percentual_sem_desagio ✅
test_honorarios_percentual_com_desagio ✅
test_honorarios_fixo_sem_desagio ✅
test_honorarios_fixo_com_desagio ✅
test_sem_honorarios ✅
test_prioridade_percentual_sobre_fixo ✅
test_valores_reais_timon ✅
test_arredondamento_correto ✅
test_principal_zero ✅
test_percentuais_extremos ✅
```

---

## [1.0.0] - 2025-10-01

### ✅ Funcionalidades Implementadas
- Sistema MVP funcional com 9 cenários de cálculo
- Interface web responsiva (HTML/CSS/JS)
- Backend FastAPI com endpoints `/api/calcular` e `/api/exportar-csv`
- Integração com template Excel via openpyxl (data_only=True)
- Export CSV completo com metadados (data, hora, parâmetros)
- Validação de inputs com Pydantic
- Logging estruturado com timestamps
- Script de inicialização Windows (`iniciar.bat`)
- Botões "Novo Cálculo", "Limpar" e "Exportar CSV" funcionais
- Limpeza de código (redução de 65% dos arquivos)
- Documentação consolidada (README, CHANGELOG, TODO, ARCHITECTURE)

### ⚠️ Limitações Conhecidas
- **Honorários dinâmicos**: Usa valores pré-calculados do template Excel (limitação do openpyxl)
- **Deságio dinâmico**: Usa valores pré-calculados do template Excel
- **Performance**: ~2 minutos por cálculo (I/O de arquivos Excel)
- **Dependência Excel**: Sistema depende 100% do template Excel para fórmulas

### 📝 Notas Técnicas
- Arquitetura baseada em template Excel protegido (somente leitura)
- openpyxl não suporta recálculo de fórmulas (limitação da biblioteca)
- Valores calculados são perdidos quando workbook é salvo com openpyxl
- Solução v1.1.0: Reimplementar todas as fórmulas em Python nativo

### 🔧 Stack Técnico
- Python 3.13
- FastAPI 0.109.0
- openpyxl 3.1.2 com data_only=True
- Uvicorn com auto-reload
- Template Excel protegido (cópia temporária)
- Mapeamento INPUT/OUTPUT de células

### ⚠️ Limitações Conhecidas
- Tempo de execução: ~112 segundos (9 leituras Excel)
- SELIC estática (não atualiza automaticamente)
- Suporte apenas single-user
- Sem autenticação

---

## [Em Desenvolvimento] - v1.1.0

### 🚀 Planejado
- Otimização de performance (1 leitura Excel, ~10s total)
- Integração API BACEN (SELIC dinâmica)
- Testes automatizados (pytest)
- Cache de resultados
- Documentação API (Swagger melhorado)

---

**Formato:** [Semantic Versioning](https://semver.org/)  
**Tipos de mudança:**
- ✨ Adicionado: Novas funcionalidades
- 🔧 Alterado: Mudanças em funcionalidades existentes
- ⚠️ Deprecado: Funcionalidades que serão removidas
- 🗑️ Removido: Funcionalidades removidas
- 🐛 Corrigido: Correções de bugs
- 🔒 Segurança: Correções de vulnerabilidades
