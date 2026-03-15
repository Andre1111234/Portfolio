#!/bin/sh

VACANCY_NAME="data+scientist"
URL="https://api.hh.ru/vacancies?text=$VACANCY_NAME&per_page=20"

curl -s -H "User-Agent: api-test-agent" "$URL" | jq '.' > hh.json