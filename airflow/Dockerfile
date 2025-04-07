FROM apache/airflow:latest

# Switch to airflow User
USER airflow

# Install the Docker, HTTP, and Airbyte providers for Airflow
RUN pip install apache-airflow-providers-docker \
    && pip install polars \
    && pip install psycopg2-binary \
    && pip install structlog \
    && pip install rapidfuzz
#    && pip install dbt-airflow \
#    && pip install dbt \
#	&& pip install dbt-core \
#    && pip install dbt-postgres \

# Switch back to root user
USER root