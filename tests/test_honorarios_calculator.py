"""
Testes para cálculo de honorários
"""
import pytest
from src.honorarios_calculator import HonorariosCalculator


class TestHonorariosCalculator:
    """Testes do calculador de honorários"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.calc = HonorariosCalculator()
    
    def test_honorarios_percentual_sem_desagio(self):
        """Testa honorários percentuais sem deságio"""
        resultado = self.calc.calcular(
            principal=100000.00,
            honorarios_perc=20.0,
            honorarios_fixo=0.0,
            desagio_honorarios=0.0
        )
        
        assert resultado['honorarios'] == 20000.00
        assert resultado['total'] == 120000.00
    
    def test_honorarios_percentual_com_desagio(self):
        """Testa honorários percentuais com deságio"""
        resultado = self.calc.calcular(
            principal=100000.00,
            honorarios_perc=20.0,
            honorarios_fixo=0.0,
            desagio_honorarios=10.0  # 10% de desconto
        )
        
        assert resultado['honorarios'] == 18000.00  # 20000 * 0.9
        assert resultado['total'] == 118000.00
    
    def test_honorarios_fixo_sem_desagio(self):
        """Testa honorários fixos sem deságio"""
        resultado = self.calc.calcular(
            principal=100000.00,
            honorarios_perc=0.0,
            honorarios_fixo=5000.00,
            desagio_honorarios=0.0
        )
        
        assert resultado['honorarios'] == 5000.00
        assert resultado['total'] == 105000.00
    
    def test_honorarios_fixo_com_desagio(self):
        """Testa honorários fixos com deságio"""
        resultado = self.calc.calcular(
            principal=100000.00,
            honorarios_perc=0.0,
            honorarios_fixo=5000.00,
            desagio_honorarios=20.0
        )
        
        assert resultado['honorarios'] == 4000.00  # 5000 * 0.8
        assert resultado['total'] == 104000.00
    
    def test_sem_honorarios(self):
        """Testa sem honorários"""
        resultado = self.calc.calcular(
            principal=100000.00,
            honorarios_perc=0.0,
            honorarios_fixo=0.0,
            desagio_honorarios=0.0
        )
        
        assert resultado['honorarios'] == 0.0
        assert resultado['total'] == 100000.00
    
    def test_prioridade_percentual_sobre_fixo(self):
        """Testa que percentual tem prioridade sobre fixo"""
        resultado = self.calc.calcular(
            principal=100000.00,
            honorarios_perc=15.0,  # Tem percentual
            honorarios_fixo=5000.00,  # Fixo é ignorado
            desagio_honorarios=0.0
        )
        
        assert resultado['honorarios'] == 15000.00  # Usa percentual
        assert resultado['total'] == 115000.00
    
    def test_valores_reais_timon(self):
        """Testa com valores reais do caso Timon"""
        # Baseado no cenário NT7 IPCA que retorna ~158M
        resultado = self.calc.calcular(
            principal=158000000.00,  # ~158 milhões
            honorarios_perc=20.0,
            honorarios_fixo=0.0,
            desagio_honorarios=0.0
        )
        
        assert resultado['honorarios'] == 31600000.00  # 20% de 158M
        assert resultado['total'] == 189600000.00
    
    def test_arredondamento_correto(self):
        """Testa arredondamento de casas decimais"""
        resultado = self.calc.calcular(
            principal=123456.789,
            honorarios_perc=12.34,
            honorarios_fixo=0.0,
            desagio_honorarios=0.0
        )
        
        # 123456.789 * 0.1234 = 15234.567626
        assert resultado['honorarios'] == 15234.57
        assert resultado['total'] == 138691.36
    
    def test_principal_zero(self):
        """Testa com principal zero"""
        resultado = self.calc.calcular(
            principal=0.0,
            honorarios_perc=20.0,
            honorarios_fixo=1000.0,
            desagio_honorarios=0.0
        )
        
        # Com principal zero, honorários percentual também é zero
        assert resultado['honorarios'] == 0.0
        assert resultado['total'] == 0.0
    
    def test_percentuais_extremos(self):
        """Testa com percentuais no limite (100%)"""
        resultado = self.calc.calcular(
            principal=50000.00,
            honorarios_perc=100.0,  # 100%
            honorarios_fixo=0.0,
            desagio_honorarios=50.0  # 50% de desconto
        )
        
        # 50000 * 100% = 50000, com 50% desconto = 25000
        assert resultado['honorarios'] == 25000.00
        assert resultado['total'] == 75000.00
