#this is a private variable author name
import math


class Solver:
    def demo(self):
        a=int(input("a"))
        b=int(input("b"))
        c=int(input("c"))
        d=b**2-4*a*c
        if(d>=0):
            disc = math.sqrt(d)
        else:
            disc=d
        print(disc)
Solver().demo()


