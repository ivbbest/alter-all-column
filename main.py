from collections import defaultdict
import itertools
from googletrans import Translator
from config import header, footer, input_file, output_dir
from pprint import pprint
from datetime import datetime


def get_tables_and_columns(data) -> defaultdict:
    """
    Получаем из файла структуру по принципу:
    Таблица : Список колонок (на русском или текущем языке)

    :return defaultdict(list)
    """
    hash_tables = defaultdict(list)

    with open(data, 'r', encoding='UTF-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('*'):
                table = line.split('*')[1]
            elif line == '':
                continue
            else:
                hash_tables[table].append(line)

    return hash_tables


# TODO: Исключить выбор колонок с английским текстом. Если колонка на английском тексте, то не переводить ее еще раз
def translate_columns() -> defaultdict:
    """
    Перевод колонок и на выходе получаем структуру:
    Таблица: список колонок на английском языке

    :return: defaultdict(list)
    """
    current_structure_data = get_tables_and_columns(input_file)
    translator = Translator()

    for table, columns in current_structure_data.items():
        columns = [translator.translate(txt, dest='en').text for txt in columns]
        current_structure_data[table] = columns

    return current_structure_data


def merged_columns_for_tables(*tables):
    """Объединение по таблицам колонок с текущим названием и переведенным"""

    merged_elements = defaultdict(list)

    for common_table in tables:
        for key, value in common_table.items():
            merged_elements[key].append(tuple(value))

    return merged_elements


# TODO: исправить на DRY c предыдущей функцией get_comment_for_column()
def get_alter_and_comment_data():
    """
    Получаем готовые строки с alter и comment для xml файла
    """
    current_name_columns = get_tables_and_columns(input_file)
    translate_name_columns = translate_columns()

    tables_and_columns = merged_columns_for_tables(current_name_columns, translate_name_columns)
    tables = tables_and_columns.keys()

    alter_data = defaultdict(list)
    comment_data = defaultdict(list)

    for table in tables:
        old_name_columns, new_name_columns = tables_and_columns[table]
        for old, new in zip(old_name_columns, new_name_columns):
            alter = f'ALTER TABLE {table} RENAME COLUMN "{old}" to {new};'
            comment = f'comment on column {table}.{old} is "{new}";'
            alter_data[table].append(alter)
            comment_data[table].append(comment)

    return alter_data, comment_data


def create_xml_file():
    """Создание xml файла"""
    alter_columns_text, comment_columns_text = get_alter_and_comment_data()
    merged_dataset = merged_columns_for_tables(alter_columns_text, comment_columns_text)
    i = 1
    tables = merged_dataset.keys()

    for table in tables:
        alter_rows, comment_rows = merged_dataset[table]
        name_file = f"{datetime.now().strftime('%Y-%m-%d')}-{i}-alter_table_{table}.xml"
        alter = '\n'.join(alter_rows)
        comment = '\n'.join(comment_rows)
        with open(f'{output_dir}/{name_file}', 'w', encoding='UTF-8') as f:
            info = f'{header}\n{alter}\ncommit;\n\n{comment}\ncommit;\n\n{footer}'
            f.write(info)

        i += 1


create_xml_file()
