WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),
products AS (
    SELECT * FROM {{ ref('stg_products') }}
),
-- Lấy tỷ giá VND hiện tại (Chỉ lấy 1 dòng)
vnd_rate AS (
    SELECT exchange_rate_to_usd AS rate
    FROM {{ ref('stg_exchange_rates') }}
    WHERE currency = 'VND'
    ORDER BY rate_updated_at DESC
    LIMIT 1
)

SELECT
    o.order_id,
    o.customer_id,
    o.product_id,
    o.order_created_at,
    o.quantity,
    p.product_price_usd,
    (o.quantity * COALESCE(p.product_price_usd, 0)) AS total_revenue_usd,
    -- Tính doanh thu VNĐ bằng cách nhân với tỷ giá (tránh NULL)
    (o.quantity * COALESCE(p.product_price_usd, 0) * COALESCE(r.rate, 1)) AS total_revenue_vnd
FROM orders o
LEFT JOIN products p ON o.product_id = p.product_id
CROSS JOIN (
    SELECT COALESCE(MAX(rate), 1) AS rate FROM vnd_rate
) r
