from crontab import CronTab
from dotenv import load_dotenv, find_dotenv
from typing import Optional

load_dotenv(find_dotenv())


def add_cron_job(command: str, moment: str, comment: Optional[str] = 'Some job') -> None:
    """
    Функция которая добавляет в CronTable команду command, которая должна выполнятся по расписанию

    :param command: - Bash комманда, которая должна выполнятся по расписанию
    :param moment: - расписание в формате cron
    :param comment: - комментарий к задаче
    :return:
    """
    with CronTab(user=True) as my_cron:
        job = my_cron.new(command=command, comment=comment)
        job.setall(moment)
        job.run()


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    add_cron_job(command='python get_rate.py', moment='1 0 * * *', comment='Get exchange rate from CBR')
