-- models/core/dim_fulfillment.sql
{{ config(materialized='table') }}
with raw as (
    select distinct status, fulfilment, courier_status, b2b, fulfilled_by
    from {{ ref('staging_raw') }}
)

select
    status,
    fulfilment,
    courier_status,
    b2b,
    fulfilled_by
from raw
