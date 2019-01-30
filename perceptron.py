class WspPR:
    x=0
    y=0
    s=0
    def __init__(self,x,y,s):
        self.x = x
        self.y = y
        self.s = s

def predictins(obj, weights):
    activat = 0
    activat += (obj.x * weights[1]) + (obj.y * weights[2]) + weights[0]
    return 1 if activat >=0 else 0

def trening(obj, learningRate,epoch):
    weigh = [0.0,0.0,0.0]
    for epochNumb in range(epoch):
        errorSummary = 0.0
        for objs in obj:
            predictio = predictins(objs,weigh)
            error = objs.s - predictio
            errorSummary = error ** 2
            weigh[0] = weigh[0] + learningRate * error
            #print(weigh[0] + learningRate * error)
            weigh[1] = weigh[1] + learningRate * error * objs.x
            weigh[2] = weigh[2] + learningRate * error * objs.y
        #print(": ".join([str(epochNumb),str(learningRate),str(errorSummary)]))
        #print(weigh)
    return weigh

weights = [1,2,-1]
wspNauczyciel = []
wspTest = []

wspNauczyciel.append(WspPR(2,7,0))
wspNauczyciel.append(WspPR(3,3,1))
wspNauczyciel.append(WspPR(3,12,0))
wspNauczyciel.append(WspPR(100,250,0))
wspNauczyciel.append(WspPR(19,50,0))
wspNauczyciel.append(WspPR(10, -10, 1))
wspNauczyciel.append(WspPR(5, 0, 1))
wspNauczyciel.append(WspPR(100, 100, 1))
wspNauczyciel.append(WspPR(12, 20, 1))
wspNauczyciel.append(WspPR(-1,3,0))
wspNauczyciel.append(WspPR(-6,-10,0))
wspNauczyciel.append(WspPR(-3,0,0))
wspNauczyciel.append(WspPR(10,101,0))
wspNauczyciel.append(WspPR(10,23,0))

wspTest.append(WspPR(-2,5,0))
wspTest.append(WspPR(10,3,1))
wspTest.append(WspPR(12,12,1))
wspTest.append(WspPR(200,250,1))
wspTest.append(WspPR(19,5,1))
wspTest.append(WspPR(30, -10, 1))
wspTest.append(WspPR(5, 4, 1))
wspTest.append(WspPR(100,-100, 1))
wspTest.append(WspPR(12, 50, 0))
wspTest.append(WspPR(-1,-9,1))
wspTest.append(WspPR(-6,10,0))
wspTest.append(WspPR(-3,-10,1))
wspTest.append(WspPR(1001,101,1))
wspTest.append(WspPR(100,203,0))


for objs in wspNauczyciel:
    wynik = predictins(objs,weights)
    if wynik == objs.s:
        result = "PASS"
    else:
        result = "FAIL"
    print(" ".join(["Wspolrzedne:",str(objs.x),str(objs.y),"oczekiwany",str(objs.s),"otrzymany",str(wynik),result]))

weights = trening(wspNauczyciel,0.1,10)
print(weights)
print("--")
for objs in wspTest:
    wynik = predictins(objs, weights)
    if wynik == objs.s:
        result = "PASS"
    else:
        result = "FAIL"
    print(" ".join(
        ["Wspolrzedne:", str(objs.x), str(objs.y), "oczekiwany", str(objs.s), "otrzymany", str(wynik), result]))