# 🚨 Análise de Dependências e Riscos - Excel

**Data:** 02/10/2025  
**Crítico:** Problemas identificados com recálculo de fórmulas

---

## 🎯 Resumo Executivo

### ✅ O Que PODEMOS Ler do Excel

**Apenas valores BRUTOS que NÃO dependem de inputs da RESUMO:**

1. ✅ **Coluna D - Principal Bruto** (linhas ímpares: 23, 28, 33...)
   - Exemplo: `='NT7'!P127`
   - Referencia outras abas, cálculos estáveis
   - **Não depende de B6-B15**

### ❌ O Que NÃO PODEMOS Ler do Excel

**Qualquer valor que dependa de células B (inputs):**

2. ❌ **Coluna E - Honorários** (mesmo linhas brutas)
   - Exemplo: `='NT7'!Q127`
   - Q127 na aba = `=P127*B3`
   - B3 na aba = `=RESUMO!B11` 
   - **❌ DEPENDE DE B11 (honorários %) - Valor desatualizado!**

3. ❌ **Coluna F - Total**
   - Exemplo: `=$B$12` ou `=D23+E23`
   - **❌ DEPENDE DE B12 ou E que depende de B11**

4. ❌ **Linhas PARES - Com deságio** (24, 29, 34...)
   - Exemplo: `=D23*(1-$B$13)`
   - **❌ DEPENDE DE B13 (deságio principal)**

---

## 📊 Mapeamento Completo de Dependências

### **Cadeia de Dependências Descoberta**

```
RESUMO!B11 (Honorários %)
    ↓
Abas de Cálculo!B3 = RESUMO!B11
    ↓  
Abas de Cálculo!Q127 = P127 * B3
    ↓
RESUMO!E23 = 'Aba'!Q127
    ↓
❌ VALOR DESATUALIZADO quando B11 muda!
```

### **Exemplo Concreto**

```
1. Excel salvo com RESUMO!B11 = 10% (honorários)
   NT7!B3 = 0.10
   NT7!Q127 = P127 * 0.10 = R$ 10.000,00

2. Sistema muda RESUMO!B11 para 20%
   ✓ Escreve: B11 = 0.20
   ✗ NT7!B3 NÃO atualiza (precisa recalcular)
   ✗ NT7!Q127 ainda é = P127 * 0.10
   
3. Sistema lê RESUMO!E23 = NT7!Q127
   ❌ Retorna: R$ 10.000,00 (errado!)
   ✓ Deveria ser: R$ 20.000,00 (com 20%)

4. Usuário recebe valor incorreto!
```

---

## ✅ Solução Implementada (v1.2.0)

### **Estratégia: Ler Apenas Valores Estáveis**

```python
# ✅ LER do Excel
principal_bruto = excel.read_cell("D23")  # OK - não depende de B

# ❌ NÃO LER do Excel
# honorarios = excel.read_cell("E23")  # ✗ Desatualizado!

# ✅ CALCULAR em Python
desagio_resultado = DesagioCalculator.aplicar_desagio(
    principal_bruto=principal_bruto,
    desagio_percentual=input_dict['desagio_principal']
)

honorarios_resultado = HonorariosCalculator.calcular(
    principal=desagio_resultado['principal_liquido'],
    honorarios_perc=input_dict['honorarios_perc'],
    honorarios_fixo=input_dict['honorarios_fixo'],
    desagio_honorarios=input_dict['desagio_honorarios']
)
```

---

## 🔍 Verificação da Implementação Atual

Vou verificar se estamos lendo apenas D (principal):

```python
# Em calculator_service.py - linha ~115
for cenario_name, line_number in OUTPUT_LINES.items():
    # ✅ Lê apenas coluna D (Principal BRUTO)
    range_address = f"D{line_number}"  # ✓ Correto!
    values = excel_calc.read_range_calculated("RESUMO", range_address)
```

**Status: ✅ CORRETO!** Estamos lendo apenas coluna D.

---

## ⚠️ RISCO CRÍTICO: Taxas SELIC Desatualizadas

### **O Problema**

```
Excel tem taxas SELIC até: Janeiro/2025
Usuário calcula em: Março/2025

❌ Faltam dados de Fev e Mar/2025!
❌ Cálculo incompleto ou incorreto
```

