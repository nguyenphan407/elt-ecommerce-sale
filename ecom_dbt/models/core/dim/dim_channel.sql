-- models/core/dim_channel.sql
{{ config(materialized='table') }}

with raw as (
    select distinct
        sales_channel, ship_service_level, promotion_ids
    from {{ ref('staging_raw') }}
)

select
    sales_channel,
    ship_service_level,
    promotion_ids
from raw
