# Автоматическая конвертация столбцов таблиц с русского на английский язык и создания файлов миграций под liquibase

1) На вход файл с таблицами и столбцами:

- settings.py -> input_file

2) На выходе папка с файлами миграций под liquibase:

- settings.py -> output_dir

3) Заполнить settings.py, кроме input_file, output_dir:

- header1, header2 - для хедера под liquibase.
- rollback_start и rollback_end - для футера под liquibase, если что-то пошло не так



## Запуск скрипта

1) Склонируйте репозиторий `git clone https://github.com/ivbbest/alter-all-column` в текущую папку.


2) Переходим в папку с проектом.

    `cd alter-all-column`


3) Установка всех зависимостей из requirements.txt:

    `python3 -m pip install -r requirements.txt`

4) Если хотим запустить основной скрипт:

- Linux:

    `python3 rename_columns_table.py`


- Windows:

    `python rename_columns_table.py`

5) Получаем xml файлы под миграции liquibase. Например:

    `output_dir = "download/xml"`
