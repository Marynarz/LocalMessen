import random
#populacje
pBadana = [] #populacja badana
wyniki = []

#sprawdzanie dopasowania
def sprDop(x):
    if x <1 or x >127:
        return 0
    return 2 * (pow(x,2) + 1)

#generator ppulacji
def genP(x):
    for i in range(0,x):
        pBadana.append(random.randint(1,127))

#let's start
def engine():
    genP(10)
    for i in range(0,10):
        print(str(sprDop(pBadana[i])))

engine()