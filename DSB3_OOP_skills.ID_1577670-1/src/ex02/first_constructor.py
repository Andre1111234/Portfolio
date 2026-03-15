import sys
import os

class Research:
    def __init__(self,file_path):
        self.file_path = file_path
        
    def file_reader(self):
        if not os.path.exists(self.file_path):
            raise Exception("File not found")
    
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
    
        if len(lines) < 2:
            raise Exception("File is too short")
    
    # 1. Проверить заголовок
        header = lines[0].strip().split(',')
        if len(header) != 2:
                raise Exception("Wrong header format")
    
    # 2. Проверить строку данных
        for i in range(1, len(lines)):
            values = lines[i].strip().split(',')
        
        if len(values) != 2:
            raise Exception(f"Wrong data line {i+1}")
        if values[0] not in ['0', '1'] or values[1] not in ['0', '1']:
            raise Exception(f"Bad values line {i+1}")
        if values[0] == values[1]:
            raise Exception(f"Same values line {i+1}")
    
    # 3. Вернуть содержимое
        with open(self.file_path, 'r') as file:
            return file.read()
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Error: need file path")
        sys.exit(1)
    
    research = Research(sys.argv[1])  # передаем путь в конструктор
    print(research.file_reader())