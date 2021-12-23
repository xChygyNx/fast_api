FROM python:3.8
COPY ./requirements.txt /src/requirements.txt
COPY ./create_cron_job.py /src/python_bin/create_cron_job.py
COPY ./get_rate.py /src/python_bin/get_rate.py
COPY ./create_table.py /src/python_bin/create_table.py
COPY ./write_in_postgres.py /src/python_bin/write_in_postgres.py
COPY ./container_reanimator.py /src/python_bin/container_reanimator.py
COPY ./run.sh /src/run.sh
RUN apt-get update
RUN apt-get -y install cron
RUN python -m pip install --upgrade pip
RUN pip install -r /src/requirements.txt
RUN chmod 777 /src/run.sh
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=very_difficult_password
ENV POSTGRES_HOST=postgres
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=exchange_db
ENV CURRENCY_TAB=currency_table
CMD /src/run.sh
