FROM python:3.7.4

ENV LANG=C.UTF-8

COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

COPY prod-requirements.txt /tmp/
RUN pip3 install -r /tmp/prod-requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 2222

CMD python run.py
