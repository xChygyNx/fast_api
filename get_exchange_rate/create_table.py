import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_currency_table(cursor):
    cursor.execute('SELECT * FROM information_schema.tables WHERE table_name=\'currency_table\'')
    if not bool(cursor.rowcount):
        query = 'CREATE TABLE currency_table ' \
                '(ID serial PRIMARY KEY NOT NULL, ' \
                'CHAR_CODE TEXT NOT NULL, ' \
                'VALUE REAL NOT NULL, ' \
                'DATE TEXT NOT NULL);'
        cursor.execute(query)


if __name__ == '__main__':
    with psycopg2.connect(user="admin", password="very_difficult_password",
                        host="postgres", port="5432", database="exchange_db") as connection:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with connection.cursor() as cursor:
            create_currency_table(cursor)
