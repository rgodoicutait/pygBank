import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from openpyxl import load_workbook, Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
from datetime import datetime
from datetime import timedelta

# classe mãe: banco?
## classe filha: crédito, débito, poupança?
### usar o pandas para salvar tudo em algum lugar?
#### Como formatar uma string como data?
##### Como chamar a subclasse para utilizar tanto as funções da classe mãe quanto a da filha?
#TODO Algum método de armazenar/acessar o histórico da pessoa (acessar o arquivo em que as movimentações foram salvas, ex: Excel, csv, etc...)
#TODO Alguma interface de texto?

db_path = r'C:\Users\sivei\OneDrive\Documentos\Projeto-Computacional\bancodedados.xlsx'

class Conta:
    def __init__(self, nome, banco, saldo, data_inicial=datetime.today()):
        self.nome = nome
        self.banco = banco
        self.saldo = saldo
        if data_inicial is str:
            self.data_inicial = datetime.strptime(data_inicial,"%d/%m/$Y")
        else:
            self.data_inicial = data_inicial
        self.extrato = {"Data":[data_inicial],"Descrição":["Saldo Inicial"],"Valor":[saldo],"Saldo":[saldo]}

    def resumo(self):
        print(f'Nome: {self.nome}')
        print(f'Banco: {self.banco}')
        print(f'Saldo: R${self.saldo:.2f}')

class Credito(Conta):
    def __init__(self, nome, banco, saldo, limite, data_fech, data_venc):
        '''Utilize as datas de fechamento e de vencimento da fatura no seguinte formato:
           dd/mm/aaaa'''
        super().__init__(nome, banco, saldo)
        self.limite = limite
        self.data_fech = datetime.strptime(data_fech,"%d/%m/%Y")
        self.data_venc = datetime.strptime(data_venc,"%d/%m/%Y")
        self.fatura_atual = pd.DataFrame(columns=['Data','Descrição','Valor','Valor Total Fatura'])
        self.arquivo_excel = db_path
        self.valor_total_fatura = 0


    def resumo(self):
        super().resumo()
        print(f'Limite: R${self.limite:.2f}')
        print(f'Data de Fechamento da Fatura: {self.data_fech}')
        print(f'Data de Vencimento da Fatura: {self.data_venc}')

    def gasto(self, data, descr, valor, parcela = 1):
        # Verifica se a fatura foi fechada
        if self.data_fech is not None and datetime.now() > self.data_fech:
            print("Fatura Fechada. Fechando automaticamente...")
            self.fechar_fatura()

        # Calcula o valor da parcela  
        valor_parcela = valor / parcela

        # Adiciona as parcelas à fatura
        for i in range(parcela):
            data_compra = datetime.strptime(data,"%d/%m/%Y")
            data_parcela = self.data_fech + timedelta(days=30 * (i+1)) # Encontra as datas das próximas parcelas da compra

            self.valor_total_fatura+=valor_parcela
            if i==0: data_fatura = data_compra
            elif i>0: data_fatura = data_parcela
            self.fatura_atual = self.fatura_atual._append({'Data':data_fatura,
                                                          'Descrição':f'{descr} {i+1}/{parcela}',
                                                          'Valor': valor_parcela, 
                                                          'Valor Total Fatura': 0},
                                                          ignore_index = True)
            
            # Ordena o DataFrame pela coluna data
            self.fatura_atual = self.fatura_atual.sort_values('Data').reset_index(drop=True)

            # Recalcula o valor total da fatura
            self.fatura_atual['Valor Total Fatura'] = self.calcular_cumsum_intervalo()

    def calcular_cumsum_intervalo(self):
        return self.fatura_atual['Valor'].cumsum()

    def proxima_data_fechamento(self):
        if self.data_fech.month == 12:
            return self.data_fech.replace(year=self.data_fech.year +1, month=1) 
        else:
            return self.data_fech.replace(month=self.data_fech.month + 1)
            
    
    def fechar_fatura(self):
        # Exibe a fatura atual
        print("\nFatura Atual:")
        
        print(self.fatura_atual)

        # Salva a fatura em um arquivo Excel
        # with pd.ExcelWriter(db_path, engine='openpyxl', mode='a') as writer:
        #     self.fatura_atual.to_excel(writer, sheet_name="Faturas", index=False)


        # Limpa a fatura atual
        self.fatura_atual = pd.DataFrame(columns=['Data','Descrição','Valor','Valor Total Fatura'])
        
        # Atualiza a data de vencimento para o próximo mês
        self.data_venc += timedelta(days=30)

    '''
        - Está "funcioinando", aparece que o arquivo esta corrompido mas aparece a primeira fatura 

        - o cabeçalho nao é o da coluna  
    '''
    def exibir_fatura(self): 
        # Carregar o arquivo Excel existente ou criar um novo
        try:
            wb = load_workbook(self.arquivo_excel)
        except FileNotFoundError:
            wb = Workbook()

        # Verificar se a planilha 'Faturas' já existe
        if 'Faturas' not in wb.sheetnames:
            ws = wb.create_sheet('Faturas')
        else:
            ws = wb['Faturas']

        # Criar um DataFrame com os dados da fatura atual
        df = self.fatura_atual

        # Verificar se a tabela já existe na planilha
        table_exists = False
        for table in ws.tables.values():
            if table.name == 'FaturaTable':
                table_exists = True
                break

        # Se a tabela ainda não existe, adicionar os dados como uma nova tabela
        if not table_exists:
            ws.append([])
            for r in dataframe_to_rows(df, index=False, header=True):
                ws.append(r)

            # Criar a tabela com o DataFrame
            tab = Table(displayName="FaturaTable", ref=f"A1:{get_column_letter(df.shape[1])}{df.shape[0] + 1}")
            style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                                   showLastColumn=False, showRowStripes=True, showColumnStripes=True)
            tab.tableStyleInfo = style
            ws.add_table(tab)

        # Salvar o arquivo Excel
        wb.save(self.arquivo_excel)


    
    #TODO Função que faz o parcelamento de compras e já adiciona as parcelas para os próximos meses.
    #TODO Cálculo de juros em caso de não pagamento da fatura na data devida************ (cada banco faz de um jeito, fica complicado)



