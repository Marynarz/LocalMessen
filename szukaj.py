import random
#globals
punkty = []

#miasta
class miasta:
    nrMiasta = 0
    wspX = 0
    wspY = 0

    def __init__(self,nr,wsx,wsy):
        self.nrMiasta = nr
        self.wspX = wsx
        self.wspY = wsy

    def allPrt(self):
        print('Nr: '+str(self.nrMiasta) + ', X: '+ str(self.wspX) + ', Y: '+str(self.wspY))

#gen
def generatorMiast(n):
    for i in range (1,n+1):
        punkty.append(miasta(i,random.randint(1,100),random.randint(1,100)))

generatorMiast(3)
for o in punkty:
    o.allPrt()