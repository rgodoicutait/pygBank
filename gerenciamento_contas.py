import pandas as pd
import json as js
import requests
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime as dt
import datetime

class banco: # Uma pequena classe para separar os bancos
    def __init__(self, banco, tipo):
        self.banco = banco
        self.tipo = tipo
        self.hoje = date.today() - datetime.timedelta(days=1)

class credito(banco): # A partir do banco, essa classe trabalha com gastos no crédito
    def __init__(self, banco, data_fech, data_venc, limite, tipo="Crédito"):
        super().__init__(banco,tipo)
        self.data_fech = data_fech
        self.data_venc = data_venc
        self.limite = limite
        self.extrato = {'Data':[],'Descrição':[],'Valor':[],'Parcelas':[]}
    
    def gasto(self, descricao, valor, data, parcelas=1):
        self.extrato['Data'].append(data)
        self.extrato['Descrição'].append(descricao)
        self.extrato['Valor'].append(valor)
        self.extrato['Parcelas'].append(parcelas)
    
    #TODO Função para pagar de pagamento do crédito
    #TODO Função para propagar as parcelas para os próximos meses
    #TODO Não deixar o usuário gastar mais do que tem, não deve ser possível obter um saldo negativo
    
    def imprime_extrato(self):
        self.tab_extr = pd.DataFrame(self.extrato)
        print('\n')
        print(self.tab_extr)
        print('\n')

class debito(banco): # A partir do banco, essa classe trabalha com as movimentações no débito
    def __init__(self,banco, data_inicio,tipo="Débito", saldo_inicial=0):
        super().__init__(banco,tipo)
        self.extrato = {'Data':[data_inicio],'Descrição':['Saldo inicial'],'Valor':[saldo_inicial],'saldo atual':[saldo_inicial]}
    
    def transacao(self,descricao, valor, data):
        self.extrato['Data'].append(data)
        self.extrato['Descrição'].append(descricao)
        self.extrato['Valor'].append(valor)
        self.extrato['saldo atual'].append(self.extrato['saldo atual'][-1]+valor)

    def imprime_extrato(self):
        self.tab_extr = pd.DataFrame(self.extrato)
        print('\n')
        print(self.tab_extr)
        print('\n')
    
#######################################################
nu_deb = debito('NuBank','30/10/2023',saldo_inicial=1000)
nu_deb.transacao('Hotel 3 diárias',-500,'31/10/2023')
nu_deb.imprime_extrato()
nu_deb.transacao('Comilão', -17.50,'01/11/2023')
nu_deb.imprime_extrato()
print(nu_deb.hoje)




