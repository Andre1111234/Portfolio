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

def identify_expression(expression):
    """Определяет тип выражения и возвращает результат"""
    expression = expression.strip()
    
    # Пропускаем пустые выражения (две запятые подряд)
    if not expression:
        return None
    
    # Проверяем, является ли выражение тикером
    ticker_upper = expression.upper()
    if ticker_upper in STOCKS:
        # Находим компанию по тикеру
        for company, ticker in COMPANIES.items():
            if ticker == ticker_upper:
                return f"{ticker_upper} is a ticker symbol for {company}"
    
    # Проверяем, является ли выражение компанией
    company_name = None
    for company in COMPANIES:
        if company.lower() == expression.lower():
            company_name = company
            break
    
    if company_name:
        ticker = COMPANIES[company_name]
        price = STOCKS.get(ticker)
        if price is not None:
            return f"{company_name} stock price is {price}"
    
    # Если не тикер и не компания
    return f"{expression} is an unknown company or an unknown ticker symbol"

def main():
    # Проверка количества аргументов
    if len(sys.argv) != 2:
        return
    
    input_string = sys.argv[1]
    
    # Разделяем строку по запятым (даже если запятая одна)
    expressions = input_string.split(',')
    
    results = []
    for expr in expressions:
        result = identify_expression(expr)
        if result is not None:  # Пропускаем пустые выражения
            results.append(result)
    
    # Выводим все результаты через перенос строки
    for result in results:
        print(result)

if __name__ == "__main__":
    main()