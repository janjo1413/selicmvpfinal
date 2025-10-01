# 🚨 ATENÇÃO: Arquivo Excel precisa ser calculado!

## Problema

O `openpyxl` não consegue calcular fórmulas do Excel automaticamente.
Quando lemos células com fórmulas, obtemos texto como `'=D23*(1-$B$13)'` em vez do valor calculado.

## Solução Rápida

**Abra o arquivo Excel UMA VEZ manualmente:**

1. Navegue até: `data\timon_01-2025.xlsx`
2. Clique duplo para abrir no Microsoft Excel
3. Aguarde as fórmulas calcularem
4. Pressione `Ctrl+S` para salvar
5. Feche o Excel

Agora as fórmulas estarão calculadas e salvas no arquivo!

## Teste

Após abrir e salvar manualmente, teste novamente o cálculo na aplicação.

---

**Nota:** Isso só precisa ser feito UMA VEZ. Depois, o openpyxl conseguirá ler os valores salvos.
