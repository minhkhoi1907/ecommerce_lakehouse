{{ config(materialized='table') }}

WITH fct_orders AS (
    SELECT * FROM {{ ref('fct_orders') }}
),
dim_products AS (
    SELECT * FROM {{ ref('dim_products') }}
)

SELECT
    p.product_category,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.quantity) AS total_items_sold,
    SUM(f.total_revenue_usd) AS total_revenue_usd,
    SUM(f.total_revenue_vnd) AS total_revenue_vnd
FROM fct_orders f
LEFT JOIN dim_products p ON f.product_id = p.product_id
GROUP BY 1
