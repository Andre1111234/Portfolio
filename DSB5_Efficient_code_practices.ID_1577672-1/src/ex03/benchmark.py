import timeit
import sys
from functools import reduce

if len(sys.argv) < 4 :
    sys.exit(0)
func_name = sys.argv[1]
calls = int(sys.argv[2])
n = int(sys.argv[3])

def reduce_5(n) :
    return reduce(lambda a,b: a + b*b, range(1, n + 1), 0)

def loop_5(n) :
    total = 0
    for i in range(1, n +1) :
        total += i * i
    return total


if func_name == "reduce":
    t = timeit.timeit("reduce_5(n)", globals=globals(), number=calls)
elif func_name == "loop":
    t = timeit.timeit("loop_5(n)", globals=globals(), number=calls)
else:
    print("Unknown function")
    sys.exit(1)
    
print(t)

