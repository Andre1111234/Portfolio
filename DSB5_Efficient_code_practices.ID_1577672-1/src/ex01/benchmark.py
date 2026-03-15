import timeit

emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
'anna@live.com', 'philipp@gmail.com']

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

t1 = timeit.timeit("loop_1(emails)", globals=globals(), number=90_000_000)
t2 = timeit.timeit("comprehension_2(emails)", globals=globals(), number=90_000_000)
t3 = timeit.timeit("map_3(emails)", globals=globals(), number=90_000_000)

if t2 <= t1 and t2 <= t3:
    print("It is better to use a list comprehension")
elif t1 <= t2 and t1 <= t3:
    print("It is better to use a loop")
else :
    print("It is better to use a map")
    
    
times = sorted([t1, t2, t3])
print(f"{times[0]} vs {times[1]} vs {times[2]}")