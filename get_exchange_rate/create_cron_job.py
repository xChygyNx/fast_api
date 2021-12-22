from crontab import CronTab
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from create_table import create_currency_table
from get_rate import request_cbr


if __name__ == '__main__':
    with psycopg2.connect(user="admin", password="very_difficult_password",
                        host="postgres", port="5432", database="exchange_db") as connection:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with connection.cursor() as cursor:
            create_currency_table(cursor)
    request_cbr()
    user = os.system('whoami')
    with CronTab(user=True) as my_cron:
        job = my_cron.new(command='python get_rate.py', comment='Get exchange rate from CBR')
        job.setall('1 0 * * *')
        job.run()
