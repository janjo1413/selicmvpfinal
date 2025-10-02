"""
Serviço de integração com API do Banco Central (BACEN)
Busca taxas SELIC atualizadas dinamicamente
"""
import logging
import requests
from datetime import datetime, date
from typing import Dict, List, Optional
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class BacenService:
    """
    Serviço para buscar taxas SELIC e TR da API do BACEN
    
    API BACEN: https://api.bcb.gov.br/dados/serie/bcdata.sgs
    Séries:
    - 11: Taxa SELIC
    - 226: Taxa Referencial (TR)
    
    Documentação: https://dadosabertos.bcb.gov.br/
    """
    
    # Códigos das séries do BACEN
    SERIES = {
        "SELIC": "11",
        "TR": "226"
    }
    
    def __init__(self, base_url: str = None):
        """
        Inicializa o serviço BACEN
        
        Args:
            base_url: URL base da API BACEN
        """
        if base_url is None:
            # Usar URL padrão da API BACEN (sem /dados no final)
            base_url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs"
        
        # Remove trailing slash if present
        self.base_url = base_url.rstrip('/')
        self.cache_dir = Path(__file__).parent.parent / "data" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.timeout = 10  # segundos
        
        logger.info(f"BacenService inicializado: {self.base_url}")
    
    def buscar_selic_periodo(
        self, 
        data_inicio: date, 
        data_fim: date,
        usar_cache: bool = True
    ) -> Optional[List[Dict]]:
        """
        Busca taxas SELIC para um período específico
        
        Args:
            data_inicio: Data inicial (YYYY-MM-DD)
            data_fim: Data final (YYYY-MM-DD)
            usar_cache: Se True, usa cache local antes de consultar API
            
        Returns:
            Lista de dicts com {'data': 'DD/MM/YYYY', 'valor': 0.00}
            None se houver erro
        """
        return self._buscar_taxa_periodo("SELIC", data_inicio, data_fim, usar_cache)
    
    def buscar_tr_periodo(
        self, 
        data_inicio: date, 
        data_fim: date,
        usar_cache: bool = True
    ) -> Optional[List[Dict]]:
        """
        Busca taxas TR (Taxa Referencial) para um período específico
        
        Args:
            data_inicio: Data inicial (YYYY-MM-DD)
            data_fim: Data final (YYYY-MM-DD)
            usar_cache: Se True, usa cache local antes de consultar API
            
        Returns:
            Lista de dicts com {'data': 'DD/MM/YYYY', 'valor': 0.00}
            None se houver erro
        """
        return self._buscar_taxa_periodo("TR", data_inicio, data_fim, usar_cache)
    
    def _buscar_taxa_periodo(
        self,
        taxa_nome: str,
        data_inicio: date,
        data_fim: date,
        usar_cache: bool = True
    ) -> Optional[List[Dict]]:
        """
        Método genérico para buscar qualquer taxa do BACEN
        
        Args:
            taxa_nome: Nome da taxa ("SELIC" ou "TR")
            data_inicio: Data inicial
            data_fim: Data final
            usar_cache: Se deve usar cache
            
        Returns:
            Lista de taxas
            
        Exemplo:
            >>> taxas = service._buscar_taxa_periodo("SELIC", date(2024, 1, 1), date(2024, 12, 31))
            >>> taxas[0]
            {'data': '02/01/2024', 'valor': 11.75}
        """
        try:
            serie_codigo = self.SERIES.get(taxa_nome)
            if not serie_codigo:
                logger.error(f"Taxa desconhecida: {taxa_nome}")
                return None
            
            # Verificar cache primeiro
            if usar_cache:
                cached_data = self._ler_cache(taxa_nome, data_inicio, data_fim)
                if cached_data:
                    logger.info(f"Dados {taxa_nome} carregados do cache ({len(cached_data)} registros)")
                    return cached_data
            
            # Formatar datas para API (DD/MM/YYYY)
            data_inicio_str = data_inicio.strftime("%d/%m/%Y")
            data_fim_str = data_fim.strftime("%d/%m/%Y")
            
            # Montar URL
            # Formato: https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados
            url = f"{self.base_url}.{serie_codigo}/dados"
            params = {
                "formato": "json",
                "dataInicial": data_inicio_str,
                "dataFinal": data_fim_str
            }
            
            logger.info(f"Buscando {taxa_nome} de {data_inicio_str} a {data_fim_str}...")
            
            # Fazer requisição
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            # Processar resposta
            dados = response.json()
            
            if not dados or len(dados) == 0:
                logger.warning(f"Nenhum dado {taxa_nome} retornado para o período")
                return None
            
            logger.info(f"✅ {len(dados)} taxas {taxa_nome} obtidas da API BACEN")
            
            # Salvar no cache
            self._salvar_cache(taxa_nome, dados, data_inicio, data_fim)
            
            return dados
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao buscar {taxa_nome} (>{self.timeout}s)")
            return self._usar_fallback(taxa_nome)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição BACEN para {taxa_nome}: {e}")
            return self._usar_fallback(taxa_nome)
            
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar {taxa_nome}: {e}", exc_info=True)
            return self._usar_fallback(taxa_nome)
    
    def buscar_selic_mes(self, ano: int, mes: int) -> Optional[float]:
        """
        Busca taxa SELIC acumulada para um mês específico
        
        Args:
            ano: Ano (ex: 2024)
            mes: Mês (1-12)
            
        Returns:
            Taxa SELIC mensal acumulada (%)
            None se houver erro
        """
        try:
            data_inicio = date(ano, mes, 1)
            
            # Último dia do mês
            if mes == 12:
                data_fim = date(ano, 12, 31)
            else:
                data_fim = date(ano, mes + 1, 1).replace(day=1)
                data_fim = data_fim.replace(day=1)  # Primeiro dia do mês seguinte
                from datetime import timedelta
                data_fim = data_fim - timedelta(days=1)  # Último dia do mês atual
            
            taxas = self.buscar_selic_periodo(data_inicio, data_fim)
            
            if not taxas:
                return None
            
            # Calcular taxa acumulada do mês
            # Fórmula: [(1 + taxa1/100) * (1 + taxa2/100) * ... - 1] * 100
            fator_acumulado = 1.0
            for registro in taxas:
                taxa_dia = float(registro['valor'])
                fator_acumulado *= (1 + taxa_dia / 100)
            
            taxa_mensal = (fator_acumulado - 1) * 100
            
            logger.info(f"SELIC {mes:02d}/{ano}: {taxa_mensal:.4f}%")
            return round(taxa_mensal, 4)
            
        except Exception as e:
            logger.error(f"Erro ao calcular SELIC mensal: {e}")
            return None
    
    def _ler_cache(self, taxa_nome: str, data_inicio: date, data_fim: date) -> Optional[List[Dict]]:
        """Lê dados do cache local se disponível e dentro do período"""
        try:
            cache_file = self.cache_dir / f"{taxa_nome.lower()}_cache.json"
            if not cache_file.exists():
                return None
            
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            
            # Verificar se cache cobre o período solicitado
            cache_inicio = datetime.strptime(cache['data_inicio'], '%Y-%m-%d').date()
            cache_fim = datetime.strptime(cache['data_fim'], '%Y-%m-%d').date()
            
            if cache_inicio <= data_inicio and cache_fim >= data_fim:
                # Filtrar dados do período
                dados_filtrados = [
                    d for d in cache['dados']
                    if data_inicio <= datetime.strptime(d['data'], '%d/%m/%Y').date() <= data_fim
                ]
                return dados_filtrados if dados_filtrados else None
            
            return None
            
        except Exception as e:
            logger.debug(f"Cache {taxa_nome} não disponível: {e}")
            return None
    
    def _salvar_cache(self, taxa_nome: str, dados: List[Dict], data_inicio: date, data_fim: date):
        """Salva dados no cache local"""
        try:
            # Criar diretório se não existir
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            
            cache_file = self.cache_dir / f"{taxa_nome.lower()}_cache.json"
            cache = {
                'taxa': taxa_nome,
                'data_inicio': data_inicio.strftime('%Y-%m-%d'),
                'data_fim': data_fim.strftime('%Y-%m-%d'),
                'atualizado_em': datetime.now().isoformat(),
                'dados': dados
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
            
            logger.debug(f"Cache {taxa_nome} salvo: {len(dados)} registros")
            
        except Exception as e:
            logger.warning(f"Erro ao salvar cache {taxa_nome}: {e}")
    
    def _usar_fallback(self, taxa_nome: str) -> Optional[List[Dict]]:
        """
        Usa cache local como fallback quando API falha
        """
        logger.warning(f"⚠️ API BACEN indisponível para {taxa_nome}. Tentando usar cache local...")
        
        try:
            cache_file = self.cache_dir / f"{taxa_nome.lower()}_cache.json"
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                
                logger.info(f"✅ Usando cache {taxa_nome} local ({len(cache['dados'])} registros)")
                return cache['dados']
        except Exception as e:
            logger.error(f"Erro ao ler cache fallback {taxa_nome}: {e}")
        
        logger.error(f"❌ Nenhuma fonte de dados {taxa_nome} disponível")
        return None
    
    def verificar_disponibilidade(self, taxa_nome: str = "SELIC") -> bool:
        """
        Verifica se a API BACEN está disponível para uma taxa específica
        
        Args:
            taxa_nome: Nome da taxa a verificar (default: SELIC)
            
        Returns:
            True se API está respondendo, False caso contrário
        """
        try:
            serie_codigo = self.SERIES.get(taxa_nome)
            if not serie_codigo:
                logger.error(f"Taxa desconhecida: {taxa_nome}")
                return False
            
            # Buscar apenas 1 registro recente para testar
            # Formato: https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/1
            url = f"{self.base_url}.{serie_codigo}/dados/ultimos/1"
            
            response = requests.get(url, params={"formato": "json"}, timeout=5)
            response.raise_for_status()
            
            logger.info(f"✅ API BACEN disponível para {taxa_nome}")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ API BACEN indisponível para {taxa_nome}: {e}")
            return False


# Funções auxiliares para uso direto
def obter_selic_atualizada(data_inicio: date, data_fim: date) -> Optional[List[Dict]]:
    """
    Função helper para obter SELIC atualizada
    
    Args:
        data_inicio: Data inicial
        data_fim: Data final
        
    Returns:
        Lista de taxas SELIC ou None
    """
    service = BacenService()
    return service.buscar_selic_periodo(data_inicio, data_fim)


def verificar_api_bacen() -> bool:
    """
    Função helper para verificar disponibilidade da API
    
    Returns:
        True se disponível
    """
    service = BacenService()
    return service.verificar_disponibilidade()
