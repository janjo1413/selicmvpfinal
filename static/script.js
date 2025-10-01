// Mapeamento de nomes de cenários
const CENARIOS_NOMES = {
    'nt7_ipca_selic': 'NT7 (IPCA/SELIC/?)',
    'nt7_periodo_cnj': 'NT7 (Período CNJ)',
    'nt6_ipca_selic': 'NT6 (IPCA/SELIC/?)',
    'jasa_ipca_selic': 'JASA (IPCA/SELIC/?)',
    'nt7_tr': 'NT7 TR',
    'nt36_tr': 'NT36 TR',
    'nt7_ipca_e': 'NT7 IPCA-E',
    'nt36_ipca_e': 'NT36 IPCA-E',
    'nt36_ipca_e_1pct': 'NT36 IPCA-E + 1% a.m.'
};

// Estado global para armazenar resultado
let ultimoResultado = null;

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    // Event listeners
    document.getElementById('calculadoraForm').addEventListener('submit', handleSubmit);
    document.getElementById('btnLimpar').addEventListener('click', limparFormulario);
    document.getElementById('btnExportar').addEventListener('click', exportarCSV);
    document.getElementById('btnNovoCalculo').addEventListener('click', novoCalculo);
    
    // Validações em tempo real
    setupValidacoes();
});

// Configurar validações
function setupValidacoes() {
    const periodoInicio = document.getElementById('periodo_inicio');
    const periodoFim = document.getElementById('periodo_fim');
    const correcaoAte = document.getElementById('correcao_ate');
    
    // Validar período fim > período início
    periodoFim.addEventListener('change', function() {
        if (periodoInicio.value && periodoFim.value) {
            if (new Date(periodoFim.value) < new Date(periodoInicio.value)) {
                alert('Período Fim deve ser maior que Período Início');
                periodoFim.value = '';
            }
        }
    });
    
    // Validar correção até >= período fim
    correcaoAte.addEventListener('change', function() {
        if (periodoFim.value && correcaoAte.value) {
            if (new Date(correcaoAte.value) < new Date(periodoFim.value)) {
                alert('Correção até deve ser maior ou igual ao Período Fim');
                correcaoAte.value = '';
            }
        }
    });
}

// Submeter formulário
async function handleSubmit(event) {
    event.preventDefault();
    
    // Coletar dados do formulário
    const formData = new FormData(event.target);
    const dados = {
        municipio: formData.get('municipio'),
        periodo_inicio: formData.get('periodo_inicio'),
        periodo_fim: formData.get('periodo_fim'),
        ajuizamento: formData.get('ajuizamento'),
        citacao: formData.get('citacao'),
        honorarios_perc: parseFloat(formData.get('honorarios_perc')) || 0, // Manter como percentual (20 = 20%)
        honorarios_fixo: parseFloat(formData.get('honorarios_fixo')) || 0,
        desagio_principal: parseFloat(formData.get('desagio_principal')) || 0, // Manter como percentual
        desagio_honorarios: parseFloat(formData.get('desagio_honorarios')) || 0, // Manter como percentual
        correcao_ate: formData.get('correcao_ate')
    };
    
    // Validar dados
    if (!validarDados(dados)) {
        return;
    }
    
    // Mostrar loading
    mostrarLoading();
    esconderErro();
    esconderResultados();
    
    try {
        // Fazer requisição
        const response = await fetch('/api/calcular', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || error.message || 'Erro ao processar cálculo');
        }
        
        const resultado = await response.json();
        ultimoResultado = resultado;
        
        // Exibir resultados
        exibirResultados(resultado);
        
    } catch (error) {
        console.error('Erro:', error);
        mostrarErro(error.message);
    } finally {
        esconderLoading();
    }
}

// Validar dados
function validarDados(dados) {
    // Validar datas não futuras
    const hoje = new Date();
    hoje.setHours(0, 0, 0, 0);
    
    const datas = [
        { campo: 'periodo_inicio', valor: dados.periodo_inicio },
        { campo: 'periodo_fim', valor: dados.periodo_fim },
        { campo: 'ajuizamento', valor: dados.ajuizamento },
        { campo: 'citacao', valor: dados.citacao },
        { campo: 'correcao_ate', valor: dados.correcao_ate }
    ];
    
    for (const data of datas) {
        const dataObj = new Date(data.valor + 'T00:00:00');
        if (dataObj > hoje) {
            alert(`${data.campo} não pode ser uma data futura`);
            return false;
        }
    }
    
    return true;
}

