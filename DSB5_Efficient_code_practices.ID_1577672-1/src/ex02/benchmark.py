import timeit
import sys

emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com']

func_name = sys.argv[1]
calls = int(sys.argv[2])

emails *= 5

def loop_1(emails) :
    result = []
    for x in emails :
        if x.endswith('@gmail.com') :
            result.append(x)
    return result
        
def comprehension_2(emails) :
    return [x for x in emails if x.endswith('@gmail.com')]

def map_3(emails) :
    return list(map(lambda x: x if x.endswith('@gmail.com') else None, emails))

def filter_4(emails) :
    return list(filter(lambda x: x.endswith('@gmail.com'),emails))

if func_name == "loop":
    t = timeit.timeit("loop_1(emails)", globals=globals(), number=calls)
elif func_name == "list_comprehension":
    t = timeit.timeit("comprehension_2(emails)", globals=globals(), number=calls)
elif func_name == "map":
    t = timeit.timeit("map_3(emails)", globals=globals(), number=calls)
elif func_name == "filter":
    t = timeit.timeit("filter_4(emails)", globals=globals(), number=calls)
else:
    print("Unknown function")
    sys.exit(1)
    
print(t)