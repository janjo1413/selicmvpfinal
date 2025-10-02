# 📊 Calculadora Trabalhista SELIC MVP

> Sistema web completo para cálculos trabalhistas com correção monetária e honorários

**Versão:** 1.2.0 (com APIs integradas)  
**Status:** ✅ Em produção

---

## 🚀 Início Rápido

### Executar localmente:
```powershell
# Windows
.\iniciar.bat

# Ou manualmente:
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Acesse: **http://localhost:8000**

---

## ✨ Funcionalidades Principais

### 📊 Cálculos Trabalhistas
- ✅ **9 cenários de cálculo** (NT7, NT6, JASA, NT36, etc.)
- ✅ **Honorários dinâmicos** (% + valor fixo)
- ✅ **Deságio do principal e honorários**
- ✅ **Correção monetária** até data especificada

### 📡 Integração com APIs Oficiais
- ✅ **BACEN**: SELIC (série 11) + TR (série 226)
- ✅ **IBGE**: IPCA (agregação 1737) + IPCA-E (agregação 7060)
- ✅ **Cache local**: Funciona offline com dados salvos
- ✅ **Validação automática**: Verifica disponibilidade das 4 taxas

### 💾 Backups Automáticos
Cada cálculo gera automaticamente:
- 📁 **Excel processado** (`data/output/MUNICIPIO_xxxxx_YYYYMMDD_HHMMSS.xlsx`)
- 📄 **CSV com resultados** (`data/output/MUNICIPIO_xxxxx_YYYYMMDD_HHMMSS.csv`)

### 📤 Exportação
- ✅ **Exportar CSV** via botão na interface
- ✅ **Download direto** do navegador

---

## 🏗️ Arquitetura

### Stack Tecnológica
- **Backend**: FastAPI (Python 3.13)
- **Frontend**: HTML/CSS/JavaScript vanilla
- **Excel**: openpyxl + template pré-calculado
- **APIs**: requests + cache local

### Estrutura do Projeto
```
selicmvpfinal/
├── src/                          # Código fonte
│   ├── main.py                   # API FastAPI
│   ├── calculator_service.py     # Orquestrador principal
│   ├── excel_template_calculator.py
│   ├── honorarios_calculator.py
│   ├── desagio_calculator.py
│   ├── bacen_service.py          # Cliente API BACEN
│   ├── ibge_service.py           # Cliente API IBGE
│   ├── taxas_validator.py        # Validação de taxas
│   └── models.py                 # Modelos Pydantic
├── static/                       # Frontend
│   ├── index.html
│   ├── script.js
│   └── styles.css
├── tests/                        # Testes automatizados
├── data/
│   ├── timon_01-2025.xlsx       # Template Excel
│   ├── cache/                    # Cache de APIs
│   └── output/                   # Backups automáticos
└── docs/                         # Documentação
    ├── ARCHITECTURE.md
    ├── GUIA_APIS.md
    ├── RELEASE_v1.2.0_FINAL.md
    └── arquivo/                  # Docs históricas
```

---

## 📖 Documentação

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)**: Arquitetura detalhada do sistema
- **[GUIA_APIS.md](docs/GUIA_APIS.md)**: Como usar as APIs BACEN e IBGE
- **[RELEASE_v1.2.0_FINAL.md](docs/RELEASE_v1.2.0_FINAL.md)**: Notas da versão atual
- **[TODO.md](docs/TODO.md)**: Roadmap de desenvolvimento

---

## 🧪 Testes

### Executar todos os testes:
```powershell
pytest
```

### Executar teste específico:
```powershell
python teste_rapido_v120.py  # Teste completo v1.2.0 (8 módulos)
python run_integration_tests.py  # Testes de integração
```

### Cobertura de Testes
- ✅ Cálculo de deságio
- ✅ Cálculo de honorários
- ✅ APIs BACEN (SELIC + TR)
- ✅ APIs IBGE (IPCA + IPCA-E)
- ✅ Validação de taxas
- ✅ Cache local
- ✅ Integração Excel vs Sistema

---

## 🔧 Configuração

### Variáveis de Ambiente (.env)
```bash
# Excel template
EXCEL_PATH=data/timon_01-2025.xlsx

# Cache
CACHE_DIR=data/cache

# Output
OUTPUT_DIR=data/output
```

### Dependências (requirements.txt)
```
fastapi==0.109.0
uvicorn==0.27.0
openpyxl==3.1.2
requests==2.31.0
python-dotenv==1.0.0
pydantic==2.5.3
```

---

## 📊 Fluxo de Cálculo

1. **Leitura do Template**: Sistema lê valores pré-calculados do Excel
2. **Aplicação de Deságio**: Desconto sobre o principal bruto
3. **Cálculo de Honorários**: % sobre principal líquido + valor fixo
4. **Aplicação de Deságio de Honorários**: Desconto sobre honorários
5. **Geração de Backups**: Excel + CSV salvos em `data/output/`
6. **Validação de Taxas**: Verifica APIs BACEN e IBGE
7. **Resposta**: JSON com 9 cenários calculados

---

## 🎯 Cenários Calculados

| Cenário | Descrição | Índices Utilizados |
|---------|-----------|-------------------|
| **NT7 (IPCA/SELIC/?)** | Nota Técnica 7 | IPCA, SELIC |
| **NT7 (Período CNJ)** | NT7 com período CNJ | IPCA, SELIC |
| **NT6 (IPCA/SELIC/?)** | Nota Técnica 6 | IPCA, SELIC |
| **JASA (IPCA/SELIC/?)** | Juros Acumulados | IPCA, SELIC |
| **NT7 TR** | NT7 com TR | TR |
| **NT36 TR** | Nota Técnica 36 com TR | TR |
| **NT7 IPCA-E** | NT7 com IPCA-E | IPCA-E |
| **NT36 IPCA-E** | NT36 com IPCA-E | IPCA-E |
| **NT36 IPCA-E + 1%** | NT36 IPCA-E + 1% a.m. | IPCA-E |

---

## 🐛 Troubleshooting

### APIs não funcionam?
- ✅ Sistema usa **cache local** automaticamente
- ✅ Verifique `data/cache/` para arquivos JSON
- ✅ Cache é atualizado quando API responde

### Cálculos muito lentos?
- ⚠️ Tempo médio: ~2 minutos por cálculo
- 📌 Otimização planejada para v1.3.0

### Excel salvo mostra valores diferentes?
- ✅ Abra no **Excel Desktop** (não navegador)
- ✅ Excel recalcula fórmulas automaticamente
- ✅ Compare com **CSV backup** para valores exatos

---

## 📝 Changelog

### v1.2.0 (Atual)
- ✅ Integração completa com APIs BACEN e IBGE
- ✅ Cache local para 4 taxas essenciais
- ✅ Backup automático (Excel + CSV)
- ✅ Validação automática de taxas
- ✅ Correção de formatos (datas e percentuais)

### v1.1.0
- ✅ Cálculo correto de honorários
- ✅ Deságio de honorários implementado
- ✅ 11 testes unitários

### v1.0.0
- ✅ MVP funcional
- ✅ 9 cenários de cálculo
- ✅ Interface web básica

---

## 👥 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto é privado e confidencial.

---

## 🔗 Links Úteis

- **API BACEN**: https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados
- **API IBGE**: https://servicodados.ibge.gov.br/api/v3/agregados/{agregacao}
- **Documentação FastAPI**: https://fastapi.tiangolo.com/
- **openpyxl Docs**: https://openpyxl.readthedocs.io/

---

**Desenvolvido com ❤️ para cálculos trabalhistas precisos**
