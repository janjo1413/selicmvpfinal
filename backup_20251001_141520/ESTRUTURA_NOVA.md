# 📁 ESTRUTURA DO PROJETO - ORGANIZADA

## ✅ Nova Estrutura (Profissional)

```
selicmvpfinal/                    # Raiz do projeto
│
├── 📁 src/                        # ⭐ CÓDIGO FONTE
│   ├── __init__.py
│   ├── main.py                    # API FastAPI (rotas e endpoints)
│   ├── calculator_service.py     # Serviço de cálculo (lógica principal)
│   ├── excel_client.py            # Cliente Excel local (openpyxl)
│   ├── config.py                  # Configurações da aplicação
│   ├── models.py                  # Modelos Pydantic (validação)
│   └── graph_client.py            # [Legado] Cliente Microsoft Graph
│
├── 📁 static/                     # ⭐ FRONTEND
│   ├── index.html                 # Interface do usuário
│   ├── styles.css                 # Estilos CSS
│   └── script.js                  # Lógica JavaScript
│
├── 📁 tests/                      # ⭐ TESTES
│   ├── test_api.py                # Testes interativos da API
│   └── test_cases.py              # Definição de casos de teste
│
├── 📁 data/                       # ⭐ DADOS
│   └── timon_01-2025.xlsx     # Planilha Excel (motor de cálculo)
│
├── 📁 docs/                       # ⭐ DOCUMENTAÇÃO
│   ├── LEIA_ME_PRIMEIRO.md       # 🌟 COMECE AQUI
│   ├── QUICKSTART_LOCAL.md       # Guia rápido
│   ├── MUDANCAS.md               # Histórico de mudanças
│   ├── ESTRUTURA.md              # Arquitetura detalhada
│   ├── TODO.md                   # Roadmap
│   ├── DEPLOY.md                 # Guias de deploy
│   └── ... outros guias
│
├── 📁 scripts/                    # ⭐ SCRIPTS
│   ├── start.bat                  # Iniciar (Windows CMD)
│   ├── start.ps1                  # Iniciar (PowerShell)
│   └── start.sh                   # Iniciar (Linux/Mac)
│
├── 📄 app.py                      # 🚀 Entrada principal da aplicação
├── 📄 iniciar.bat                 # Atalho rápido para start.bat
├── 📄 README.md                   # README principal do projeto
├── 📄 requirements.txt            # Dependências Python
├── 📄 .env                        # Configuração (não commitar)
├── 📄 .env.example                # Exemplo de configuração
├── 📄 .gitignore                  # Arquivos ignorados pelo Git
├── 📄 Dockerfile                  # Container Docker
├── 📄 docker-compose.yml          # Orquestração Docker
├── 📄 Procfile                    # Deploy Heroku
└── 📄 runtime.txt                 # Versão Python (Heroku)
```

---

## 📊 Organização por Função

### 🐍 **Backend (Python)**
```
src/
├── main.py              → API REST (FastAPI)
├── calculator_service.py → Lógica de negócio
├── excel_client.py      → Manipulação Excel
├── config.py            → Configurações
└── models.py            → Validação de dados
```

### 🎨 **Frontend (Web)**
```
static/
├── index.html    → Interface HTML
├── styles.css    → Estilos visuais
└── script.js     → Lógica JavaScript
```

### 🧪 **Testes**
```
tests/
├── test_api.py       → Testes da API
└── test_cases.py     → Casos de teste
```

### 📊 **Dados**
```
data/
└── timon_01-2025.xlsx    → Planilha Excel
```

### 📖 **Documentação**
```
docs/
├── LEIA_ME_PRIMEIRO.md     → Início rápido
├── QUICKSTART_LOCAL.md     → Guia detalhado
├── ESTRUTURA.md            → Arquitetura
└── ...                     → Outros guias
```

### 🚀 **Scripts**
```
scripts/
├── start.bat    → Windows CMD
├── start.ps1    → PowerShell
└── start.sh     → Linux/Mac
```

---

## 🎯 Arquivos Principais

| Arquivo | Função | Importância |
|---------|--------|-------------|
| `app.py` | Entrada da aplicação | ⭐⭐⭐⭐⭐ |
| `src/main.py` | API REST | ⭐⭐⭐⭐⭐ |
| `src/calculator_service.py` | Lógica de cálculo | ⭐⭐⭐⭐⭐ |
| `src/excel_client.py` | Manipula Excel | ⭐⭐⭐⭐⭐ |
| `static/index.html` | Interface web | ⭐⭐⭐⭐ |
| `data/*.xlsx` | Dados | ⭐⭐⭐⭐⭐ |
| `.env` | Configuração | ⭐⭐⭐⭐ |
| `README.md` | Documentação | ⭐⭐⭐ |

