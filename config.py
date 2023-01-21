files = 'upload/data.txt'
# alter_txt = 'ALTER TABLE {table_name} RENAME COLUMN {old_name_column} to {new_name_column}'
header = '''<?xml version="1.0" encoding="UTF-8"?>

<databaseChangeLog

        xmlns="http://www.liquibase.org/xml/ns/dbchangelog"

        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

        xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.9.xsd">

    <changeSet id="alter table {table_name}" author="Irkhin-VB" dbms="oracle">

        <sql>
'''

footer = '''</sql>

                                               </changeSet>

                                               </databaseChangeLog>

                               '''