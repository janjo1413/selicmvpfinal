# 📋 Guia de Organização do Projeto

## 🎯 Princípios de Organização

### 1. **Minimalismo**
- ✅ Menos arquivos = Mais clareza
- ✅ 1 README principal na raiz
- ✅ Docs detalhados apenas em `docs/`
- ❌ Evitar duplicação de informação

### 2. **Separação de Responsabilidades**
```
src/       → Código Python (lógica de negócio)
static/    → Frontend (HTML/CSS/JS)
data/      → Dados (Excel, CSVs)
tests/     → Testes automatizados
docs/      → Documentação detalhada
scripts/   → Scripts auxiliares
```

### 3. **Convenções de Nomenclatura**

#### Arquivos Python
```python
# Classes: PascalCase
class CalculadoraService:
    pass

# Funções: snake_case
def calcular_valores():
    pass

# Constantes: UPPER_CASE
API_PORT = 8000
```

#### Arquivos Excel
```
[cidade]_[mes]-[ano].xlsx
```
✅ `timon_01-2025.xlsx`  
❌ `TIMON 01 2025.xlsx`

#### Arquivos de Documentação
```
UPPER_CASE.md para docs principais
lowercase.md para utilitários
```

---

## 📂 Estrutura de Pastas

### **Raiz** (mínimo essencial)
```
./
├── app.py              → Entrada principal
├── iniciar.bat         → Atalho de execução
├── requirements.txt    → Dependências
├── .env                → Configuração (não versionar)
├── .env.example        → Template de config
├── README.md           → Documentação principal
└── .gitignore          → Arquivos ignorados
```

### **src/** (código fonte)
```
src/
├── main.py                  → API FastAPI (rotas)
├── calculator_service.py   → Lógica de cálculo
├── excel_client.py          → Manipulação Excel
├── config.py                → Configurações
├── models.py                → Modelos Pydantic
└── __init__.py              → Package marker
```

**Regras:**
- ✅ 1 arquivo = 1 responsabilidade
- ✅ Máximo 300 linhas por arquivo
- ❌ Não misturar lógica de negócio com API
- ❌ Não criar subpastas desnecessárias

### **static/** (frontend)
```
static/
├── index.html    → Estrutura
├── styles.css    → Estilo
└── script.js     → Lógica
```

**Regras:**
- ✅ Vanilla JS (sem frameworks para MVP)
- ✅ CSS puro (sem preprocessadores)
- ❌ Não criar assets/images/ até necessário

### **data/** (dados)
```
data/
└── timon_01-2025.xlsx
```

**Regras:**
- ✅ Apenas arquivos Excel de trabalho
- ✅ Backups em subpasta `backups/` se necessário
- ❌ Não versionar arquivos grandes (use .gitignore)

### **tests/** (testes)
```
tests/
├── test_api.py       → Testes de API
└── test_cases.py     → Casos de teste
```

**Regras:**
- ✅ 1 arquivo de teste por módulo
- ✅ Prefixo `test_` obrigatório
- ❌ Não criar subpastas até ter 10+ arquivos

### **docs/** (documentação detalhada)
```
docs/
├── QUICKSTART_LOCAL.md    → Início rápido
├── SETUP.md               → Configuração avançada
├── DEPLOY.md              → Deploy em produção
└── TODO.md                → Roadmap
```

**Regras:**
- ✅ Máximo 5 arquivos .md
- ✅ UPPERCASE para docs principais
- ❌ Não duplicar info do README principal
- ❌ Não criar docs/ dentro de docs/

### **scripts/** (scripts auxiliares)
```
scripts/
├── start.bat     → Windows
├── start.sh      → Linux/Mac
└── start.ps1     → PowerShell
```

**Regras:**
- ✅ Scripts de inicialização/deploy
- ✅ Documentar argumentos no cabeçalho
- ❌ Não colocar lógica de negócio aqui

---

## 🚫 O Que Evitar

### ❌ Não Criar Pasta Backup na Raiz
```
# Errado:
./backup/
./backup_20251001/
./old/

# Certo:
./data/backups/
```

