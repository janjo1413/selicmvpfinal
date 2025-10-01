# 🚀 INÍCIO RÁPIDO - Excel Local (MVP Simplificado)

## ✅ Configuração Ultra-Simples (2 minutos)

### 1️⃣ Instalar Dependências

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt
```

### 2️⃣ Configurar .env

```powershell
# Copiar arquivo de exemplo
copy .env.example .env
```

O arquivo `.env` já está configurado! Você só precisa garantir que a planilha está na pasta:

```ini
EXCEL_FILE_PATH=timon_01-2025.xlsx
```

### 3️⃣ Verificar Planilha

Certifique-se de que o arquivo Excel está na **mesma pasta** do projeto:

```
selicmvpfinal/
├── main.py
├── timon_01-2025.xlsx  ← Deve estar aqui
└── ...
```

### 4️⃣ Executar

```powershell
python main.py
```

**Acesse:** http://localhost:8000

---

## 🎯 Como Funciona (Excel Local)

```
Browser (Formulário)
       ↓
FastAPI Backend
       ↓
Abre Excel Local (openpyxl)
       ↓
Escreve inputs nas células
       ↓
Salva e reabre (força recálculo)
       ↓
Lê outputs calculados
       ↓
Retorna JSON para frontend
```

**Vantagens:**
- ✅ Sem necessidade de Azure/Microsoft Graph
- ✅ Funciona offline
- ✅ Configuração em 2 minutos
- ✅ Ideal para MVP

**Limitações:**
- ⚠️ Apenas 1 usuário por vez (arquivo fica bloqueado)
- ⚠️ Não funciona em servidor cloud sem adaptação
- ⚠️ Salva alterações no arquivo original

---

## 🧪 Testar

### Teste Rápido

1. Acesse http://localhost:8000
2. Preencha o formulário (valores padrão já estão preenchidos)
3. Clique em **Calcular**
4. Aguarde 5-15 segundos
5. Veja os 9 cenários calculados

### Teste via Script

```powershell
python test_api.py
```

---

## 📊 Estrutura da Planilha

A planilha deve ter uma aba chamada **"RESUMO"** com:

**Inputs (onde o sistema escreve):**
- B6: Município
- E6: Período Início
- F6: Período Fim
- B7: Ajuizamento
- B8: Citação
- B11: Honorários %
- B12: Honorários Fixo
- B13: Deságio Principal
- B14: Deságio Honorários
- B15: Correção até

**Outputs (de onde o sistema lê):**
- Linhas 24, 29, 34, 39, 44, 49, 54, 64, 69
- Colunas D (Principal), E (Honorários), F (Total)

---

## ⚠️ Importante

### Backup da Planilha

O sistema **salva alterações** na planilha. Faça backup antes de testar:

```powershell
copy "timon_01-2025.xlsx" "timon_01-2025.xlsx"
```

### Arquivo Aberto

Se a planilha estiver aberta no Excel, o sistema não conseguirá acessá-la. **Feche o Excel** antes de executar.

---

## 🔧 Troubleshooting

### Erro: "Arquivo Excel não encontrado"
- Verifique se o arquivo está na pasta do projeto
- Verifique o nome no `.env` (EXCEL_FILE_PATH)

### Erro: "Permission denied"
- Feche o arquivo Excel (não pode estar aberto)
- Verifique permissões da pasta

### Erro: "Aba 'RESUMO' não encontrada"
- Verifique se a planilha tem uma aba chamada "RESUMO"
- Confira maiúsculas/minúsculas

### Cálculos incorretos
- Certifique-se de que as fórmulas estão corretas na planilha
- Tente abrir e salvar manualmente a planilha uma vez

---

## 🚀 Próximos Passos

### Para Produção

Se quiser usar em produção com múltiplos usuários:

1. **Opção 1:** Migrar para Microsoft Graph (ver SETUP.md)
2. **Opção 2:** Criar cópia da planilha por sessão
3. **Opção 3:** Usar fila de jobs (apenas 1 execução por vez)

### Melhorias

- [ ] Criar cópia temporária da planilha por execução
- [ ] Adicionar lock de arquivo
- [ ] Implementar fila de processamento
- [ ] Migrar para Microsoft Graph (multi-usuário)

---

## ✅ Checklist

Antes de considerar MVP pronto:

- [ ] Planilha está na pasta do projeto
- [ ] `.env` configurado
- [ ] Dependências instaladas
- [ ] API inicia sem erros
- [ ] Formulário carrega
- [ ] Cálculo completa com sucesso
- [ ] Outputs aparecem corretamente
- [ ] CSV exporta
- [ ] Valores batem com planilha manual

---

**Versão:** 1.0.0 (Excel Local - MVP Simplificado)  
**Status:** ✅ Pronto para usar  
**Tempo de Setup:** 2 minutos  
**Última Atualização:** 01/10/2025
