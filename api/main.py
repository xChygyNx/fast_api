from typing import Optional
from datetime import datetime
from fastapi import FastAPI
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
app = FastAPI()
CURRENCIES = {'AUD', 'AZN', 'GBP', 'AMD', 'BYN', 'BGN', 'BRL', 'HUF', 'HKD',
              'DKK', 'USD', 'EUR', 'INR', 'KZT', 'CAD', 'KGS', 'CNY', 'MDL',
              'NOK', 'PLN', 'RON', 'XDR', 'SGD', 'TJS', 'TRY', 'TMT', 'UZS',
              'UAH', 'CZK', 'SEK', 'CHF', 'ZAR', 'KRW', 'JPY'}

@app.get("/rate")
async def get_rate():
    """
    Возвращает полный список курсов валют на сегодняшнее число

    :return:
    """
    today = datetime.today().strftime('%d.%m.%Y')
    with psycopg2.connect(user=os.environ["POSTGRES_USER"], password=os.environ["POSTGRES_PASSWORD"],
                          host=os.environ["POSTGRES_HOST"], port=os.environ["POSTGRES_PORT"],
                          database=os.environ["POSTGRES_DB"]) as connection:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT CHAR_CODE, NAME, VALUE, COUNT, DATE "
                           f"FROM {os.environ['CURRENCY_TAB']} "
                           f"WHERE DATE='{today}'")
            result = []
            for rec in cursor:
                result.append({'Code': rec[0], 'Currency': rec[1], 'Rate': rec[2], 'Count': rec[3], 'Date': rec[4]})
    return result


@app.get("/rate/{char_code}")
async def get_definite_rate(char_code: str, date: Optional[str] = None):
    """
    Возвращает курс валюты, имеющий заданный тикер и на заданную дату (по умолчпнию
    на сегодняшнее число)

    :param char_code: - тикер валюты
    :param date: - интересующая дата в формате '%dd.%mm.%yyyy'
    :return:
    """
    if char_code.upper() not in CURRENCIES:
        return 'ERROR: Send currency char code is unknown'
    if date is None:
        date = datetime.today().strftime('%d.%m.%Y')
    try:
        datetime.strptime(date, '%d.%m.%Y')
    except ValueError:
        return "Send invalid date"
    with psycopg2.connect(user=os.environ["POSTGRES_USER"], password=os.environ["POSTGRES_PASSWORD"],
                          host=os.environ["POSTGRES_HOST"], port=os.environ["POSTGRES_PORT"],
                          database=os.environ["POSTGRES_DB"]) as connection:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT CHAR_CODE, NAME, VALUE, COUNT, DATE "
                           f"FROM {os.environ['CURRENCY_TAB']} "
                           f"WHERE CHAR_CODE='{char_code.upper()}' AND DATE='{date}'")
            if not bool(cursor.rowcount):
                return "Absence need information"
            else:
                rec = cursor.fetchone()
                return {'Code': rec[0],
                        'Currency': rec[1],
                        'Rate': rec[2],
                        'Count': rec[3],
                        'Date': rec[4]}

if __name__ == '__main__':
    load_dotenv(find_dotenv())
