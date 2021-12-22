FROM python:3.8
COPY ./requirements.txt /src/requirements.txt
COPY ./create_cron_job.py /src/python_bin/create_cron_job.py
COPY ./get_rate.py /src/python_bin/get_rate.py
COPY ./create_table.py /src/python_bin/create_table.py
COPY ./container_reanimator.py /src/python_bin/container_reanimator.py
COPY ./run.sh /src/run.sh
RUN apt-get update
RUN apt-get -y install cron
RUN python -m pip install --upgrade pip
RUN pip install -r /src/requirements.txt
RUN chmod 777 /src/run.sh
CMD /src/run.sh
