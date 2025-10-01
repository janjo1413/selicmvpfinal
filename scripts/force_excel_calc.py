"""
Script para forçar cálculo das fórmulas no Excel
Execute uma vez para preparar a planilha
"""
import sys
from pathlib import Path

EXCEL_PATH = Path("data/timon_01-2025.xlsx").absolute()

print("\n" + "=" * 60)
print("  🔧 Forçando Cálculo do Excel")
print("=" * 60)

print(f"\nArquivo: {EXCEL_PATH}")

if not EXCEL_PATH.exists():
    print(f"\n❌ Erro: Arquivo não encontrado!")
    sys.exit(1)

# Tentar usar pywin32 (COM)
try:
    import win32com.client
    
    print("\n✅ Usando COM Automation (pywin32)")
    print("\n1. Abrindo Excel...")
    
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False  # Rodar em background
    excel.DisplayAlerts = False
    
    print("2. Abrindo planilha...")
    workbook = excel.Workbooks.Open(str(EXCEL_PATH))
    
    print("3. Forçando recálculo...")
    excel.Calculate()
    workbook.RefreshAll()
    
    print("4. Salvando...")
    workbook.Save()
    
    print("5. Fechando...")
    workbook.Close(SaveChanges=True)
    excel.Quit()
    
    print("\n✅ Sucesso! Planilha calculada e salva.")
    print("\nAgora você pode usar a aplicação normalmente.")
    
except ImportError:
    print("\n⚠️  pywin32 não instalado.")
    print("\n📋 SOLUÇÃO MANUAL:")
    print("\n1. Abra o arquivo:")
    print(f"   {EXCEL_PATH}")
    print("\n2. Aguarde o Excel calcular as fórmulas")
    print("\n3. Pressione Ctrl+S para salvar")
    print("\n4. Feche o Excel")
    print("\n5. Execute a aplicação novamente")
    print("\n" + "-" * 60)
    print("\nOu instale pywin32 e execute este script novamente:")
    print("   pip install pywin32")
    print("   python scripts/force_excel_calc.py")
    
except Exception as e:
    print(f"\n❌ Erro: {e}")
    print("\nTente a solução manual (veja acima)")
    sys.exit(1)

print("\n" + "=" * 60 + "\n")
