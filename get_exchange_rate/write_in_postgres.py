import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from typing import OrderedDict
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def insert_record_in_table(record: OrderedDict, cursor, today: str):
    cursor.execute(f'SELECT * FROM {os.environ["CURRENCY_TABLE"]} WHERE CHAR_CODE=\'{record["CharCode"]}\' AND DATE=\'{today}\'')
    if not bool(cursor.rowcount):
        insert_query = f'INSERT INTO {os.environ["CURRENCY_TABLE"]} (CHAR_CODE, VALUE, DATE) ' \
                       f'VALUES (\'{record["CharCode"]}\', {record["Value"].replace(",", ".")}, \'{today}\')'
        cursor.execute(insert_query)


def write_rate(valutes: OrderedDict, today: str):
    # Подключение к существующей базе данных
    with psycopg2.connect(user=os.environ["POSTGRES_USER"], password=os.environ["POSTGRES_PASSWORD"],
                          host=os.environ["POSTGRES_HOST"], port=os.environ["POSTGRES_PORT"],
                          database=os.environ["POSTGRES_DB"]) as connection:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with connection.cursor() as cursor:
            for record in valutes:
                insert_record_in_table(record, cursor, today)
