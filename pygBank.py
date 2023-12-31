import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from openpyxl import load_workbook, Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
from datetime import datetime, timedelta, date
import os

'''
Banking System - Documentation

This program implements a simple banking system with credit, checking, and savings accounts.

Modules and Libraries Used:
- numpy
- matplotlib.pyplot
- pandas
- openpyxl
- datetime
- os

Example Usage:
- Create instances of the Credit, Checking, and Savings account classes.
- Perform operations such as expenses, receipts, export, and query of invoices/extractions.
'''

class Conta:
    '''
    - Attributes:
        - name (str): User's name.
        - bank (str): Bank name.
        - folder_path (str): Program folder path.

    - Methods:
        - __init__(self, name, bank): Initializes an instance of the Account class.
        - summary(self): Displays an account summary.

    '''
    def __init__(self, nome, banco):
        self.nome = nome
        self.banco = banco
    # Adquirindo o caminho da pasta em que o programa está armazenado
        diretorio_atual = os.getcwd()
        nome_arquivo = os.path.basename(diretorio_atual)
        self.caminho_pasta = diretorio_atual.replace(nome_arquivo,'')

    def resumo(self):
        print(f'Nome: {self.nome}')
        print(f'Banco: {self.banco}')
        print(f'Saldo: R${self.saldo:.2f}')

class Credito(Conta):
    '''
    - Attributes:
        - limit (float): Credit limit.
        - closing_date (datetime): Invoice closing date.
        - due_date (datetime): Invoice due date.
        - current_invoice (DataFrame): DataFrame to store invoice transactions.
        - cred_file (str): Path of the CSV file to export/import the invoice.

    - Methods:
        - __init__(self, name, bank, limit, closing_date, due_date): Initializes an instance of the Credit class.
        - summary(self): Displays a summary of the credit account.
        - expense(self, date, descr, value, installment=1): Records an expense in the credit account.
        - export_invoice(self, path=None): Exports the invoice to a CSV file.
        - query_invoice(self, path=None): Queries the invoice from a CSV file.
    '''
    def __init__(self, nome, banco, limite, data_fech, data_venc):
        '''Utilize as datas de fechamento e de vencimento da fatura no seguinte formato:
           dd/mm/aaaa'''
        super().__init__(nome, banco)
        self.limite = limite
        self.data_fech = datetime.strptime(data_fech,"%d/%m/%Y")
        self.data_venc = datetime.strptime(data_venc,"%d/%m/%Y")
        self.fatura_atual = pd.DataFrame(columns=['Data','Descrição','Valor'])
        self.arq_cred = self.caminho_pasta + self.nome + '_' + banco + '_' + 'Credito.csv'

    def resumo(self):
        super().resumo()
        print(f'Limite: R${self.limite:.2f}')
        print(f'Data de Fechamento da Fatura: {self.data_fech}')
        print(f'Data de Vencimento da Fatura: {self.data_venc}')

    def gasto(self, data, descr, valor, parcela = 1):
        # Calcula o valor da parcela  
        valor_parcela = valor / parcela
        # Adiciona as parcelas à fatura
        for i in range(parcela):
            data_compra = datetime.strptime(data,"%d/%m/%Y")
            if i==0: data_fatura = data_compra
            elif i>0: data_fatura = self.data_fech + timedelta(days=30 * (i+1)) # Encontra as datas das próximas parcelas da compra
            
            self.fatura_atual = self.fatura_atual._append({'Data':data_fatura,
                                                          'Descrição':f'{descr} {i+1}/{parcela}',
                                                          'Valor': valor_parcela,
                                                          'Valor Total Fatura': 0},
                                                          ignore_index = True)
            
        # Recalcula o valor total da fatura

        data_ref=[]
        dia_data_fech = self.data_fech.day
        for x in self.fatura_atual['Data']:
            if x.day<dia_data_fech and x.month==1:
                data_ref.append(x+pd.offsets.MonthBegin(0)+pd.DateOffset(days=self.data_fech.day - 1))
            elif x.day<dia_data_fech:
                data_ref.append(x+pd.offsets.MonthBegin(-1)+pd.DateOffset(days=self.data_fech.day - 1))
            elif x.day>=dia_data_fech:
                data_ref.append(x+pd.offsets.MonthBegin(0)+pd.DateOffset(days=self.data_fech.day - 1))
        self.fatura_atual['Data_Ref']=data_ref
        self.fatura_atual = self.fatura_atual.sort_values(by="Data",ignore_index=True)
        self.fatura_atual['Valor'] = pd.to_numeric(self.fatura_atual['Valor'], errors='coerce')
        self.fatura_atual['Valor Total Fatura']=self.fatura_atual.groupby([self.fatura_atual['Data_Ref'].dt.year, self.fatura_atual['Data_Ref'].dt.month])['Valor'].cumsum()
    
    def exportar_fatura(self,path=None):
        if path != None:
            self.arq_cred=path
        self.fatura_atual['Data'] =self.fatura_atual['Data'].apply(lambda x: x.strftime('%d/%m/%Y'))
        self.fatura_atual['Data_Ref'] =self.fatura_atual['Data_Ref'].apply(lambda x: x.strftime('%d/%m/%Y'))
        self.fatura_atual.to_csv(self.arq_cred,';',index=False,encoding='utf-8')

        print('fatura exportada para: ' + self.arq_cred)

    def consultar_fatura(self,path=None):
        if path != None:
            self.arq_cred=path
        self.fatura_atual=pd.read_csv(self.arq_cred,sep=';',header=0,index_col=False)
        self.fatura_atual['Data'] = pd.to_datetime(self.fatura_atual['Data'], format='%d/%m/%Y')
        
