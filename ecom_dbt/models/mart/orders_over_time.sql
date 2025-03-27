{{ config(materialized='table') }}
select
    t.year,
    t.month,
    count(distinct f.order_id) as total_orders,
    sum(f.amount) as total_revenue
from {{ ref('fact') }} f
join {{ ref('dim_time') }} t on f.order_date = t.order_date
group by t.year, t.month