// Mostrar loading
function mostrarLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('btnCalcular').disabled = true;
}

// Esconder loading
function esconderLoading() {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('btnCalcular').disabled = false;
}

// Mostrar erro
function mostrarErro(mensagem) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.innerHTML = `<strong>❌ Erro:</strong> ${mensagem}`;
    errorDiv.style.display = 'block';
    
    // Scroll para o erro
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Esconder erro
function esconderErro() {
    document.getElementById('errorMessage').style.display = 'none';
}

// Esconder resultados
function esconderResultados() {
    document.getElementById('resultados').style.display = 'none';
}

// Exibir resultados
function exibirResultados(resultado) {
    const resultadosDiv = document.getElementById('resultados');
    const contentDiv = document.getElementById('resultadosContent');
    const metadataDiv = document.getElementById('metadata');
    
    // Limpar conteúdo anterior
    contentDiv.innerHTML = '';
    
    // Criar cards para cada cenário
    for (const [key, dados] of Object.entries(resultado.outputs)) {
        const card = criarCardCenario(key, dados);
        contentDiv.appendChild(card);
    }
    
    // Exibir metadata
    metadataDiv.innerHTML = `
        <p><strong>Run ID:</strong> ${resultado.run_id}</p>
        <p><strong>Timestamp:</strong> ${formatarDataHora(resultado.timestamp)}</p>
        <p><strong>Tempo de Execução:</strong> ${resultado.execution_time_ms}ms</p>
        <p><strong>Versão da Planilha:</strong> ${resultado.workbook_version || 'N/A'}</p>
        <p><strong>SELIC:</strong> ${resultado.selic_context.message}</p>
    `;
    
    // Mostrar seção de resultados
    resultadosDiv.style.display = 'block';
    
    // Scroll para resultados
    resultadosDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Criar card de cenário
function criarCardCenario(key, dados) {
    const card = document.createElement('div');
    card.className = 'result-card';
    
    const nome = CENARIOS_NOMES[key] || key;
    
    card.innerHTML = `
        <h3>${nome}</h3>
        <div class="result-row">
            <span class="result-label">Principal:</span>
            <span class="result-value">${formatarMoeda(dados.principal)}</span>
        </div>
        <div class="result-row">
            <span class="result-label">Honorários:</span>
            <span class="result-value">${formatarMoeda(dados.honorarios)}</span>
        </div>
        <div class="result-row">
            <span class="result-label">Total:</span>
            <span class="result-value">${formatarMoeda(dados.total)}</span>
        </div>
    `;
    
    return card;
}

// Formatar moeda
function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(valor);
}

// Formatar data e hora
function formatarDataHora(iso) {
    const data = new Date(iso);
    return data.toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Limpar formulário
function limparFormulario() {
    // Reset do formulário
    const form = document.getElementById('calculadoraForm');
    if (form) {
        form.reset();
    }
    
    // Limpar resultado global
    ultimoResultado = null;
    
    // Esconder seções
    esconderResultados();
    esconderErro();
    
    // Log para debug
    console.log('Formulário limpo com sucesso');
}

// Novo cálculo
function novoCalculo() {
    esconderResultados();
    document.getElementById('calculadoraForm').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Exportar CSV
async function exportarCSV() {
    if (!ultimoResultado) {
        alert('Nenhum resultado disponível para exportar');
        return;
    }
    
    try {
        const response = await fetch('/api/exportar-csv', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(ultimoResultado)
        });
        
        if (!response.ok) {
            throw new Error('Erro ao exportar CSV');
        }
        
        // Download do arquivo
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `calculo_${ultimoResultado.run_id.substring(0, 8)}.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
    } catch (error) {
        console.error('Erro ao exportar:', error);
        alert('Erro ao exportar CSV: ' + error.message);
    }
}
