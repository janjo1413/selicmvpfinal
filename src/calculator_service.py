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
from desagio_calculator import DesagioCalculator
from bacen_service import BacenService
from taxas_validator import TaxasValidator
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
# IMPORTANTE: Lê linhas BRUTAS (sem deságio) e aplica deságio em Python
# Linhas ÍMPARES = Valor bruto (referencia abas de cálculo)
# Linhas PARES = Valor com deságio Excel (=linha_anterior * (1-B13))
OUTPUT_LINES = {
    "nt7_ipca_selic": 23,      # Era 24 - agora lê BRUTO
    "nt7_periodo_cnj": 28,     # Era 29 - agora lê BRUTO
    "nt6_ipca_selic": 33,      # Era 34 - agora lê BRUTO
    "jasa_ipca_selic": 38,     # Era 39 - agora lê BRUTO
    "nt7_tr": 43,              # Era 44 - agora lê BRUTO
    "nt36_tr": 48,             # Era 49 - agora lê BRUTO
    "nt7_ipca_e": 53,          # Era 54 - agora lê BRUTO
    "nt36_ipca_e": 63,         # Era 64 - agora lê BRUTO
    "nt36_ipca_e_1pct": 68,    # Era 69 - agora lê BRUTO
}


class CalculadoraService:
    """Serviço de cálculo trabalhista"""
    
    def __init__(self):
        self.excel_path = EXCEL_FULL_PATH
        self.bacen_service = BacenService()
    
    def _format_date_for_excel(self, date_obj):
        """Formata data para formato aceito pelo Excel (retorna datetime object)"""
        # openpyxl aceita datetime.date diretamente - não converter para string
        return date_obj
    
    def _format_percentage_for_excel(self, percent_value):
        """Converte percentual (ex: 20) para fração decimal (0.20) para Excel"""
        # Excel espera 0.20 quando a célula tem formato de porcentagem
        return percent_value / 100.0
    
    def _salvar_csv_backup(self, inputs: CalculadoraInput, results: Dict, run_id: str, csv_path: Path):
        """Salva CSV com dados calculados + inputs (backup automático)"""
        import csv
        
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                
                # Cabeçalho
                writer.writerow(['=== BACKUP AUTOMÁTICO DE CÁLCULO ==='])
                writer.writerow(['Run ID:', run_id])
                writer.writerow(['Timestamp:', datetime.now().isoformat()])
                writer.writerow([])
                
                # Inputs
                writer.writerow(['=== INPUTS ==='])
                writer.writerow(['Município:', inputs.municipio])
                writer.writerow(['Período:', f"{inputs.periodo_inicio} a {inputs.periodo_fim}"])
                writer.writerow(['Ajuizamento:', inputs.ajuizamento])
                writer.writerow(['Citação:', inputs.citacao])
                writer.writerow(['Honorários (%):', inputs.honorarios_perc])
                writer.writerow(['Honorários (R$):', inputs.honorarios_fixo])
                writer.writerow(['Deságio Principal (%):', inputs.desagio_principal])
                writer.writerow(['Deságio Honorários (%):', inputs.desagio_honorarios])
                writer.writerow(['Correção até:', inputs.correcao_ate])
                writer.writerow([])
                
                # Resultados calculados
                writer.writerow(['=== RESULTADOS CALCULADOS ==='])
                writer.writerow(['Cenário', 'Principal', 'Honorários', 'Total'])
                
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
                
                for cenario_key, cenario_data in results.items():
                    nome = cenarios_nomes.get(cenario_key, cenario_key)
                    writer.writerow([
                        nome,
                        f"R$ {cenario_data.principal:,.2f}",
                        f"R$ {cenario_data.honorarios:,.2f}",
                        f"R$ {cenario_data.total:,.2f}"
                    ])
            
            logger.info(f"[{run_id}] 📄 CSV backup salvo em: {csv_path}")
            
        except Exception as e:
            logger.warning(f"[{run_id}] Erro ao salvar CSV backup: {e}")

    
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
                
                # 2. *** IMPORTANTE: LER VALORES DO TEMPLATE PRIMEIRO (antes de modificar) ***
                # O openpyxl perde valores calculados ao salvar, então precisamos ler ANTES
                logger.info(f"[{run_id}] Lendo valores calculados do template ORIGINAL")
                logger.info(f"[{run_id}] Aplicando deságio do principal e calculando honorários em Python...")
                
                # Preparar input_dict para cálculos
                input_dict = inputs.model_dump()
                
                # Instanciar calculadoras
                desagio_calc = DesagioCalculator()
                hon_calc = HonorariosCalculator()
                
                results = {}
                for cenario_name, line_number in OUTPUT_LINES.items():
                    # Ler coluna D (Principal BRUTO) da linha
                    range_address = f"D{line_number}"
                    values = excel_calc.read_range_calculated("RESUMO", range_address)
                    
                    if values and len(values) > 0:
                        # Principal BRUTO vem do Excel
                        principal_bruto = float(values[0][0]) if values[0][0] is not None else 0.0
                        
                        # 1. Aplicar deságio no principal
                        desagio_resultado = desagio_calc.aplicar_desagio(
                            principal_bruto=principal_bruto,
                            desagio_percentual=input_dict['desagio_principal']
                        )
                        principal_liquido = desagio_resultado['principal_liquido']
                        
                        # 2. Calcular honorários sobre principal LÍQUIDO
                        hon_resultado = hon_calc.calcular(
                            principal=principal_liquido,
                            honorarios_perc=input_dict['honorarios_perc'],
                            honorarios_fixo=input_dict['honorarios_fixo'],
                            desagio_honorarios=input_dict['desagio_honorarios']
                        )
                        
                        results[cenario_name] = CenarioOutput(
                            principal=principal_liquido,
                            honorarios=hon_resultado['honorarios'],
                            total=hon_resultado['total']
                        )
                        
                        logger.debug(
                            f"[{run_id}] {cenario_name}: "
                            f"P_bruto={principal_bruto:,.2f}, "
                            f"P_líquido={principal_liquido:,.2f}, "
                            f"H={hon_resultado['honorarios']:,.2f}, "
                            f"T={hon_resultado['total']:,.2f}"
                        )
                    else:
                        logger.warning(f"[{run_id}] Dados inválidos para {cenario_name} na linha {line_number}")
                        results[cenario_name] = CenarioOutput(
                            principal=0.0,
                            honorarios=0.0,
                            total=0.0
                        )
                
                # 3. AGORA sim, escrever inputs no Excel (para exportar)
                logger.info(f"[{run_id}] Escrevendo inputs via openpyxl (para exportar Excel)")
                
                # Campos que são percentuais (Excel espera frações: 0.20 = 20%)
                percentage_fields = ['honorarios_perc', 'desagio_principal', 'desagio_honorarios']
                
                for field_name, (worksheet, address) in INPUT_MAPPING.items():
                    value = input_dict[field_name]
                    
                    # Formatar datas (retorna datetime object)
                    if hasattr(value, 'strftime'):
                        value = self._format_date_for_excel(value)
                    
                    # Converter percentuais (20 -> 0.20)
                    elif field_name in percentage_fields:
                        value = self._format_percentage_for_excel(value)
                    
                    # Escrever na célula
                    excel_calc.write_cell(worksheet, address, value)
                    logger.debug(f"[{run_id}] {field_name} = {value} -> {worksheet}!{address}")
                
                # 4. Salvar Excel com inputs escritos (para exportar)
                logger.info(f"[{run_id}] Salvando Excel com inputs...")
                excel_calc.save_workbook()
                
                # 5. Copiar para data/output/
                output_dir = Path("data/output")
                output_dir.mkdir(parents=True, exist_ok=True)
                
                municipio_safe = inputs.municipio.replace(" ", "_").replace("-", "_")
                output_filename = f"{municipio_safe}_{run_id[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                output_path = output_dir / output_filename
                
                import shutil
                shutil.copy2(excel_calc.temp_path, output_path)
                logger.info(f"[{run_id}] 📁 Excel processado salvo em: {output_path}")
                excel_output_path_str = str(output_path.absolute())
                
                # Workbook será fechado automaticamente pelo context manager
                logger.info(f"[{run_id}] Fechando workbook")
            
            # 5. Salvar CSV backup automático (para ter dados calculados legíveis)
            csv_filename = f"{municipio_safe}_{run_id[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            csv_path = output_dir / csv_filename
            self._salvar_csv_backup(inputs, results, run_id, csv_path)
            
            # 6. Validar completude das taxas
            taxas_status = self._validar_taxas(
                inputs.periodo_inicio,
                inputs.periodo_fim,
                inputs.correcao_ate
            )
            
            # 7. Buscar informações SELIC (opcional - não bloqueia execução)
            selic_info = self._obter_info_selic(inputs.periodo_inicio, inputs.correcao_ate)
            selic_info["taxas_validacao"] = taxas_status
            
            # 8. Preparar resposta
            execution_time = int((time.time() - start_time) * 1000)
            logger.info(f"[{run_id}] Execução concluída em {execution_time}ms")
            
            return CalculadoraOutput(
                run_id=run_id,
                timestamp=datetime.now(),
                workbook_version=workbook_version,
                inputs=inputs.model_dump(mode='json'),
                outputs=results,
                selic_context=selic_info,
                execution_time_ms=execution_time,
                excel_output_path=excel_output_path_str
            )
            
        except Exception as e:
            logger.error(f"[{run_id}] Erro durante execução: {str(e)}", exc_info=True)
            # Context manager já fecha o workbook
            raise
    
    def _obter_info_selic(self, data_inicio, data_fim) -> Dict[str, Any]:
        """
        Obtém informações sobre disponibilidade e status da SELIC
        
        Args:
            data_inicio: Data inicial do período
            data_fim: Data final do período
            
        Returns:
            Dict com informações sobre SELIC
        """
        try:
            # Verificar disponibilidade da API
            api_disponivel = self.bacen_service.verificar_disponibilidade()
            
            if api_disponivel:
                # Tentar buscar dados do período
                taxas = self.bacen_service.buscar_selic_periodo(
                    data_inicio, 
                    data_fim,
                    usar_cache=True
                )
                
                if taxas and len(taxas) > 0:
                    return {
                        "updated": True,
                        "source": "API BACEN",
                        "registros": len(taxas),
                        "periodo": f"{data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}",
                        "message": f"✅ {len(taxas)} taxas SELIC obtidas da API BACEN"
                    }
                else:
                    return {
                        "updated": False,
                        "source": "Cache local",
                        "message": "⚠️ API BACEN disponível mas sem dados para o período. Usando cache."
                    }
            else:
                return {
                    "updated": False,
                    "source": "Offline",
                    "message": "⚠️ API BACEN indisponível. Usando taxas do Excel."
                }
                
        except Exception as e:
            logger.warning(f"Erro ao obter info SELIC: {e}")
            return {
                "updated": False,
                "source": "Erro",
                "message": f"❌ Erro ao consultar SELIC: {str(e)}"
            }
    
    def _validar_taxas(self, data_inicio, data_fim, correcao_ate) -> Dict[str, Any]:
        """
        Valida se Excel tem todas as taxas necessárias para o período
        
        Args:
            data_inicio: Data inicial do período
            data_fim: Data final do período
            correcao_ate: Data até quando corrigir
            
        Returns:
            Dict com status da validação
        """
        try:
            validator = TaxasValidator()
            resultado = validator.verificar_completo(
                data_inicio,
                data_fim,
                correcao_ate
            )
            
            # Log de avisos se houver
            if not resultado["todas_taxas_disponiveis"]:
                logger.warning(f"Taxas incompletas: {resultado['recomendacao']}")
                for aviso in resultado.get("avisos", []):
                    logger.warning(f"  {aviso}")
            else:
                logger.info("✅ Todas as taxas disponíveis no Excel")
            
            return resultado
            
        except Exception as e:
            logger.error(f"Erro ao validar taxas: {e}")
            return {
                "todas_taxas_disponiveis": None,
                "erro": str(e),
                "message": "⚠️ Não foi possível validar disponibilidade das taxas"
            }
