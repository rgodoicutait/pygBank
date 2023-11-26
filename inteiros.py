class inteiro:
    def __init__(self):
        self.n = 0

    def __call__(self,h=1):
        self.n+=h

##########################

j = inteiro()
print(j.n)
j(2)
print(j.n)
j()
print(j.n)
j(10)
print(j.n)

