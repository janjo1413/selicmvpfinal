' Script VBS para calcular Excel e retornar valores
' Uso: cscript //nologo excel_calc.vbs <caminho_excel> <worksheet> <range>

Dim args, excelPath, worksheetName, rangeAddress
Set args = WScript.Arguments

If args.Count < 3 Then
    WScript.Echo "ERRO: Argumentos insuficientes"
    WScript.Quit 1
End If

excelPath = args(0)
worksheetName = args(1)
rangeAddress = args(2)

' Criar objeto Excel
On Error Resume Next
Dim objExcel, objWorkbook, objWorksheet
Set objExcel = CreateObject("Excel.Application")

If Err.Number <> 0 Then
    WScript.Echo "ERRO: Nao foi possivel criar objeto Excel"
    WScript.Quit 1
End If

objExcel.Visible = False
objExcel.DisplayAlerts = False
objExcel.ScreenUpdating = False

' Abrir planilha
Set objWorkbook = objExcel.Workbooks.Open(excelPath)

If Err.Number <> 0 Then
    WScript.Echo "ERRO: Nao foi possivel abrir planilha"
    objExcel.Quit
    WScript.Quit 1
End If

' Selecionar worksheet
Set objWorksheet = objWorkbook.Worksheets(worksheetName)

If Err.Number <> 0 Then
    WScript.Echo "ERRO: Worksheet nao encontrado"
    objWorkbook.Close False
    objExcel.Quit
    WScript.Quit 1
End If

' Forçar cálculo
objExcel.CalculateFull

' Ler valores do range
Dim cellValues, i, j
cellValues = objWorksheet.Range(rangeAddress).Value

' Output formato CSV
If IsArray(cellValues) Then
    For i = LBound(cellValues, 1) To UBound(cellValues, 1)
        For j = LBound(cellValues, 2) To UBound(cellValues, 2)
            WScript.Echo cellValues(i, j)
        Next
    Next
Else
    WScript.Echo cellValues
End If

' Fechar SEM salvar
objWorkbook.Close False
objExcel.Quit

WScript.Quit 0
