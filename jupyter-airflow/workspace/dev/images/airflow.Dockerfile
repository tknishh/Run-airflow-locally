FROM phidata/airflow:2.5.0

RUN pip install --upgrade pip

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY workspace/dev/airflow/resources/requirements-airflow.txt /
RUN pip install -r /requirements-airflow.txt

COPY workspace/dev/airflow/resources/webserver_config.py ${AIRFLOW_HOME}/

# Install python3 kernel for jupyter
RUN ipython kernel install --name "python3"
