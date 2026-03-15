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
    # Проверка количества аргументов
    if len(sys.argv) != 2:
        return
    
    ticker_input = sys.argv[1].strip()
    
    # Проверка на пустую строку
    if not ticker_input:
        print("Unknown ticker")
        return
    
    # Регистронезависимый поиск компании по тикеру
    company_name = None
    for company, ticker in COMPANIES.items():
        if ticker.lower() == ticker_input.lower():
            company_name = company
            break
    
    if company_name is None:
        print("Unknown ticker")
    else:
        # Получаем цену акции в верхнем регистре
        price = STOCKS.get(ticker_input.upper())
        if price is not None:
            print(f"{company_name} {price}")
        else:
            print("Unknown ticker")

if __name__ == "__main__":
    main()