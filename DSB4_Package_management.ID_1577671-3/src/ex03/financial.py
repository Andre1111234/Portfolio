#!/usr/bin/env python3
import sys
import time
import requests
from bs4 import BeautifulSoup


def get__dataFinancial(ticker, field_name):
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        ),
        'Accept': (
            'text/html,application/xhtml+xml,application/xml;q=0.9,'
            'image/avif,image/webp,image/apng,*/*;q=0.8'
        ),
        'Accept-Language': 'en-US,en;q=0.9'
    }

    # sleep обязателен
    time.sleep(5)

    url = f"https://finance.yahoo.com/quote/{ticker}/financials"
    responce = requests.get(url, headers=headers, timeout=10)
    responce.raise_for_status()

    soup = BeautifulSoup(responce.content, 'html.parser')

    field_element = soup.find_all('div', {'class': 'row lv-0 yf-t22klz'})

    for row in field_element:
        div_title = row.find('div', class_='rowTitle yf-t22klz')
        if not div_title:
            continue

        attribute_title = div_title.get('title', '').strip()
        text_title = div_title.text.strip()

        if field_name == attribute_title or field_name == text_title:
            return tuple(
                element.text.strip()
                for element in row.find_all('div', class_='column')
            )

    raise Exception("Field not found")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: ./financial.py <TICKER> <FIELD>")
        sys.exit(1)

    ticker = sys.argv[1]
    field = sys.argv[2]

    print(get__dataFinancial(ticker, field))