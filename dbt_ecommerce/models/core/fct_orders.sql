{{
    config(
        materialized='incremental',
        unique_key=['order_id', 'product_id']
    )
}}

WITH orders AS (
    SELECT 
        order_id,
        customer_id,
        product_id,
        order_created_at,
        quantity
    FROM {{ ref('stg_orders') }}
    {% if is_incremental() %}
      WHERE order_created_at > (SELECT MAX(order_created_at) FROM {{ this }})
    {% endif %}
),
products AS (
    SELECT 
        product_id,
        product_price_usd
    FROM {{ ref('dim_products') }}
),
rates AS (
    SELECT 
        exchange_rate_to_usd,
        rate_updated_at::DATE as rate_date
    FROM {{ ref('stg_exchange_rates') }}
    WHERE currency = 'VND'
)

SELECT
    o.order_id,
    o.customer_id,
    o.product_id,
    o.order_created_at,
    o.quantity,
    p.product_price_usd,
    (o.quantity * COALESCE(p.product_price_usd, 0)) AS total_revenue_usd,
    (o.quantity * COALESCE(p.product_price_usd, 0) * 
        COALESCE(
            r.exchange_rate_to_usd, 
            (SELECT exchange_rate_to_usd FROM rates ORDER BY rate_date DESC LIMIT 1),
            25000
        )
    ) AS total_revenue_vnd
FROM orders o
LEFT JOIN products p ON o.product_id = p.product_id
LEFT JOIN rates r ON CAST(o.order_created_at AS DATE) = r.rate_date
