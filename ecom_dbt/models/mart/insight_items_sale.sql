{{ config(materialized='table') }}
{% set run_date = modules.datetime.date.today() %}
select
    p.sku,
    SUM(f.qty) as qty,
    SUM(f.amount) as total_sales,
    '{{ run_date }}' as run_date
from {{ ref('dim_product') }} p
join {{ ref('fact') }} f on f.sku = p.sku
group by p.sku