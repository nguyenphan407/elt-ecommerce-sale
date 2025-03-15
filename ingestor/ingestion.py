import os
import polars as pl
import psgcopg2
import structlog

log = structlog.get_logger()

CONNECTION = psgcopg2.connect(
    host=os.environ['POSTGRES_HOST'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    database=os.environ['POSTGRES_DB']
)

def ingest_raw_customer(self, connection):


