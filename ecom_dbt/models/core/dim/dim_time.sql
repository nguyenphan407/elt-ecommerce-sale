-- models/core/dim_time.sql
{{ config(materialized='table') }}
with raw as (
    select distinct order_date
    from {{ ref('staging_raw') }}
)

select
    order_date,
    extract(year from order_date) as year,
    extract(quarter from order_date) as quarter,
    extract(month from order_date) as month,
    extract(day from order_date) as day
from raw
