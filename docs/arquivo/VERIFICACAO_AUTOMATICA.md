# 🔍 Guia de Verificação Automática

## Objetivo

A verificação automática valida se os cálculos do sistema estão corretos comparando com valores reais da planilha Excel em diferentes cenários e municípios.

**Diferença de Testes Unitários:**
- ❌ NÃO testa funções isoladas
- ✅ Valida aderência à realidade
- ✅ Usa casos reais de municípios
- ✅ Prova que sistema replica planilha

## Como Usar

### 1. Abrir a Planilha Excel

```powershell
# Abrir Excel
start data\timon_01-2025.xlsx
```

### 2. Coletar Valores Esperados

**Na aba RESUMO:**

1. Configure um cenário de teste:
   - Município: TIMON
   - Período: 01/01/2000 a 01/12/2006
   - Ajuizamento: 01/05/2005
   - Citação: 01/06/2006
   - Honorários %: 20
   - Deságio Principal: 0
   - Deságio Honorários: 0

2. Anote os valores calculados:
   - Linha 24 (NT7 IPCA/SELIC): Coluna D (Principal)
   - Linha 29 (NT7 Período CNJ): Coluna D
   - Linha 34 (NT6 IPCA/SELIC): Coluna D
   - Etc...

### 3. Configurar Script de Verificação

Edite `verificacao_automatica.py`:

```python
CASOS_VERIFICACAO = [
    CasoVerificacao(
        nome="TIMON - Caso Padrão",
        inputs={
            "municipio": "TIMON",
            "periodo_inicio": date(2000, 1, 1),
            "periodo_fim": date(2006, 12, 1),
            "ajuizamento": date(2005, 5, 1),
            "citacao": date(2006, 6, 1),
            "honorarios_perc": 20.0,
            "honorarios_fixo": 0.0,
            "desagio_principal": 0.0,
            "desagio_honorarios": 0.0,
            "correcao_ate": date(2025, 1, 1)
        },
        valores_esperados={
            "nt7_ipca_selic": {
                "principal_esperado": 123456.78,  # ⬅️ VALOR DO EXCEL
                "honorarios_esperado": 0.0,  # Sistema calcula
                "total_esperado": 0.0  # Sistema calcula
            },
            "nt7_periodo_cnj": {
                "principal_esperado": 234567.89,  # ⬅️ VALOR DO EXCEL
                "honorarios_esperado": 0.0,
                "total_esperado": 0.0
            },
            # ... outros cenários
        }
    )
]
```

### 4. Executar Verificação

```powershell
python verificacao_automatica.py
```

### 5. Interpretar Resultados

#### ✅ Sucesso Total
```
✅ TODOS OS CASOS VERIFICADOS COM SUCESSO!
Taxa de sucesso: 100.0%
```

#### ⚠️ Divergências Encontradas
```
⚠️ ATENÇÃO: 1 caso(s) com divergências!

⚠️ nt7_ipca_selic: Principal divergente
    Esperado: R$ 123,456.78
    Calculado: R$ 123,457.00
    Diferença: 0.0018%
```

**Ações:**
1. Se diferença < 0.01%: Arredondamento normal ✅
2. Se diferença > 1%: Investigar cálculo ❌
3. Se todos divergem: Verificar inputs ⚠️

## Casos Recomendados

### Caso 1: Sem Deságio
Valida cálculo básico sem descontos.

### Caso 2: Com Deságio Principal
Valida aplicação de desconto no principal.

### Caso 3: Com Deságio Honorários
Valida desconto nos honorários.

### Caso 4: Deságio Completo
Valida desconto em principal E honorários.

### Caso 5: Honorários Fixos
Valida honorários com valor fixo (não percentual).

## Múltiplos Municípios

Para validação completa, adicione casos de diferentes municípios:

```python
CASOS_VERIFICACAO = [
    # TIMON
    CasoVerificacao(nome="TIMON - Caso 1", ...),
    CasoVerificacao(nome="TIMON - Caso 2", ...),
    
    # SÃO LUÍS
    CasoVerificacao(nome="SAO LUIS - Caso 1", ...),
    CasoVerificacao(nome="SAO LUIS - Caso 2", ...),
    
    # IMPERATRIZ
    CasoVerificacao(nome="IMPERATRIZ - Caso 1", ...),
]
```

## Margem de Erro

Por padrão: **0.01%** (1 centavo em R$ 10.000)

Para ajustar:

```python
CasoVerificacao(
    nome="Caso Especial",
    inputs={...},
    valores_esperados={...},
    margem_erro=0.1  # 0.1% = R$ 10 em R$ 10.000
)
```

## Troubleshooting

### Erro: "Nenhum caso configurado"
```
❌ Nenhum caso de verificação configurado!
```
**Solução**: Adicione ao menos 1 caso em `CASOS_VERIFICACAO`

### Warning: "Valores zerados"
```
⚠️ ATENÇÃO: Todos os valores esperados estão zerados!
```
**Solução**: Configure `principal_esperado` com valores reais do Excel

### Erro: "Cenário não encontrado"
```
❌ Cenário 'nt7_ipca_selic' não encontrado nos resultados
```
**Solução**: Verifique nome do cenário em `OUTPUT_LINES` (calculator_service.py)

### Erro: Excel não encontrado
```
ERROR - Excel não encontrado: data/timon_01-2025.xlsx
```
**Solução**: Verifique caminho do Excel em `.env`

## Exemplo Completo

```python
# 1. Configurar caso
caso = CasoVerificacao(
    nome="TIMON - Completo",
    inputs={
        "municipio": "TIMON",
        "periodo_inicio": date(2000, 1, 1),
        "periodo_fim": date(2006, 12, 1),
        "ajuizamento": date(2005, 5, 1),
        "citacao": date(2006, 6, 1),
        "honorarios_perc": 20.0,
        "honorarios_fixo": 0.0,
        "desagio_principal": 20.0,  # 20% desconto
        "desagio_honorarios": 10.0,  # 10% desconto
        "correcao_ate": date(2025, 1, 1)
    },
    valores_esperados={
        "nt7_ipca_selic": {
            "principal_esperado": 98765.43,  # Do Excel
            "honorarios_esperado": 0.0,  # Sistema calcula: 98765.43 * 20% * 90% = 17777.78
            "total_esperado": 0.0  # Sistema calcula: 98765.43 + 17777.78 = 116543.21
        }
    }
)

# 2. Executar
verificador = VerificadorAutomatico()
resultado = verificador.verificar_caso(caso)

# 3. Verificar
if resultado['sucesso']:
    print("✅ Caso validado com sucesso!")
else:
    print("❌ Divergências encontradas:")
    for diff in resultado['diferencas']:
        print(f"  - {diff['cenario']}: {diff['diferenca_percentual']:.2f}%")
```

## Boas Práticas

1. **✅ Configure valores reais**: Sempre use valores do Excel, nunca invente
2. **✅ Teste múltiplos cenários**: Sem/com deságio, percentual/fixo
3. **✅ Valide todos os municípios**: Cada município pode ter fórmulas diferentes
4. **✅ Execute frequentemente**: A cada mudança no código
5. **✅ Documente divergências**: Se encontrar diferenças, documente o motivo

## Limitações

- ⚠️ Não valida fórmulas internas (apenas resultado final)
- ⚠️ Requer configuração manual dos valores esperados
- ⚠️ Não detecta erros na planilha Excel original

## Próximas Melhorias

- [ ] Leitura automática de valores do Excel
- [ ] Interface gráfica para configuração
- [ ] Relatório HTML com gráficos
- [ ] Integração com CI/CD
- [ ] Validação de múltiplas planilhas
