'''class CONTA:
    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial

######
conta_eleno = CONTA(50)

conta_eleno.saldo = 500000000 # hacker alterando a conta do eleno

print(conta_eleno)'''

class conta: # Qualquer def que exista dentro de uma classe é chamada de método
    def __init__(self, nome, saldo_inicial=0): # saldo_inicial=0 é um padrão que será utilizado caso não seja especificado o saldo incial
        self._nome = nome
        self._saldo = saldo_inicial # O _ antes é só uma convenção para variáveis 'protegidas'
        x = 8 # Variável local da função init
    
    @property # Decorador que decora uma propriedade específica
    def saldo(self): # vai proteger a variável _saldo # getter (pegador, acessador, quem consegue) da propriedade saldo
        return self._saldo
    
    @property
    def nome(self):
        return self._nome
    
    @saldo.setter
    def saldo(self, dados): #setter, ajusta a propriedade saldo
        try: # Comando que o python tenta rodar
            valor, senha = dados # extrai os valores da tupla
        except TypeError: # se der erro ele vem para a exceção, ele irá aparecer se a pessoa fornecer os dados fora do formato certo
            raise('Forneça o novo saldo e a senha correta!')
        else:
            if senha == 'senha123':
                self._saldo = valor
                print('Saldo alterado')
            else:
                raise('Senha incorreta!')
            
    @nome.setter
    def nome(self, valor):
        self._nome = valor
            
#######

LE = conta('Eleno',60)
# print(LE.saldo)
# LE.saldo = (5000000, 'senha12') # dados como tupla, algo iterável
# print(LE.saldo)

# Juros
y = LE.saldo*1.1
LE.saldo= (y, 'senha123')
print(LE.saldo)