from collections import defaultdict
from googletrans import Translator
from settings import header1, header2, footer, input_file, output_dir
from pprint import pprint
from datetime import datetime

translator = Translator()


def get_tables_and_columns(file) -> dict:
    """
    Получаем из файла структуру по принципу:
    Таблица : Список колонок (на русском или текущем языке)

    :return defaultdict(list)
    """
    hash_tables = defaultdict(list)

    with open(file, 'r', encoding='UTF-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('*'):
                table = line.split('*')[1]
            elif line == '':
                continue
            else:
                hash_tables[table].append(line)

    return hash_tables


# TODO: подумать над реализацией популярного сервиса deepl для перевода https://github.com/DeepLcom/deepl-python
def translated_word(text: str | list[str]) -> str | list[str]:
    """Перевод отдельного текста или слова"""
    return translator.translate(text, dest='en').text


# TODO: Исключить выбор колонок с английским текстом. Если колонка на английском тексте,
#  то не переводить его еще раз
# TODO: Создать словарь для кэширования данных по переводу. Если слово уже есть в словаре,
#  то дополнительно не нужно его переводить, а брать данные из словаря
def translated_all_columns(file) -> dict:
    """
    Перевод колонок и на выходе получаем структуру:
    Таблица: список колонок на английском языке

    :return: defaultdict(list)
    """

    current_structure_data = get_tables_and_columns(file)

    for table, columns in current_structure_data.items():
        columns = list(map(translated_word, columns))

        # подумать как исправить код, чтобы работала мнемизация
        # columns = list(
        #     map(lambda txt, dictionary_words={'ТБ': 'TB'}: dictionary_words.setdefault(txt, translated_word(txt)),
        #         columns))

        current_structure_data[table] = columns

    return current_structure_data


def merged_columns_for_tables(*tables) -> dict:
    """Объединение по таблицам колонок с текущим названием и переведенным"""

    merged_elements = defaultdict(list)

    for common_table in tables:
        for key, value in common_table.items():
            merged_elements[key].append(tuple(value))

    return merged_elements


# TODO: исправить на DRY c предыдущей функцией create_xml_file() в части обработки двух списков/кортежей.
#  Начиная с for table in tables: и до формирования конкретных данных
def get_alter_and_comment_data(file):
    """
    Получаем готовые строки с alter и comment для xml файла из входящего текстового файла
    """
    current_name_columns = get_tables_and_columns(file)
    translate_name_columns = translated_all_columns(file)

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


# TODO: исправить на DRY c предыдущей функцией get_alter_and_comment_data() в части обработки двух списков/кортежей.
#  Начиная с for table in tables: и до формирования конкретных данных
def create_xml_file(file) -> None:
    """Создание xml файла на основе текстового файла с входящими данными"""
    alter_columns_text, comment_columns_text = get_alter_and_comment_data(file)
    merged_dataset = merged_columns_for_tables(alter_columns_text, comment_columns_text)
    tables = merged_dataset.keys()

    i = 1

    for table in tables:
        alter_rows, comment_rows = merged_dataset[table]
        name_file = f"{datetime.now().strftime('%Y-%m-%d')}-{i}-alter_table_{table}.xml"
        alter = '\n'.join(alter_rows)
        comment = '\n'.join(comment_rows)
        with open(f'{output_dir}/{name_file}', 'w', encoding='UTF-8') as f:
            info = f'{header1} {table}\" {header2}\n{alter}\ncommit;\n\n{comment}\ncommit;\n\n{footer}'
            f.write(info)

        i += 1


if __name__ == "__main__":
    create_xml_file(input_file)
