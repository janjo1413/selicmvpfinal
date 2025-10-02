"""
Calculadora de Deságio
Implementa aplicação de deságio sobre principal
"""
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class DesagioCalculator:
    """Calcula deságio sobre valores principais"""
    
    @staticmethod
    def aplicar_desagio(
        principal_bruto: float,
        desagio_percentual: float
    ) -> Dict[str, float]:
        """
        Aplica deságio sobre o valor principal
        
        Args:
            principal_bruto: Valor principal antes do deságio
            desagio_percentual: Percentual de deságio (0-100)
            
        Returns:
            Dict com 'principal_bruto', 'desagio_valor', 'principal_liquido'
            
        Exemplos:
            >>> calc = DesagioCalculator()
            >>> calc.aplicar_desagio(100000, 20)
            {
                'principal_bruto': 100000.0,
                'desagio_valor': 20000.0,
                'principal_liquido': 80000.0
            }
            
            >>> calc.aplicar_desagio(50000, 0)
            {
                'principal_bruto': 50000.0,
                'desagio_valor': 0.0,
                'principal_liquido': 50000.0
            }
        """
        try:
            # Validar entrada
            if principal_bruto < 0:
                logger.warning(f"Principal bruto negativo: {principal_bruto}")
                principal_bruto = 0.0
            
            if desagio_percentual < 0 or desagio_percentual > 100:
                logger.warning(f"Deságio inválido: {desagio_percentual}%. Usando 0%")
                desagio_percentual = 0.0
            
            # Calcular deságio
            if desagio_percentual > 0:
                desagio_valor = principal_bruto * (desagio_percentual / 100)
                principal_liquido = principal_bruto - desagio_valor
                
                logger.info(
                    f"Deságio aplicado: {desagio_percentual}% sobre R$ {principal_bruto:,.2f} "
                    f"= R$ {desagio_valor:,.2f} (Líquido: R$ {principal_liquido:,.2f})"
                )
            else:
                desagio_valor = 0.0
                principal_liquido = principal_bruto
                logger.debug(f"Sem deságio. Principal: R$ {principal_bruto:,.2f}")
            
            return {
                "principal_bruto": round(principal_bruto, 2),
                "desagio_valor": round(desagio_valor, 2),
                "principal_liquido": round(principal_liquido, 2)
            }
            
        except Exception as e:
            logger.error(f"Erro ao calcular deságio: {e}")
            return {
                "principal_bruto": principal_bruto,
                "desagio_valor": 0.0,
                "principal_liquido": principal_bruto
            }
