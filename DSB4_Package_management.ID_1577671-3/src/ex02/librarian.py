#!/usr/bin/env python3

import sys
import os
import subprocess

# Проверяем корректную виртуальную среду
venv = os.getenv("VIRTUAL_ENV")
if not venv or "wasabiel" not in venv:
    raise EnvironmentError("Wrong virtual environment")

# Создаём requirements.txt с нужными пакетами
with open("requirements.txt", "w") as file:
    file.write("beautifulsoup4\n")
    file.write("pytest\n")
    file.close()
    
subprocess.run(
    [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
    check=True
)

result = subprocess.run(
    [sys.executable, "-m", "pip", "freeze"],
    stdout=subprocess.PIPE,
    text=True,
    check=True
)

print(result.stdout)

# Перезаписываем requirements.txt установленными версиями
with open("requirements.txt", "w") as file:
    file.write(result.stdout)
    file.close()