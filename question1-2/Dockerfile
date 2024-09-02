FROM apache/airflow:2.10.0
ENV AIRFLOW_HOME=/opt/airflow

USER root
RUN apt-get update -qq && apt-get install vim -qqq

RUN  python -m pip install --upgrade pip
RUN  python -m pip install python-dotenv

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir clickhouse-connect

WORKDIR $AIRFLOW_HOME
USER $AIRFLOW_UID