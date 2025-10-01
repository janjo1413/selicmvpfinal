"""
Configurações da aplicação
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Arquivo Excel Local
EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH", "data/timon_01-2025.xlsx")

# Diretório base do projeto (raiz, não src/)
BASE_DIR = Path(__file__).parent.parent  # Sobe um nível para chegar na raiz

# Caminho completo do Excel
EXCEL_FULL_PATH = BASE_DIR / EXCEL_FILE_PATH

# API
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# BACEN API (FASE 2)
BACEN_API_BASE = os.getenv("BACEN_API_BASE", "https://api.bcb.gov.br/dados/serie/bcdata.sgs")
BACEN_SERIE_SELIC = os.getenv("BACEN_SERIE_SELIC", "432")

# Timeouts
EXECUTION_TIMEOUT = 60  # 60 segundos

# Rate Limiting
RATE_LIMIT_PER_MINUTE = 10
