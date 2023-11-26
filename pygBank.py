import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# classe mãe: banco?
## classe filha: crédito, débito, poupança?
### usar o pandas para salvar tudo em algum lugar?
#### Como formatar uma string como data?
##### Como chamar a subclasse para utilizar tanto as funções da classe mãe quanto a da filha?
#TODO Algum método de armazenar/acessar o histórico da pessoa (acessar o arquivo em que as movimentações foram salvas, ex: Excel, csv, etc...)
#TODO Alguma interface de texto?

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

    def resumo(self):
        super().resumo()
        print(f'Limite: R${self.limite:.2f}')
        print(f'Data de Fechamento da Fatura: {self.data_fech}')
        print(f'Data de Vencimento da Fatura: {self.data_venc}')
    
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

nu_deb = ContaCorrente("Tainá","NuBank",11000,0)
nu_deb.debito("Guitarra (Fender)",5000)
nu_deb.recebimento("Pix do além",1000)
nu_deb.debito("Um agrado pro meu xuxu",4000)
nu_deb.Extrato()
