import sys
import os

class Research:
    def __init__(self, file_path):
        self.file_path = file_path
        
    def file_reader(self, has_header=True):
        if not os.path.exists(self.file_path):
            raise Exception("File not found") # исключение без вывода ошибки
    
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
    
        if len(lines) < 2:
            raise Exception("File is too short")
    
        header = lines[0].strip().split(',')
        if len(header) != 2:
            raise Exception("Wrong header format")

        result = []
        start_index = 1 if has_header else 0
        
        for i in range(start_index, len(lines)):
            values = lines[i].strip().split(',')
        
            if len(values) != 2:
                raise Exception(f"Wrong data line {i+1}")
            if values[0] not in ['0', '1'] or values[1] not in ['0', '1']:
                raise Exception(f"Bad values line {i+1}")
            if values[0] == values[1]:
                raise Exception(f"Same values line {i+1}")
            
            result.append([int(values[0]), int(values[1])]) #в конец списка добавление
        
        return result
    
    class Calculations:
        def counts(self, data):
            heads = sum(pair[0] for pair in data)
            tails = sum(pair[1] for pair in data)
            return heads, tails
        
        def fractions(self, heads, tails):
            total = heads + tails
            if total == 0:
                return 0, 0
            head_fraction = heads / total
            tail_fraction = tails / total
            return head_fraction, tail_fraction
        
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 first_nest.py <file_path>")
        sys.exit(1)
    
    try:
        research = Research(sys.argv[1])
        data = research.file_reader()
        print(data)
        
        calc = research.Calculations()
        heads, tails = calc.counts(data)
        print(heads, tails)
        
        head_frac, tail_frac = calc.fractions(heads, tails)
        print(f"{head_frac:.4f} {tail_frac:.4f}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)