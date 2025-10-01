"""
Serviço principal de cálculo
"""
import logging
import time
import uuid
from datetime import datetime
from typing import Dict, Any
from pathlib import Path
from models import CalculadoraInput, CalculadoraOutput, CenarioOutput
from excel_template_calculator import ExcelTemplateCalculator
from honorarios_calculator import HonorariosCalculator
from config import EXCEL_FULL_PATH

logger = logging.getLogger(__name__)


# Mapeamento de células de INPUT (Aba: RESUMO)
INPUT_MAPPING = {
    "municipio": ("RESUMO", "B6"),
    "periodo_inicio": ("RESUMO", "E6"),
    "periodo_fim": ("RESUMO", "F6"),
    "ajuizamento": ("RESUMO", "B7"),
    "citacao": ("RESUMO", "B8"),
    "honorarios_perc": ("RESUMO", "B11"),
    "honorarios_fixo": ("RESUMO", "B12"),
    "desagio_principal": ("RESUMO", "B13"),
    "desagio_honorarios": ("RESUMO", "B14"),
    "correcao_ate": ("RESUMO", "B15"),
}

# Mapeamento de células de OUTPUT (Aba: RESUMO)
# Formato: linha -> (D=Principal, E=Honorários, F=Total)
OUTPUT_LINES = {
    "nt7_ipca_selic": 24,
    "nt7_periodo_cnj": 29,
    "nt6_ipca_selic": 34,
    "jasa_ipca_selic": 39,
    "nt7_tr": 44,
    "nt36_tr": 49,
    "nt7_ipca_e": 54,
    "nt36_ipca_e": 64,
    "nt36_ipca_e_1pct": 69,
}


class CalculadoraService:
    """Serviço de cálculo trabalhista"""
    
    def __init__(self):
        self.excel_path = EXCEL_FULL_PATH
    
    def _format_date_for_excel(self, date_obj) -> str:
        """Formata data para formato aceito pelo Excel"""
        return date_obj.strftime("%Y-%m-%d")

    
    def calcular(self, inputs: CalculadoraInput) -> CalculadoraOutput:
        """
        Executa o fluxo completo de cálculo via COM (sem salvar arquivo)
        
        Args:
            inputs: Dados de entrada validados
            
        Returns:
            Resultado do cálculo com todos os cenários
        """
        run_id = str(uuid.uuid4())
        start_time = time.time()
        
        logger.info(f"[{run_id}] Iniciando execução COM")
        logger.info(f"[{run_id}] Inputs validados: {inputs.model_dump()}")
        
        try:
            # Usar template protegido (cria cópia temporária)
            with ExcelTemplateCalculator(self.excel_path) as excel_calc:
                
                # 1. Obter versão da planilha
                workbook_version = "TIMON 01-2025"
                
                # 2. Escrever inputs via openpyxl
                logger.info(f"[{run_id}] Escrevendo inputs via openpyxl")
                input_dict = inputs.model_dump()
                
                for field_name, (worksheet, address) in INPUT_MAPPING.items():
                    value = input_dict[field_name]
                    
                    # Formatar datas
                    if hasattr(value, 'strftime'):
                        value = self._format_date_for_excel(value)
                    
                    # Escrever na célula
                    excel_calc.write_cell(worksheet, address, value)
                    logger.info(f"[{run_id}] {field_name} = {value} -> {worksheet}!{address}")
                
                # 3. Salvar cópia temporária
                logger.info(f"[{run_id}] Salvando cópia temporária...")
                calc_start = time.time()
                excel_calc.save_workbook()
                calc_time = int((time.time() - calc_start) * 1000)
                logger.info(f"[{run_id}] Salvamento concluído em {calc_time}ms")
                
                # 4. Ler outputs calculados (Excel fornece apenas Principal)
                logger.info(f"[{run_id}] Lendo outputs D24:F69 calculados")
                logger.info(f"[{run_id}] Calculando honorários em Python...")
                
                # Instanciar calculadora de honorários
                hon_calc = HonorariosCalculator()
                
                results = {}
                for cenario_name, line_number in OUTPUT_LINES.items():
                    # Ler coluna D (Principal) da linha
                    range_address = f"D{line_number}"
                    values = excel_calc.read_range_calculated("RESUMO", range_address)
                    
                    if values and len(values) > 0:
                        # Principal vem do Excel
                        principal = float(values[0][0]) if values[0][0] is not None else 0.0
                        
                        # Honorários e Total calculados em Python
                        hon_resultado = hon_calc.calcular(
                            principal=principal,
                            honorarios_perc=input_dict['honorarios_perc'],
                            honorarios_fixo=input_dict['honorarios_fixo'],
                            desagio_honorarios=input_dict['desagio_honorarios']
                        )
                        
                        results[cenario_name] = CenarioOutput(
                            principal=principal,
                            honorarios=hon_resultado['honorarios'],
                            total=hon_resultado['total']
                        )
                        
                        logger.debug(f"[{run_id}] {cenario_name}: P={principal:,.2f}, H={hon_resultado['honorarios']:,.2f}, T={hon_resultado['total']:,.2f}")
                    else:
                        logger.warning(f"[{run_id}] Dados inválidos para {cenario_name} na linha {line_number}")
                        results[cenario_name] = CenarioOutput(
                            principal=0.0,
                            honorarios=0.0,
                            total=0.0
                        )
                
                # Workbook será fechado automaticamente pelo context manager
                logger.info(f"[{run_id}] Fechando workbook")
            
            # 5. Preparar resposta
            execution_time = int((time.time() - start_time) * 1000)
            logger.info(f"[{run_id}] Execução concluída em {execution_time}ms")
            
            return CalculadoraOutput(
                run_id=run_id,
                timestamp=datetime.now(),
                workbook_version=workbook_version,
                inputs=inputs.model_dump(mode='json'),
                outputs=results,
                selic_context={
                    "updated": False,
                    "message": "SELIC não atualizada nesta execução (FASE 1)"
                },
                execution_time_ms=execution_time
            )
            
        except Exception as e:
            logger.error(f"[{run_id}] Erro durante execução: {str(e)}", exc_info=True)
            # Context manager já fecha o workbook
            raise
