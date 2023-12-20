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



class Conta:
    def __init__(self, nome, banco, saldo, db_path, data_inicial=datetime.today()):
        self.nome = nome
        self.banco = banco
        self.saldo = saldo
        self.db_path = db_path
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
    def __init__(self, nome, banco, saldo, limite, data_fech, data_venc,db_path):
        '''Utilize as datas de fechamento e de vencimento da fatura no seguinte formato:
           dd/mm/aaaa'''
        super().__init__(nome, banco, saldo,db_path)
        self.limite = limite
        self.data_fech = datetime.strptime(data_fech,"%d/%m/%Y")
        self.data_venc = datetime.strptime(data_venc,"%d/%m/%Y")
        self.fatura_atual = pd.DataFrame(columns=['Data','Descrição','Valor'])
        self.arquivo_excel = db_path


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
            if i==0: data_fatura = data_compra
            elif i>0: data_fatura = data_parcela
            self.fatura_atual = self.fatura_atual._append({'Data':data_fatura,
                                                          'Descrição':f'{descr} {i+1}/{parcela}',
                                                          'Valor': valor_parcela,
                                                          'Valor Total Fatura': 0},
                                                          ignore_index = True)
            
        # Recalcula o valor total da fatura
        self.fatura_atual['Data'] = pd.to_datetime(self.fatura_atual['Data'], format='%d/%m/%Y')
        data_ref=[]
        for x in self.fatura_atual['Data']:
            if x.day<18 and x.month==1:
                data_ref.append(x+pd.offsets.MonthBegin(0)+pd.DateOffset(days=self.data_fech.day - 1))
            elif x.day<18:
                data_ref.append(x+pd.offsets.MonthBegin(-1)+pd.DateOffset(days=self.data_fech.day - 1))
            elif x.day>=18:
                data_ref.append(x+pd.offsets.MonthBegin(0)+pd.DateOffset(days=self.data_fech.day - 1))
        self.fatura_atual['Data_Ref']=data_ref
    
        self.fatura_atual = self.fatura_atual.sort_values(by="Data")
        self.fatura_atual['Valor'] = pd.to_numeric(self.fatura_atual['Valor'], errors='coerce')
        self.fatura_atual['Valor Total Fatura']=self.fatura_atual.groupby([self.fatura_atual['Data_Ref'].dt.year, self.fatura_atual['Data_Ref'].dt.month])['Valor'].cumsum()

            
    
    def fechar_fatura(self):
        # Exibe a fatura atual

        # Salva a fatura em um arquivo Excel
        self.fatura_atual.to_csv(self.db_path,';',index=False)
        
    def exibir_fatura(self): 
        caminho = self.db_path
        db_fatura = pd.read_csv(caminho,header = 0)

    #TODO Cálculo de juros em caso de não pagamento da fatura na data devida************ (cada banco faz de um jeito, fica complicado)

class ContaCorrente(Conta):
    def __init__(self, nome, banco, saldo, db_path, taxa=0):
        super().__init__(nome, banco, saldo, db_path)
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
# path = r"C:\Users\rafae\OneDrive\Faculdade\10º Período\Projeto Computacional\bancodedados.xlsx"
path = r"C:\Users\rafae\OneDrive\Faculdade\10º Período\Projeto Computacional\bancodedados.csv"
# nu_deb = ContaCorrente("Tainá","NuBank",1100,0)
# nu_deb.debito("Uber Demar",15)
# nu_deb.recebimento("Pix",100)
# nu_deb.Extrato()

nu_cred = Credito("Rafael","NuBank",100,3000,"18/12/2023","26/12/2023",db_path=path)
nu_cred.gasto("27/12/2023","Uber",12.50)
nu_cred.gasto("28/12/2023","SSD",250,3)
nu_cred.gasto("30/12/2023","Passagem Lorena - SP",90,4)
nu_cred.gasto("31/12/2023","Chá",50)
nu_cred.gasto("20/02/2023","Guitar Hero 3",300)
print(nu_cred.fatura_atual)
nu_cred.fechar_fatura()
