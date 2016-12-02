

from sympy import *

class Check:
    def test(self):
        M = symbols('M')
        ans1 = 2*'M'
        y = Matrix([1, 2])+Matrix(ans1)-Matrix([5, 8])
       # y = ans1 - 1
        ans = solve(y,M)
        print(ans)
Check().test()
