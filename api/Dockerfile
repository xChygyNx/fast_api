FROM python:3.8
COPY ./requirements.txt /src/requirements.txt
COPY ./main.py /src/python_bin/main.py
RUN apt-get update
RUN python -m pip install --upgrade pip
RUN pip install -r /src/requirements.txt
CMD uvicorn src.python_bin.main:app --host 0.0.0.0
