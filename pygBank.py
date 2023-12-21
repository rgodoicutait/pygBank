import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from openpyxl import load_workbook, Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
from datetime import datetime
from datetime import timedelta
import os



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
    # Adquirindo o caminho da pasta em que o programa está armazenado
        diretorio_atual = os.getcwd()
        nome_arquivo = os.path.basename(diretorio_atual)
        self.caminho_pasta = diretorio_atual.replace(nome_arquivo,'')

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
    
    def exportar_fatura(self,path=None):
        if path != None:
            self.arq_cred=path
        self.fatura_atual['Data'] =self.fatura_atual['Data'].apply(lambda x: x.strftime('%d/%m/%y'))
        self.fatura_atual['Data_Ref'] =self.fatura_atual['Data_Ref'].apply(lambda x: x.strftime('%d/%m/%y'))
        self.fatura_atual.to_csv(self.arq_cred,';',index=False,encoding='utf-8')

        print('fatura exportada para: ' + self.arq_cred)

    def consultar_fatura(self,path=None):
        if path != None:
            self.arq_cred=path
        self.fatura_atual=pd.read_csv(self.arq_cred,sep=';',header=0)
        

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

nu_cred = Credito('Rafael','NuBank',100,3000,'18/12/2023','26/12/2023')
# nu_cred.gasto('20/12/2023','Padaria',10)
# nu_cred.gasto('21/12/2023','Manutenção carro',1000,4)
# nu_cred.gasto('26/12/2023','Celular',2400,12)
# nu_cred.exportar_fatura(r'C:\Users\rafae\OneDrive\Faculdade\10º Período\Projeto Computacional\credito.csv')
# nu_cred.exportar_fatura()
nu_cred.consultar_fatura()
nu_cred.gasto('30/12/2023','Mercado',198.80)
print(nu_cred.fatura_atual)
