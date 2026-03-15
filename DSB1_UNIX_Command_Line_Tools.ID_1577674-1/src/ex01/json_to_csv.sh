#!/bin/sh
# запуск из ex01
# Создаем файл с заголовком
echo '"id","created_at","name","has_test","alternate_url"' > hh.csv

# Добавляем данные
jq -r -f filter.jq ../ex00/hh.json >> hh.csv