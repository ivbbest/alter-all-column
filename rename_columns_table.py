# flake8: noqa
import re
import time
from collections import defaultdict
from datetime import datetime
from string import ascii_letters

from deep_translator import GoogleTranslator
from googletrans import Translator

from settings import (
    fixed_words_in_translation,
    header1,
    header2,
    input_file,
    output_dir,
    rollback_end,
    rollback_start,
)

translator = Translator()


def get_tables_and_columns(file) -> dict:
    """
    Получаем из файла структуру по принципу:
    Таблица : Список колонок (на русском или текущем языке)

    :return defaultdict(list)
    """
    hash_tables = defaultdict(list)

    with open(file, encoding="UTF-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("*"):
                table = line.split("*")[1]
            elif line == "":
                continue
            else:
                hash_tables[table].append(line)

    return hash_tables


def is_english_word(word: str) -> bool:
    """Проверка столбец на английском назван или нет"""
    return len(set(ascii_letters) & set(word)) > 0


def translated_word(text: str | list[str]) -> str | list[str] | None:
    """Перевод отдельного текста или слова"""
    try:
        translate_txt = fixed_words_in_translation.get(
            text, GoogleTranslator(source="ru", target="en").translate(text=text)
        )
        return re.sub(r"\s", "_", translate_txt)
    except ConnectionError:
        pass


# TODO: Исключить выбор колонок с английским текстом.
#  Если колонка на английском тексте,
#  то не переводить его еще раз
# TODO: Создать словарь для кэширования данных по переводу.
#  Если слово уже есть в словаре,
#  то дополнительно не нужно его переводить, а брать данные из словаря
def translated_all_columns(tables_and_columns) -> dict:
    """
    Перевод колонок и на выходе получаем структуру:
    Таблица: список колонок на английском языке

    :return: defaultdict(list)
    """
    translated_data = defaultdict(list)

    for table, columns in tables_and_columns.items():
        columns = list(map(translated_word, columns))

        translated_data[table] = columns

    return translated_data


def merged_columns_for_tables(*tables) -> dict:
    """Объединение по таблицам колонок с текущим названием и переведенным"""

    merged_elements = defaultdict(list)
    for common_table in tables:
        for key, value in common_table.items():
            merged_elements[key].append(tuple(value))

    return merged_elements


# TODO: исправить на DRY c предыдущей функцией create_xml_file()
#  в части обработки двух списков/кортежей.
#  Начиная с for table in tables: и до формирования конкретных данных
def get_alter_and_comment_data(file):
    """
    Получаем готовые строки с alter и comment для
    xml файла из входящего текстового файла
    """
    current_name_columns = get_tables_and_columns(file)
    translate_name_columns = translated_all_columns(current_name_columns)

    tables_and_columns = merged_columns_for_tables(
        current_name_columns, translate_name_columns
    )
    tables = tables_and_columns.keys()

    alter_data = defaultdict(list)
    comment_data = defaultdict(list)
    rollback_data = defaultdict(list)

    for table in tables:
        old_name_columns, new_name_columns = tables_and_columns[table]
        for old, new in zip(old_name_columns, new_name_columns):
            alter = f'ALTER TABLE {table} RENAME COLUMN "{old}" to {new};'
            comment = f'comment on column {table}.{new} is "{old}";'
            rollback = f'ALTER TABLE {table} RENAME COLUMN "{new}" to "{old}";'
            alter_data[table].append(alter)
            comment_data[table].append(comment)
            rollback_data[table].append(rollback)

    return alter_data, comment_data, rollback_data


# TODO: исправить на DRY c предыдущей функцией
#  get_alter_and_comment_data() в части обработки двух списков/кортежей.
#  Начиная с for table in tables: и до формирования конкретных данных
def create_xml_file(file) -> None:
    """Создание xml файла на основе текстового файла с входящими данными"""
    (
        alter_columns_text,
        comment_columns_text,
        rollback_columns_text,
    ) = get_alter_and_comment_data(file)
    merged_dataset = merged_columns_for_tables(
        alter_columns_text, comment_columns_text, rollback_columns_text
    )
    tables = merged_dataset.keys()

    i = 1

    for table in tables:
        alter_rows, comment_rows, rollback_rows = merged_dataset[table]
        name_file = f"""{datetime.now().strftime('%Y-%m-%d')}-{i}-alter_table_{table}.xml"""  # noqa: E501
        alter = "\n".join(alter_rows)
        comment = "\n".join(comment_rows)
        rollback = "\n".join(rollback_rows)
        with open(f"{output_dir}/{name_file}", "w", encoding="UTF-8") as f:
            info = f"""{header1} {table}" {header2}\n{alter}\ncommit;
                        \n\n{comment}\ncommit;
                        \n{rollback_start}{rollback}{rollback_end}"""
            f.write(info)

        i += 1


def main():
    t_start = time.perf_counter()
    create_xml_file(input_file)
    print(f"Время выполнения скрипта = {time.perf_counter() - t_start}")


if __name__ == "__main__":
    main()
