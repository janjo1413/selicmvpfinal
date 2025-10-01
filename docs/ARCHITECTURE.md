# Arquitetura do Sistema

## v1.0.0 - Template Excel (Atual)

### Fluxo de Dados
```
[Usuário] → [Frontend HTML/JS] → [FastAPI] → [ExcelTemplateCalculator]
                                                      ↓
                                              [Template Excel]
                                                      ↓
                                              [Valores Lidos]
                                                      ↓
                                          [Resposta JSON/CSV]
```

### Limitações da Arquitetura v1.0
1. **Dependência do Template**: Sistema depende 100% do arquivo Excel com fórmulas pré-calculadas
2. **Openpyxl**: Biblioteca não suporta recálculo de fórmulas (limitação fundamental)
3. **Valores Estáticos**: Honorários e Deságio não calculam dinamicamente
4. **Performance**: ~2 minutos por cálculo devido a I/O de arquivos Excel
5. **Manutenibilidade**: Fórmulas complexas "escondidas" no Excel, difícil debugar

### Como Funciona (v1.0)
1. Cria cópia temporária do template Excel
2. **NÃO** escreve inputs no Excel (causa perda de valores calculados)
3. Lê valores pré-calculados do template (data_only=True)
4. Retorna valores ao usuário
5. Deleta cópia temporária

## v1.1.0 - Cálculos Nativos (Planejado)

### Nova Arquitetura
```
[Usuário] → [Frontend] → [FastAPI] → [CalculationEngine (Python)]
                                              ↓
                                    [Módulos de Correção]
                                    - ipca_calculator.py
                                    - selic_calculator.py
                                    - tr_calculator.py
                                              ↓
                                    [Fórmulas Nativas]
                                              ↓
                                    [Valores Calculados]
                                              ↓
                                    [Resposta JSON/CSV]
```

### Benefícios da Nova Arquitetura
1. ✅ **Honorários Dinâmicos**: Cálculo em tempo real baseado em inputs
2. ✅ **Performance**: ~10s por cálculo (20x mais rápido)
3. ✅ **Testável**: Testes unitários para cada função
4. ✅ **Manutenível**: Código Python legível e documentado
5. ✅ **Sem Dependências Externas**: Não precisa de Excel instalado
6. ✅ **Escalável**: Pode adicionar novos cenários facilmente

### Módulos a Implementar

#### 1. `src/calculators/base.py`
```python
class BaseCalculator:
    """Classe base para todos os calculadores"""
    def calculate(self, principal, taxa, periodo): ...
```

#### 2. `src/calculators/ipca.py`
```python
class IPCACalculator(BaseCalculator):
    """Correção monetária por IPCA"""
    def apply_correction(self, valor, indices_ipca): ...
```

#### 3. `src/calculators/selic.py`
```python
class SELICCalculator(BaseCalculator):
    """Correção por taxa SELIC"""
    def apply_correction(self, valor, taxas_selic): ...
```

#### 4. `src/calculators/scenarios.py`
```python
class ScenarioCalculator:
    """Orquestra cálculos dos 9 cenários"""
    def calculate_nt7_ipca(self, inputs): ...
    def calculate_nt6_selic(self, inputs): ...
    # ... outros cenários
```

#### 5. `src/calculators/honorarios.py`
```python
class HonorariosCalculator:
    """Cálculo dinâmico de honorários"""
    def calculate(self, valor_principal, percentual): ...
```

### Estratégia de Migração
1. **Fase 1**: Implementar calculadores base (IPCA, SELIC, TR)
2. **Fase 2**: Implementar 1 cenário completo (NT7 IPCA)
3. **Fase 3**: Validar precisão vs Excel (margem <0.01%)
4. **Fase 4**: Implementar demais cenários
5. **Fase 5**: Substituir ExcelTemplateCalculator por CalculationEngine
6. **Fase 6**: Manter Excel apenas como referência/documentação

### Fórmulas a Implementar

#### Correção IPCA
```
Valor Corrigido = Valor Inicial × (Índice Final / Índice Inicial)
```

#### Correção SELIC
```
Valor Corrigido = Valor Inicial × ∏(1 + SELIC_diária)
```

#### Honorários
```
Honorários = (Principal + Juros + Correção) × (% Honorários / 100)
```

#### Deságio
```
Valor com Deságio = Principal × (1 - Deságio/100)
```

### Testes Necessários
- [ ] test_ipca_calculator.py - Validar correção IPCA
- [ ] test_selic_calculator.py - Validar correção SELIC
- [ ] test_tr_calculator.py - Validar correção TR
- [ ] test_honorarios.py - Validar cálculo de honorários
- [ ] test_scenarios.py - Validar cada um dos 9 cenários
- [ ] test_integration.py - Validar fluxo completo end-to-end

### Dados Necessários
- Histórico IPCA (IBGE API ou arquivo CSV)
- Histórico SELIC (BACEN API ou arquivo CSV)
- Histórico TR (BACEN API ou arquivo CSV)
- Fallback para dados offline caso APIs indisponíveis
