import threading
import time

z = []

class probka(threading.Thread):
    lock = 0
    number = 0
    def __init__(self, loc, numb):
        self.lock = loc
        self.number = numb
        threading.Thread.__init__(self)

    def run(self):
        for i in range(0,10):
            #print(i)
            self.lock.acquire()
            z.append(i)
            time.sleep(self.number)
            print(z)
            self.lock.release()
            time.sleep(self.number)

loc = threading.Lock()
x = probka(loc,1)
y = probka(loc,2)

x.setName("Watek x")
y.setName("Watek y")

y.start()
x.start()

x.join()
y.join()
