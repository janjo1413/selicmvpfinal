"""
Calculadora de Honorários
Implementa cálculos de honorários advocatícios em Python
"""
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class HonorariosCalculator:
    """Calcula honorários baseado em percentual ou valor fixo"""
    
    @staticmethod
    def calcular(
        principal: float,
        honorarios_perc: float,
        honorarios_fixo: float,
        desagio_honorarios: float
    ) -> Dict[str, float]:
        """
        Calcula honorários e total
        
        Args:
            principal: Valor principal já calculado pelo Excel
            honorarios_perc: Percentual de honorários (0-100)
            honorarios_fixo: Valor fixo de honorários em R$
            desagio_honorarios: Percentual de deságio nos honorários (0-100)
            
        Returns:
            Dict com 'honorarios' e 'total'
            
        Exemplos:
            >>> calc = HonorariosCalculator()
            >>> calc.calcular(100000, 20, 0, 0)
            {'honorarios': 20000.0, 'total': 120000.0}
            
            >>> calc.calcular(100000, 0, 5000, 10)
            {'honorarios': 4500.0, 'total': 104500.0}
        """
        try:
            # Se tem percentual, usa percentual (prioridade sobre fixo)
            if honorarios_perc > 0:
                honorarios_bruto = principal * (honorarios_perc / 100)
                logger.debug(f"Honorários %: {principal:,.2f} * {honorarios_perc}% = {honorarios_bruto:,.2f}")
            else:
                # Senão, usa valor fixo
                honorarios_bruto = honorarios_fixo
                logger.debug(f"Honorários fixo: R$ {honorarios_fixo:,.2f}")
            
            # Aplica deságio nos honorários se houver
            if desagio_honorarios > 0:
                fator_desagio = 1 - (desagio_honorarios / 100)
                honorarios_liquido = honorarios_bruto * fator_desagio
                logger.debug(f"Deságio {desagio_honorarios}%: {honorarios_bruto:,.2f} * {fator_desagio} = {honorarios_liquido:,.2f}")
            else:
                honorarios_liquido = honorarios_bruto
            
            # Calcula total
            total = principal + honorarios_liquido
            
            logger.info(f"Honorários calculados: R$ {honorarios_liquido:,.2f} (Total: R$ {total:,.2f})")
            
            return {
                "honorarios": round(honorarios_liquido, 2),
                "total": round(total, 2)
            }
            
        except Exception as e:
            logger.error(f"Erro ao calcular honorários: {e}")
            return {
                "honorarios": 0.0,
                "total": principal
            }
