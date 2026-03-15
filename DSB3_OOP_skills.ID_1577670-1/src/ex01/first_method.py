
class Research:
    def file_reader(self):
        with open('data.csv', mode = 'r') as file:
            data = file.read()
        return data 

if __name__ == '__main__':
    obj = Research()
    result = obj.file_reader()
    print(result)