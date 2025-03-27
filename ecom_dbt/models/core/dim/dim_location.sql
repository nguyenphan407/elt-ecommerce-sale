-- models/core/dim_location.sql
{{ config(materialized='table') }}
with raw as (
    select distinct
        ship_postal_code,
        ship_city,
        ship_state,
        ship_country
    from {{ ref('staging_raw') }}
)

select
    ship_postal_code,
    ship_city,
    ship_state,
    ship_country
from raw
