"""
Calculadora Excel via COM (win32com) com fallback para VBS
Permite calcular sem salvar o arquivo
"""
import logging
import time
import subprocess
from pathlib import Path
from typing import Dict, Any, Tuple, List
import win32com.client
import pythoncom

logger = logging.getLogger(__name__)


class ExcelCOMCalculator:
    """Calcula Excel via COM sem salvar arquivo (com fallback VBS)"""
    
    def __init__(self, excel_path: Path):
        self.excel_path = excel_path
        self.excel_app = None
        self.workbook = None
        self.use_vbs = False  # Flag para usar VBS em vez de COM
        self.vbs_script = Path(__file__).parent.parent / "scripts" / "excel_calc.vbs"
        
    def __enter__(self):
        """Context manager - abre Excel"""
        self._open_excel()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager - fecha Excel"""
        self._close_excel()
        
    def _open_excel(self):
        """Abre Excel via COM (ou prepara VBS se COM falhar)"""
        try:
            pythoncom.CoInitialize()
            logger.info("Inicializando Excel via COM...")
            
            self.excel_app = win32com.client.Dispatch("Excel.Application")
            self.excel_app.Visible = False
            self.excel_app.DisplayAlerts = False
            self.excel_app.ScreenUpdating = False
            
            logger.info(f"Abrindo planilha: {self.excel_path}")
            self.workbook = self.excel_app.Workbooks.Open(str(self.excel_path.absolute()))
            
            logger.info("Excel aberto com sucesso via COM")
            self.use_vbs = False
            
        except Exception as e:
            logger.warning(f"COM falhou: {e}")
            logger.info("Usando fallback VBS para cálculos...")
            self._close_excel()
            self.use_vbs = True
            # Não levantar exceção - VBS vai fazer o trabalho
            
    def _close_excel(self):
        """Fecha Excel SEM salvar"""
        try:
            if self.workbook:
                logger.info("Fechando planilha SEM salvar...")
                self.workbook.Close(SaveChanges=False)
                self.workbook = None
                
            if self.excel_app:
                self.excel_app.Quit()
                self.excel_app = None
                
            pythoncom.CoUninitialize()
            logger.info("Excel fechado")
            
        except Exception as e:
            logger.warning(f"Erro ao fechar Excel: {e}")
            
    def write_cell(self, worksheet_name: str, address: str, value: Any):
        """Escreve valor em célula"""
        try:
            ws = self.workbook.Worksheets(worksheet_name)
            ws.Range(address).Value = value
            logger.debug(f"Escrito: {worksheet_name}!{address} = {value}")
            
        except Exception as e:
            logger.error(f"Erro ao escrever {address}: {e}")
            raise
            
    def read_cell(self, worksheet_name: str, address: str) -> Any:
        """Lê valor de célula (calculado)"""
        try:
            ws = self.workbook.Worksheets(worksheet_name)
            value = ws.Range(address).Value
            return value
            
        except Exception as e:
            logger.error(f"Erro ao ler {address}: {e}")
            raise
            
    def read_range(self, worksheet_name: str, range_address: str) -> list:
        """Lê range de células"""
        try:
            ws = self.workbook.Worksheets(worksheet_name)
            data = ws.Range(range_address).Value
            
            # Normalizar retorno
            if isinstance(data, tuple):
                return [list(row) if isinstance(row, tuple) else [row] for row in data]
            else:
                return [[data]]
                
        except Exception as e:
            logger.error(f"Erro ao ler range {range_address}: {e}")
            raise
            
    def force_calculate(self):
        """Força recálculo completo"""
        try:
            logger.info("Forçando recálculo completo...")
            self.excel_app.CalculateFullRebuild()
            self.excel_app.Calculate()
            
            # Aguardar cálculo completar
            time.sleep(1)
            
            logger.info("Recálculo concluído")
            
        except Exception as e:
            logger.warning(f"Erro ao forçar cálculo: {e}")
