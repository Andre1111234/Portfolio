import timeit
import random
from collections import Counter

N = 1_000_000
data = [random.randint(0, 100) for _ in range(N)]

def my_count_dict(lst):
    counts = {i: 0 for i in range(101)}
    for x in lst:
        counts[x] += 1
    return counts

def my_top10(lst):
    counts = my_count_dict(lst)
    items = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    return items[:10]

def counter_dict(lst):
    return Counter(lst)

def counter_top10(lst):
    return Counter(lst).most_common(10)

if __name__ == "__main__":
    calls = 10  # или другое число

    t_my_dict = timeit.timeit("my_count_dict(data)", globals=globals(), number=calls)
    t_counter_dict = timeit.timeit("counter_dict(data)", globals=globals(), number=calls)

    t_my_top = timeit.timeit("my_top10(data)", globals=globals(), number=calls)
    t_counter_top = timeit.timeit("counter_top10(data)", globals=globals(), number=calls)

    print(f"my function: {t_my_dict:.7f}")
    print(f"Counter: {t_counter_dict:.7f}")
    print(f"my top: {t_my_top:.7f}")
    print(f"Counter's top: {t_counter_top:.7f}")