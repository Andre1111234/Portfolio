import pandas as pd
import re


INPUT_FILE = "Выгрузка данных.xlsx"
OUTPUT_FILE = "output_split1.xlsx"


def normalize_text(text):
    text = str(text)
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_article(text):

    match = re.search(
        r'част\w*\s*(\d+)\s*стат\w*\s*([\d\.]+)',
        text,
        re.IGNORECASE
    )

    if match:
        return f"ч.{match.group(1)} ст.{match.group(2)} КоАП РФ"

    match = re.search(
        r'стат\w*\s*([\d\.]+)',
        text,
        re.IGNORECASE
    )

    if match:
        return f"ст.{match.group(1)} КоАП РФ"

    return ""


def extract_fine(text):

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

    match = re.search(
        r'вступил\w*\s*в\s*законную\s*силу\s*(\d{2}\.\d{2}\.\d{4})',
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return ""


df = pd.read_excel(INPUT_FILE)

rows = []

for _, row in df.iterrows():

    base_number = row.get("Номер", "")
    base_date = row.get("Дата", "")
    subject = row.get("Субъект", "")

    text = normalize_text(row.get("Описание", ""))

    # ищем все завершённые блоки
    cases = re.findall(
        r'(.*?вступил\w*\s*в\s*законную\s*силу\s*\d{2}\.\d{2}\.\d{4}\.)',
        text,
        re.IGNORECASE
    )

    for case in cases:

        article = extract_article(case)
        fine = extract_fine(case)
        effective = extract_effective_date(case)

        rows.append({
            "Номер": base_number,
            "Дата постановления": base_date,
            "Субъект": subject,
            "Статья КоАП": article,
            "Штраф": fine,
            "Дата вступления": effective
        })


new_df = pd.DataFrame(rows)

new_df.to_excel(OUTPUT_FILE, index=False)

print("Готово:", OUTPUT_FILE)