from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
from docker.types import Mount
from datetime import datetime

from include.ecom.tasks import _ingest_raw_fact, _clean_data, _write_to_dw

with DAG(
    dag_id="ecom",
    schedule_interval="@daily",
    start_date=datetime(2025, 3, 22),
    catchup=False,
) as dag:
    ingest_data= PythonOperator(
        task_id="ingest_data",
        python_callable=_ingest_raw_fact
    )

    clean_data = PythonOperator(
        task_id="clean_data",
        python_callable=_clean_data,
        op_kwargs = {
            "df": "{{ task_instance.xcom_pull(task_ids='ingest_data', key='return_value') }}"
        }
    )

    write_to_dw = PythonOperator(
        task_id="write_to_dw",
        python_callable=_write_to_dw,
        op_kwargs = {
            "df": "{{ task_instance.xcom_pull(task_ids='clean_data') }}"
        }
    )

    dbt_transform = DockerOperator(
        task_id='dbt_run',
        image='ghcr.io/dbt-labs/dbt-postgres:1.4.7',
        command=[
            "run",
            "--profiles-dir",
            "/root",
            "--project-dir",
            "/opt/dbt",
            "--full-refresh",
        ],
        api_version='auto',
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mount_tmp_dir=False,
        mounts = [
            Mount(source='/Users/phanhoangnguyen/LearnNew/elt-ecommerce-sale/ecom_dbt',
                  target='/opt/dbt', type='bind'),
            Mount(source='/Users/phanhoangnguyen/.dbt', target='/root', type='bind'),
        ]
    )

    ingest_data >> clean_data >> write_to_dw >> dbt_transform