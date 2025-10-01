# 📝 Changelog

Todas as mudanças notáveis serão documentadas neste arquivo.

---

## [1.0.0] - 2025-10-01

### ✅ Funcionalidades Implementadas
- Sistema MVP funcional com 9 cenários de cálculo
- Interface web responsiva (HTML/CSS/JS)
- Backend FastAPI com endpoints `/api/calcular` e `/api/exportar-csv`
- Integração com template Excel via openpyxl (data_only=True)
- Export CSV completo com metadados (data, hora, parâmetros)
- Validação de inputs com Pydantic
- Logging estruturado com timestamps
- Script de inicialização Windows (`iniciar.bat`)
- Botões "Novo Cálculo", "Limpar" e "Exportar CSV" funcionais
- Limpeza de código (redução de 65% dos arquivos)
- Documentação consolidada (README, CHANGELOG, TODO, ARCHITECTURE)

### ⚠️ Limitações Conhecidas
- **Honorários dinâmicos**: Usa valores pré-calculados do template Excel (limitação do openpyxl)
- **Deságio dinâmico**: Usa valores pré-calculados do template Excel
- **Performance**: ~2 minutos por cálculo (I/O de arquivos Excel)
- **Dependência Excel**: Sistema depende 100% do template Excel para fórmulas

### 📝 Notas Técnicas
- Arquitetura baseada em template Excel protegido (somente leitura)
- openpyxl não suporta recálculo de fórmulas (limitação da biblioteca)
- Valores calculados são perdidos quando workbook é salvo com openpyxl
- Solução v1.1.0: Reimplementar todas as fórmulas em Python nativo

### 🔧 Stack Técnico
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
