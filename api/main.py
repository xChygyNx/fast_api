from typing import Optional
from datetime import datetime

from fastapi import FastAPI
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

app = FastAPI()
CURRENCIES = {'AUD', 'AZN', 'GBP', 'AMD', 'BYN', 'BGN', 'BRL', 'HUF', 'HKD',
              'DKK', 'USD', 'EUR', 'INR', 'KZT', 'CAD', 'KGS', 'CNY', 'MDL',
              'NOK', 'PLN', 'RON', 'XDR', 'SGD', 'TJS', 'TRY', 'TMT', 'UZS',
              'UAH', 'CZK', 'SEK', 'CHF', 'ZAR', 'KRW', 'JPY'}

@app.get("/rate")
async def get_rate():
    today = datetime.today().strftime('%d.%m.%Y')
    with psycopg2.connect(user="admin", password="very_difficult_password",
                          host="postgres", port="5432", database="exchange_db") as connection:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT CHAR_CODE, VALUE, DATE "
                           f"FROM currency_table "
                           f"WHERE DATE='{today}'")
            result = []
            for rec in cursor:
                result.append({'Currency': rec[0], 'Rate': rec[1], 'Date': rec[2]})
    return result


@app.get("/rate/{char_code}")
async def get_definite_rate(char_code: str, date: Optional[str] = None):
    if char_code.upper() not in CURRENCIES:
        return 'ERROR: Send currency char code is unknown'
    if date is None:
        date = datetime.today().strftime('%d.%m.%Y')
    try:
        datetime.strptime(date, '%d.%m.%Y')
    except ValueError:
        return "Send invalid date"
    with psycopg2.connect(user="admin", password="very_difficult_password",
                        host="postgres", port="5432", database="exchange_db") as connection:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT CHAR_CODE, VALUE, DATE "
                           f"FROM currency_table "
                           f"WHERE CHAR_CODE='{char_code.upper()}' AND DATE='{date}'")
            if not bool(cursor.rowcount):
                return "Absence need information"
            else:
                rec = cursor.fetchone()
                return {'Currency': rec[0],
                        'Rate': rec[1],
                        'Date': rec[2]}
