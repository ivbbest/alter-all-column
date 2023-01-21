from collections import defaultdict
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


# TODO: исправить на DRY c предыдущей функцией get_comment_for_column()
def get_data_alter_name_columns():
    """
    Мэппинг Alter column для текущего текста колонок и колонок на английском.
    Содержимое в дальнейшем используется для создания итогового xml файла.

    :in1: Таблица : Список колонок (на русском или текущем языке)
    :in2:  Таблица: список колонок на английском языке
    :return: defaultdict(list)
    """
    old_name_structure = get_tables_and_columns(input_file)
    new_name_structure = translate_columns()
    alter_name_data = defaultdict(list)

    for table1, column1 in old_name_structure.items():
        for table2, column2 in new_name_structure.items():
            list_all_columns = list(zip(column1, column2))
            for elem in list_all_columns:
                old, new = elem
                data = f'ALTER TABLE {table1} RENAME COLUMN "{old}" to {new};'
                alter_name_data[table1].append(data)

    return alter_name_data


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

    for table1, column1 in old_name_structure.items():
        for table2, column2 in new_name_structure.items():
            list_all_columns = list(zip(column1, column2))
            for elem in list_all_columns:
                old, new = elem
                data = f'comment on column {table1}.{new} is "{old}";'
                comment_name_data[table1].append(data)

    return comment_name_data


# TODO: некорректно добавляется информация. 3 раза создается один и тот же файл, а также 3 раза добавляется разделы alter и comments
def create_xml_file():
    alter_columns_text = get_data_alter_name_columns()
    comment_columns_text = get_comment_for_column()
    i = 1

    for table1, column1 in alter_columns_text.items():
        for table2, column2 in comment_columns_text.items():
            name_file = f"{datetime.now()}-{i}-alter_table_{table2}.xml"
            alter = '\n'.join(column1)
            comment = '\n'.join(column2)
            with open(f'{output_dir}/{name_file}', 'w', encoding='UTF-8') as f:
                info = f'{header}\n{alter}\ncommit;\n{comment}\ncommit;\n{footer}'
                f.write(info)

            i += 1


create_xml_file()
