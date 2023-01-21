from collections import defaultdict
from googletrans import Translator

files = 'upload/data.txt'


def get_tables_and_columns(data) -> defaultdict:
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
    current_structure_data = get_tables_and_columns(files)
    translator = Translator()

    for table, columns in current_structure_data.items():
        columns = [translator.translate(txt, dest='en').text for txt in columns]
        current_structure_data[table] = columns

    return current_structure_data


