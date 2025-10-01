"""
Modelos de dados (Pydantic)
"""
from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from typing import Optional, Dict, Any
from decimal import Decimal


class CalculadoraInput(BaseModel):
    """Modelo de entrada para cálculo trabalhista"""
    municipio: str = Field(..., description="Nome do município")
    periodo_inicio: date = Field(..., description="Data de início do período (AAAA-MM-DD)")
    periodo_fim: date = Field(..., description="Data de fim do período (AAAA-MM-DD)")
    ajuizamento: date = Field(..., description="Data de ajuizamento (AAAA-MM-DD)")
    citacao: date = Field(..., description="Data de citação (AAAA-MM-DD)")
    honorarios_perc: float = Field(0.0, ge=0.0, le=100.0, description="Honorários percentual (0 a 100)")
    honorarios_fixo: float = Field(0.0, ge=0.0, description="Honorários fixo em reais")
    desagio_principal: float = Field(0.0, ge=0.0, le=100.0, description="Deságio sobre principal (0 a 100)")
    desagio_honorarios: float = Field(0.0, ge=0.0, le=100.0, description="Deságio sobre honorários (0 a 100)")
    correcao_ate: date = Field(..., description="Data de correção até (AAAA-MM-DD)")
    
    @field_validator('periodo_fim')
    @classmethod
    def validar_periodo_fim(cls, v, info):
        if 'periodo_inicio' in info.data and v < info.data['periodo_inicio']:
            raise ValueError('Período fim deve ser maior que período início')
        return v
    
    @field_validator('correcao_ate')
    @classmethod
    def validar_correcao_ate(cls, v, info):
        if 'periodo_fim' in info.data and v < info.data['periodo_fim']:
            raise ValueError('Correção até deve ser maior ou igual ao período fim')
        return v
    
    @field_validator('periodo_inicio', 'periodo_fim', 'ajuizamento', 'citacao', 'correcao_ate')
    @classmethod
    def validar_data_futura(cls, v):
        if v > date.today():
            raise ValueError('Data não pode ser futura')
        return v


class CenarioOutput(BaseModel):
    """Resultado de um cenário de cálculo"""
    principal: float = Field(..., description="Valor principal após deságio")
    honorarios: float = Field(..., description="Valor de honorários")
    total: float = Field(..., description="Total (principal + honorários)")


class CalculadoraOutput(BaseModel):
    """Modelo de saída do cálculo"""
    run_id: str = Field(..., description="ID único da execução")
    timestamp: datetime = Field(..., description="Data/hora da execução")
    workbook_version: Optional[str] = Field(None, description="Versão/etag da planilha")
    inputs: Dict[str, Any] = Field(..., description="Echo dos inputs")
    outputs: Dict[str, CenarioOutput] = Field(..., description="Resultados dos cenários")
    selic_context: Dict[str, Any] = Field(default_factory=dict, description="Contexto da SELIC")
    execution_time_ms: int = Field(..., description="Tempo de execução em ms")


class ErrorResponse(BaseModel):
    """Resposta de erro padrão"""
    error: str = Field(..., description="Tipo do erro")
    message: str = Field(..., description="Mensagem de erro")
    details: Optional[Dict[str, Any]] = Field(None, description="Detalhes adicionais")
