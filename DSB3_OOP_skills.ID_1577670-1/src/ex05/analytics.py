import os
from random import randint

class Research:
    def __init__(self, file_path):
        self.file_path = file_path
        
    def file_reader(self, has_header=True):
        if not os.path.exists(self.file_path):
            raise Exception("File not found")
    
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
            
            result.append([int(values[0]), int(values[1])])
        
        return result
    
    class Calculations:
        def __init__(self, data):
            self.data = data
        
        def counts(self):
            heads = sum(pair[0] for pair in self.data)
            tails = sum(pair[1] for pair in self.data)
            return heads, tails
        
        def fractions(self, heads, tails):
            total = heads + tails
            if total == 0:
                return 0, 0
            head_fraction = heads / total
            tail_fraction = tails / total
            return head_fraction, tail_fraction

class Analytics(Research.Calculations):
    def __init__(self, data):
        super().__init__(data)
    
    def predict_random(self, num_predictions):
        predictions = []
        for _ in range(num_predictions):
            prediction = randint(0, 1)
            if prediction == 1:
                predictions.append([1, 0])
            else:
                predictions.append([0, 1])
        return predictions
    
    def predict_last(self, research_instance):
        data = research_instance.file_reader()
        return data[-1] if data else None
    
    def save_file(self, data, filename, extension):
        full_filename = f"{filename}.{extension}"
        with open(full_filename, 'w') as file:
            file.write(data)