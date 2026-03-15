#!/bin/sh

# Копируем первую строку с заголовками
head -1 ../ex02/hh_sorted.csv > hh_positions.csv

# Читаем файл построчно, начиная со второй строки
tail -n +2 ../ex02/hh_sorted.csv | while IFS= read -r line; do
    # Извлекаем части строки с учетом CSV формата
    id=$(echo "$line" | cut -d',' -f1)
    created_at=$(echo "$line" | cut -d',' -f2)
    name=$(echo "$line" | cut -d',' -f3- | cut -d',' -f1)  # Берем все до следующей запятой
    has_test=$(echo "$line" | rev | cut -d',' -f2 | rev)   # Предпоследнее поле
    alternate_url=$(echo "$line" | rev | cut -d',' -f1 | rev)  # Последнее поле
    
    # Проверяем, есть ли в названии "Junior"
    if echo "$name" | grep -q -i "Junior"; then
        level="Junior"
    # Проверяем, есть ли в названии "Middle"  
    elif echo "$name" | grep -q -i "Middle"; then
        level="Middle"
    # Проверяем, есть ли в названии "Senior"
    elif echo "$name" | grep -q -i "Senior"; then
        level="Senior"
    # Если ничего не нашли, ставим "-"
    else
        level="-"
    fi
    
    # Собираем новую строку с уровнем вместо названия
    new_line="$id,$created_at,\"$level\",$has_test,$alternate_url"
    
    # Добавляем строку в файл
    echo "$new_line" >> hh_positions.csv
done