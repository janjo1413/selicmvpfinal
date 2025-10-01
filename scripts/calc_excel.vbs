' Script VBS para abrir Excel, calcular e salvar
Set objExcel = CreateObject("Excel.Application")
objExcel.Visible = False
objExcel.DisplayAlerts = False

' Abrir arquivo
strFilePath = CreateObject("Scripting.FileSystemObject").GetAbsolutePathName("data\timon_01-2025.xlsx")
Set objWorkbook = objExcel.Workbooks.Open(strFilePath)

' Forçar cálculo
objExcel.CalculateBeforeSave = True
objExcel.Calculation = -4105 ' xlCalculationAutomatic
objWorkbook.Application.Calculate

' Salvar
objWorkbook.Save

' Fechar
objWorkbook.Close True
objExcel.Quit

' Limpar objetos
Set objWorkbook = Nothing
Set objExcel = Nothing

WScript.Echo "Planilha calculada e salva com sucesso!"
