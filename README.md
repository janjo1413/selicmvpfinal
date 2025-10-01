#  Calculadora Trabalhista MVP

> Sistema web que calcula valores trabalhistas usando Excel local como motor de cálculo

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)

---

##  Início Rápido

```powershell
pip install -r requirements.txt
.\iniciar.bat
```

Acesse: **http://localhost:8000** 

---

##  Estrutura

```
src/           Código Python
static/        Interface web
data/          Excel (timon_01-2025.xlsx)
tests/         Testes
docs/          Documentação detalhada
```

---

##  Configuração (.env)

```ini
EXCEL_FILE_PATH=data/timon_01-2025.xlsx
API_PORT=8000
```

---

##  API Endpoints

**POST** `/api/calcular` - Calcula valores  
**GET** `/api/exportar-csv` - Exporta CSV

---

##  Documentação Completa

- [QUICKSTART_LOCAL.md](docs/QUICKSTART_LOCAL.md) - Setup local
- [SETUP.md](docs/SETUP.md) - Configuração avançada
- [DEPLOY.md](docs/DEPLOY.md) - Deploy produção
- [TODO.md](docs/TODO.md) - Roadmap

---

##  Problemas Comuns

**Excel não encontrado:** `ls data\*.xlsx`  
**Porta em uso:** Mude `API_PORT` no `.env`  
**Erro módulos:** `pip install -r requirements.txt --force-reinstall`

---

##  Importante

Faça backup do Excel antes de usar!

```powershell
Copy-Item data\timon_01-2025.xlsx data\backup.xlsx
```

---

**v2.1** | 01/10/2025 |  Produção
