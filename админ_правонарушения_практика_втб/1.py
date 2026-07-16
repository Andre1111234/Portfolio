import pandas as pd
import re


INPUT_FILE ="Выгрузка данных.xlsx"
OUTPUT_FILE = "output_parsed.xlsx"


def normalize_text(text):
    text = str(text)
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_article(text):

    text = normalize_text(text)

    # часть + статья (универсально)
    match = re.search(
        r'част\w*\s*(\d+)\s*стат\w*\s*([\d\.]+)',
        text,
        re.IGNORECASE
    )

    if match:
        return f"ч.{match.group(1)} ст.{match.group(2)} КоАП РФ"

    # только статья
    match = re.search(
        r'стат\w*\s*([\d\.]+)',
        text,
        re.IGNORECASE
    )

    if match:
        return f"ст.{match.group(1)} КоАП РФ"

    return ""


def extract_fine(text):

    text = normalize_text(text)

    if re.search(r'предупрежден\w*', text, re.IGNORECASE):
        return "предупреждение"

    match = re.search(
        r'штраф\w*\s*в\s*размере\s*([\d\s]+)',
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).replace(" ", "")

    return ""


def extract_effective_date(text):

    text = normalize_text(text)

    match = re.search(
        r'вступил\w*\s*в\s*законную\s*силу\s*(\d{2}\.\d{2}\.\d{4})',
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return ""


df = pd.read_excel(INPUT_FILE)

df["Описание"] = df["Описание"].astype(str)

df["Статья КоАП"] = df["Описание"].apply(extract_article)
df["Штраф"] = df["Описание"].apply(extract_fine)
df["Дата вступления"] = df["Описание"].apply(extract_effective_date)

df.to_excel(OUTPUT_FILE, index=False)

print("Готово:", OUTPUT_FILE)