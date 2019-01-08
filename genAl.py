import random
#populacje
pBadana = [] #populacja badana
wyniki = []

#sprawdzanie dopasowania
def sprDop(x):
    #print(x)
    if x <1 or x >127:
        del pBadana[pBadana.index(x)]
        return 0
    return 2 * (pow(x,2) + 1)

#generator ppulacji
def genP(x):
    for i in range(0,x):
        pBadana.append(random.randint(1,127))
    pBadana.sort()

#mutacja
def mutant(x):
    mutantGen = 1<< random.randint(0,7) #1 przesuwamy bitowo, losowa pomiedzy najstarszym a najmlodszym bitem
    #print("Mutant gen: " + str(mutantGen))
    return x^mutantGen #exclusive or

#krzyzowanie
def cross(x,y):
    locus = 7 - random.randint(0,7)
    #tworzenie maski bitowej d przneoseznia loculusa
    bMask = 0
    for i in range(0,locus):
        bMask = bMask | 1<< i
    #wyluskanie elemntu do zmiany
    tempX = x & bMask
    tempY = y & bMask
    negBMask = ~bMask
    headX = x & negBMask
    headY = y & negBMask

    sumX = headX | tempY
    sumY = headY | tempX
    pBadana[pBadana.index(x)] = sumX
    pBadana[pBadana.index(y)] = sumY

#sterwanie mutacjami i kombinacjami
def mutSteer():
    for nbs, p in enumerate(pBadana):
        pBadana[nbs] = mutant(p)
    for p in pBadana:
        cross(p, pBadana[random.randint(0,len(pBadana)-1)])

#let's start
def engine():
    genP(5)
    resultFlag = False
    genNo = 0
    while not resultFlag:
        print("Generacja: " + str(genNo))
        genP(10 - len(pBadana))
        for probka in pBadana:
            tempW = sprDop(probka)
            if tempW == 32260:  #najwyzsze mozliwe dopasowanie
                resultFlag = True
            print(str(probka) + ": " + str(tempW))
        del pBadana[0:5]
        mutSteer()  #mutujemy tylko te które zostały w selekcji
        print("-------------------------")
        genNo +=1

engine()
print(sprDop(127))