### **Onde as Taxas São Usadas**

As abas de cálculo (NT7, NT6, etc.) usam taxas de:
- 📊 **SELIC**: Série histórica mês a mês
- 📊 **IPCA**: Índices mensais
- 📊 **TR**: Taxas mensais
- 📊 **IPCA-E**: Índices mensais

### **Solução em Andamento**

1. ✅ **API BACEN integrada** (v1.2.0)
   - Busca taxas SELIC atualizadas
   - Cache local para offline
   - Fallback automático

2. 🔄 **Próximo passo** (v1.3.0)
   - **Atualizar o Excel** com taxas da API
   - Ou **calcular SELIC em Python** (sem Excel)

---

## 📋 Checklist de Validação

### ✅ O que está SEGURO

- [x] Lemos apenas Principal Bruto (coluna D, linhas ímpares)
- [x] Aplicamos deságio em Python
- [x] Calculamos honorários em Python
- [x] Calculamos total em Python
- [x] API BACEN disponível para taxas atualizadas

### ⚠️ O que precisa ATENÇÃO

- [ ] **Taxas SELIC no Excel** - Podem ficar desatualizadas
- [ ] **Taxas IPCA no Excel** - Podem ficar desatualizadas
- [ ] **Taxas TR no Excel** - Podem ficar desatualizadas

### 🔄 Próximas Ações (v1.3.0)

1. **Detectar taxas desatualizadas**
   ```python
   ultima_taxa_excel = date(2025, 1, 31)
   data_calculo = date(2025, 3, 15)
   
   if data_calculo > ultima_taxa_excel:
       # ⚠️ Avisar usuário
       # ✓ Buscar taxas faltantes na API BACEN
       # ✓ Atualizar Excel ou calcular em Python
   ```

2. **API IBGE para IPCA/IPCA-E**
   - Similar à API BACEN
   - Buscar índices atualizados

3. **Validação automática de completude**
   ```python
   def verificar_taxas_completas(data_inicio, data_fim):
       # Verifica se Excel tem todas as taxas necessárias
       # Busca faltantes nas APIs
       # Alerta se alguma taxa não disponível
   ```

---

## 🎓 Regras de Ouro

### **O que LER do Excel**

✅ **SIM:** Valores que referenciam OUTRAS ABAS sem usar células B  
✅ **SIM:** Fórmulas que fazem cálculos internos da aba  
✅ **SIM:** Valores fixos (números, textos)

### **O que NÃO LER do Excel**

❌ **NÃO:** Fórmulas que usam `RESUMO!$B$11` até `$B$15`  
❌ **NÃO:** Fórmulas que multiplicam por `(1-$B$13)` ou similar  
❌ **NÃO:** Células que dependem de outras que mudaram

### **O que CALCULAR em Python**

✅ **SIM:** Deságio (principal e honorários)  
✅ **SIM:** Honorários (% ou fixo)  
✅ **SIM:** Total (principal + honorários)  
🔄 **FUTURO:** Correções monetárias (SELIC, IPCA, TR)

---

## 📞 Recomendações Finais

### **Para o Usuário**

1. ⚠️ **Verificar data das taxas no Excel**
   - Abrir Excel e verificar última coluna de taxas
   - Se calcular meses futuros, avisar sistema

2. ✅ **Confiar no sistema para deságio e honorários**
   - Valores sempre atualizados
   - Calculados dinamicamente

3. 🔄 **Aguardar v1.3.0 para atualização automática de taxas**

### **Para o Desenvolvedor**

1. ✅ **NUNCA ler colunas E ou F do Excel**
   - Sempre calcular em Python

2. ✅ **NUNCA ler linhas pares (24, 29, 34...)**
   - Sempre ler linhas ímpares (23, 28, 33...)

3. 🔄 **Próxima prioridade: Verificar completude das taxas**
   - Implementar detecção de lacunas
   - Integrar API BACEN no cálculo real
   - Adicionar API IBGE

---

**Status Atual:** ✅ Sistema seguro dentro das limitações conhecidas  
**Próximo Release:** v1.3.0 - Atualização automática de taxas
