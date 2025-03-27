{{ config(materialized='table') }}
with raw as (
    select
        order_id,
        order_date,
        status,
        fulfilment,
        sales_channel,
        qty,
        amount,
        currency,
        sku,
        ship_postal_code
    from {{ ref( 'staging_raw' ) }}
)

select
    order_id,
    qty,
    amount,
    currency,
    order_date,
    sku,
    ship_postal_code,
    sales_channel,
    status
from raw