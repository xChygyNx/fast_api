import requests
from datetime import datetime
import xmltodict
import write_in_postgres
from dotenv import load_dotenv, find_dotenv
import time


class RequestError(Exception):
    def __init__(self, answer: requests.Response):
        self.message = f"Банк России ответил ошибкой\n" \
                       f"Код ответа: {answer.status_code}\n" \
                       f"Текст ошибки: {answer.text}"
        super().__init__(self.message)


URL = "https://www.cbr.ru/scripts/XML_daily.asp"
PARAM = "date_req"


def request_cbr():
    date = datetime.now().strftime('%d/%m/%Y')
    for i in range(61):
        response = requests.get(url=URL, params={PARAM: date})
        if response.status_code == 200:
            content = xmltodict.parse(response.content)
            valutes, today = content['ValCurs']['Valute'], content['ValCurs']['@Date']
            write_in_postgres.write_rate(valutes, today)
            return
        else:
            time.sleep(60)
    raise RequestError(response)


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    request_cbr()
