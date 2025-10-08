"""
BATERIA COMPLETA DE TESTES AUTOMATIZADOS
Testa 10 municipios variados com diferentes combinacoes de inputs
"""
import win32com.client
import os
import time
import requests
import shutil
from datetime import datetime
import json

# Lista de 10 municipios para teste (variados)
MUNICIPIOS_TESTE = [
    "TIMON",
    "FORTALEZA", 
    "SAO LUIS",
    "TERESINA",
    "CAMPO MAIOR",
    "PARNAIBA",
    "PICOS",
    "FLORIANO",
    "CAXIAS",
    "BACABAL"
]

# Configuracoes de teste (3 cenarios diferentes)
CENARIOS_INPUT = [
    {
        "nome": "Sem_Honorarios",
        "honorarios_perc": 0.0,
        "honorarios_fixo": 0.0,
        "desagio_principal": 20.0,
        "desagio_honorarios": 20.0
    },
    {
        "nome": "Com_Honorarios_30pct",
        "honorarios_perc": 30.0,
        "honorarios_fixo": 55550.0,
        "desagio_principal": 20.0,
        "desagio_honorarios": 20.0
    },
    {
        "nome": "Sem_Desagio",
        "honorarios_perc": 10.0,
        "honorarios_fixo": 10000.0,
        "desagio_principal": 0.0,
        "desagio_honorarios": 0.0
    }
]

# Datas padrao para todos os testes
DATAS_PADRAO = {
    "periodo_inicio": "2000-01-01",
    "periodo_fim": "2006-12-01",
    "ajuizamento": "2005-05-01",
    "citacao": "2006-06-01",
    "correcao_ate": "2025-01-01"
}

# Cenarios de output a testar
CENARIOS_OUTPUT = [
    "nt7_ipca_selic",
    "nt7_periodo_cnj",
    "nt6_ipca_selic",
    "jasa_ipca_selic",
    "nt7_tr",
    "nt36_tr",
    "nt7_ipca_e",
    "nt36_ipca_e",
    "nt36_ipca_e_1pct"
]

# Mapeamento de linhas de output
LINHAS_OUTPUT = {
    "nt7_ipca_selic": 24,
    "nt7_periodo_cnj": 29,
    "nt6_ipca_selic": 34,
    "jasa_ipca_selic": 39,
    "nt7_tr": 44,
    "nt36_tr": 49,
    "nt7_ipca_e": 54,
    "nt36_ipca_e": 64,
    "nt36_ipca_e_1pct": 69,
}

