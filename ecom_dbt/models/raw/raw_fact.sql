{{ config(materialized='table') }}
SELECT * FROM {{ source('ecom', 'raw_fact') }}