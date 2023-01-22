input_file = 'upload/data.txt'
output_dir = 'upload/xml'
header1 = '''<?xml version="1.0" encoding="UTF-8"?>\n<databaseChangeLog\n
        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"\n
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n
        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.9.xsd">\n
    <changeSet id="alter table'''
header2 = 'author="Irkhin-VB" dbms="oracle">\n<sql>'

footer = '</sql>\n</changeSet>\n</databaseChangeLog>'
