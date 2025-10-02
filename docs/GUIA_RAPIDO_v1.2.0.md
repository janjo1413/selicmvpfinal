# 🚀 Guia Rápido - v1.2.0

## Novidades desta Versão

✅ **Deságio do Principal** - Agora funciona!  
✅ **SELIC Dinâmica** - API do Banco Central integrada  
✅ **Verificação Automática** - Valida com casos reais

---

## Início Rápido

### 1. Iniciar o Sistema
```powershell
.\iniciar.bat
```

### 2. Testar Novas Funcionalidades
```powershell
python teste_rapido.py
```

Você verá:
```
✅ Deságio do Principal: PASSOU
✅ API BACEN: PASSOU
✅ Cálculo Completo: PASSOU
🎉 Sistema funcionando!
```

### 3. Usar Interface Web
Abra: http://localhost:8000

**Novos campos disponíveis:**
- **Deságio Principal (%)**: 0 a 100
- **Deságio Honorários (%)**: 0 a 100

---

## Como Funciona Agora

### Cálculo com Deságio

**Exemplo:**
- Principal bruto (do Excel): R$ 100.000,00
- Deságio principal: 20%
- **→ Principal líquido: R$ 80.000,00**

- Honorários: 20% sobre R$ 80k = R$ 16.000,00
- Deságio honorários: 10%
- **→ Honorários líquidos: R$ 14.400,00**

- **Total: R$ 94.400,00**

### SELIC Dinâmica

O sistema agora:
1. Tenta buscar taxas atualizadas da API BACEN
2. Se offline, usa cache local
3. Se cache não existe, usa Excel

**Você verá no resultado:**
```json
"selic_context": {
  "source": "API BACEN",
  "message": "✅ 365 taxas obtidas"
}
```

---

## Validação de Cálculos

### Passo 1: Coletar Valores do Excel

1. Abra `data/timon_01-2025.xlsx`
2. Configure um cenário na aba RESUMO
3. Anote valores da coluna D (Principal)

### Passo 2: Configurar Verificação

Edite `verificacao_automatica.py`:

```python
valores_esperados={
    "nt7_ipca_selic": {
        "principal_esperado": 123456.78,  # ← Valor do Excel
        "honorarios_esperado": 0.0,
        "total_esperado": 0.0
    }
}
```

### Passo 3: Executar

```powershell
python verificacao_automatica.py
```

**Resultado esperado:**
```
✅ TODOS OS CASOS VERIFICADOS COM SUCESSO!
Taxa de sucesso: 100.0%
```

---

## Troubleshooting

### "API BACEN indisponível"
**Normal!** Sistema funciona offline usando cache.

### "Valores esperados zerados"
Configure valores reais do Excel no script de verificação.

### "Excel não encontrado"
Verifique caminho em `.env`:
```env
EXCEL_FILE_PATH=data/timon_01-2025.xlsx
```

---

## Arquivos Importantes

```
📄 README.md                    → Documentação principal
📄 teste_rapido.py              → Testar funcionalidades
📄 verificacao_automatica.py    → Validar cálculos

📁 docs/
  📄 BACEN_INTEGRATION.md       → Guia API BACEN
  📄 VERIFICACAO_AUTOMATICA.md  → Guia validação
  📄 RELEASE_v1.2.0.md          → Resumo executivo
```

---

## Próximos Passos

### Para Você (Usuário)

1. **Testar deságio**
   - Use interface web
   - Configure deságio de 10%, 20%, 30%
   - Valide resultados

2. **Validar com casos reais**
   - Configure script de verificação
   - Use valores reais de diferentes municípios
   - Execute validação

3. **Verificar SELIC**
   - Checar logs se API está funcionando
   - Ver arquivo de cache: `data/selic_cache.json`

### Para Próxima Versão (v1.3.0)

1. **Aplicar SELIC no cálculo**
   - Usar taxas da API no Excel
   - Validar diferenças

2. **Expandir verificação**
   - Mais municípios
   - Todos os cenários

3. **API IBGE**
   - Buscar IPCA atualizado

---

## Comandos Úteis

### Iniciar sistema
```powershell
.\iniciar.bat
```

### Testar funcionalidades
```powershell
python teste_rapido.py
```

### Validar cálculos
```powershell
python verificacao_automatica.py
```

### Ver logs
```powershell
# Logs aparecem no terminal do servidor
```

### Limpar cache SELIC
```powershell
del data\selic_cache.json
```

---

## Suporte

- 📖 Leia: `docs/RELEASE_v1.2.0.md`
- 🌐 API BACEN: `docs/BACEN_INTEGRATION.md`
- 🔍 Verificação: `docs/VERIFICACAO_AUTOMATICA.md`
- 📝 Pendências: `docs/TODO.md`

---

**v1.2.0** | 02/10/2025 | ✅ Funcional