### ❌ Não Duplicar Documentação
```
# Errado:
README.md
docs/README.md
docs/LEIA_ME_PRIMEIRO.md
COMECE_AQUI.md

# Certo:
README.md (principal)
docs/QUICKSTART_LOCAL.md
```

### ❌ Não Criar Arquivos Temporários na Raiz
```
# Errado:
./temp.py
./test.xlsx
./backup.md

# Certo:
Use .gitignore e mantenha em /tmp ou delete após uso
```

### ❌ Não Criar Subpastas Prematuras
```
# Errado (para MVP):
src/services/
src/controllers/
src/models/
src/utils/
src/helpers/

# Certo:
src/
├── main.py
├── calculator_service.py
└── models.py
```

**Regra:** Só crie subpastas quando tiver 8+ arquivos relacionados.

---

## ✅ Checklist de Organização

Antes de commitar, verifique:

- [ ] README.md na raiz está atualizado
- [ ] Sem arquivos duplicados (*.md, *.py)
- [ ] Sem pastas de backup na raiz
- [ ] .env não está versionado
- [ ] Arquivos nomeados corretamente
- [ ] Máximo 15 itens na raiz
- [ ] Docs/ tem max 5 arquivos
- [ ] Tests/ tem prefixo test_
- [ ] Sem TODOs ou FIXMEs no código

---

## 🔧 Comandos Úteis

### Listar estrutura
```powershell
tree /F /A
```

### Contar arquivos por pasta
```powershell
Get-ChildItem -Recurse | Group-Object Directory | Select Name, Count
```

### Encontrar duplicatas
```powershell
Get-ChildItem -Recurse *.md | Group-Object Name | Where Count -gt 1
```

### Limpar arquivos temporários
```powershell
Remove-Item *.tmp, *.log, *.bak -Force
```

---

## 📊 Métricas de Qualidade

| Métrica | Ideal | Limite |
|---------|-------|--------|
| Arquivos na raiz | 10-12 | 15 |
| Arquivos em docs/ | 3-4 | 5 |
| Arquivos em src/ | 5-7 | 10 |
| Linhas por arquivo .py | 150-250 | 300 |
| Nível de subpastas | 2 | 3 |

---

## 🎯 Boas Práticas

1. **README Principal = Portal de Entrada**
   - Links para docs detalhados
   - Quickstart em 3 passos
   - Máximo 150 linhas

2. **1 Responsabilidade por Arquivo**
   - `calculator_service.py` → Lógica de cálculo
   - `excel_client.py` → Manipulação Excel
   - `main.py` → Rotas API

3. **DRY (Don't Repeat Yourself)**
   - Se a info está no README, não repita em docs/
   - Use links: `[Veja detalhes](docs/SETUP.md)`

4. **YAGNI (You Aren't Gonna Need It)**
   - Não crie estruturas para "futuro"
   - Refatore quando necessário (8+ arquivos)

5. **Mantenha Plano**
   - Estrutura plana é mais fácil de navegar
   - Subpastas apenas quando inevitável

---

## 🚀 Evolução da Estrutura

### MVP (Agora)
```
./
├── src/          (6 arquivos)
├── static/       (3 arquivos)
├── data/         (1 arquivo)
├── tests/        (2 arquivos)
├── docs/         (4 arquivos)
└── scripts/      (3 arquivos)
```

### Fase 2 (SELIC)
```
src/
├── api/          (rotas separadas)
├── services/     (lógica de negócio)
└── integrations/ (BACEN, etc)
```

### Fase 3 (Autenticação)
```
src/
├── api/
├── services/
├── auth/         (JWT, OAuth)
└── db/           (modelos SQLAlchemy)
```

**Regra:** Refatore estrutura apenas quando dor real aparecer.

---

## 📝 Template de Commit

```
feat: adicionar nova funcionalidade X
fix: corrigir bug em Y
docs: atualizar README
refactor: reorganizar estrutura de Z
test: adicionar teste para W
```

---

**Criado:** 01/10/2025  
**Versão:** 1.0  
**Autor:** Organização Inteligente ™
