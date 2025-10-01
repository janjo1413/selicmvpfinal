"""
API REST com FastAPI
"""
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from models import CalculadoraInput, CalculadoraOutput, ErrorResponse
from calculator_service import CalculadoraService
from datetime import datetime
import csv
import io
from collections import defaultdict
import time

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title="Calculadora Trabalhista API",
    description="API para cálculo de valores trabalhistas usando Excel como motor",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting simples
rate_limit_storage = defaultdict(list)
RATE_LIMIT = 10  # requisições
RATE_WINDOW = 60  # segundos


def check_rate_limit(ip: str) -> bool:
    """Verifica rate limit por IP"""
    now = time.time()
    # Limpar timestamps antigos
    rate_limit_storage[ip] = [ts for ts in rate_limit_storage[ip] if now - ts < RATE_WINDOW]
    
    if len(rate_limit_storage[ip]) >= RATE_LIMIT:
        return False
    
    rate_limit_storage[ip].append(now)
    return True


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Middleware de rate limiting"""
    client_ip = request.client.host
    
    if not check_rate_limit(client_ip):
        return JSONResponse(
            status_code=429,
            content={"error": "RateLimitExceeded", "message": "Muitas requisições. Tente novamente em 1 minuto."}
        )
    
    response = await call_next(request)
    return response


@app.get("/api/health")
async def health():
    """Endpoint de health check"""
    return {
        "status": "online",
        "service": "Calculadora Trabalhista",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/calcular", response_model=CalculadoraOutput, responses={
    400: {"model": ErrorResponse},
    500: {"model": ErrorResponse}
})
async def calcular(inputs: CalculadoraInput):
    """
    Executa cálculo trabalhista
    
    - **municipio**: Nome do município
    - **periodo_inicio**: Data de início (AAAA-MM-DD)
    - **periodo_fim**: Data de fim (AAAA-MM-DD)
    - **ajuizamento**: Data de ajuizamento (AAAA-MM-DD)
    - **citacao**: Data de citação (AAAA-MM-DD)
    - **honorarios_perc**: Honorários % (0.0 a 1.0)
    - **honorarios_fixo**: Honorários fixo (R$)
    - **desagio_principal**: Deságio principal (0.0 a 1.0)
    - **desagio_honorarios**: Deságio honorários (0.0 a 1.0)
    - **correcao_ate**: Data de correção até (AAAA-MM-DD)
    """
    try:
        logger.info(f"Nova requisição de cálculo: {inputs.municipio}")
        
        service = CalculadoraService()
        result = service.calcular(inputs)
        
        return result
        
    except ValueError as e:
        logger.warning(f"Erro de validação: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        logger.error(f"Erro interno: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao processar cálculo: {str(e)}")


@app.post("/api/exportar-csv")
async def exportar_csv(result: CalculadoraOutput):
    """
    Exporta resultado em formato CSV
    """
    try:
        # Criar CSV em memória
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Cabeçalho
        writer.writerow(['Cenário', 'Principal', 'Honorários', 'Total'])
        
        # Mapeamento de nomes amigáveis
        cenarios_nomes = {
            "nt7_ipca_selic": "NT7 (IPCA/SELIC/?)",
            "nt7_periodo_cnj": "NT7 (Período CNJ)",
            "nt6_ipca_selic": "NT6 (IPCA/SELIC/?)",
            "jasa_ipca_selic": "JASA (IPCA/SELIC/?)",
            "nt7_tr": "NT7 TR",
            "nt36_tr": "NT36 TR",
            "nt7_ipca_e": "NT7 IPCA-E",
            "nt36_ipca_e": "NT36 IPCA-E",
            "nt36_ipca_e_1pct": "NT36 IPCA-E + 1% a.m.",
        }
        
        # Dados dos cenários
        for cenario_key, cenario_data in result.outputs.items():
            nome = cenarios_nomes.get(cenario_key, cenario_key)
            writer.writerow([
                nome,
                f"{cenario_data.principal:.2f}",
                f"{cenario_data.honorarios:.2f}",
                f"{cenario_data.total:.2f}"
            ])
        
        # Linha em branco
        writer.writerow([])
        
        # Inputs
        writer.writerow(['Inputs:'])
        writer.writerow(['Município', result.inputs.get('municipio')])
        writer.writerow(['Período', f"{result.inputs.get('periodo_inicio')} a {result.inputs.get('periodo_fim')}"])
        writer.writerow(['Ajuizamento', result.inputs.get('ajuizamento')])
        writer.writerow(['Citação', result.inputs.get('citacao')])
        writer.writerow(['Honorários', '%', result.inputs.get('honorarios_perc')])
        writer.writerow(['Honorários', 'Fixo', result.inputs.get('honorarios_fixo')])
        writer.writerow(['Deságio', 'Principal', result.inputs.get('desagio_principal')])
        writer.writerow(['Deságio', 'Honorários', result.inputs.get('desagio_honorarios')])
        writer.writerow(['Correção até', result.inputs.get('correcao_ate')])
        
        # Linha em branco
        writer.writerow([])
        
        # Metadata
        writer.writerow(['Metadata:'])
        writer.writerow(['Run ID', result.run_id])
        writer.writerow(['Timestamp', result.timestamp.isoformat()])
        writer.writerow(['Workbook Version', result.workbook_version or 'N/A'])
        writer.writerow(['Execution Time (ms)', result.execution_time_ms])
        
        # Preparar resposta
        output.seek(0)
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=calculo_{result.run_id[:8]}.csv"
            }
        )
        
    except Exception as e:
        logger.error(f"Erro ao exportar CSV: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro ao exportar CSV: {str(e)}")


# Servir arquivos estáticos (frontend)
# Caminho absoluto para a pasta static na raiz do projeto
from pathlib import Path
STATIC_DIR = Path(__file__).parent.parent / "static"

try:
    if STATIC_DIR.exists():
        app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
        logger.info(f"Frontend servido de: {STATIC_DIR}")
    else:
        logger.warning(f"Diretório 'static' não encontrado em: {STATIC_DIR}")
except RuntimeError as e:
    logger.warning(f"Erro ao montar static: {e}")


if __name__ == "__main__":
    import uvicorn
    import config
    
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True,
        log_level="info"
    )
