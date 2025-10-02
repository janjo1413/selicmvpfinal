"""
Detector de Taxas Desatualizadas
Verifica se o Excel tem todas as taxas necessárias para o período solicitado
"""
import logging
from datetime import date
from dateutil.relativedelta import relativedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class TaxasValidator:
    """Valida completude das taxas no Excel"""
    
    # Data da última atualização conhecida do Excel
    # TODO: Ler automaticamente do Excel ou configurar
    ULTIMA_ATUALIZACAO_EXCEL = date(2025, 1, 31)
    
    @staticmethod
    def verificar_periodo(
        data_inicio: date,
        data_fim: date,
        nome_taxa: str = "SELIC/IPCA"
    ) -> Dict:
        """
        Verifica se Excel tem taxas para todo o período
        
        Args:
            data_inicio: Data inicial do cálculo
            data_fim: Data final do cálculo
            nome_taxa: Nome da taxa para mensagem
            
        Returns:
            Dict com status e mensagens
        """
        try:
            ultima_taxa = TaxasValidator.ULTIMA_ATUALIZACAO_EXCEL
            
            # Se data_fim é posterior à última atualização
            if data_fim > ultima_taxa:
                meses_faltantes = TaxasValidator._calcular_meses_faltantes(
                    ultima_taxa, 
                    data_fim
                )
                
                return {
                    "completo": False,
                    "status": "desatualizado",
                    "ultima_taxa_disponivel": ultima_taxa.strftime("%d/%m/%Y"),
                    "meses_faltantes": meses_faltantes,
                    "message": (
                        f"⚠️ Excel tem taxas até {ultima_taxa.strftime('%m/%Y')}. "
                        f"Faltam {meses_faltantes} meses para cobrir até "
                        f"{data_fim.strftime('%m/%Y')}."
                    ),
                    "recomendacao": (
                        "Use API BACEN/IBGE para buscar taxas atualizadas ou "
                        "ajuste a data de correção até a última taxa disponível."
                    )
                }
            else:
                return {
                    "completo": True,
                    "status": "ok",
                    "ultima_taxa_disponivel": ultima_taxa.strftime("%d/%m/%Y"),
                    "message": f"✅ Excel tem todas as taxas {nome_taxa} necessárias."
                }
                
        except Exception as e:
            logger.error(f"Erro ao verificar período: {e}")
            return {
                "completo": None,
                "status": "erro",
                "message": f"❌ Erro ao verificar taxas: {str(e)}"
            }
    
    @staticmethod
    def _calcular_meses_faltantes(data_inicial: date, data_final: date) -> int:
        """Calcula número de meses entre duas datas"""
        diff = relativedelta(data_final, data_inicial)
        return diff.years * 12 + diff.months + (1 if diff.days > 0 else 0)
    
    @staticmethod
    def verificar_selic(data_inicio: date, data_fim: date) -> Dict:
        """Verifica completude das taxas SELIC"""
        return TaxasValidator.verificar_periodo(data_inicio, data_fim, "SELIC")
    
    @staticmethod
    def verificar_ipca(data_inicio: date, data_fim: date) -> Dict:
        """Verifica completude dos índices IPCA"""
        return TaxasValidator.verificar_periodo(data_inicio, data_fim, "IPCA")
    
    @staticmethod
    def verificar_completo(
        periodo_inicio: date,
        periodo_fim: date,
        correcao_ate: date
    ) -> Dict:
        """
        Verificação completa de todas as taxas necessárias
        
        Args:
            periodo_inicio: Início do período trabalhado
            periodo_fim: Fim do período trabalhado
            correcao_ate: Data até quando corrigir
            
        Returns:
            Dict com status detalhado
        """
        # Data mais recente que precisamos
        data_limite = max(periodo_fim, correcao_ate)
        
        # Verificar cada tipo de taxa
        selic_status = TaxasValidator.verificar_selic(periodo_inicio, data_limite)
        ipca_status = TaxasValidator.verificar_ipca(periodo_inicio, data_limite)
        
        # Consolidar resultado
        todas_ok = selic_status["completo"] and ipca_status["completo"]
        
        avisos = []
        if not selic_status["completo"]:
            avisos.append(selic_status["message"])
        if not ipca_status["completo"]:
            avisos.append(ipca_status["message"])
        
        return {
            "todas_taxas_disponiveis": todas_ok,
            "selic": selic_status,
            "ipca": ipca_status,
            "avisos": avisos,
            "recomendacao": (
                "✅ Todas as taxas disponíveis. Cálculo confiável." 
                if todas_ok else
                "⚠️ Algumas taxas indisponíveis. Considere atualizar Excel ou "
                "usar APIs (BACEN/IBGE) para dados recentes."
            )
        }


def validar_taxas_periodo(
    periodo_inicio: date,
    periodo_fim: date,
    correcao_ate: date
) -> Dict:
    """
    Função helper para validação de taxas
    
    Returns:
        Status da validação
    """
    validator = TaxasValidator()
    return validator.verificar_completo(periodo_inicio, periodo_fim, correcao_ate)


# Exemplo de uso
if __name__ == "__main__":
    # Cenário 1: Dentro do período disponível
    print("📊 Cenário 1: Cálculo até Janeiro/2025")
    resultado1 = validar_taxas_periodo(
        periodo_inicio=date(2020, 1, 1),
        periodo_fim=date(2023, 12, 31),
        correcao_ate=date(2025, 1, 15)
    )
    print(f"Status: {resultado1['todas_taxas_disponiveis']}")
    print(f"Recomendação: {resultado1['recomendacao']}\n")
    
    # Cenário 2: Além do período disponível
    print("📊 Cenário 2: Cálculo até Março/2025 (taxas desatualizadas)")
    resultado2 = validar_taxas_periodo(
        periodo_inicio=date(2020, 1, 1),
        periodo_fim=date(2023, 12, 31),
        correcao_ate=date(2025, 3, 31)
    )
    print(f"Status: {resultado2['todas_taxas_disponiveis']}")
    if resultado2['avisos']:
        for aviso in resultado2['avisos']:
            print(f"  {aviso}")
    print(f"Recomendação: {resultado2['recomendacao']}")
