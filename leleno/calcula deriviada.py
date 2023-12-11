from typing import Any


def f(x):
    return x**2

class derivada:
    def __init__(self,func,h=1e-5):
        self.f = func
        self.h = h
       # pass
    def __call__(self,x):
        der = (self.f(x+self.h)-self.f(x))/self.h
        return der

df = derivada(f)

# help(round) # por causa do saldo de contas tem que ter duas casas decimais. Sim, principalmente para divisão de parcelas

print(df(3))