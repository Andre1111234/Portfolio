#!/bin/sh

# Результирующий файл
output_file="concatenated.csv"

# Находим все CSV файлы с датами в имени (правильный паттерн)
csv_files=$(ls -1 *.csv 2>/dev/null | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}\.csv$' | sort)

if [ -z "$csv_files" ]; then
    echo "No date CSV files found. Run partitioner.sh first."
    echo "Available files:"
    ls -la *.csv
    exit 1
fi

# Берем заголовок из первого файла
head -1 $(echo "$csv_files" | head -1) > "$output_file"

# Объединяем данные из всех файлов (без заголовков)
for file in $csv_files; do
    tail -n +2 "$file" >> "$output_file"
done

echo "Concatenated all files into: $output_file"
echo "Total lines in result: $(wc -l < "$output_file")"