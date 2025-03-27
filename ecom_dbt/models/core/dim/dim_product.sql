-- models/core/dim_product.sql
{{ config(materialized='table') }}
with raw as (
    select distinct
        sku,
        style,
        category,
        size,
        asin
    from {{ ref('staging_raw') }}
)

select
    sku,
    style,
    category,
    size,
    asin
from raw

