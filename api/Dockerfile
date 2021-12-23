FROM python:3.8
COPY ./requirements.txt /src/requirements.txt
COPY ./main.py /src/python_bin/main.py
RUN apt-get update
RUN python -m pip install --upgrade pip
RUN pip install -r /src/requirements.txt
RUN python /src/python_bin/main.py
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=very_difficult_password
ENV POSTGRES_HOST=postgres
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=exchange_db
ENV CURRENCY_TAB=currency_table
CMD uvicorn src.python_bin.main:app --host 0.0.0.0
