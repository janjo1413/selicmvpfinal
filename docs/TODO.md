# 🚧 TODO - Roadmap do Projeto

## ✅ FASE 1 - MVP Básico (CONCLUÍDA)

- [x] Estrutura do projeto
- [x] Backend FastAPI
- [x] Cliente Microsoft Graph
- [x] Mapeamento de inputs/outputs
- [x] Frontend HTML/CSS/JS
- [x] Validações de formulário
- [x] Rate limiting
- [x] Exportação CSV
- [x] Casos de teste
- [x] Documentação
- [x] Scripts de deploy

## 🔄 FASE 2 - SELIC Dinâmica (OPCIONAL)

### 2.1 Investigação (1 semana)
- [ ] Abrir planilha e identificar aba "Tabela de Correão e Juros"
- [ ] Mapear estrutura de colunas (identificar coluna SELIC)
- [ ] Identificar faixa de células com SELIC
- [ ] Testar atualização manual de 1 valor
- [ ] Validar que atualização não quebra fórmulas

### 2.2 API BACEN
- [ ] Implementar cliente para API BACEN SGS
- [ ] Testar séries: 11, 432, 4390, 4189
- [ ] Definir qual série usar (recomendação: 432 - Meta SELIC)
- [ ] Implementar cache de consultas
- [ ] Tratamento de erros e timeout

### 2.3 Atualização de SELIC
- [ ] Implementar função `atualizar_selic()` no `calculator_service.py`
- [ ] Escrever valores no range correto da planilha
- [ ] Validar que cálculos refletem novos valores
- [ ] Adicionar flag `selic_atualizar` no input

### 2.4 Políticas de Lacunas
- [ ] Implementar modo **Estrito** (fail-fast)
- [ ] Implementar modo **Permissivo** (carry-forward)
- [ ] Adicionar warnings/alertas no frontend
- [ ] Configuração via .env ou input

### 2.5 Fallbacks
- [ ] Override manual via JSON input
- [ ] Importação de CSV com SELIC customizada
- [ ] Validação de formato CSV
- [ ] Merge de dados BACEN + CSV

### 2.6 Auditoria
- [ ] Criar aba `selic_resolver` na planilha
- [ ] Registrar competências atualizadas
- [ ] Registrar fonte de dados (API/CSV/Override)
- [ ] Timestamp de atualização
- [ ] Salvar log em banco de dados

### 2.7 Frontend
- [ ] Checkbox "Atualizar SELIC"
- [ ] Modal de configuração avançada
- [ ] Exibir competências atualizadas
- [ ] Alertas de lacunas
- [ ] Upload de CSV para override

## 🗄️ FASE 3 - Persistência e Histórico

### 3.1 Banco de Dados
- [ ] Escolher DB (PostgreSQL ou MongoDB)
- [ ] Criar schema/models
- [ ] Implementar CRUD de execuções
- [ ] Migrar de SQLite/JSON para DB produção

### 3.2 Histórico
- [ ] Endpoint para listar execuções anteriores
- [ ] Endpoint para buscar por Run ID
- [ ] Frontend: página de histórico
- [ ] Filtros: data, município, cenário

### 3.3 Comparação
- [ ] Comparar 2 execuções lado a lado
- [ ] Diff de inputs
- [ ] Diff de outputs
- [ ] Visualização de variação percentual

## 📊 FASE 4 - Dashboard e Analytics

### 4.1 Métricas
- [ ] Tempo médio de execução
- [ ] Taxa de sucesso/erro
- [ ] Municípios mais consultados
- [ ] Cenários mais usados
- [ ] Latência de APIs (Graph + BACEN)

### 4.2 Dashboard Admin
- [ ] Página de monitoramento
- [ ] Gráficos de uso
- [ ] Logs em tempo real
- [ ] Alertas de erro
- [ ] Estatísticas de rate limiting

### 4.3 Exportação Avançada
- [ ] Excel (.xlsx) com formatação
- [ ] PDF com logo/cabeçalho
- [ ] Envio por email
- [ ] Webhook para integração

## 🔐 FASE 5 - Autenticação e Multi-tenant

### 5.1 Sistema de Login
- [ ] Autenticação JWT
- [ ] Cadastro de usuários
- [ ] Perfis (Admin, Usuário)
- [ ] Recuperação de senha

### 5.2 Multi-tenant
- [ ] Organizações/escritórios
- [ ] Múltiplas planilhas por tenant
- [ ] Isolamento de dados
- [ ] Cobrança por uso

### 5.3 Permissões
- [ ] RBAC (Role-Based Access Control)
- [ ] Limites por plano
- [ ] Quotas de execução

## 🚀 FASE 6 - Otimização e Escala

### 6.1 Performance
- [ ] Cache de sessões Excel
- [ ] Pool de conexões Graph API
- [ ] Paralelização de leitura de outputs
- [ ] CDN para assets estáticos

### 6.2 Escalabilidade
- [ ] Fila de jobs (Celery/RQ)
- [ ] Workers assíncronos
- [ ] Load balancer
- [ ] Auto-scaling

### 6.3 Confiabilidade
- [ ] Retry automático com exponential backoff
- [ ] Circuit breaker
- [ ] Health checks avançados
- [ ] Alertas PagerDuty/Slack

## 🧪 FASE 7 - Testes e Qualidade

### 7.1 Testes Unitários
- [ ] Cobertura > 80%
- [ ] Testes de models
- [ ] Testes de serviços
- [ ] Testes de API

### 7.2 Testes de Integração
- [ ] Mock do Microsoft Graph
- [ ] Mock do BACEN
- [ ] Testes end-to-end

### 7.3 CI/CD
- [ ] GitHub Actions
- [ ] Testes automáticos
- [ ] Deploy automático
- [ ] Rollback automático

## 📱 FASE 8 - Mobile e PWA

- [ ] Progressive Web App (PWA)
- [ ] Instalável (Add to Home Screen)
- [ ] Offline-first (cache)
- [ ] Push notifications
- [ ] App nativo (React Native - futuro)

## 🌍 FASE 9 - Internacionalização

- [ ] Suporte PT-BR, EN, ES
- [ ] Formatação de moeda por locale
- [ ] Formatação de data por locale
- [ ] Documentação multilíngue

## 🤖 FASE 10 - IA e Automação

- [ ] Preenchimento inteligente (sugerir valores)
- [ ] Detecção de anomalias nos resultados
- [ ] Previsão de SELIC futura (ML)
- [ ] Chatbot para suporte

---

## 🎯 Priorização

### Alto Impacto, Curto Prazo
1. FASE 2: SELIC Dinâmica (2-3 semanas)
2. FASE 3.1: Banco de dados (1 semana)
3. FASE 5.1: Sistema de login (2 semanas)

### Médio Impacto
4. FASE 4: Dashboard (2 semanas)
5. FASE 6.1: Performance (1 semana)
6. FASE 7: Testes (contínuo)

### Baixo Impacto / Longo Prazo
7. FASE 8: Mobile (1 mês)
8. FASE 9: i18n (2 semanas)
9. FASE 10: IA (exploratório)

---

**Última Atualização:** 01/10/2025  
**Versão Atual:** 1.0.0 (FASE 1)  
**Próxima Milestone:** FASE 2 - SELIC Dinâmica
