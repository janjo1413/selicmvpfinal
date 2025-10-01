# 🧮 Calculadora Trabalhista - MVP

Aplicação web que calcula valores trabalhistas usando planilha Excel como motor de cálculo, integrada com Microsoft Graph API.

## 📋 Funcionalidades

- ✅ Formulário web para entrada de dados
- ✅ Integração com Microsoft Graph Excel API
- ✅ Cálculo de 9 cenários trabalhistas diferentes
- ✅ Exportação de resultados em CSV
- ✅ Rate limiting (10 requisições/minuto)
- ✅ Interface responsiva

## 🏗️ Arquitetura

- **Backend:** Python + FastAPI
- **Frontend:** HTML + CSS + JavaScript
- **Excel:** Microsoft Graph API
- **Cálculo:** Excel Online (OneDrive/SharePoint)

## 📦 Instalação

### 1. Requisitos

- Python 3.8+
- Conta Microsoft Azure
- Planilha Excel no OneDrive/SharePoint

### 2. Clonar Repositório

```bash
git clone <seu-repositorio>
cd selicmvpfinal
```

### 3. Instalar Dependências

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

### 4. Configurar Azure AD

1. Acesse [Azure Portal](https://portal.azure.com)
2. Vá em **Azure Active Directory** > **App registrations** > **New registration**
3. Configurações:
   - **Name:** Calculadora Trabalhista
   - **Supported account types:** Single tenant
   - **Redirect URI:** (deixe vazio por enquanto)
4. Após criar, anote:
   - **Application (client) ID**
   - **Directory (tenant) ID**
5. Vá em **Certificates & secrets** > **New client secret**
   - Anote o **Value** (CLIENT_SECRET)
6. Vá em **API permissions** > **Add a permission**
   - Microsoft Graph > Application permissions
   - Adicione: `Files.ReadWrite.All`, `Sites.ReadWrite.All`
   - Clique em **Grant admin consent**

### 5. Obter IDs da Planilha

#### Método 1: Via OneDrive Web
1. Abra a planilha no OneDrive
2. URL será algo como: `https://onedrive.live.com/...?id=XXXXXXXX`
3. O `id=` é seu WORKBOOK_ID

#### Método 2: Via Microsoft Graph Explorer
```bash
# Acesse: https://developer.microsoft.com/graph/graph-explorer
# Execute: GET /me/drive/root/children
# Procure sua planilha e copie o "id"
```

### 6. Configurar Variáveis de Ambiente

```bash
# Copie o arquivo de exemplo
copy .env.example .env

# Edite .env com seus dados:
CLIENT_ID=seu_client_id
CLIENT_SECRET=seu_client_secret
TENANT_ID=seu_tenant_id
WORKBOOK_ID=id_da_planilha_excel
DRIVE_ID=id_do_drive  # Opcional, use se não for /me/drive
```

### 7. Executar Aplicação

```bash
python main.py
```

Acesse: http://localhost:8000

## 🧪 Testes

### Caso de Teste 1: Timon Real

```json
{
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
```

**Objetivo:** Validar que os valores calculados batem 100% com a planilha manual.

## 📊 Mapeamento de Células

### Inputs (Aba: RESUMO)

| Campo | Célula | Tipo |
|-------|--------|------|
| Município | B6 | String |
| Período Início | E6 | Data |
| Período Fim | F6 | Data |
| Ajuizamento | B7 | Data |
| Citação | B8 | Data |
| Honorários (%) | B11 | Decimal |
| Honorários (fixo) | B12 | Decimal |
| Deságio Principal | B13 | Decimal |
| Deságio Honorários | B14 | Decimal |
| Correção até | B15 | Data |

### Outputs (Aba: RESUMO)

| Cenário | Linha | Colunas (D/E/F) |
|---------|-------|-----------------|
| NT7 (IPCA/SELIC/?) | 24 | Principal/Hon./Total |
| NT7 (Período CNJ) | 29 | Principal/Hon./Total |
| NT6 (IPCA/SELIC/?) | 34 | Principal/Hon./Total |
| JASA (IPCA/SELIC/?) | 39 | Principal/Hon./Total |
| NT7 TR | 44 | Principal/Hon./Total |
| NT36 TR | 49 | Principal/Hon./Total |
| NT7 IPCA-E | 54 | Principal/Hon./Total |
| NT36 IPCA-E | 64 | Principal/Hon./Total |
| NT36 IPCA-E + 1% a.m. | 69 | Principal/Hon./Total |

## 🔌 API Endpoints

### POST /api/calcular

Executa cálculo trabalhista.

**Request:**
```json
{
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
```

**Response:**
```json
{
  "run_id": "uuid",
  "timestamp": "2025-10-01T10:00:00",
  "workbook_version": "etag",
  "inputs": {...},
  "outputs": {
    "nt7_ipca_selic": {
      "principal": 123456.78,
      "honorarios": 18518.52,
      "total": 141975.30
    },
    ...
  },
  "selic_context": {...},
  "execution_time_ms": 8234
}
```

### POST /api/exportar-csv

Exporta resultado em CSV.

**Request:** Objeto JSON do resultado
**Response:** Arquivo CSV para download

## 🚨 Troubleshooting

### Erro: "Unauthorized"
- Verifique CLIENT_ID, CLIENT_SECRET e TENANT_ID
- Confirme que deu "Grant admin consent" nas permissões

### Erro: "ItemNotFound"
- Verifique WORKBOOK_ID
- Confirme que a planilha está acessível

### Erro: "SessionExpired"
- Normal após 7 minutos de inatividade
- O sistema tenta recriar automaticamente

### Cálculo muito lento
- Planilha pode ter muitas fórmulas
- Considere otimizar a planilha Excel

## 📚 Documentação

- [Microsoft Graph Excel API](https://learn.microsoft.com/graph/api/resources/excel)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Prompt Mestre](README.md) - Especificação completa

## 🔒 Segurança

- ✅ Validação de inputs
- ✅ Rate limiting (10 req/min)
- ✅ Timeout de 60s por execução
- ✅ Sessões Excel temporárias (não persiste)
- ⚠️ **Use HTTPS em produção**
- ⚠️ **Não commite .env no Git**

## 📝 TODO - FASE 2

- [ ] Integração com API BACEN para SELIC dinâmica
- [ ] Modo estrito vs permissivo para lacunas de SELIC
- [ ] Fallback CSV para SELIC
- [ ] Override manual de SELIC
- [ ] Aba de auditoria `selic_resolver`
- [ ] Persistência em banco de dados
- [ ] Dashboard de métricas

## 📄 Licença

MIT

## 👤 Autor

Desenvolvido conforme especificações do Prompt Mestre v2.0

---

**Versão:** 1.0.0 (FASE 1 - MVP Básico)  
**Status:** ✅ Funcional  
**Última Atualização:** 01/10/2025
