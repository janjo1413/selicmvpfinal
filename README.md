# 📊 Ca**Versão:** 1.1.0 🎉  
**Status:** ✅ Funcional com Honorários Dinâmicos

---

## ✨ Novidades v1.1.0

- ✅ **Honorários calculam corretamente!** Implementado em Python
- ✅ **Suporte a honorários percentuais e fixos**
- ✅ **Deságio de honorários funcional**
- ✅ **11 testes unitários** garantindo precisão
- ✅ **Logs detalhados** para debug

## ⚠️ Limitações Conhecidas (v1.1.0)

- **Performance**: ~2 minutos por cálculo (será otimizado na v1.2.0)
- **Deságio do Principal**: Ainda não implementado (próxima versão)

> 💡 **v1.2.0 Planejada**: Implementar deságio de principal + otimização de performance (~10s).alhista MVP

> Sistema web que calcula valores trabalhistas usando Excel local como motor de cálculo

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)

**Versão:** 1.0.0  
**Status:** ✅ Funcional

---

## ⚠️ Limitações Conhecidas (v1.0.0)

Esta versão é um MVP funcional com algumas limitações que serão resolvidas na v1.1.0:

- **Honorários (%)**: Não calcula dinamicamente. Usa valores pré-calculados do template Excel.
- **Deságio (%)**: Não calcula dinamicamente. Usa valores pré-calculados do template Excel.
- **Performance**: ~2 minutos por cálculo (será otimizado para ~10s na v1.1.0)

> � **v1.1.0 Planejada**: Reimplementação completa com cálculos nativos em Python, eliminando dependência do Excel e habilitando cálculos dinâmicos.

---

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Instalação

```powershell
pip install -r requirements.txt
.\iniciar.bat

```

### Instalação

Acesse: **http://localhost:8000** 

```bash

# 1. Clone o repositório---

git clone https://github.com/janjo1413/selicmvpfinal.git

cd selicmvpfinal##  Estrutura



# 2. Execute o instalador (Windows)```

.\iniciar.batsrc/           Código Python

```static/        Interface web

data/          Excel (timon_01-2025.xlsx)

O script vai:tests/         Testes

- ✅ Criar ambiente virtual Pythondocs/          Documentação detalhada

- ✅ Instalar dependências```

- ✅ Iniciar servidor em http://localhost:8000

---

### Uso

##  Configuração (.env)

1. Abra http://localhost:8000 no navegador

2. Preencha os dados do processo```ini

3. Clique em **Calcular**EXCEL_FILE_PATH=data/timon_01-2025.xlsx

4. Veja os 9 cenários de correçãoAPI_PORT=8000

5. **Exportar CSV** para baixar resultados```



------



## 📁 Estrutura##  API Endpoints



```**POST** `/api/calcular` - Calcula valores  

selicmvpfinal/**GET** `/api/exportar-csv` - Exporta CSV

├── app.py                 # Entry point

├── src/                   # Backend Python---

│   ├── main.py           # FastAPI app

│   ├── calculator_service.py##  Documentação Completa

│   ├── excel_template_calculator.py

│   ├── models.py- [QUICKSTART_LOCAL.md](docs/QUICKSTART_LOCAL.md) - Setup local

│   └── config.py- [SETUP.md](docs/SETUP.md) - Configuração avançada

├── static/               # Frontend- [DEPLOY.md](docs/DEPLOY.md) - Deploy produção

│   ├── index.html- [TODO.md](docs/TODO.md) - Roadmap

│   ├── styles.css

│   └── script.js---

├── data/                 # Planilhas Excel

│   └── timon_01-2025.xlsx##  Problemas Comuns

├── docs/                 # Documentação

│   └── TODO.md          # Pendências**Excel não encontrado:** `ls data\*.xlsx`  

└── iniciar.bat          # Script de inicialização**Porta em uso:** Mude `API_PORT` no `.env`  

```**Erro módulos:** `pip install -r requirements.txt --force-reinstall`



------



## 🎯 Funcionalidades##  Importante



### ✅ Implementado (v1.0.0)Faça backup do Excel antes de usar!

- 9 cenários de correção monetária:

  - NT7 (IPCA/SELIC/?)```powershell

  - NT7 (Período CNJ)Copy-Item data\timon_01-2025.xlsx data\backup.xlsx

  - NT6 (IPCA/SELIC/?)```

  - JASA (IPCA/SELIC/?)

  - NT7 TR---

  - NT36 TR

  - NT7 IPCA-E**v2.1** | 01/10/2025 |  Produção

  - NT36 IPCA-E
  - NT36 IPCA-E + 1% a.m.
- Cálculo de honorários (% ou fixo)
- Deságio configurável
- Export CSV completo
- Interface responsiva

### 🔄 Em Desenvolvimento (v1.1.0)
- Otimização de performance (112s → ~10s)
- Integração com API BACEN (SELIC dinâmica)
- Testes automatizados

---

## ⚙️ Configuração

Crie `.env` na raiz (ou copie `.env.example`):

```env
# Excel
EXCEL_FILE_PATH=data/timon_01-2025.xlsx

# API
API_HOST=0.0.0.0
API_PORT=8000

# BACEN (Fase 2)
BACEN_API_BASE=https://api.bcb.gov.br/dados/serie/bcdata.sgs
BACEN_SERIE_SELIC=432
```

---

## 🛠️ Tecnologias

- **Backend:** Python 3.13, FastAPI 0.109.0
- **Excel:** openpyxl 3.1.2 (leitura com data_only=True)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Server:** Uvicorn

---

## 📊 API Endpoints

### `POST /api/calcular`
Calcula todos os cenários.

**Request:**
```json
{
  "municipio": "TIMON",
  "periodo_inicio": "2000-01-01",
  "periodo_fim": "2006-12-01",
  "ajuizamento": "2005-05-01",
  "citacao": "2006-06-01",
  "honorarios_perc": 20.0,
  "honorarios_fixo": 0.0,
  "desagio_principal": 20.0,
  "desagio_honorarios": 20.0,
  "correcao_ate": "2025-01-01"
}
```

**Response:** JSON com 9 cenários (principal, honorários, total)

### `POST /api/exportar-csv`
Exporta resultado em CSV.

---

## 🐛 Problemas Conhecidos

1. **Performance:** Tempo de execução ~112s (otimização na v1.1.0)
2. **OneDrive:** Pode interferir com arquivos Excel (usar C:\Temp se necessário)
3. **SELIC estática:** Taxas não atualizam automaticamente (v1.1.0)

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'feat: Minha feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto é proprietário. Todos os direitos reservados.

---

## 📞 Contato

Para bugs ou sugestões:
- 🐛 Abra uma issue no GitHub
- 📧 Entre em contato com a equipe

---

## 📚 Documentação Adicional

- **Pendências:** Ver `docs/TODO.md`
- **Histórico:** Ver `CHANGELOG.md`

---

**Última atualização:** 01/10/2025
