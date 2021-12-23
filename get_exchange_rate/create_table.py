import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv, find_dotenv
from get_rate import request_cbr

load_dotenv(find_dotenv())


def create_currency_table(cursor):
    cursor.execute(f'SELECT * FROM information_schema.tables WHERE table_name=\'{os.environ["CURRENCY_TAB"]}\'')
    if not bool(cursor.rowcount):
        query = f'CREATE TABLE {os.environ["CURRENCY_TAB"]} ' \
                f'(ID serial PRIMARY KEY NOT NULL, ' \
                f'CHAR_CODE TEXT NOT NULL, ' \
                f'COUNT TEXT NOT NULL, ' \
                f'VALUE REAL NOT NULL, ' \
                f'DATE TEXT NOT NULL);'
        cursor.execute(query)


if __name__ == '__main__':
    with psycopg2.connect(user=os.environ["POSTGRES_USER"], password=os.environ["POSTGRES_PASSWORD"],
                          host=os.environ["POSTGRES_HOST"], port=os.environ["POSTGRES_PORT"],
                          database=os.environ["POSTGRES_DB"]) as connection:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with connection.cursor() as cursor:
            create_currency_table(cursor)
    request_cbr()
