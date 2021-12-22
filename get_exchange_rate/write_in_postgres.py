import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from typing import OrderedDict


def insert_record_in_table(record: OrderedDict, cursor, today: str):
    cursor.execute(f'SELECT * FROM currency_table WHERE CHAR_CODE=\'{record["CharCode"]}\' AND DATE=\'{today}\'')
    if not bool(cursor.rowcount):
        insert_query = f'INSERT INTO currency_table (CHAR_CODE, VALUE, DATE) ' \
                       f'VALUES (\'{record["CharCode"]}\', {record["Value"].replace(",", ".")}, \'{today}\')'
        cursor.execute(insert_query)


def write_rate(valutes: OrderedDict, today: str):
    # Подключение к существующей базе данных
    with psycopg2.connect(user="admin", password="very_difficult_password",
                        host="postgres", port="5432", database="exchange_db") as connection:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with connection.cursor() as cursor:
            for record in valutes:
                insert_record_in_table(record, cursor, today)
