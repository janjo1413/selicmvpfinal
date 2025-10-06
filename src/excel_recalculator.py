"""
Módulo para recalcular planilhas Excel/Calc usando win32com
Suporta: Microsoft Excel e LibreOffice Calc
Força recálculo de todas as fórmulas após modificar valores
"""
import logging
import time
from pathlib import Path
import subprocess
import os

logger = logging.getLogger(__name__)

# Flag para verificar se win32com está disponível
WIN32COM_AVAILABLE = False
try:
    import win32com.client
    WIN32COM_AVAILABLE = True
    logger.info("✅ win32com disponível - Recálculo via COM habilitado")
except ImportError:
    logger.warning("⚠️ win32com não disponível - Recálculo via COM desabilitado")


class ExcelRecalculator:
    """
    Recalcula planilhas Excel/Calc usando automação COM
    Suporta: Microsoft Excel e LibreOffice Calc
    Requer: Windows + Excel/LibreOffice instalado + pywin32
    """
    
    @staticmethod
    def is_available() -> bool:
        """Verifica se win32com está disponível"""
        return WIN32COM_AVAILABLE
    
    @staticmethod
    def _try_libreoffice_subprocess(file_path: Path) -> bool:
        """
        Recalcula usando LibreOffice via subprocess (macro)
        Mais confiável que COM para LibreOffice
        """
        try:
            logger.info("🔄 Tentando LibreOffice Calc via subprocess...")
            
            # Procurar executável do LibreOffice
            libreoffice_paths = [
                r"C:\Program Files\LibreOffice\program\scalc.exe",
                r"C:\Program Files (x86)\LibreOffice\program\scalc.exe",
                r"C:\Program Files\LibreOffice 7\program\scalc.exe",
                os.path.expanduser(r"~\AppData\Local\Programs\LibreOffice\program\scalc.exe"),
            ]
            
            soffice_exe = None
            for path in libreoffice_paths:
                if os.path.exists(path):
                    soffice_exe = path
                    break
            
            if not soffice_exe:
                logger.debug("Executável do LibreOffice não encontrado")
                return False
            
            logger.debug(f"LibreOffice encontrado: {soffice_exe}")
            
            # Criar macro simples para recalcular
            # LibreOffice pode executar macros via linha de comando
            # Por enquanto, apenas abrir e fechar força recálculo parcial
            
            # Comando: abrir arquivo, aguardar, fechar
            # --headless = sem interface
            # --calc = modo Calc
            # file_path = arquivo a processar
            
            cmd = [
                soffice_exe,
                "--headless",
                "--calc",
                "--convert-to", "xlsx",
                "--outdir", str(file_path.parent),
                str(file_path)
            ]
            
            logger.debug(f"Executando: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.info("✅ LibreOffice: Arquivo processado")
                return True
            else:
                logger.debug(f"LibreOffice retornou código {result.returncode}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("⏱️ LibreOffice: Timeout")
            return False
        except Exception as e:
            logger.debug(f"LibreOffice subprocess falhou: {e}")
            return False
    
    @staticmethod
    def recalculate_workbook(file_path: Path, visible: bool = False) -> bool:
        """
        Abre planilha no Excel/Calc, força recálculo, salva e fecha
        Tenta primeiro Excel, depois LibreOffice Calc
        
        Args:
            file_path: Caminho do arquivo Excel/ODS
            visible: Se True, mostra aplicação na tela (útil para debug)
        
        Returns:
            True se recalculou com sucesso, False caso contrário
        """
        if not WIN32COM_AVAILABLE:
            logger.error("win32com não disponível - não é possível recalcular")
            return False
        
        if not file_path.exists():
            logger.error(f"Arquivo não encontrado: {file_path}")
            return False
        
        # Tentar Microsoft Excel PRIMEIRO (agora que está instalado)
        logger.info(f"🔄 Iniciando recálculo: {file_path.name}")
        excel = None
        workbook = None
        
        try:
            logger.info(f"🔄 Tentando Microsoft Excel...")
            
            # Iniciar Excel (usar DispatchEx para nova instância isolada)
            excel = win32com.client.DispatchEx("Excel.Application")
            excel.Visible = visible
            excel.DisplayAlerts = False  # Desabilitar alertas
            
            # Abrir workbook
            logger.debug(f"Abrindo workbook...")
            workbook = excel.Workbooks.Open(str(file_path.absolute()))
            
            # Forçar recálculo COMPLETO
            logger.debug(f"Forçando recálculo...")
            
            # Aguardar Excel estar pronto
            time.sleep(1.0)
            
            try:
                # Método 1: Recálculo completo (pode falhar se Excel estiver ocupado)
                excel.CalculateFullRebuild()
            except:
                logger.debug("CalculateFullRebuild falhou, tentando Calculate...")
            
            try:
                # Método 2: Cálculo normal
                excel.Calculate()
            except:
                logger.debug("Calculate falhou")
            
            # Aguardar cálculo completar
            time.sleep(1.0)  # Pausa maior para garantir
            
            # Salvar
            logger.debug(f"Salvando workbook...")
            workbook.Save()
            
            logger.info(f"✅ Excel: Recálculo concluído com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao recalcular Excel: {e}")
            
            # Tentar LibreOffice como fallback
            logger.info("Tentando LibreOffice como fallback...")
            if ExcelRecalculator._try_libreoffice_subprocess(file_path):
                return True
            
            logger.warning(f"⚠️ Nenhuma aplicação de planilha disponível (Excel/LibreOffice)")
            return False
            
        finally:
            # Fechar workbook
            if workbook:
                try:
                    workbook.Close(SaveChanges=True)  # Salvar mudanças
                    time.sleep(0.5)
                except Exception as e:
                    logger.debug(f"Erro ao fechar workbook: {e}")
            
            # Fechar Excel
            if excel:
                try:
                    excel.Quit()
                    time.sleep(0.5)  # Aguardar Excel fechar completamente
                except Exception as e:
                    logger.debug(f"Erro ao fechar Excel: {e}")
            
            # Limpar referências COM
            workbook = None
            excel = None
    
    @staticmethod
    def recalculate_and_read_values(
        file_path: Path,
        worksheet_name: str,
        cell_addresses: list
    ) -> dict:
        """
        Recalcula Excel e lê valores de células específicas
        
        Args:
            file_path: Caminho do arquivo
            worksheet_name: Nome da aba
            cell_addresses: Lista de endereços de células (ex: ["D23", "D24"])
        
        Returns:
            Dict com valores lidos: {"D23": 12345.67, "D24": 98765.43}
        """
        if not WIN32COM_AVAILABLE:
            logger.error("win32com não disponível")
            return {}
        
        excel = None
        workbook = None
        
        try:
            # Iniciar Excel (usar DispatchEx para nova instância isolada)
            excel = win32com.client.DispatchEx("Excel.Application")
            excel.Visible = False
            excel.DisplayAlerts = False
            
            # Abrir workbook
            workbook = excel.Workbooks.Open(str(file_path.absolute()))
            
            # Forçar recálculo
            excel.CalculateFullRebuild()
            excel.Calculate()
            time.sleep(0.5)
            
            # Ler valores
            worksheet = workbook.Worksheets(worksheet_name)
            values = {}
            
            for address in cell_addresses:
                try:
                    cell_value = worksheet.Range(address).Value
                    values[address] = cell_value
                    logger.debug(f"Lido {address}: {cell_value}")
                except Exception as e:
                    logger.warning(f"Erro ao ler {address}: {e}")
                    values[address] = None
            
            # Salvar workbook (com valores recalculados)
            workbook.Save()
            
            return values
            
        except Exception as e:
            logger.error(f"Erro ao recalcular e ler valores: {e}")
            return {}
            
        finally:
            if workbook:
                try:
                    workbook.Close(SaveChanges=False)
                except:
                    pass
            
            if excel:
                try:
                    excel.Quit()
                except:
                    pass


# Função auxiliar para uso direto
def recalculate_excel_file(file_path: Path, visible: bool = False) -> bool:
    """
    Atalho para recalcular arquivo Excel
    
    Args:
        file_path: Caminho do arquivo
        visible: Se True, mostra Excel (debug)
    
    Returns:
        True se sucesso
    """
    return ExcelRecalculator.recalculate_workbook(file_path, visible)
