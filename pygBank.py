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
Sistema Bancário - Documentação

Este programa implementa um sistema bancário simples com contas de crédito, conta corrente e conta poupança.

Módulos e Bibliotecas Utilizados:
- numpy
- matplotlib.pyplot
- pandas
- openpyxl
- datetime
- os

Exemplo de Uso:
- Criar instâncias das classes Credito, ContaCorrente e ContaPoupanca.
- Realizar operações como gastos, recebimentos, exportação e consulta de faturas/extratos.

'''

class Conta:
    '''
    - Atributos:
        - nome (str): Nome do usuário.
        - banco (str): Nome do banco.
        - caminho_pasta (str): Caminho da pasta do programa.

    - Métodos:
        - __init__(self, nome, banco): Inicializa uma instância da classe Conta.
        - resumo(self): Exibe um resumo da conta.
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
    - Atributos:
        - limite (float): Limite de crédito.
        - data_fech (datetime): Data de fechamento da fatura.
        - data_venc (datetime): Data de vencimento da fatura.
        - fatura_atual (DataFrame): DataFrame para armazenar as transações da fatura.
        - arq_cred (str): Caminho do arquivo CSV para exportar/importar a fatura.

    - Métodos:
        - __init__(self, nome, banco, limite, data_fech, data_venc): Inicializa uma instância da classe Credito.
        - resumo(self): Exibe um resumo da conta de crédito.
        - gasto(self, data, descr, valor, parcela=1): Registra uma despesa na conta de crédito.
        - exportar_fatura(self, path=None): Exporta a fatura para um arquivo CSV.
        - consultar_fatura(self, path=None): Consulta a fatura a partir de um arquivo CSV.

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
    - Atributos:
        - extrato (DataFrame): DataFrame para armazenar transações da conta corrente.
        - arq_cc (str): Caminho do arquivo CSV para exportar/importar o extrato.

    - Métodos:
        - __init__(self, nome, banco): Inicializa uma instância da classe ContaCorrente.
        - recebimento(self, data, desc, valor): Registra um recebimento na conta corrente.
        - gasto(self, data, desc, valor): Registra um gasto na conta corrente.
        - exportar_extrato(self, path=None): Exporta o extrato para um arquivo CSV.
        - consultar_extrato(self, path=None): Consulta o extrato a partir de um arquivo CSV.


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
    - Atributos:
        - rendimento (float): Percentual de rendimento da conta poupança.

    - Métodos:
        - __init__(self, nome, saldo, rendimento): Inicializa uma instância da classe ContaPoupanca.
        - resumo(self): Exibe um resumo da conta poupança.
'''
    def __init__(self, nome, saldo, rendimento):
        super().__init__(nome, saldo)
        self.rendimento = rendimento

    def resumo(self):
        super().resumo()
        print(f'Rendimento: {self.rendimento}%')

