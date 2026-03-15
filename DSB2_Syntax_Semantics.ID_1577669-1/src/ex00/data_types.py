def data_types():
    a = 52              # int целое
    b = "hello"         # str строка/текст
    c = 3.14            # float число с запятой/дроби
    d = True            # bool логический да/нет
    e = [1, 2, 3]       # list список 
    f = {"key": "val"}  # dict словарь
    g = (7, 8, 9)       # tuple константы (список неизменяей)
    h = {4, 5, 6}       # set множество (уникальные значения)
    
    types_list = [type(a), type(b), type(c), type(d), type(e), type(f), type(g), type(h)]
    print(types_list)

if __name__ == '__main__':
    data_types()