class ContaCorrente(Conta):
    '''
    - Attributes:
        - statement (DataFrame): DataFrame to store checking account transactions.
        - checking_file (str): Path of the CSV file to export/import the statement.

    - Methods:
        - __init__(self, name, bank): Initializes an instance of the Checking class.
        - receipt(self, date, desc, value): Records a receipt in the checking account.
        - expense(self, date, desc, value): Records an expense in the checking account.
        - export_statement(self, path=None): Exports the statement to a CSV file.
        - query_statement(self, path=None): Queries the statement from a CSV file.

    '''
    def __init__(self,nome,banco):
        super().__init__(nome, banco)
        self.extrato=pd.DataFrame(columns=['Data','Descrição','Valor'])
        self.arq_cc = self.caminho_pasta + self.nome + '_' + banco + '_' + 'CC.csv'
    
    def recebimento(self,data,desc,valor):
        self.extrato = self.extrato._append({'Data':datetime.strptime(data,'%d/%m/%Y'),
                                             'Descrição':desc,
                                             'Valor':valor,
                                             'Saldo':0}, ignore_index=True)
        self.extrato['Data'] = pd.to_datetime(self.extrato['Data'], format='%d/%m/%Y')
        self.extrato = self.extrato.sort_values(by="Data",ignore_index=True)
        self.extrato['Saldo'] = self.extrato['Valor'].cumsum()

    def gasto(self,data,desc,valor):
        if self.extrato['Saldo'].any() - valor <0:
            print('Não há saldo suficiente')
        else:
            self.extrato = self.extrato._append({'Data':datetime.strptime(data,'%d/%m/%Y'),
                                                'Descrição':desc,
                                                'Valor':-valor,
                                                'Saldo':0}, ignore_index=True)
            self.extrato['Data'] = pd.to_datetime(self.extrato['Data'], format='%d/%m/%Y')
            self.extrato = self.extrato.sort_values(by="Data",ignore_index=True)
            self.extrato['Saldo'] = self.extrato['Valor'].cumsum()

    def exportar_extrato(self,path=None):
        if path != None:
            self.arq_cc=path
        self.extrato['Data'] =self.extrato['Data'].apply(lambda x: x.strftime('%d/%m/%Y'))
        self.extrato.to_csv(self.arq_cc,';',index=False,encoding='utf-8')
    
    def consultar_extrato(self,path=None):
        if path != None:
            self.arq_cc=path
        self.extrato=pd.read_csv(self.arq_cc,sep=';',header=0,index_col=False)
        self.extrato['Data'] = pd.to_datetime(self.extrato['Data'], format='%d/%m/%Y')

class ContaPoupanca(Conta):
    '''
    - Attributes:
        - interest (float): Savings account interest rate.

    - Methods:
        - __init__(self, name, balance, interest): Initializes an instance of the Savings class.
        - summary(self): Displays a summary of the savings account.
    '''
    def __init__(self, nome, saldo, rendimento):
        super().__init__(nome, saldo)
        self.rendimento = rendimento

    def resumo(self):
        super().resumo()
        print(f'Rendimento: {self.rendimento}%')

nu_cred = Credito('Rafael','NuBank',5000,'18/12/2023','26/12/2023')
# nu_cred.gasto('30/12/2023','Ceia',50,3)
nu_cred.gasto('3/2/2024','Celular',1500,24)
# nu_cred.consultar_fatura()
# # nu_cred.gasto('02/02/2023','Carnaval',1000,5)
print(nu_cred.fatura_atual)


# nu_deb = ContaCorrente('Rafael','NuBank')
# # nu_deb.recebimento('1/1/2024','Pix',500)
# # nu_deb.gasto('2/1/2024','Padaria',30)
# # nu_deb.gasto('3/1/2024','Shopping',1000)
# # nu_deb.exportar_extrato()
# nu_deb.consultar_extrato()
# # nu_deb.recebimento('5/12/2023','RAM',150)
# # nu_deb.exportar_extrato()
# print(nu_deb.extrato)
