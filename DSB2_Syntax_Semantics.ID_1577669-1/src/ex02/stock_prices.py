import sys

COMPANIES = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT', 
    'Netflix': 'NFLX',
    'Tesla': 'TSLA',
    'Nokia': 'NOK'
}

STOCKS = {
    'AAPL': 287.73,
    'MSFT': 173.79,
    'NFLX': 416.90, 
    'TSLA': 724.88,
    'NOK': 3.37
}

def main():
    # ВСЕ что внутри функции - с ОТСТУПОМ!
    if len(sys.argv) != 2:
        return
    
    company_name = sys.argv[1].strip()  # Добавил strip() для пробелов
    
    # Проверка на пустую строку
    if not company_name:
        print("Unknown company")
        return
    
    # Регистронезависимый поиск
    company_key = None
    for key in COMPANIES:
        if key.lower() == company_name.lower():
            company_key = key
            break
    
    if company_key is None:
        print("Unknown company")
    else:
        ticker = COMPANIES[company_key]
        price = STOCKS.get(ticker)
        print(price)

if __name__ == "__main__":
    main()