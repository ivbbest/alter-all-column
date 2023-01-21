from collections import defaultdict
from googletrans import Translator
from config import header, footer, files
from pprint import pprint


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


def translate_columns() -> defaultdict:
    """
    Перевод колонок и на выходе получаем структуру:
    Таблица: список колонок на английском языке

    :return: defaultdict(list)
    """
    current_structure_data = get_tables_and_columns(files)
    translator = Translator()

    for table, columns in current_structure_data.items():
        columns = [translator.translate(txt, dest='en').text for txt in columns]
        current_structure_data[table] = columns

    return current_structure_data


def get_data_alter_name_columns():
    """
    Мэппинг Alter column для текущего текста колонок и колонок на английском.
    Содержимое в дальнейшем используется для создания итогового xml файла.

    :in1: Таблица : Список колонок (на русском или текущем языке)
    :in2:  Таблица: список колонок на английском языке
    :return: defaultdict(list)
    """
    old_name_structure = get_tables_and_columns(files)
    new_name_structure = translate_columns()
    alter_name_data = defaultdict(list)

    for table1, column1 in old_name_structure.items():
        for table2, column2 in new_name_structure.items():
            list_all_columns = list(zip(column1, column2))
            for elem in list_all_columns:
                old, new = elem
                data = f'ALTER TABLE {table1} RENAME COLUMN "{old}" to {new}'
                alter_name_data[table1].append(data)

    return alter_name_data


pprint(get_data_alter_name_columns())
