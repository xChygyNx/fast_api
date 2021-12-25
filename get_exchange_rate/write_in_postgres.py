import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from typing import OrderedDict, List
import os
from dotenv import load_dotenv, find_dotenv
from psycopg2.extras import execute_values

load_dotenv(find_dotenv())


def insert_records_in_table(records: List[OrderedDict], cursor, today: str):
    """
    Функция из списка передаваемых записей находит те, которых нет в таблице, собирает
    из них список кортежей значений полей, и с помощью psycopg2.extras.execute_values
    разом заносит их в таблицу

    :param
    :record - данные, которые необходимо внести в таблицу
    :cursor - psycopg2 курсор, необходимый для выполнения действий с БД exchange_rate
    :today - дата, к которой относятся передаваемые записи
    """
    result = []
    for record in records:
        cursor.execute(f'SELECT * FROM {os.environ["CURRENCY_TAB"]} '
                       f'WHERE CHAR_CODE=\'{record["CharCode"]}\' AND DATE=\'{today}\'')
        if not bool(cursor.rowcount):
            result.append((record['CharCode'], record['Name'], record['Nominal'],
                           record['Value'].replace(',', '.'), today))
    execute_values(cursor, f'INSERT INTO {os.environ["CURRENCY_TAB"]} '
                           f'(CHAR_CODE, NAME, COUNT, VALUE, DATE) VALUES %s', result)


def write_rate(valutes: List[OrderedDict], today: str):
    """
    Функция создает соединение и курсор для внесения переданных записей в таблицу БД
    передает их вместе с записями функции которая уже непосредственно вносит записи в PostgreSQL

    :param valutes: - записи, которые необходимо внести
    :param today: - дата, к которой относятся передаваемые записи
    :return:
    """
    with psycopg2.connect(user=os.environ["POSTGRES_USER"], password=os.environ["POSTGRES_PASSWORD"],
                          host=os.environ["POSTGRES_HOST"], port=os.environ["POSTGRES_PORT"],
                          database=os.environ["POSTGRES_DB"]) as connection:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with connection.cursor() as cursor:
            insert_records_in_table(valutes, cursor, today)
