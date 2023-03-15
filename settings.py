# flake8: noqa
input_file = "upload/data.txt"
output_dir = "download/xml"
header1 = """<?xml version="1.0" encoding="UTF-8"?>\n<databaseChangeLog
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.9.xsd">
    <changeSet id="alter table"""
header2 = 'author="Irkhin-VB" dbms="oracle">\n<sql>'
# tmp = '2*NVfLB$#*1bFAWc9H1oCIW2j'
rollback_start = "</sql>\n<rollback>\n\t<sql>\n"
rollback_end = "\n</sql>\n</rollback>\n</changeSet>\n</databaseChangeLog>"
fixed_words_in_translation = {
    "ЦУЗ": "CUZ",
    "Тип объекта": "Tip object",
    "Вид объекта": "Vid object",
    "НПЦ1Торг": "NPC1Torg",
}
