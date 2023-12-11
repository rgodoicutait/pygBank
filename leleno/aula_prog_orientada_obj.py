### Programação orientada por objetos

# instâncias = exemplares de um objeto -> definem  as características do objeto

##### Definição da classe Vetor2D

import numpy as np

class Vetor2D:
# Métodos especiais --> já são definidos pelo python e possuem a seguinte estrutrua __metodo__
    # self (pode usar a palavra que quiser, mas geralmente é self) = argumento de atribuição a objeto
    # self é uma palavra genérica para definir qualquer objeto que pertença a essa classe
    def __init__(self, x, y): # Inicialização da classe
        self.xcomp = x
        self.ycomp = y # Atributos do objeto do tipo (da classe) Vetor2D

    def __str__(self):# 'string' -> o que o print extrai quando chamado para imprimir o objeto
        return f'Vetor2D({self.xcomp},{self.ycomp})'
    
    def __add__(self,other): # dá um atributo de soma ao operador '+'
        x = self.xcomp + other.xcomp
        y = self.ycomp + other.ycomp
        return Vetor2D(x,y)   # Sobrecarga do operador '+'
    
    # def soma(self,other):
    #     return Vetor2D(self.xcomp+other.xcomp, self.ycomp+other.ycomp)

    def __neg__(self): # método que retorna o valor negativo de self
        return Vetor2D(-self.xcomp,-self.ycomp)

    def __sub__(self,other): # método de subtração 
        return self + (-other)
    
    def __mul__(self,other): # self é sempre do tipo da classe, other não necessariamente
        if isinstance(other,Vetor2D):    # isinstance retorna true se o objeto other pertence à vetor 2D
            # Produto escalar de 2 vetores
            return self.xcomp*other.xcomp + self.ycomp*other.ycomp
        else:
            # Produto de vetor por escalar
            return Vetor2D(self.xcomp*other, self.ycomp*other)
    
    __rmul__ = __mul__  # Inverte a ordem de self e other para que a ordem dos fatores não altere o produto

    def norm(self): # Norma do vetor
        return np.sqrt(self * self)
    
    #TODO: testar mais dimensões
    
# isso me dá lembranças de GA com a Gabi, quando ela falava dos axiomas dos vetores

##### Criar objetos da classe Vetor2D

v1 = Vetor2D(3,2)  # v1 = 3i + 2j -> instância de um objeto definido pela classe Vetor2D sendo guardada em v1
v2 = Vetor2D(5,8)
v3 = Vetor2D(10,7)
v4 = Vetor2D(1,1)
# v1 e v2 são objetos do mesmo tipo (Vetor2D), mas com atributos diferentes
print(v1.xcomp, v2.ycomp)

# v1.xcomp = 5 # Atualiza o atributo de xcomp para 5
print(v1.xcomp)
print(v1+v2+v3+v4)

# v5 = v1.soma(v2)
# print(v5)
print(v1*v2*v3)
print(v1.norm())

