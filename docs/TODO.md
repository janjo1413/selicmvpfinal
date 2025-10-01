# 📋 TODO - Pendências e Melhorias

**Versão Atual:** 1.0.0  
**Última Atualização:** 01/10/2025

---

## 🔥 Prioridade Alta (v1.1.0 - Próxima versão)

### 🎯 Objetivo Principal: Remover Dependência do Excel

#### Reimplementação de Cálculos em Python
- [ ] **Módulo de Correção IPCA**: Implementar fórmula de correção monetária
- [ ] **Módulo de Correção SELIC**: Implementar fórmula com taxas diárias
- [ ] **Módulo de Correção TR**: Implementar fórmula de correção
- [ ] **Cálculo Dinâmico de Honorários**: Implementar % sobre valores calculados
- [ ] **Cálculo Dinâmico de Deságio**: Implementar % sobre principal
- [ ] **Validação de Precisão**: Comparar Python vs Excel (margem erro < 0.01%)
- [ ] **Implementar 9 Cenários**: NT7, NT6, JASA, TR, IPCA-E, etc.

#### Performance
- [ ] Otimizar tempo de execução: ~2min → ~10s (20x mais rápido)
- [ ] Remover operações de I/O desnecessárias
- [ ] Implementar cálculos diretos sem arquivos temporários

#### Integrações Externas
- [ ] **API BACEN**: Buscar taxas SELIC atualizadas automaticamente
- [ ] **API IBGE**: Buscar índices IPCA atualizados automaticamente
- [ ] **Fallback Offline**: Arquivo CSV local para taxas/índices históricos

#### Qualidade de Código
- [ ] **Testes Unitários**: pytest para cada função de cálculo (coverage > 80%)
- [ ] **Testes de Integração**: Validar cenários completos end-to-end
- [ ] **Documentação**: Docstrings detalhadas com exemplos de uso

---

## 🟡 Prioridade Média (v1.2.0)

### Segurança
- [ ] Autenticação JWT
- [ ] Rate limiting (proteção contra DDoS)
- [ ] CORS configurado para produção
- [ ] Input sanitization aprimorado

### Persistência
- [ ] Banco de dados (PostgreSQL ou SQLite)
- [ ] Histórico de cálculos por usuário
- [ ] Salvar templates personalizados

### UI/UX
- [ ] Gráficos comparativos (Chart.js)
- [ ] Dark mode
- [ ] Design responsivo mobile melhorado
- [ ] Tooltips explicativos nos campos

---

## 🟢 Prioridade Baixa (Futuro)

### Features Avançadas
- [ ] Export PDF com relatório completo
- [ ] Comparação de múltiplos cálculos lado a lado
- [ ] Batch processing (calcular vários casos de uma vez)
- [ ] Templates personalizados (múltiplas planilhas)

### Cálculos
- [ ] Implementar fórmulas em Python puro (eliminar Excel)
- [ ] Validar precisão matemática com 6+ casas decimais
- [ ] Adicionar novos índices de correção

### Deploy
- [ ] Containerização Docker
- [ ] CI/CD com GitHub Actions
- [ ] Deploy em Heroku/Railway/Render
- [ ] Monitoring com Sentry
- [ ] Backup automático

---

## 🐛 Bugs Conhecidos

### Performance
- ⚠️ Tempo de execução muito lento (~112s)
  - **Causa:** 9 leituras separadas do Excel
  - **Solução:** Ler todos os ranges de uma vez (v1.1.0)

### Compatibilidade
- ⚠️ OneDrive interfere com arquivos Excel
  - **Workaround:** Usar `C:\Temp` ou desabilitar sync temporariamente
  - **Solução:** Implementar lock de arquivo ou usar DB (v1.2.0)

### Limitações
- ⚠️ SELIC não atualiza automaticamente
  - **Solução:** API BACEN (v1.1.0)
- ⚠️ Não suporta múltiplos usuários simultâneos
  - **Solução:** Database + queue system (v1.2.0)

---

## 💡 Ideias Futuras (Não Priorizadas)

- App mobile (React Native)
- Integração com sistemas de tribunais (e-SAJ, PJe)
- OCR para extrair dados de documentos PDF
- IA para sugerir melhores estratégias de correção
- Marketplace de templates de cálculo
- API pública REST + GraphQL
- Notificações por email/SMS
- Colaboração em tempo real (múltiplos usuários)
- Versionamento de cálculos
- Auditoria completa de alterações

---

## 📊 Métricas de Sucesso

### v1.1.0 (Performance + BACEN)
- ⏱️ Tempo execução: <10 segundos
- 📈 SELIC atualizada diariamente via API
- ✅ 50%+ test coverage
- 👥 Suportar 10 usuários simultâneos

### v1.2.0 (Auth + Persistência)
- 🔐 100% requisições autenticadas
- 💾 Histórico de 100+ cálculos salvos
- 🚫 Zero ataques DDoS bem-sucedidos
- 👥 50+ usuários cadastrados

### v2.0.0 (Cálculos Python)
- ⚡ <5 segundos por cálculo
- 🎯 Precisão 99.99% vs Excel
- 📊 100% fórmulas documentadas
- 🚀 Suportar 100 usuários simultâneos

---

## 🎯 Próximos Passos Imediatos

1. **Semana 1-2:** Otimizar leitura Excel (v1.1.0)
2. **Semana 3-4:** Integrar API BACEN
3. **Semana 5-6:** Testes automatizados
4. **Release v1.1.0:** Performance + SELIC dinâmica

---

**Contribuições:** Abra uma issue no GitHub para sugerir novas features!
