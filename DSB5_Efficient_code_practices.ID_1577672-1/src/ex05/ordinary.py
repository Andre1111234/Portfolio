import sys
import resource

if len(sys.argv) < 2 :
    print("Usage: ./ordinary.py <path_to_file>")
    sys.exit(1)

file_path = sys.argv[1]

def reading_file(path) :
    with open(path,'r') as file:
        return file.readlines()
    
if __name__ == '__main__' :
    lines = reading_file(file_path)
    
    for line in lines :
        pass

    usage = resource.getrusage(resource.RUSAGE_SELF)

    peak_memory_gb = usage.ru_maxrss / (1024**3)

    time_spent = usage.ru_utime + usage.ru_stime

    print(f"Peak Memory Usage = {peak_memory_gb:.3f} GB")
    print(f"User Mode Time + System Mode Time = {time_spent:.2f}s")