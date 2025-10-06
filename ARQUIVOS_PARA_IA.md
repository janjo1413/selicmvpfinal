# 📚 GUIA DE CONTEXTO PARA IA

## 🎯 Arquivos Essenciais (Leia PRIMEIRO)

### 1. Documentação Principal
```
README.md                    # Visão geral, quick start, 9 cenários, troubleshooting
docs/ARCHITECTURE.md         # Arquitetura completa do sistema
CHANGELOG.md                 # Histórico de mudanças e versões
```

**Por que começar aqui**: Dá visão geral do projeto, propósito, como funciona e evolução.

---

## 🏗️ Código Core (Essencial)

### 2. Modelos de Dados
```
src/models.py               # Todas as estruturas de dados (Input/Output)
```
**O que aprende**: Estrutura dos dados, campos obrigatórios, validações Pydantic.

### 3. Serviço Principal
```
src/calculator_service.py   # Orquestrador principal do sistema
```
**O que aprende**: 
- Fluxo completo de cálculo (ler Excel → calcular → gravar → backup CSV)
- Como os 20 cenários são processados
- Sistema de backup dual (Excel + CSV)
- Formatação de dados para Excel (datas, percentagens)

### 4. Calculadoras Específicas
```
src/excel_template_calculator.py   # Gerencia Excel template e cálculo base
src/honorarios_calculator.py       # Cálculo de honorários com deságio
```
**O que aprende**:
- Como o Excel é lido e manipulado (openpyxl)
- Cálculo de honorários (% + fixo + deságio)
- Arquivos temporários e gerenciamento

### 5. Configuração
```
src/config.py               # Constantes, paths, configurações
```
**O que aprende**: Caminhos de arquivos, valores padrão, configurações do sistema.

---

## 🌐 Interface & API

### 6. API
```
app.py                      # FastAPI endpoints (/api/calcular, /api/status)
```
**O que aprende**: Endpoints disponíveis, formato de requisição/resposta, CORS.

### 7. Frontend
```
static/index.html           # Interface HTML
static/script.js            # Lógica JavaScript (fetch, formatação)
static/styles.css           # Estilos CSS
```
**O que aprende**: Como usuário interage com o sistema, UX, validações cliente.

---

## 🧪 Testes (Opcional mas Recomendado)

### 8. Testes Unitários e Integração
```
tests/test_honorarios_calculator.py     # Testes de honorários
tests/test_integracao_excel_vs_site.py  # Validação Excel vs API
tests/test_api.py                       # Testes de endpoints
```
**O que aprende**: Como sistema é testado, casos de uso, validações.

---

## 📊 Dados & Deploy

### 9. Template Excel
```
data/timon_01-2025.xlsx     # Template Excel com 20 cenários pré-calculados
```
**O que aprende**: Estrutura do Excel, abas, fórmulas, células importantes.

### 10. Deploy
```
Dockerfile                  # Containerização
docker-compose.yml          # Orquestração
requirements.txt            # Dependências Python
Procfile                    # Deploy Heroku
runtime.txt                 # Versão Python
```
**O que aprende**: Como projeto é deployado, dependências, ambiente.

---

## 📋 RESUMO: Ordem de Leitura Recomendada

### Contexto Rápido (5 arquivos - 10 min)
1. `README.md` - Visão geral
2. `docs/ARCHITECTURE.md` - Arquitetura
3. `src/models.py` - Estrutura de dados
4. `src/calculator_service.py` - Lógica principal
5. `app.py` - API endpoints

### Contexto Completo (15 arquivos - 30 min)
**Adicione aos 5 acima**:
6. `src/excel_template_calculator.py`
7. `src/honorarios_calculator.py`
8. `src/config.py`
9. `static/script.js`
10. `static/index.html`
11. `CHANGELOG.md`
12. `tests/test_integracao_excel_vs_site.py`
13. `requirements.txt`
14. `Dockerfile`
15. Skim `data/timon_01-2025.xlsx` (abas RESUMO e NT7)

### Contexto Expert (Todo o src/ e tests/)
**Para contribuição ou debug profundo**: Leia todos os arquivos acima + todos em `tests/`

---

## 🔑 Informações Críticas

### Limitações Conhecidas
- **openpyxl**: Quando salva Excel, valores calculados de fórmulas são perdidos (retornam None com `data_only=True`)
- **Solução**: Ler Excel ANTES de escrever inputs, calcular deságio/honorários em Python
- **Template TIMON**: Apenas TIMON tem valores pré-calculados; outros municípios têm dados brutos na aba "Repasse Geral"

### Fluxo Crítico
```
1. Copiar template → arquivo temporário
2. Ler valores calculados (ANTES de modificar)
3. Escrever inputs do usuário
4. Salvar Excel (fórmulas preservadas, mas valores None)
5. Copiar para output/
6. Criar CSV backup com valores lidos no passo 2
```

### Formatos Excel
- **Datas**: Passar `datetime.date` objects (não strings)
- **Percentagens**: Converter para fração (20.0 → 0.20)
- **Valores**: Float direto

---

## 💡 Dicas para IA

### Para Entender o Projeto
Leia na ordem: README → ARCHITECTURE → models.py → calculator_service.py

### Para Modificar Cálculos
Foque em: `excel_template_calculator.py`, `honorarios_calculator.py`, `calculator_service.py`

### Para Modificar API
Foque em: `app.py`, `models.py`, `static/script.js`

### Para Debug
Leia: `tests/test_integracao_excel_vs_site.py` (mostra como sistema deveria funcionar)

### Para Deploy
Leia: `Dockerfile`, `docker-compose.yml`, `requirements.txt`, `Procfile`

---

## 📝 Contexto Adicional

### Estrutura de Pastas
```
src/                # Código Python principal
static/             # Frontend (HTML/CSS/JS)
tests/              # Testes automatizados
data/               # Templates Excel e outputs
docs/               # Documentação adicional
scripts/            # Scripts auxiliares
```

### Tecnologias
- **Backend**: Python 3.13, FastAPI, openpyxl, pandas
- **Frontend**: Vanilla JS (sem frameworks)
- **Deploy**: Docker, Heroku
- **Testes**: pytest

### Cenários Suportados
20 cenários de cálculo baseados em:
- Notas Técnicas: NT7, NT6, NT36
- Correções: IPCA+SELIC, TR+SELIC
- Tipos: JASA vs Outros Índices
- Períodos: Diferentes combinações de datas

---

## ⚠️ O Que NÃO Ler (Obsoleto/Temporário)

```
docs/arquivo/               # Documentação arquivada (versões antigas)
src/__pycache__/            # Cache Python (ignorar)
tests/__pycache__/          # Cache pytest (ignorar)
*.pyc                       # Bytecode compilado (ignorar)
```

---

## 🚀 Quick Start para IA

```bash
# 1. Ler documentação
cat README.md
cat docs/ARCHITECTURE.md

# 2. Entender estrutura de dados
cat src/models.py

# 3. Entender lógica principal
cat src/calculator_service.py

# 4. Ver API
cat app.py

# 5. Ver testes (para entender casos de uso)
cat tests/test_integracao_excel_vs_site.py
```

---

**Última atualização**: Janeiro 2025
**Versão do sistema**: 1.2.0
**Autor**: Sistema de Cálculo de Honorários - TIMON
