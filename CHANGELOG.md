# 📝 Changelog

Todas as mudanças notáveis serão documentadas neste arquivo.

---

## [1.0.0] - 2025-10-01

### ✨ Adicionado
- Sistema completo de cálculo trabalhista
- 9 cenários de correção monetária (NT7, NT6, JASA, TR, IPCA-E, etc.)
- Interface web responsiva (HTML/CSS/JS)
- Backend FastAPI com endpoints /api/calcular e /api/exportar-csv
- Integração com Excel via openpyxl (data_only=True)
- Cálculo de honorários (percentual ou fixo)
- Deságio configurável
- Export CSV completo com metadados
- Validação de inputs com Pydantic
- Logging estruturado
- Script de inicialização Windows (iniciar.bat)
- Configuração via variáveis de ambiente (.env)
- Documentação completa (README.md, docs/)

### 🔧 Técnico
- Python 3.13
- FastAPI 0.109.0
- openpyxl 3.1.2 com data_only=True
- Uvicorn com auto-reload
- Template Excel protegido (cópia temporária)
- Mapeamento INPUT/OUTPUT de células

### ⚠️ Limitações Conhecidas
- Tempo de execução: ~112 segundos (9 leituras Excel)
- SELIC estática (não atualiza automaticamente)
- Suporte apenas single-user
- Sem autenticação

---

## [Em Desenvolvimento] - v1.1.0

### 🚀 Planejado
- Otimização de performance (1 leitura Excel, ~10s total)
- Integração API BACEN (SELIC dinâmica)
- Testes automatizados (pytest)
- Cache de resultados
- Documentação API (Swagger melhorado)

---

**Formato:** [Semantic Versioning](https://semver.org/)  
**Tipos de mudança:**
- ✨ Adicionado: Novas funcionalidades
- 🔧 Alterado: Mudanças em funcionalidades existentes
- ⚠️ Deprecado: Funcionalidades que serão removidas
- 🗑️ Removido: Funcionalidades removidas
- 🐛 Corrigido: Correções de bugs
- 🔒 Segurança: Correções de vulnerabilidades
