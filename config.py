input_file = 'upload/data.txt'
output_dir = 'upload/xml'
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