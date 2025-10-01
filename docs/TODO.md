# 📋 TODO - Pendências e Melhorias

**Versão Atual:** 1.0.0  
**Última Atualização:** 01/10/2025

---

## 🔥 Prioridade Alta (v1.1.0 - Próxima versão)

### Performance
- [ ] Otimizar leitura Excel: Ler todos os 9 cenários em uma operação
- [ ] Reduzir tempo de execução de 112s para ~10s
- [ ] Implementar cache em memória para resultados recentes

### API BACEN
- [ ] Integrar API BACEN para taxas SELIC atualizadas
- [ ] Implementar cache de taxas (Redis ou arquivo local)
- [ ] Fallback para taxas locais se API falhar

### Testes
- [ ] Testes unitários com pytest (coverage mínimo 50%)
- [ ] Testes de integração para endpoints
- [ ] Validar precisão dos cálculos vs Excel manual

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
