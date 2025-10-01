"""
Cliente para Microsoft Graph API
"""
import requests
import logging
from typing import Optional, Dict, Any, List
from msal import ConfidentialClientApplication
import config

logger = logging.getLogger(__name__)


class GraphClient:
    """Cliente para interagir com Microsoft Graph Excel API"""
    
    def __init__(self):
        self.client_app = ConfidentialClientApplication(
            config.CLIENT_ID,
            authority=config.AUTHORITY,
            client_credential=config.CLIENT_SECRET,
        )
        self.token = None
        self.session_id = None
        self.workbook_id = config.WORKBOOK_ID
        self.drive_id = config.DRIVE_ID
        
    def _get_token(self) -> str:
        """Obtém token de acesso do Azure AD"""
        if self.token:
            return self.token
            
        result = self.client_app.acquire_token_for_client(scopes=config.SCOPE)
        
        if "access_token" in result:
            self.token = result["access_token"]
            logger.info("Token obtido com sucesso")
            return self.token
        else:
            error = result.get("error")
            error_desc = result.get("error_description")
            logger.error(f"Erro ao obter token: {error} - {error_desc}")
            raise Exception(f"Erro na autenticação: {error}")
    
    def _get_headers(self) -> Dict[str, str]:
        """Retorna headers com autenticação"""
        headers = {
            "Authorization": f"Bearer {self._get_token()}",
            "Content-Type": "application/json"
        }
        
        if self.session_id:
            headers["workbook-session-id"] = self.session_id
            
        return headers
    
    def _get_base_url(self) -> str:
        """Retorna URL base para o workbook"""
        if self.drive_id:
            return f"{config.GRAPH_API_ENDPOINT}/drives/{self.drive_id}/items/{self.workbook_id}/workbook"
        return f"{config.GRAPH_API_ENDPOINT}/me/drive/items/{self.workbook_id}/workbook"
    
    def create_session(self, persist_changes: bool = False) -> str:
        """
        Cria uma sessão de trabalho no Excel
        
        Args:
            persist_changes: Se True, salva alterações na planilha
            
        Returns:
            Session ID
        """
        url = f"{self._get_base_url()}/createSession"
        payload = {"persistChanges": persist_changes}
        
        response = requests.post(url, headers=self._get_headers(), json=payload)
        response.raise_for_status()
        
        data = response.json()
        self.session_id = data.get("id")
        logger.info(f"Sessão criada: {self.session_id}")
        
        return self.session_id
    
    def close_session(self):
        """Fecha a sessão atual"""
        if not self.session_id:
            return
            
        url = f"{self._get_base_url()}/closeSession"
        
        try:
            response = requests.post(url, headers=self._get_headers())
            response.raise_for_status()
            logger.info(f"Sessão fechada: {self.session_id}")
        except Exception as e:
            logger.warning(f"Erro ao fechar sessão: {e}")
        finally:
            self.session_id = None
    
    def write_cell(self, worksheet: str, address: str, value: Any):
        """
        Escreve um valor em uma célula
        
        Args:
            worksheet: Nome da aba
            address: Endereço da célula (ex: 'B6')
            value: Valor a escrever
        """
        url = f"{self._get_base_url()}/worksheets/{worksheet}/range(address='{address}')"
        payload = {"values": [[value]]}
        
        response = requests.patch(url, headers=self._get_headers(), json=payload)
        response.raise_for_status()
        
        logger.debug(f"Escrito {value} em {worksheet}!{address}")
    
    def read_range(self, worksheet: str, address: str) -> List[List[Any]]:
        """
        Lê valores de um range
        
        Args:
            worksheet: Nome da aba
            address: Endereço do range (ex: 'D24:F69')
            
        Returns:
            Matriz de valores
        """
        url = f"{self._get_base_url()}/worksheets/{worksheet}/range(address='{address}')"
        
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        
        data = response.json()
        values = data.get("values", [])
        
        logger.debug(f"Lido range {worksheet}!{address}: {len(values)} linhas")
        
        return values
    
    def calculate(self, calculation_type: str = "Full"):
        """
        Executa cálculo na planilha
        
        Args:
            calculation_type: Tipo de cálculo ('Full', 'FullRebuild', 'Recalculate')
        """
        url = f"{self._get_base_url()}/application/calculate"
        payload = {"calculationType": calculation_type}
        
        response = requests.post(url, headers=self._get_headers(), json=payload)
        response.raise_for_status()
        
        logger.info(f"Cálculo executado: {calculation_type}")
    
    def get_workbook_version(self) -> Optional[str]:
        """Obtém versão/etag da planilha"""
        try:
            url = f"{config.GRAPH_API_ENDPOINT}/me/drive/items/{self.workbook_id}"
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            
            data = response.json()
            return data.get("eTag")
        except Exception as e:
            logger.warning(f"Não foi possível obter versão da planilha: {e}")
            return None
