#!/bin/sh

# Читаем файл из Exercise 03
input_file="../ex03/hh_positions.csv"

# Извлекаем уникальные даты (без времени и кавычек) из колонки created_at
dates=$(tail -n +2 "$input_file" | cut -d',' -f2 | cut -d'T' -f1 | tr -d '"' | sort -u)

# Сохраняем заголовок
header=$(head -1 "$input_file")

# Для каждой уникальной даты создаем отдельный файл
for date in $dates; do
    # Создаем файл с именем даты (без кавычек)
    filename="${date}.csv"
    
    # Записываем заголовок
    echo "$header" > "$filename"
    
    # Добавляем строки с этой датой (ищем дату в кавычках)
    grep "\"${date}T" "$input_file" >> "$filename"
    
    echo "Created: $filename"
done