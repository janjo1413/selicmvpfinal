"""
Serviço para integração com a API do IBGE
Permite buscar taxas de IPCA e IPCA-E atualizadas dinamicamente
"""

import requests
import json
import logging
from datetime import date, datetime
from typing import Optional, List, Dict
from pathlib import Path

logger = logging.getLogger(__name__)


class IbgeService:
    """
    Cliente para API do IBGE - Sistema de Recuperação Automática (SIDRA)
    
    Taxas disponíveis:
    - IPCA (Índice Nacional de Preços ao Consumidor Amplo) - Agregação 1737
    - IPCA-E (IPCA Especial) - Agregação 7060
    
    Documentação: https://servicodados.ibge.gov.br/api/docs/agregados
    
    Exemplo:
        >>> service = IbgeService()
        >>> taxas = service.buscar_ipca_periodo(date(2024, 1, 1), date(2024, 12, 31))
        >>> taxas[0]
        {'data': '01/2024', 'valor': 0.42}
    """
    
    AGREGACOES = {
        "IPCA": "1737",
        "IPCA-E": "7060"
    }
    
    def __init__(self, cache_dir: str = "data/cache", timeout: int = 10):
        """
        Inicializa serviço IBGE
        
        Args:
            cache_dir: Diretório para armazenar cache local
            timeout: Timeout para requisições HTTP (segundos)
        """
        self.base_url = "https://servicodados.ibge.gov.br/api/v3/agregados"
        self.cache_dir = Path(cache_dir)
        self.timeout = timeout
        
        logger.info("IbgeService inicializado")
    
    def buscar_ipca_periodo(
        self, 
        data_inicio: date, 
        data_fim: date,
        usar_cache: bool = True
    ) -> Optional[List[Dict]]:
        """
        Busca taxas IPCA para um período específico
        
        Args:
            data_inicio: Data inicial (YYYY-MM-DD)
            data_fim: Data final (YYYY-MM-DD)
            usar_cache: Se True, usa cache local antes de consultar API
            
        Returns:
            Lista de dicts com {'data': 'MM/YYYY', 'valor': 0.00}
            None se houver erro
        """
        return self._buscar_taxa_periodo("IPCA", data_inicio, data_fim, usar_cache)
    
    def buscar_ipca_e_periodo(
        self, 
        data_inicio: date, 
        data_fim: date,
        usar_cache: bool = True
    ) -> Optional[List[Dict]]:
        """
        Busca taxas IPCA-E para um período específico
        
        Args:
            data_inicio: Data inicial (YYYY-MM-DD)
            data_fim: Data final (YYYY-MM-DD)
            usar_cache: Se True, usa cache local antes de consultar API
            
        Returns:
            Lista de dicts com {'data': 'MM/YYYY', 'valor': 0.00}
            None se houver erro
        """
        return self._buscar_taxa_periodo("IPCA-E", data_inicio, data_fim, usar_cache)
    
    def _buscar_taxa_periodo(
        self,
        taxa_nome: str,
        data_inicio: date,
        data_fim: date,
        usar_cache: bool = True
    ) -> Optional[List[Dict]]:
        """
        Método genérico para buscar qualquer taxa do IBGE
        
        Args:
            taxa_nome: Nome da taxa ("IPCA" ou "IPCA-E")
            data_inicio: Data inicial
            data_fim: Data final
            usar_cache: Se deve usar cache
            
        Returns:
            Lista de taxas mensais
            
        Exemplo:
            >>> taxas = service._buscar_taxa_periodo("IPCA", date(2024, 1, 1), date(2024, 12, 31))
            >>> taxas[0]
            {'data': '01/2024', 'valor': 0.42}
        """
        try:
            agregacao = self.AGREGACOES.get(taxa_nome)
            if not agregacao:
                logger.error(f"Taxa desconhecida: {taxa_nome}")
                return None
            
            # Verificar cache primeiro
            if usar_cache:
                cached_data = self._ler_cache(taxa_nome, data_inicio, data_fim)
                if cached_data:
                    logger.info(f"Dados {taxa_nome} carregados do cache ({len(cached_data)} registros)")
                    return cached_data
            
            # Formatar período para API (YYYYMM-YYYYMM)
            periodo_inicio = data_inicio.strftime("%Y%m")
            periodo_fim = data_fim.strftime("%Y%m")
            periodo_str = f"{periodo_inicio}-{periodo_fim}"
            
            # Montar URL
            # Estrutura: /agregacao/periodos/YYYYMM-YYYYMM/variaveis/63?localidades=N1[all]
            # Variável 63 = Variação mensal (%)
            # N1[all] = Brasil
            url = f"{self.base_url}/{agregacao}/periodos/{periodo_str}/variaveis/63"
            params = {
                "localidades": "N1[all]"
            }
            
            logger.info(f"Buscando {taxa_nome} de {data_inicio.strftime('%m/%Y')} a {data_fim.strftime('%m/%Y')}...")
            
            # Fazer requisição
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            # Processar resposta (estrutura complexa do IBGE)
            dados_json = response.json()
            
            if not dados_json or len(dados_json) == 0:
                logger.warning(f"Nenhum dado {taxa_nome} retornado para o período")
                return None
            
            # Extrair dados da estrutura do IBGE
            # Formato: [{"resultados": [{"series": [{"serie": {"YYYYMM": "valor"}}]}]}]
            dados_processados = self._processar_resposta_ibge(dados_json)
            
            if not dados_processados:
                logger.warning(f"Não foi possível processar dados {taxa_nome}")
                return None
            
            logger.info(f"✅ {len(dados_processados)} taxas {taxa_nome} obtidas da API IBGE")
            
            # Salvar no cache
            self._salvar_cache(taxa_nome, dados_processados, data_inicio, data_fim)
            
            return dados_processados
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao buscar {taxa_nome} (>{self.timeout}s)")
            return self._usar_fallback(taxa_nome)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição IBGE para {taxa_nome}: {e}")
            return self._usar_fallback(taxa_nome)
            
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar {taxa_nome}: {e}", exc_info=True)
            return self._usar_fallback(taxa_nome)
    
    def _processar_resposta_ibge(self, dados_json: List[Dict]) -> List[Dict]:
        """
        Processa a resposta complexa da API do IBGE
        
        Estrutura esperada:
        [
            {
                "resultados": [
                    {
                        "series": [
                            {
                                "serie": {
                                    "202401": "0.42",
                                    "202402": "0.83",
                                    ...
                                }
                            }
                        ]
                    }
                ]
            }
        ]
        
        Args:
            dados_json: Resposta JSON da API
            
        Returns:
            Lista de dicts com {'data': 'MM/YYYY', 'valor': 0.00}
        """
        try:
            resultados = []
            
            # Navegar pela estrutura aninhada
            for item in dados_json:
                if 'resultados' not in item:
                    continue
                
                for resultado in item['resultados']:
                    if 'series' not in resultado:
                        continue
                    
                    for serie_obj in resultado['series']:
                        if 'serie' not in serie_obj:
                            continue
                        
                        serie = serie_obj['serie']
                        
                        # Processar cada período (YYYYMM: "valor")
                        for periodo_str, valor_str in serie.items():
                            try:
                                # Converter YYYYMM para MM/YYYY
                                ano = periodo_str[:4]
                                mes = periodo_str[4:6]
                                data_formatada = f"{mes}/{ano}"
                                
                                # Converter valor
                                valor = float(valor_str)
                                
                                resultados.append({
                                    'data': data_formatada,
                                    'valor': valor
                                })
                            except (ValueError, KeyError) as e:
                                logger.warning(f"Erro ao processar período {periodo_str}: {e}")
                                continue
            
            return resultados
            
        except Exception as e:
            logger.error(f"Erro ao processar resposta IBGE: {e}")
            return []
    
    def _ler_cache(self, taxa_nome: str, data_inicio: date, data_fim: date) -> Optional[List[Dict]]:
        """Lê dados do cache local se disponível e dentro do período"""
        try:
            cache_file = self.cache_dir / f"{taxa_nome.lower().replace('-', '_')}_cache.json"
            if not cache_file.exists():
                return None
            
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            
            # Verificar se cache cobre o período solicitado
            cache_inicio = datetime.strptime(cache['data_inicio'], '%Y-%m-%d').date()
            cache_fim = datetime.strptime(cache['data_fim'], '%Y-%m-%d').date()
            
            if cache_inicio <= data_inicio and cache_fim >= data_fim:
                # Filtrar dados do período
                dados_filtrados = []
                for d in cache['dados']:
                    # Converter MM/YYYY para date
                    mes, ano = d['data'].split('/')
                    data_registro = date(int(ano), int(mes), 1)
                    
                    if data_inicio <= data_registro <= data_fim:
                        dados_filtrados.append(d)
                
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
            
            cache_file = self.cache_dir / f"{taxa_nome.lower().replace('-', '_')}_cache.json"
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
        logger.warning(f"⚠️ API IBGE indisponível para {taxa_nome}. Tentando usar cache local...")
        
        try:
            cache_file = self.cache_dir / f"{taxa_nome.lower().replace('-', '_')}_cache.json"
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                
                logger.info(f"✅ Usando cache {taxa_nome} local ({len(cache['dados'])} registros)")
                return cache['dados']
        
        except Exception as e:
            logger.error(f"Erro ao ler cache fallback {taxa_nome}: {e}")
        
        logger.error(f"❌ Nenhuma fonte de dados {taxa_nome} disponível")
        return None
    
    def verificar_disponibilidade(self, taxa_nome: str = "IPCA") -> bool:
        """
        Verifica se a API IBGE está disponível para uma taxa específica
        
        Args:
            taxa_nome: Nome da taxa a verificar (default: IPCA)
            
        Returns:
            True se API está respondendo, False caso contrário
        """
        try:
            agregacao = self.AGREGACOES.get(taxa_nome)
            if not agregacao:
                logger.error(f"Taxa desconhecida: {taxa_nome}")
                return False
            
            # Buscar apenas último período para testar
            hoje = date.today()
            periodo_str = hoje.strftime("%Y%m")
            url = f"{self.base_url}/{agregacao}/periodos/{periodo_str}/variaveis/63"
            params = {"localidades": "N1[all]"}
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            logger.info(f"✅ API IBGE disponível para {taxa_nome}")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ API IBGE indisponível para {taxa_nome}: {e}")
            return False


# Funções auxiliares para uso direto
def obter_ipca_atualizado(data_inicio: date, data_fim: date) -> Optional[List[Dict]]:
    """
    Atalho para buscar IPCA atualizado
    
    Args:
        data_inicio: Data inicial do período
        data_fim: Data final do período
        
    Returns:
        Lista de taxas IPCA mensais
    """
    service = IbgeService()
    return service.buscar_ipca_periodo(data_inicio, data_fim)


def obter_ipca_e_atualizado(data_inicio: date, data_fim: date) -> Optional[List[Dict]]:
    """
    Atalho para buscar IPCA-E atualizado
    
    Args:
        data_inicio: Data inicial do período
        data_fim: Data final do período
        
    Returns:
        Lista de taxas IPCA-E mensais
    """
    service = IbgeService()
    return service.buscar_ipca_e_periodo(data_inicio, data_fim)
