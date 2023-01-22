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


def merged_translations_columns():
    """Объединение по таблицам колонок с текущим названием и переведенным"""
    current_name_columns = get_tables_and_columns(input_file)
    translate_name_columns = translate_columns()
    merged_elements = defaultdict(list)

    for common_table in (current_name_columns, translate_name_columns):
        for key, value in common_table.items():
            merged_elements[key].append(tuple(value))

    return merged_elements


# TODO: исправить на DRY c предыдущей функцией get_comment_for_column()
def get_alter_and_comment_data():
    """
    Получаем готовые строки с alter и comment для xml файла
    """
    tables_and_columns = merged_translations_columns()
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


# TODO: исправить на DRY c предыдущей функцией get_data_alter_name_columns()
# TODO: неправильно добавляется связка новый - старый комментарий. Неверный порядок вписывается.
def get_comment_for_column():
    """
    Получаем комментарии на русском языке для каждого столбца
    :return:
    """
    old_name_structure = get_tables_and_columns(input_file)
    new_name_structure = translate_columns()
    comment_name_data = defaultdict(list)
    breakpoint()

    for table1, column1 in old_name_structure.items():
        for table2, column2 in new_name_structure.items():
            list_all_columns = list(zip(column1, column2))
            for elem in list_all_columns:
                old, new = elem
                data = f'comment on column {table1}.{new} is "{old}";'
                comment_name_data[table1].append(data)

    return comment_name_data


# TODO: некорректно добавляется информация. 3 раза создается один и тот же файл, а также 3 раза добавляется разделы alter и comments
# def create_xml_file():
#     alter_columns_text = get_data_alter_name_columns()
#     comment_columns_text = get_comment_for_column()
#     i = 1
#
#     for table1, column1 in alter_columns_text.items():
#         for table2, column2 in comment_columns_text.items():
#             name_file = f"{datetime.now()}-{i}-alter_table_{table2}.xml"
#             alter = '\n'.join(column1)
#             comment = '\n'.join(column2)
#             with open(f'{output_dir}/{name_file}', 'w', encoding='UTF-8') as f:
#                 info = f'{header}\n{alter}\ncommit;\n{comment}\ncommit;\n{footer}'
#                 f.write(info)
#
#             i += 1


# create_xml_file()
pprint(get_alter_and_comment_data())