class TesteBateria:
    def __init__(self):
        self.resultados = []
        self.falhas = []
        self.url_site = "http://localhost:8000/api/calcular"
        self.temp_path = r"C:\Users\jgque\AppData\Local\Temp\teste_bateria.xlsx"
        self.total_testes = 0
        self.testes_ok = 0
        self.testes_falha = 0
        
    def log(self, mensagem):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {mensagem}")
    
    def calcular_planilha(self, municipio, params):
        """Recalcula planilha e retorna valores"""
        try:
            os.remove(self.temp_path)
        except:
            pass
        
        shutil.copy('data/timon_01-2025.xlsx', self.temp_path)
        
        excel = win32com.client.DispatchEx("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False
        
        wb = excel.Workbooks.Open(os.path.abspath(self.temp_path))
        ws = wb.Worksheets("RESUMO")
        
        # Escrever inputs
        ws.Range("B6").Value = municipio
        ws.Range("E6").Value = params["periodo_inicio"]
        ws.Range("F6").Value = params["periodo_fim"]
        ws.Range("B7").Value = params["ajuizamento"]
        ws.Range("B8").Value = params["citacao"]
        ws.Range("B11").Value = params["honorarios_perc"] / 100.0
        ws.Range("B12").Value = params["honorarios_fixo"]
        ws.Range("B13").Value = params["desagio_principal"] / 100.0
        ws.Range("B14").Value = params["desagio_honorarios"] / 100.0
        ws.Range("B15").Value = params["correcao_ate"]
        
        # Recalcular
        excel.CalculateFullRebuild()
        excel.Calculate()
        wb.Save()
        
        # Ler outputs
        valores = {}
        for cenario, linha in LINHAS_OUTPUT.items():
            d = ws.Range(f"D{linha}").Value
            e = ws.Range(f"E{linha}").Value
            f = ws.Range(f"F{linha}").Value
            
            # Tratar None como 0
            d = float(d) if d is not None else 0.0
            e = float(e) if e is not None else 0.0
            f = float(f) if f is not None else 0.0
            
            valores[cenario] = {
                'principal': d,
                'honorarios': e + f,
                'total': d + e + f
            }
        
        wb.Close(SaveChanges=False)
        excel.Quit()
        time.sleep(0.5)
        
        try:
            os.remove(self.temp_path)
        except:
            pass
        
        return valores
    
    def calcular_site(self, municipio, params):
        """Chama API do site"""
        payload = {
            "municipio": municipio,
            **params
        }
        
        try:
            response = requests.post(self.url_site, json=payload, timeout=600)
            if response.status_code == 200:
                return response.json()
            else:
                self.log(f"ERRO: Site retornou status {response.status_code}")
                return None
        except Exception as e:
            self.log(f"ERRO ao chamar site: {str(e)}")
            return None
    
    def comparar_valores(self, planilha, site, cenario):
        """Compara valores com tolerancia de 1 centavo"""
        if cenario not in site.get('outputs', {}):
            return False, "Cenario nao encontrado no site"
        
        site_data = site['outputs'][cenario]
        
        p_planilha = planilha['principal']
        h_planilha = planilha['honorarios']
        t_planilha = planilha['total']
        
        p_site = float(site_data['principal'])
        h_site = float(site_data['honorarios'])
        t_site = float(site_data['total'])
        
        diff_p = abs(p_planilha - p_site)
        diff_h = abs(h_planilha - h_site)
        diff_t = abs(t_planilha - t_site)
        
        if diff_p < 0.01 and diff_h < 0.01 and diff_t < 0.01:
            return True, "OK"
        else:
            msg = f"Principal: diff R$ {diff_p:.2f}, Honorarios: diff R$ {diff_h:.2f}, Total: diff R$ {diff_t:.2f}"
            return False, msg
    
    def executar_teste(self, municipio, cenario_input):
        """Executa um teste completo para um municipio e cenario"""
        self.total_testes += 1
        nome_cenario = cenario_input['nome']
        
        self.log(f"")
        self.log(f"{'='*100}")
        self.log(f"TESTE #{self.total_testes}: {municipio} - {nome_cenario}")
        self.log(f"{'='*100}")
        
        # Montar parametros
        params = {**DATAS_PADRAO, **cenario_input}
        params.pop('nome')  # Remover campo 'nome' que nao e input
        
        # 1. Calcular na planilha
        self.log(f"[1/3] Recalculando planilha...")
        valores_planilha = self.calcular_planilha(municipio, params)
        self.log(f"OK - Planilha recalculada")
        
        # 2. Calcular no site
        self.log(f"[2/3] Chamando API do site (pode demorar 5+ min)...")
        resultado_site = self.calcular_site(municipio, params)
        
        if not resultado_site:
            self.log(f"FALHA - Site nao retornou resultado")
            self.falhas.append({
                'teste': f"{municipio}_{nome_cenario}",
                'erro': 'Site nao retornou resultado',
                'params': params
            })
            self.testes_falha += 1
            return False
        
        self.log(f"OK - Site retornou resultado")
        
        # 3. Comparar todos os cenarios
        self.log(f"[3/3] Comparando 9 cenarios de output...")
        
        cenarios_ok = 0
        cenarios_falha = 0
        
        for cenario_output in CENARIOS_OUTPUT:
            ok, msg = self.comparar_valores(
                valores_planilha[cenario_output],
                resultado_site,
                cenario_output
            )
            
            if ok:
                cenarios_ok += 1
                self.log(f"  OK - {cenario_output}")
            else:
                cenarios_falha += 1
                self.log(f"  FALHA - {cenario_output}: {msg}")
                self.falhas.append({
                    'teste': f"{municipio}_{nome_cenario}_{cenario_output}",
                    'erro': msg,
                    'planilha': valores_planilha[cenario_output],
                    'site': resultado_site['outputs'].get(cenario_output, {}),
                    'params': params
                })
        
        if cenarios_falha == 0:
            self.log(f"")
            self.log(f"SUCESSO - Todos os 9 cenarios OK")
            self.testes_ok += 1
            return True
        else:
            self.log(f"")
            self.log(f"FALHA - {cenarios_falha} cenarios divergentes")
            self.testes_falha += 1
            return False
    
    def gerar_relatorio(self):
        """Gera relatorio final"""
        print("\n" + "="*100)
        print("RELATORIO FINAL DA BATERIA DE TESTES")
        print("="*100)
        print(f"\nTotal de testes executados: {self.total_testes}")
        print(f"Testes OK: {self.testes_ok} ({self.testes_ok/self.total_testes*100:.1f}%)")
        print(f"Testes com falha: {self.testes_falha} ({self.testes_falha/self.total_testes*100:.1f}%)")
        
        if self.falhas:
            print(f"\n{'='*100}")
            print(f"DETALHAMENTO DAS FALHAS ({len(self.falhas)} divergencias)")
            print("="*100)
            for i, falha in enumerate(self.falhas[:10], 1):  # Mostrar ate 10 primeiras
                print(f"\n[{i}] {falha['teste']}")
                print(f"    Erro: {falha['erro']}")
            
            if len(self.falhas) > 10:
                print(f"\n... e mais {len(self.falhas) - 10} falhas")
        else:
            print(f"\n{'='*100}")
            print("PARABENS! TODOS OS TESTES PASSARAM!")
            print("="*100)
        
        # Salvar relatorio em JSON
        with open('relatorio_testes.json', 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_testes': self.total_testes,
                'testes_ok': self.testes_ok,
                'testes_falha': self.testes_falha,
                'falhas': self.falhas
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\nRelatorio completo salvo em: relatorio_testes.json")

def main():
    print("="*100)
    print("BATERIA DE TESTES AUTOMATIZADOS")
    print("="*100)
    print(f"\nConfiguracao:")
    print(f"  - Municipios: {len(MUNICIPIOS_TESTE)}")
    print(f"  - Cenarios de input: {len(CENARIOS_INPUT)}")
    print(f"  - Total de testes: {len(MUNICIPIOS_TESTE) * len(CENARIOS_INPUT)}")
    print(f"  - Tempo estimado: ~{len(MUNICIPIOS_TESTE) * len(CENARIOS_INPUT) * 5} minutos")
    
    input("\nPressione ENTER para iniciar os testes...")
    
    bateria = TesteBateria()
    
    # Executar testes
    for municipio in MUNICIPIOS_TESTE:
        for cenario in CENARIOS_INPUT:
            sucesso = bateria.executar_teste(municipio, cenario)
            
            # Se falhou, parar (conforme especificacao)
            if not sucesso:
                print("\n" + "="*100)
                print("TESTES INTERROMPIDOS - FALHA DETECTADA")
                print("="*100)
                bateria.gerar_relatorio()
                return
            
            # Aguardar um pouco entre testes para nao sobrecarregar
            time.sleep(2)
    
    # Gerar relatorio final
    bateria.gerar_relatorio()

if __name__ == "__main__":
    main()
