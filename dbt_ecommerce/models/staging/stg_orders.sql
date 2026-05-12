SELECT
    order_id,
    customer_id,
    product_id,
    CAST(quantity AS INTEGER) AS quantity,
    CAST(order_date AS TIMESTAMP) AS order_created_at
FROM {{ source('ecommerce', 'raw_orders') }}