class ContaCorrente(Conta):
    def __init__(self, nome, banco, saldo, taxa=0):
        super().__init__(nome, banco, saldo)
        self.taxa = taxa

    def debito(self, descr, valor, data=datetime.today()):
        self.extrato["Data"].append(data)
        self.extrato["Descrição"].append(descr)
        self.extrato["Valor"].append(-valor)
        if self.saldo - valor <0:
            print("transação inválida") #TODO transformar em mensagem de erro e permitir redigitação
        else:
            self.saldo=self.saldo - valor
            self.extrato["Saldo"].append(self.saldo)
    
    def recebimento(self, descr, valor, data=datetime.today()):
        self.extrato["Data"].append(data)
        self.extrato["Descrição"].append(descr)
        self.extrato["Valor"].append(valor)
        self.saldo = self.saldo + valor
        self.extrato["Saldo"].append(self.saldo)

    def Extrato(self): #TODO delimitar datas para printar o extrato
        print(pd.DataFrame(self.extrato))


    def resumo(self):
        super().resumo()
        print(f'Taxa: {self.taxa}%')


class ContaPoupanca(Conta):
    def __init__(self, nome, saldo, rendimento):
        super().__init__(nome, saldo)
        self.rendimento = rendimento

    def resumo(self):
        super().resumo()
        print(f'Rendimento: {self.rendimento}%')

##########

nu_deb = ContaCorrente("Tainá","NuBank",1100,0)
nu_deb.debito("Uber Demar",15)
nu_deb.recebimento("Pix",100)
nu_deb.Extrato()

nu_cred = Credito("Rafael","NuBank",100,3000,"18/12/2023","26/12/2023")
nu_cred.gasto("27/12/2023","Uber",12.50)
nu_cred.gasto("28/12/2023","SSD",250,3)
#nu_cred.gasto("30/12/2023","Passagem Lorena - SP",90,4)
#nu_cred.gasto("31/12/2023","Chá",50)

nu_cred.exibir_fatura()
nu_cred.fechar_fatura()
