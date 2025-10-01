"""
Módulo principal - entrada da aplicação
"""
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Importar e executar
from src.main import app

if __name__ == "__main__":
    import uvicorn
    from src.config import API_HOST, API_PORT
    
    uvicorn.run(
        "src.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
        log_level="info"
    )
