import numpy as np
import testDepend2 as t2


def func1(N):
    for i in range(N):
        print("Hello!")
        c2 = t2.testDep2()
        c2.func1()
        

def func2(N):
    x = np.zeros(N)
    x += 1000
    func1(100)
    return x

def func3(N):
    x = np.zeros(1000)
    x = x * N
    return x

def func4(N):
    x = 0
    for i in range(N):
        for j in range(i,N):
            x += (i*j)
    return x

class myClass:
    def __init__(self, name):
        self.name = name

    def func5(self, x, *y, **z):
        func3(100)
        func3(100)
        print("Hello! I am " + self.name)

c1 = myClass("funny")
c2 = t2.testDep2()
c2.gamer()

c1.func5()
func2(500)
func1(100)