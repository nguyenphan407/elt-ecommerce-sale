{{ config(materialized='table') }}
select
    l.ship_city as city,
    SUM(f.amount) as total_sales
from {{ ref( 'dim_location' ) }} l
join {{ ref( 'fact' ) }} f on f.ship_postal_code = l.ship_postal_code
group by l.ship_city