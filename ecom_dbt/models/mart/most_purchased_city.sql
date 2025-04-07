{{ config(materialized='table') }}
select
    l.ship_state as state,
    l.Code as iso_code,
    SUM(f.amount) as total_sales
from {{ ref( 'dim_location' ) }} l
join {{ ref( 'fact' ) }} f on f.ship_postal_code = l.ship_postal_code
group by l.ship_state, l.Code