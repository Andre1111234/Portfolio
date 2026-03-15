
class Must_Read:
    with open('data.csv', mode = 'r') as file:
        data = file.read()
    print(data) 

if __name__ == '__main__':
    Must_Read