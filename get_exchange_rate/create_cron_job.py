from crontab import CronTab
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from create_table import create_currency_table
from get_rate import request_cbr
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    with psycopg2.connect(user=os.environ["POSTGRES_USER"], password=os.environ["POSTGRES_PASSWORD"],
                          host=os.environ["POSTGRES_HOST"], port=os.environ["POSTGRES_PORT"],
                          database=os.environ["POSTGRES_DB"]) as connection:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with connection.cursor() as cursor:
            create_currency_table(cursor)
    request_cbr()
    user = os.system('whoami')
    with CronTab(user=True) as my_cron:
        job = my_cron.new(command='python get_rate.py', comment='Get exchange rate from CBR')
        job.setall('1 0 * * *')
        job.run()
