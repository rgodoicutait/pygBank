class averager:
    
    def __init__(self):
        self.lista=[]
        self.media=None

    def __call__(self,novo,action='append'):
        if action=='append':
            self.lista.append(novo)
        elif action =='remove':
            self.pop() # remove o último
        self.media = sum(self.lista)/len(self.lista)
    

###############################

L= averager()
print(L.media) #warning: vazio
L(4)
print(L.media) # 4
L(6)
print(L.media) # 5
L(9)
print(L.media) # 19/3


