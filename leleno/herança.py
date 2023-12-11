import datetime
class pessoa:
    def __init__(self, nome, data_nascimento, loc_nasc):
        self.dados={}
        self.dados['Nome'] = nome
        self.altera_dados('Data de Nascimento',data_nascimento)
        self.dados['Local de nascimento']=loc_nasc

    # def data_nasc(self, data_de_nasc):
    #     self.dados['Data de Nascimento'] = datetime.datetime.strptime(data_de_nasc,'%d/%m/%Y')

    def altera_dados(self,dado,valor): # Tentei criar uma função que altera os dados em caso de preenchimento incorreto
        if dado == 'Data de Nascimento': # Acho que deu bom
            self.dados[dado] = datetime.datetime.strptime(valor,'%d/%m/%Y')
        else:
            self.dados[dado] = valor

    def idade(self):
        today = datetime.date.today()
        nasc = self.dados['Data de Nascimento']
        age = today.year - nasc.year - ((today.month,today.day)<(nasc.month,nasc.day))
        self.dados['Idade']=age
        return age
    
    def __str__(self):
        self.idade()
        dados_str=''
        for key, value in self.dados.items():
            dados_str+=f'{key}: {value}\n'
        return dados_str
    
# subclasse de pessoa aluno é uma pessoa, mas nem toda pessoa é um aluno
class aluno(pessoa):
    def __init__(self, nome, data_nasc,loc_nasc,NUSP,curso):
        super().__init__(nome,data_nasc,loc_nasc) # super refere-se a classe superior, a classe mãe.
        self.dados['NUSP'] = NUSP
        self.dados['Curso'] = curso

if __name__ =='__main__':
    rafael = aluno('Rafael Godoy Cutait','01/04/2001','Itu',11314780,'Engenharia Física')
    print(rafael)
    rafael.altera_dados('Data de Nascimento','12/04/2001')
    print(rafael)
    rafael.altera_dados('Nome','Rafael Godoi Cutait')
    print(rafael)

    taina = aluno('Tainá','07/11/2000','São Roça',11390723,'Engenharia Química')
    print(taina)

# To com fome :(