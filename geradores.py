def inteiro():
    '''
    DocString -> Uma string que aparece quando o comando help é utilizao, essa string mostra a documentação da função criada
    A função inteiro retorna números inteiros:
    Função geradora
    '''
    n=0 # Inicialização da função geradora
    while True: # Cada interação acontece em um 'next()'
        yield n # Entra no lugar de return
        n+=1

def cores():
    list_cores=['Vermelho','Azul','Preto','Verde']
    n=0 
    while True:
        yield list_cores[n]
        n = (n+1)%len(list_cores)


gera_inteiro = inteiro()
print(next(gera_inteiro)) # ->0
print(next(gera_inteiro)) # ->1
print(next(gera_inteiro)) # ->2

gera_cor = cores()
print(next(gera_cor))
print(next(gera_cor))
print(next(gera_cor))
print(next(gera_cor))
print(next(gera_cor))


# Maneira alternativa -> principalmenta para o problema dos números inteiros