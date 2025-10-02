"""
Validador completo de taxas - verifica SELIC, IPCA, TR e IPCA-E
Usa APIs do BACEN e IBGE para determinar disponibilidade real
"""

import logging
from datetime import date
from typing import Dict, List, Optional
from dataclasses import dataclass

from src.bacen_service import BacenService
from src.ibge_service import IbgeService

logger = logging.getLogger(__name__)


@dataclass
class ResultadoValidacaoTaxa:
    """Resultado da validação de uma taxa específica"""
    taxa_nome: str
    disponivel_excel: bool
    disponivel_api: bool
    ultimo_mes_excel: Optional[str]  # MM/YYYY
    ultimo_mes_api: Optional[str]    # MM/YYYY
    meses_faltando: int
    requer_atualizacao: bool
    mensagem: str


class TaxasCompletoValidator:
    """
    Validador completo que verifica disponibilidade de todas as taxas
    
    Verifica 4 taxas essenciais:
    - SELIC (Banco Central)
    - TR - Taxa Referencial (Banco Central)
    - IPCA (IBGE)
    - IPCA-E (IBGE)
    
    Usa APIs para determinar se há meses faltando no Excel
    
    Exemplo:
        >>> validator = TaxasCompletoValidator()
        >>> resultado = validator.validar_todas(date(2020, 1, 1), date(2025, 10, 1))
        >>> print(resultado['resumo'])
        {'total_taxas': 4, 'ok': 0, 'desatualizadas': 4}
    """
    
    # Data da última atualização manual do Excel
    ULTIMA_ATUALIZACAO_EXCEL = date(2025, 1, 31)
    
    def __init__(self):
        """Inicializa serviços de API"""
        self.bacen = BacenService()
        self.ibge = IbgeService()
        
        logger.info("TaxasCompletoValidator inicializado")
    
    def validar_todas(
        self, 
        data_inicio: date, 
        data_fim: date,
        verificar_apis: bool = True
    ) -> Dict:
        """
        Valida disponibilidade de todas as 4 taxas
        
        Args:
            data_inicio: Data inicial do cálculo
            data_fim: Data final do cálculo
            verificar_apis: Se True, tenta buscar nas APIs para confirmar disponibilidade
            
        Returns:
            Dict com resultados detalhados:
            {
                'resumo': {'total_taxas': 4, 'ok': 0, 'desatualizadas': 4},
                'taxas': {
                    'SELIC': ResultadoValidacaoTaxa(...),
                    'TR': ResultadoValidacaoTaxa(...),
                    'IPCA': ResultadoValidacaoTaxa(...),
                    'IPCA-E': ResultadoValidacaoTaxa(...)
                },
                'requer_atualizacao': True,
                'mensagem': 'Excel desatualizado. 4/4 taxas precisam de atualização.'
            }
        """
        resultados = {}
        
        # Validar cada taxa
        resultados['SELIC'] = self._validar_selic(data_inicio, data_fim, verificar_apis)
        resultados['TR'] = self._validar_tr(data_inicio, data_fim, verificar_apis)
        resultados['IPCA'] = self._validar_ipca(data_inicio, data_fim, verificar_apis)
        resultados['IPCA-E'] = self._validar_ipca_e(data_inicio, data_fim, verificar_apis)
        
        # Gerar resumo
        total = len(resultados)
        ok = sum(1 for r in resultados.values() if not r.requer_atualizacao)
        desatualizadas = total - ok
        
        resumo = {
            'total_taxas': total,
            'ok': ok,
            'desatualizadas': desatualizadas
        }
        
        # Mensagem final
        if desatualizadas == 0:
            mensagem = f"✅ Todas as {total} taxas estão atualizadas no Excel."
            requer_atualizacao = False
        else:
            mensagem = f"⚠️ Excel desatualizado. {desatualizadas}/{total} taxas precisam de atualização."
            requer_atualizacao = True
        
        return {
            'resumo': resumo,
            'taxas': resultados,
            'requer_atualizacao': requer_atualizacao,
            'mensagem': mensagem
        }
    
    def _validar_selic(self, data_inicio: date, data_fim: date, verificar_api: bool) -> ResultadoValidacaoTaxa:
        """Valida disponibilidade da SELIC"""
        try:
            # Verificar Excel
            disponivel_excel = data_fim <= self.ULTIMA_ATUALIZACAO_EXCEL
            ultimo_mes_excel = self.ULTIMA_ATUALIZACAO_EXCEL.strftime("%m/%Y")
            
            # Calcular meses faltando
            meses_faltando = self._calcular_meses_faltando(self.ULTIMA_ATUALIZACAO_EXCEL, data_fim)
            
            # Verificar API se solicitado
            disponivel_api = False
            ultimo_mes_api = None
            
            if verificar_api and meses_faltando > 0:
                try:
                    # Tentar buscar últimos dados
                    dados_api = self.bacen.buscar_selic_periodo(
                        self.ULTIMA_ATUALIZACAO_EXCEL,
                        data_fim,
                        usar_cache=False
                    )
                    
                    if dados_api and len(dados_api) > 0:
                        disponivel_api = True
                        # Último registro: {'data': 'DD/MM/YYYY', 'valor': ...}
                        ultimo_registro = dados_api[-1]['data']
                        # Converter DD/MM/YYYY para MM/YYYY
                        partes = ultimo_registro.split('/')
                        ultimo_mes_api = f"{partes[1]}/{partes[2]}"
                        
                except Exception as e:
                    logger.warning(f"Erro ao verificar API SELIC: {e}")
            
            # Determinar se requer atualização
            requer_atualizacao = meses_faltando > 0
            
            # Mensagem
            if requer_atualizacao:
                if disponivel_api:
                    mensagem = f"SELIC: Excel até {ultimo_mes_excel}, API até {ultimo_mes_api}. {meses_faltando} meses faltando."
                else:
                    mensagem = f"SELIC: Excel até {ultimo_mes_excel}. {meses_faltando} meses faltando (API não verificada)."
            else:
                mensagem = f"SELIC: OK até {ultimo_mes_excel}"
            
            return ResultadoValidacaoTaxa(
                taxa_nome="SELIC",
                disponivel_excel=disponivel_excel,
                disponivel_api=disponivel_api,
                ultimo_mes_excel=ultimo_mes_excel,
                ultimo_mes_api=ultimo_mes_api,
                meses_faltando=meses_faltando,
                requer_atualizacao=requer_atualizacao,
                mensagem=mensagem
            )
            
        except Exception as e:
            logger.error(f"Erro ao validar SELIC: {e}")
            return ResultadoValidacaoTaxa(
                taxa_nome="SELIC",
                disponivel_excel=False,
                disponivel_api=False,
                ultimo_mes_excel=None,
                ultimo_mes_api=None,
                meses_faltando=-1,
                requer_atualizacao=True,
                mensagem=f"Erro ao validar SELIC: {e}"
            )
    
    def _validar_tr(self, data_inicio: date, data_fim: date, verificar_api: bool) -> ResultadoValidacaoTaxa:
        """Valida disponibilidade da TR"""
        try:
            disponivel_excel = data_fim <= self.ULTIMA_ATUALIZACAO_EXCEL
            ultimo_mes_excel = self.ULTIMA_ATUALIZACAO_EXCEL.strftime("%m/%Y")
            meses_faltando = self._calcular_meses_faltando(self.ULTIMA_ATUALIZACAO_EXCEL, data_fim)
            
            disponivel_api = False
            ultimo_mes_api = None
            
            if verificar_api and meses_faltando > 0:
                try:
                    dados_api = self.bacen.buscar_tr_periodo(
                        self.ULTIMA_ATUALIZACAO_EXCEL,
                        data_fim,
                        usar_cache=False
                    )
                    
                    if dados_api and len(dados_api) > 0:
                        disponivel_api = True
                        ultimo_registro = dados_api[-1]['data']
                        partes = ultimo_registro.split('/')
                        ultimo_mes_api = f"{partes[1]}/{partes[2]}"
                        
                except Exception as e:
                    logger.warning(f"Erro ao verificar API TR: {e}")
            
            requer_atualizacao = meses_faltando > 0
            
            if requer_atualizacao:
                if disponivel_api:
                    mensagem = f"TR: Excel até {ultimo_mes_excel}, API até {ultimo_mes_api}. {meses_faltando} meses faltando."
                else:
                    mensagem = f"TR: Excel até {ultimo_mes_excel}. {meses_faltando} meses faltando (API não verificada)."
            else:
                mensagem = f"TR: OK até {ultimo_mes_excel}"
            
            return ResultadoValidacaoTaxa(
                taxa_nome="TR",
                disponivel_excel=disponivel_excel,
                disponivel_api=disponivel_api,
                ultimo_mes_excel=ultimo_mes_excel,
                ultimo_mes_api=ultimo_mes_api,
                meses_faltando=meses_faltando,
                requer_atualizacao=requer_atualizacao,
                mensagem=mensagem
            )
            
        except Exception as e:
            logger.error(f"Erro ao validar TR: {e}")
            return ResultadoValidacaoTaxa(
                taxa_nome="TR",
                disponivel_excel=False,
                disponivel_api=False,
                ultimo_mes_excel=None,
                ultimo_mes_api=None,
                meses_faltando=-1,
                requer_atualizacao=True,
                mensagem=f"Erro ao validar TR: {e}"
            )
    
    def _validar_ipca(self, data_inicio: date, data_fim: date, verificar_api: bool) -> ResultadoValidacaoTaxa:
        """Valida disponibilidade do IPCA"""
        try:
            disponivel_excel = data_fim <= self.ULTIMA_ATUALIZACAO_EXCEL
            ultimo_mes_excel = self.ULTIMA_ATUALIZACAO_EXCEL.strftime("%m/%Y")
            meses_faltando = self._calcular_meses_faltando(self.ULTIMA_ATUALIZACAO_EXCEL, data_fim)
            
            disponivel_api = False
            ultimo_mes_api = None
            
            if verificar_api and meses_faltando > 0:
                try:
                    dados_api = self.ibge.buscar_ipca_periodo(
                        self.ULTIMA_ATUALIZACAO_EXCEL,
                        data_fim,
                        usar_cache=False
                    )
                    
                    if dados_api and len(dados_api) > 0:
                        disponivel_api = True
                        # Último registro já vem como {'data': 'MM/YYYY', 'valor': ...}
                        ultimo_mes_api = dados_api[-1]['data']
                        
                except Exception as e:
                    logger.warning(f"Erro ao verificar API IPCA: {e}")
            
            requer_atualizacao = meses_faltando > 0
            
            if requer_atualizacao:
                if disponivel_api:
                    mensagem = f"IPCA: Excel até {ultimo_mes_excel}, API até {ultimo_mes_api}. {meses_faltando} meses faltando."
                else:
                    mensagem = f"IPCA: Excel até {ultimo_mes_excel}. {meses_faltando} meses faltando (API não verificada)."
            else:
                mensagem = f"IPCA: OK até {ultimo_mes_excel}"
            
            return ResultadoValidacaoTaxa(
                taxa_nome="IPCA",
                disponivel_excel=disponivel_excel,
                disponivel_api=disponivel_api,
                ultimo_mes_excel=ultimo_mes_excel,
                ultimo_mes_api=ultimo_mes_api,
                meses_faltando=meses_faltando,
                requer_atualizacao=requer_atualizacao,
                mensagem=mensagem
            )
            
        except Exception as e:
            logger.error(f"Erro ao validar IPCA: {e}")
            return ResultadoValidacaoTaxa(
                taxa_nome="IPCA",
                disponivel_excel=False,
                disponivel_api=False,
                ultimo_mes_excel=None,
                ultimo_mes_api=None,
                meses_faltando=-1,
                requer_atualizacao=True,
                mensagem=f"Erro ao validar IPCA: {e}"
            )
    
    def _validar_ipca_e(self, data_inicio: date, data_fim: date, verificar_api: bool) -> ResultadoValidacaoTaxa:
        """Valida disponibilidade do IPCA-E"""
        try:
            disponivel_excel = data_fim <= self.ULTIMA_ATUALIZACAO_EXCEL
            ultimo_mes_excel = self.ULTIMA_ATUALIZACAO_EXCEL.strftime("%m/%Y")
            meses_faltando = self._calcular_meses_faltando(self.ULTIMA_ATUALIZACAO_EXCEL, data_fim)
            
            disponivel_api = False
            ultimo_mes_api = None
            
            if verificar_api and meses_faltando > 0:
                try:
                    dados_api = self.ibge.buscar_ipca_e_periodo(
                        self.ULTIMA_ATUALIZACAO_EXCEL,
                        data_fim,
                        usar_cache=False
                    )
                    
                    if dados_api and len(dados_api) > 0:
                        disponivel_api = True
                        ultimo_mes_api = dados_api[-1]['data']
                        
                except Exception as e:
                    logger.warning(f"Erro ao verificar API IPCA-E: {e}")
            
            requer_atualizacao = meses_faltando > 0
            
            if requer_atualizacao:
                if disponivel_api:
                    mensagem = f"IPCA-E: Excel até {ultimo_mes_excel}, API até {ultimo_mes_api}. {meses_faltando} meses faltando."
                else:
                    mensagem = f"IPCA-E: Excel até {ultimo_mes_excel}. {meses_faltando} meses faltando (API não verificada)."
            else:
                mensagem = f"IPCA-E: OK até {ultimo_mes_excel}"
            
            return ResultadoValidacaoTaxa(
                taxa_nome="IPCA-E",
                disponivel_excel=disponivel_excel,
                disponivel_api=disponivel_api,
                ultimo_mes_excel=ultimo_mes_excel,
                ultimo_mes_api=ultimo_mes_api,
                meses_faltando=meses_faltando,
                requer_atualizacao=requer_atualizacao,
                mensagem=mensagem
            )
            
        except Exception as e:
            logger.error(f"Erro ao validar IPCA-E: {e}")
            return ResultadoValidacaoTaxa(
                taxa_nome="IPCA-E",
                disponivel_excel=False,
                disponivel_api=False,
                ultimo_mes_excel=None,
                ultimo_mes_api=None,
                meses_faltando=-1,
                requer_atualizacao=True,
                mensagem=f"Erro ao validar IPCA-E: {e}"
            )
    
    def _calcular_meses_faltando(self, ultima_atualizacao: date, data_fim: date) -> int:
        """
        Calcula quantos meses estão faltando entre última atualização e data fim
        
        Args:
            ultima_atualizacao: Data da última atualização do Excel
            data_fim: Data final do cálculo
            
        Returns:
            Número de meses faltando (0 se não falta nada)
        """
        if data_fim <= ultima_atualizacao:
            return 0
        
        # Calcular diferença em meses
        meses = (data_fim.year - ultima_atualizacao.year) * 12
        meses += data_fim.month - ultima_atualizacao.month
        
        return max(0, meses)
    
    def gerar_relatorio(self, resultado: Dict) -> str:
        """
        Gera relatório formatado da validação
        
        Args:
            resultado: Dict retornado por validar_todas()
            
        Returns:
            String com relatório formatado
        """
        linhas = []
        linhas.append("=" * 70)
        linhas.append("VALIDAÇÃO DE TAXAS - RELATÓRIO COMPLETO")
        linhas.append("=" * 70)
        linhas.append("")
        
        # Resumo
        resumo = resultado['resumo']
        linhas.append(f"📊 RESUMO:")
        linhas.append(f"   Total de taxas: {resumo['total_taxas']}")
        linhas.append(f"   ✅ Atualizadas: {resumo['ok']}")
        linhas.append(f"   ⚠️  Desatualizadas: {resumo['desatualizadas']}")
        linhas.append("")
        
        # Detalhes por taxa
        linhas.append("📋 DETALHES POR TAXA:")
        linhas.append("")
        
        for taxa_nome, taxa_resultado in resultado['taxas'].items():
            status = "✅" if not taxa_resultado.requer_atualizacao else "⚠️"
            linhas.append(f"{status} {taxa_resultado.mensagem}")
        
        linhas.append("")
        linhas.append("=" * 70)
        linhas.append(resultado['mensagem'])
        linhas.append("=" * 70)
        
        return "\n".join(linhas)


def validar_taxas_necessarias(data_inicio: date, data_fim: date) -> Dict:
    """
    Atalho para validar todas as taxas necessárias
    
    Args:
        data_inicio: Data inicial do cálculo
        data_fim: Data final do cálculo
        
    Returns:
        Dict com resultados da validação
    """
    validator = TaxasCompletoValidator()
    return validator.validar_todas(data_inicio, data_fim)
