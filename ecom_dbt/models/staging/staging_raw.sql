{{ config(materialized='table') }}

select
    idx,
    order_id,
    order_date,
    status,
    fulfilment,
    sales_channel,
    ship_service_level,
    style,
    sku,
    category,
    size,
    asin,
    courier_status,
    qty,
    currency,
    amount,
    LOWER(COALESCE(ship_city, '')) AS ship_city,
    ship_state,
    CAST(SPLIT_PART(ship_postal_code, '.', 1) AS TEXT) as ship_postal_code,
    ship_country,
    promotion_ids,
    b2b,
    fulfilled_by
from {{ ref('raw_fact') }}
