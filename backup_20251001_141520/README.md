# 🧮 Calculadora Trabalhista - MVP# 🎯 PROMPT MESTRE - MVP WEB CALCULADORA TRABALHISTA



> Aplicação web que calcula valores trabalhistas usando planilha Excel local como motor de cálculo.**Versão:** 2.0  

**Data:** 01/10/2025  

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)**Objetivo:** Criar aplicação web que usa planilha Excel como motor de cálculo com SELIC dinâmica

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)

[![Status](https://img.shields.io/badge/Status-MVP%20Ready-success.svg)]()---



---## 📋 VISÃO GERAL



## 🚀 Início RápidoAplicação web **SEM LOGIN** que:

1. Recebe inputs do usuário via formulário

### Windows (PowerShell)2. Escreve nas células mapeadas da planilha Excel

```powershell3. Atualiza dados de SELIC via API Banco Central (opcional)

.\scripts\start.bat4. Executa cálculos no Excel (via Microsoft Graph API)

```5. Lê outputs calculados

6. Exibe resultados na tela

Acesse: **http://localhost:8000**7. Permite exportar CSV



---**Princípio fundamental:** NÃO reimplementar regras de negócio. A planilha Excel é o backend de cálculo.



## 📋 Pré-requisitos---



- Python 3.8 ou superior## 🏗️ ARQUITETURA

- Arquivo Excel na pasta `data/`

- 2 minutos de tempo### Stack Recomendado

- **Backend:** Python (FastAPI) ou Node.js (Express)

---- **Frontend:** HTML/CSS/JS simples ou React

- **Armazenamento:** OneDrive/SharePoint (planilha .xlsx)

## 📂 Estrutura do Projeto- **Cálculo:** Microsoft Graph Excel API (sessão temporária)

- **SELIC:** API Banco Central SGS

```

selicmvpfinal/### Componentes

│```

├── 📁 src/                      # Código fonte┌─────────────┐      ┌──────────────┐      ┌─────────────────┐

│   ├── main.py                  # API FastAPI│   Browser   │─────▶│   Backend    │─────▶│ Microsoft Graph │

│   ├── calculator_service.py   # Lógica de cálculo│  (UI Form)  │◀─────│  (API REST)  │◀─────│   (Excel API)   │

│   ├── excel_client.py          # Cliente Excel local└─────────────┘      └──────┬───────┘      └─────────────────┘

│   ├── config.py                # Configurações                            │

│   └── models.py                # Modelos de dados                            ▼

│                     ┌──────────────┐

├── 📁 static/                   # Frontend (HTML/CSS/JS)                     │  API BACEN   │

│   ├── index.html                     │  (SGS/SELIC) │

│   ├── styles.css                     └──────────────┘

│   └── script.js```

│

├── 📁 tests/                    # Testes### Fluxo de Execução

│   ├── test_api.py```

│   └── test_cases.py1. Usuário preenche formulário

│2. Backend valida inputs

├── 📁 data/                     # Arquivos Excel3. Abre sessão Excel (Microsoft Graph)

│   └── timon_01-2025.xlsx4. [OPCIONAL] Atualiza SELIC via API BACEN

│5. Escreve inputs nas células mapeadas

├── 📁 docs/                     # Documentação6. Executa workbook.application.calculate()

│   ├── LEIA_ME_PRIMEIRO.md     ⭐ COMECE AQUI7. Lê outputs das células mapeadas

│   ├── QUICKSTART_LOCAL.md8. Fecha sessão Excel

│   ├── ESTRUTURA.md9. Retorna JSON com resultados + metadata

│   └── ...10. Frontend exibe resultados + botão "Exportar CSV"

│```

├── 📁 scripts/                  # Scripts de inicialização

│   ├── start.bat---

│   ├── start.ps1

│   └── start.sh## 📥 MAPEAMENTO DE INPUTS

│

├── app.py                       # Entrada principal### Aba: **RESUMO**

├── requirements.txt             # Dependências

├── .env                         # Configuração| Campo | Célula | Tipo | Validação | Exemplo |

└── README.md                    # Este arquivo|-------|--------|------|-----------|---------|

```| Município | B6 | String | Obrigatório | "TIMON" |

| Período (Início) | E6 | Data | AAAA-MM-DD | "2000-01-01" |

---| Período (Fim) | F6 | Data | AAAA-MM-DD | "2006-12-01" |

| Ajuizamento | B7 | Data | AAAA-MM-DD | "2005-05-01" |

## 📖 Documentação| Citação | B8 | Data | AAAA-MM-DD | "2006-06-01" |

| Honorários (%) | B11 | Decimal | 0.00 - 1.00 | 0.15 (15%) |

| Documento | Descrição || Honorários (fixo) | B12 | Decimal | ≥ 0 | 5000.00 |

|-----------|-----------|| Deságio Principal | B13 | Decimal | 0.00 - 1.00 | 0.20 (20%) |

| **[docs/LEIA_ME_PRIMEIRO.md](docs/LEIA_ME_PRIMEIRO.md)** | ⭐ **Comece por aqui!** || Deságio Honorários | B14 | Decimal | 0.00 - 1.00 | 0.20 (20%) |

| [docs/QUICKSTART_LOCAL.md](docs/QUICKSTART_LOCAL.md) | Guia rápido Excel local || Correção até | B15 | Data | AAAA-MM-DD | "2025-01-01" |

| [docs/MUDANCAS.md](docs/MUDANCAS.md) | O que mudou? |

| [docs/ESTRUTURA.md](docs/ESTRUTURA.md) | Arquitetura detalhada |### Validações Frontend

| [docs/TODO.md](docs/TODO.md) | Roadmap e próximas fases |- Datas: formato AAAA-MM-DD, não pode ser futura

- Percentuais: 0-100% (converter para decimal no backend)

---- Moeda: aceitar R$ 1.234,56 (converter para decimal)

- Período Fim > Período Início

## 🎯 Funcionalidades- Correção até ≥ Período Fim



- ✅ Formulário web para entrada de dados---

- ✅ Integração com Excel local (openpyxl)

- ✅ Cálculo de 9 cenários trabalhistas## 📤 MAPEAMENTO DE OUTPUTS

- ✅ Exportação de resultados em CSV

- ✅ Interface responsiva### Aba: **RESUMO**

- ✅ Rate limiting (10 req/min)

- ✅ Validações automáticasTodos os outputs estão em **3 colunas**:

- **Coluna D:** Principal (após deságio)

---- **Coluna E:** Honorários %

- **Coluna F:** Total (Principal + Honorários)

## 🔧 Configuração

| Cenário | Linha | D (Principal) | E (Hon. %) | F (Total) |

### 1. Instalar dependências|---------|-------|---------------|------------|-----------|

| NT7 (IPCA/SELIC/?) | 24 | D24 | E24 | F24 |

```powershell| NT7 (Período CNJ) | 29 | D29 | E29 | F29 |

python -m venv venv| NT6 (IPCA/SELIC/?) | 34 | D34 | E34 | F34 |

.\venv\Scripts\Activate.ps1| JASA (IPCA/SELIC/?) | 39 | D39 | E39 | F39 |

pip install -r requirements.txt| NT7 TR | 44 | D44 | E44 | F44 |

```| NT36 TR | 49 | D49 | E49 | F49 |

| NT7 IPCA-E | 54 | D54 | E54 | F54 |

### 2. Configurar .env| NT36 IPCA-E | 64 | D64 | E64 | F64 |

| NT36 IPCA-E + 1% a.m. | 69 | D69 | E69 | F69 |

O arquivo `.env` já está configurado! Verifique apenas o caminho do Excel:

**Total de células a ler:** 27 (9 cenários × 3 colunas)

```ini

EXCEL_FILE_PATH=data/timon_01-2025.xlsx### Formato JSON de Resposta

``````json

{

### 3. Executar  "run_id": "uuid-v4",

  "timestamp": "2025-01-15T14:30:00Z",

```powershell  "workbook_version": "etag-ou-hash",

python app.py  "inputs": { /* echo dos inputs */ },

# OU  "outputs": {

.\scripts\start.bat    "nt7_ipca_selic": {

```      "principal": 123456.78,

      "honorarios": 18518.52,

---      "total": 141975.30

    },

## 🧪 Testar    "nt7_periodo_cnj": { /* ... */ },

    // ... demais cenários

### Teste Manual  },

1. Acesse http://localhost:8000  "selic_context": {

2. Preencha o formulário    "updated": false,

3. Clique em "Calcular"    "message": "SELIC não atualizada nesta execução"

4. Veja os 9 cenários  }

}

### Teste Automatizado```

```powershell

python tests/test_api.py---

```

## 📊 SELIC DINÂMICA (FASE 2)

---

### ⚠️ IMPORTANTE - Estrutura Existente

## 📊 Cenários Calculados

A planilha **JÁ possui** aba **"Tabela de Correão e Juros"** com dados históricos.  

A aplicação calcula **9 cenários** diferentes:**NÃO criar novas abas na FASE 1.**



1. NT7 (IPCA/SELIC/?)### API Banco Central SGS

2. NT7 (Período CNJ)

3. NT6 (IPCA/SELIC/?)**Endpoint Base:**

4. JASA (IPCA/SELIC/?)```

5. NT7 TRhttps://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json&dataInicial=DD/MM/AAAA&dataFinal=DD/MM/AAAA

6. NT36 TR```

7. NT7 IPCA-E

8. NT36 IPCA-E**Séries Candidatas:**

9. NT36 IPCA-E + 1% a.m.- **11:** SELIC diária (over)

- **432:** Meta SELIC (% a.a.)

---- **4390:** SELIC acumulada no mês

- **4189:** SELIC acumulada no mês (anualizada base 252)

## 🏗️ Arquitetura

**Exemplo de Resposta:**

``````json

Browser (Formulário)[

       ↓  {"data": "01/01/2024", "valor": "11.75"},

FastAPI Backend (src/main.py)  {"data": "01/02/2024", "valor": "11.25"}

       ↓]

Calculator Service (src/calculator_service.py)```

       ↓

Excel Client (src/excel_client.py)### Estratégia de Implementação

       ↓

Arquivo Excel Local (data/)#### FASE 1 - MVP SEM SELIC (Recomendado)

       ↓- ✅ Usar dados de SELIC já presentes na planilha

Resultados (JSON + CSV)- ✅ NÃO modificar estrutura de abas

```- ✅ Focar em: inputs → cálculo → outputs



---#### FASE 2 - SELIC Dinâmica

1. **Investigação (1 semana):**

## 📦 Tecnologias   - Abrir aba "Tabela de Correão e Juros"

   - Identificar coluna(s) com SELIC (provavelmente coluna K)

- **Backend:** Python 3.11 + FastAPI   - Mapear faixa de células (ex: K10:K350)

- **Frontend:** HTML5 + CSS3 + JavaScript   - Testar atualização manual de 1 valor

- **Excel:** openpyxl

- **Validação:** Pydantic2. **Implementação:**

   ```python

---   # Pseudocódigo

   def atualizar_selic(session, periodo_inicio, periodo_fim):

## ⚠️ Importante       # 1. Consultar API BACEN

       dados = bacen_api.get_selic(periodo_inicio, periodo_fim)

- **Feche o Excel** antes de usar o sistema       

- **Faça backup** da planilha original       # 2. Preparar range de células

- Sistema funciona para **1 usuário por vez** (ideal para MVP)       range_address = "Tabela de Correão e Juros!K10:K350"

       

---       # 3. Escrever valores

       for linha, valor in enumerate(dados):

## 🚀 Próximos Passos           session.range(f"K{10+linha}").update(valor)

       

1. Execute `.\scripts\start.bat`       # 4. Salvar metadados

2. Teste com dados de exemplo       return {

3. Valide outputs com planilha manual           "updated": True,

4. Leia a documentação completa em `docs/`           "count": len(dados),

           "source": "API BACEN SGS série 432"

---       }

   ```

## 🐛 Troubleshooting

### Política de Lacunas

### Erro: "Arquivo Excel não encontrado"

- Verifique se a planilha está em `data/`**Modo Estrito (fail-fast):**

- Confira o nome no `.env````python

if competencia_faltando:

### Erro: "Permission denied"    raise ValueError(f"SELIC não disponível para {competencia}")

- Feche o arquivo Excel```

- Verifique permissões da pasta

**Modo Permissivo (carry-forward):**

Ver mais em: **[docs/QUICKSTART_LOCAL.md](docs/QUICKSTART_LOCAL.md)**```python

if competencia_faltando:

---    valor = ultima_competencia_disponivel

    warnings.append(f"Usando SELIC de {ultima_data}: {valor}%")

## 📄 Licença```



MIT License### Fallbacks



---1. **Override Manual:**

   ```json

## 👤 Autor   {

     "selic_override": {

Desenvolvido conforme especificação do Prompt Mestre v2.0       "2025-01": 10.75  // Força este valor apenas para esta execução

     }

---   }

   ```

## 📞 Suporte

2. **Importar CSV:**

- 📖 Documentação: Ver pasta `docs/`   ```csv

- 🐛 Issues: GitHub   data,taxa_anual

- 💬 Dúvidas: Consultar [docs/QUICKSTART_LOCAL.md](docs/QUICKSTART_LOCAL.md)   2024-01-01,11.75

   2024-02-01,11.25

---   ```



<div align="center">### Aba de Auditoria (FASE 2)



**⭐ Se este projeto foi útil, deixe uma estrela!**Criar aba **`selic_resolver`** para log:



---| Competência | Valor Usado | Fonte | Timestamp |

|-------------|-------------|-------|-----------|

**Versão:** 1.0.0 (Excel Local - MVP)  | 2024-01 | 11.75 | API BACEN | 2025-01-15 14:30 |

**Status:** ✅ Pronto para usar  | 2024-02 | 11.25 | API BACEN | 2025-01-15 14:30 |

**Última Atualização:** 01/10/2025| 2025-01 | 10.75 | Override | 2025-01-15 14:30 |



</div>---


## 🔌 MICROSOFT GRAPH API

### Setup
1. Registrar app no Azure AD
2. Permissões necessárias: `Files.ReadWrite`, `Sites.ReadWrite.All`
3. Obter token OAuth2

### Endpoints Principais

```javascript
// 1. Criar sessão de trabalho
POST /me/drive/items/{item-id}/workbook/createSession
{
  "persistChanges": false  // Sessão temporária
}

// 2. Escrever inputs
PATCH /me/drive/items/{item-id}/workbook/worksheets/RESUMO/range(address='B6')
{
  "values": [["TIMON"]]
}

// 3. Executar cálculo
POST /me/drive/items/{item-id}/workbook/application/calculate
{
  "calculationType": "Full"
}

// 4. Ler outputs
GET /me/drive/items/{item-id}/workbook/worksheets/RESUMO/range(address='D24:F69')

// 5. Fechar sessão
DELETE /me/drive/items/{item-id}/workbook/closeSession
```

### Timeout
- Sessão expira em **7 minutos** sem atividade
- Implementar retry se sessão expirar
- Timeout máximo de execução: **60 segundos**

---

## 💾 PERSISTÊNCIA (Mínima)

### Salvar por Execução
```json
{
  "run_id": "uuid",
  "timestamp": "ISO 8601",
  "workbook_version": "etag-ou-sha256",
  "inputs": { /* objeto JSON */ },
  "outputs": { /* objeto JSON */ },
  "selic_context": {
    "updated": true/false,
    "source": "API BACEN / CSV / Override",
    "competencias": [
      {"data": "2024-01", "valor": 11.75, "fonte": "API"}
    ]
  },
  "execution_time_ms": 8234
}
```

### Storage
- **FASE 1:** SQLite local ou arquivos JSON
- **FASE 2+:** PostgreSQL ou MongoDB

---

## 🎨 INTERFACE (UI)

### Página Única (SPA)

```
┌─────────────────────────────────────────────┐
│  🧮 Calculadora Trabalhista                 │
├─────────────────────────────────────────────┤
│  📝 Dados do Processo                       │
│  ┌─────────────────────────────────────┐   │
│  │ Município:        [____________]    │   │
│  │ Período Início:   [__/__/____]      │   │
│  │ Período Fim:      [__/__/____]      │   │
│  │ Ajuizamento:      [__/__/____]      │   │
│  │ Citação:          [__/__/____]      │   │
│  │ Honorários (%):   [____]%           │   │
│  │ Honorários (R$):  R$ [__________]   │   │
│  │ Deságio Principal: [____]%          │   │
│  │ Deságio Honorários: [____]%         │   │
│  │ Correção até:     [__/__/____]      │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  [🔄 SELIC: Usar dados atuais ☐]           │
│  [⚙️ Calcular]                              │
├─────────────────────────────────────────────┤
│  📊 Resultados (após cálculo)               │
│  ┌─────────────────────────────────────┐   │
│  │ NT7 (IPCA/SELIC/?):                 │   │
│  │ • Principal: R$ 123.456,78          │   │
│  │ • Honorários: R$ 18.518,52          │   │
│  │ • Total: R$ 141.975,30              │   │
│  │                                      │   │
│  │ NT7 (Período CNJ):                  │   │
│  │ • Principal: R$ 98.765,43           │   │
│  │ ...                                  │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  [📥 Exportar CSV]  [🔗 Copiar Link]       │
│                                             │
│  ℹ️ Run ID: abc-123 | 15/01/2025 14:30     │
└─────────────────────────────────────────────┘
```

### Elementos Principais
- ✅ Formulário com validação em tempo real
- ✅ Loading spinner durante cálculo (5-30s)
- ✅ Exibição clara dos 9 cenários
- ✅ Botão "Exportar CSV" (gera arquivo local)
- ✅ Mensagem de SELIC usada (se FASE 2)
- ✅ Responsivo (mobile-friendly)

---

## 📤 EXPORTAÇÃO CSV

### Formato
```csv
Cenário,Principal,Honorários,Total
NT7 (IPCA/SELIC/?),123456.78,18518.52,141975.30
NT7 (Período CNJ),98765.43,14814.81,113580.24
NT6 (IPCA/SELIC/?),110000.00,16500.00,126500.00
JASA (IPCA/SELIC/?),105000.00,15750.00,120750.00
NT7 TR,95000.00,14250.00,109250.00
NT36 TR,92000.00,13800.00,105800.00
NT7 IPCA-E,115000.00,17250.00,132250.00
NT36 IPCA-E,112000.00,16800.00,128800.00
NT36 IPCA-E + 1% a.m.,118000.00,17700.00,135700.00

Inputs:
Município,TIMON
Período,2000-01-01 a 2006-12-01
Ajuizamento,2005-05-01
Citação,2006-06-01
Honorários,%,0.15
Honorários,Fixo,5000.00
Deságio,Principal,0.20
Deságio,Honorários,0.20
Correção até,2025-01-01

Metadata:
Run ID,abc-123-def
Timestamp,2025-01-15T14:30:00Z
Workbook Version,v1.2.3
```

---

## ✅ CRITÉRIOS DE ACEITE

### FASE 1 - MVP Básico
- [ ] Backend conecta ao Microsoft Graph e abre/fecha sessão
- [ ] Escreve 10 inputs nas células corretas (B6, E6, F6, B7, B8, B11-B15)
- [ ] Executa `calculate()` com sucesso
- [ ] Lê 27 outputs (D/E/F nas linhas 24,29,34,39,44,49,54,64,69)
- [ ] UI exibe resultados formatados (moeda brasileira)
- [ ] Exportação CSV funciona e contém todos os dados
- [ ] **3 casos de teste com outputs idênticos à planilha manual** (diferença < 0.01%)

### FASE 2 - SELIC Dinâmica (Opcional)
- [ ] Identifica coluna SELIC na aba "Tabela de Correão e Juros"
- [ ] Consulta API BACEN com sucesso (séries 11/432/4390/4189)
- [ ] Atualiza células de SELIC sem quebrar fórmulas
- [ ] Modo Estrito bloqueia se faltar competência
- [ ] Modo Permissivo usa carry-forward e alerta usuário
- [ ] Fallback CSV funciona
- [ ] Override manual funciona
- [ ] Aba `selic_resolver` registra auditoria
- [ ] Caso de teste com SELIC recente (2024/2025) passa

---

## 🧪 CASOS DE TESTE

### Caso 1: Timon Real (Validação)
```json
{
  "inputs": {
    "municipio": "TIMON",
    "periodo_inicio": "2000-01-01",
    "periodo_fim": "2006-12-01",
    "ajuizamento": "2005-05-01",
    "citacao": "2006-06-01",
    "honorarios_perc": 0.0,
    "honorarios_fixo": 0.0,
    "desagio_principal": 0.2,
    "desagio_honorarios": 0.2,
    "correcao_ate": "2025-01-01"
  }
}
```
**Objetivo:** Valores devem bater 100% com planilha manual.

### Caso 2: Honorários Percentual
```json
{
  "inputs": {
    "municipio": "SAO LUIS",
    "periodo_inicio": "2010-01-01",
    "periodo_fim": "2015-12-01",
    "ajuizamento": "2014-03-01",
    "citacao": "2015-06-01",
    "honorarios_perc": 0.15,
    "honorarios_fixo": 0.0,
    "desagio_principal": 0.1,
    "desagio_honorarios": 0.05,
    "correcao_ate": "2024-12-01"
  }
}
```
**Objetivo:** Testar cálculo de honorários percentuais.

### Caso 3: SELIC Recente (FASE 2)
```json
{
  "inputs": {
    "municipio": "FORTALEZA",
    "periodo_inicio": "2023-01-01",
    "periodo_fim": "2024-12-01",
    "ajuizamento": "2024-06-01",
    "citacao": "2024-09-01",
    "honorarios_perc": 0.2,
    "honorarios_fixo": 0.0,
    "desagio_principal": 0.0,
    "desagio_honorarios": 0.0,
    "correcao_ate": "2025-01-01"
  },
  "selic_atualizar": true
}
```
**Objetivo:** Garantir que SELIC 2024/2025 seja atualizada via API BACEN.

---

## 📊 OBSERVABILIDADE

### Logs Obrigatórios
```python
logger.info(f"[{run_id}] Iniciando execução")
logger.info(f"[{run_id}] Inputs validados: {inputs}")
logger.info(f"[{run_id}] Abrindo sessão Excel (workbook_id: {workbook_id})")
logger.info(f"[{run_id}] Escrevendo inputs nas células B6-B15")
logger.info(f"[{run_id}] Executando calculate() - aguarde...")
logger.info(f"[{run_id}] Cálculo concluído em {calc_time}ms")
logger.info(f"[{run_id}] Lendo outputs D24:F69")
logger.info(f"[{run_id}] Fechando sessão Excel")
logger.info(f"[{run_id}] Execução concluída em {total_time}ms")
```

### Métricas (FASE 2+)
- Tempo médio de execução
- Taxa de sucesso/erro
- Chamadas API BACEN (count, latência)
- Sessões Excel (abertas, fechadas, expiradas)

---

## 🚨 TRATAMENTO DE ERROS

### Erros Comuns
1. **Sessão Excel expirada:**
   ```python
   if error.code == "SessionExpired":
       retry_with_new_session()
   ```

2. **Célula não encontrada:**
   ```python
   if error.code == "ItemNotFound":
       raise ValueError(f"Célula {address} não existe na planilha")
   ```

3. **API BACEN indisponível:**
   ```python
   if bacen_api.timeout():
       logger.warning("API BACEN indisponível, usando dados locais")
       use_fallback_csv()
   ```

4. **Cálculo muito lento (>60s):**
   ```python
   if execution_time > 60:
       raise TimeoutError("Cálculo excedeu 60 segundos")
   ```

---

## 🔒 SEGURANÇA (Mínima)

- ✅ Validar todos os inputs (tipo, range, formato)
- ✅ Sanitizar strings antes de escrever no Excel
- ✅ Rate limiting: 10 execuções/minuto por IP
- ✅ Timeout: 60s por execução
- ✅ Não expor token Microsoft Graph no frontend
- ✅ HTTPS obrigatório em produção

---

## 📦 ENTREGÁVEIS

### FASE 1
1. ✅ Código fonte (backend + frontend)
2. ✅ README com instruções de setup
3. ✅ 3 casos de teste documentados com outputs esperados
4. ✅ Scripts de deploy (Docker/Heroku/Vercel)

### FASE 2
5. ✅ Documentação de integração API BACEN
6. ✅ Scripts de fallback CSV
7. ✅ Aba `selic_resolver` na planilha

---

## 🎓 REFERÊNCIAS

### APIs
- Microsoft Graph Excel: https://learn.microsoft.com/graph/api/resources/excel
- BACEN SGS: https://www3.bcb.gov.br/sgspub/

### Bibliotecas
**Python:**
```bash
pip install fastapi uvicorn requests openpyxl pandas python-dotenv
```

**Node.js:**
```bash
npm install express @microsoft/microsoft-graph-client axios dotenv
```

---

## ✅ CHECKLIST FINAL

### Antes de Começar
- [ ] Ler este documento completo
- [ ] Confirmar acesso à planilha no OneDrive/SharePoint
- [ ] Registrar app no Azure AD (Microsoft Graph)
- [ ] Escolher stack (Python ou Node.js)
- [ ] Clonar repositório e configurar ambiente

### Durante Desenvolvimento
- [ ] Implementar backend (inputs → cálculo → outputs)
- [ ] Implementar frontend (formulário + resultados)
- [ ] Adicionar validações
- [ ] Implementar exportação CSV
- [ ] Executar 3 casos de teste
- [ ] Documentar setup no README

### Antes de Entregar
- [ ] Outputs idênticos à planilha manual (3 casos)
- [ ] UI responsiva em mobile
- [ ] Logs funcionando
- [ ] Deploy em ambiente de teste
- [ ] Documentação completa

---

**FIM DO PROMPT MESTRE**

**Versão:** 2.0  
**Última Atualização:** 01/10/2025  
**Validado com:** `timon_01-2025.xlsx`
