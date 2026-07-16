import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


URL = "https://cbr.ru/rbr/adm_proc/"

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0"
}


all_data = []
last_max = 0


for page in range(1, 100):

    print("Page:", page)

    data = {

        "UniDbQuery.Posted": "True",

        "UniDbQuery.From": "01.01.2025",

        "UniDbQuery.To": "31.12.2026",

        "UniDbQuery.PageIndex": str(page)

    }

    response = session.post(URL, headers=headers, data=data)

    soup = BeautifulSoup(response.text, "html.parser")

    records = soup.find_all("div", class_="cross-result")

    if not records:
        break


    numbers = []

    for record in records:

        num = record.find("span", class_="number")
        date = record.find("span", class_="date")
        title = record.find("div", class_="title")
        subtitle = record.find("div", class_="subtitle")

        number = int(num.text.strip())

        numbers.append(number)

        all_data.append({

            "Номер": number,
            "Дата": date.text.strip(),
            "Субъект": title.text.strip(),
            "Описание": subtitle.text.strip()

        })


    max_num = max(numbers)

    print("Max:", max_num)

    if max_num <= last_max:
        break

    last_max = max_num

    time.sleep(0.2)


print("Total:", len(all_data))


df = pd.DataFrame(all_data)

df.drop_duplicates(subset=["Номер"], inplace=True)

df.to_excel("cbr_437_full.xlsx", index=False)

print("Done")