---

## 🚀 Como Usar

### Opção 1: Atalho Rápido (Raiz)
```powershell
.\iniciar.bat
```

### Opção 2: Script na Pasta
```powershell
cd scripts
.\start.bat
```

### Opção 3: Executar Diretamente
```powershell
python app.py
```

---

## 📝 Convenções

### Nomes de Arquivos
- **Python:** `snake_case.py`
- **Markdown:** `UPPERCASE.md` ou `PascalCase.md`
- **Config:** `.lowercase`

### Estrutura de Pastas
- **src/**: Código fonte (imports relativos)
- **static/**: Arquivos servidos diretamente
- **tests/**: Testes isolados
- **docs/**: Documentação versionada
- **data/**: Arquivos de dados
- **scripts/**: Scripts executáveis

---

## 🔄 Comparação: Antes vs Depois

### ❌ **Antes (Desorganizado)**
```
selicmvpfinal/
├── main.py
├── calculator_service.py
├── excel_client.py
├── config.py
├── models.py
├── test_api.py
├── test_cases.py
├── README.md
├── SETUP.md
├── TODO.md
├── ... 20+ arquivos na raiz
└── timon_01-2025.xlsx
```
**Problemas:**
- 30+ arquivos na raiz
- Difícil encontrar código
- Confusão entre docs e código
- Planilha misturada com código

### ✅ **Depois (Organizado)**
```
selicmvpfinal/
├── src/          → Código
├── static/       → Frontend
├── tests/        → Testes
├── data/         → Planilhas
├── docs/         → Documentação
├── scripts/      → Scripts
├── app.py        → Entrada
└── README.md     → Visão geral
```
**Vantagens:**
- ✅ Estrutura clara
- ✅ Fácil navegação
- ✅ Separação de responsabilidades
- ✅ Escalável
- ✅ Profissional

---

## 🎓 Benefícios da Nova Estrutura

### 1. **Modularidade**
- Cada pasta tem um propósito claro
- Fácil adicionar novos módulos
- Imports organizados

### 2. **Manutenibilidade**
- Código fácil de encontrar
- Documentação separada
- Testes isolados

### 3. **Colaboração**
- Estrutura padrão da indústria
- Novos desenvolvedores entendem rápido
- Git diffs mais limpos

### 4. **Escalabilidade**
- Adicionar novas features é simples
- Migrar para microserviços mais fácil
- Deploy mais organizado

---

## 📦 Imports Atualizados

### Antes:
```python
from calculator_service import CalculadoraService
from models import CalculadoraInput
```

### Depois:
```python
from src.calculator_service import CalculadoraService
from src.models import CalculadoraInput
```

---

## 🔧 Configuração Atualizada

### .env (atualizado)
```ini
# Caminho atualizado para pasta data/
EXCEL_FILE_PATH=data/timon_01-2025.xlsx
```

### config.py (atualizado)
```python
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
EXCEL_FULL_PATH = BASE_DIR / EXCEL_FILE_PATH
```

---

## ✅ Checklist de Migração

- [x] Criar pastas: src/, static/, tests/, data/, docs/, scripts/
- [x] Mover arquivos Python para src/
- [x] Mover arquivos de teste para tests/
- [x] Mover documentação para docs/
- [x] Mover planilha para data/
- [x] Mover scripts para scripts/
- [x] Atualizar .env com novos caminhos
- [x] Criar app.py na raiz
- [x] Criar README.md principal
- [x] Atualizar scripts de inicialização
- [x] Criar este guia de estrutura

---

## 🎯 Próximos Passos

1. ✅ Execute `.\iniciar.bat`
2. ✅ Teste se tudo funciona
3. ✅ Leia `docs/LEIA_ME_PRIMEIRO.md`
4. ✅ Comece a desenvolver!

---

## 📞 Dúvidas?

- Leia: `docs/LEIA_ME_PRIMEIRO.md`
- Veja: `README.md` na raiz
- Consulte: `docs/QUICKSTART_LOCAL.md`

---

**Estrutura Atualizada:** 01/10/2025  
**Versão:** 2.0 (Organizada)  
**Status:** ✅ Migração completa
