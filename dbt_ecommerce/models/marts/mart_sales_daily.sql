{{ config(materialized='table') }}

WITH fct_orders AS (
    SELECT * FROM {{ ref('fct_orders') }}
)

SELECT
    CAST(order_created_at AS DATE) AS sale_date,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_items_sold,
    SUM(total_revenue_usd) AS total_revenue_usd,
    SUM(total_revenue_vnd) AS total_revenue_vnd
FROM fct_orders
GROUP BY 1
