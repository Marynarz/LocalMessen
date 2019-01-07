import random
import math as m
import matplotlib.pyplot as plt
#globals
punkty = []

#miasta
class miasta:
    nrMiasta = 0
    wspX = 0.0
    wspY = 0.0

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

def tabCr():
    for o in punkty:
        for p in punkty:
            if o.nrMiasta == p.nrMiasta:
                pass
            else:
                dist = m.sqrt(m.pow(m.fabs(p.wspY - o.wspY),2)+m.pow(m.fabs(p.wspX - p.wspX),2))
                print("Nr: " + str(o.nrMiasta) +" to Nr: "+ str(p.nrMiasta)+ ", DIST: "+str(dist))
def plotCr():
    plt.title("Punkty do odwiedzenia")
    plt.xlabel("X")
    plt.ylabel("Y")
    X = []
    Y = []
    for o in punkty:
        X.append(o.wspX)
        Y.append(o.wspY)
        plt.annotate(str(o.nrMiasta),(o.wspX,o.wspY))
    #plt.plot(X,Y)
    plt.scatter(X,Y)
    plt.grid()
    plt.show()

generatorMiast(15)
for o in punkty:
    o.allPrt()
tabCr()
plotCr()

