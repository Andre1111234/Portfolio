# caesar.py
import sys

def caesar_cipher(text, shift, mode='encode'):
    """
    Шифрует или дешифрует текст с помощью шифра Цезаря
    """
    # Проверка на кириллицу
    for char in text:
        if '\u0400' <= char <= '\u04FF':  # Диапазон кириллических символов
            raise ValueError("The script does not support your language yet.")
    
    result = []
    
    for char in text:
        if char.isalpha():
            # Определяем базовый код для алфавита (A-Z или a-z)
            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')
            
            # Сдвигаем символ
            if mode == 'encode':
                shifted_char = chr((ord(char) - base + shift) % 26 + base)
            else:  # decode
                shifted_char = chr((ord(char) - base - shift) % 26 + base)
            
            result.append(shifted_char)
        else:
            # Цифры и спецсимволы не изменяем
            result.append(char)
    
    return ''.join(result)

def main():
    # Проверка количества аргументов
    if len(sys.argv) != 4:
        raise ValueError("Wrong number of arguments")
    
    mode = sys.argv[1].lower()
    text = sys.argv[2]
    
    try:
        shift = int(sys.argv[3])
    except ValueError:
        raise ValueError("Shift must be an integer")
    
    # Проверка режима
    if mode not in ['encode', 'decode']:
        raise ValueError("Mode must be 'encode' or 'decode'")
    
    # Выполняем шифрование/дешифрование
    result = caesar_cipher(text, shift, mode)
    print(result)

if __name__ == '__main__':
    main()