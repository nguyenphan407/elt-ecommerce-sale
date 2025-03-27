{{ config(materialized='table') }}
{% set run_date = modules.datetime.date.today() %}
select
    p.category,
    SUM(f.amount) as total_amount,
    '{{ run_date }}' as run_date
from {{ ref( 'dim_product' ) }} p
join {{ ref( 'fact' ) }} f on p.sku = f.sku
where f.order_date < '{{ run_date }}'
group by p.category, run_date