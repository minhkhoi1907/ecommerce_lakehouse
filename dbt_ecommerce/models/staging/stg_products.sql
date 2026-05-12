SELECT
    product_id,
    name AS product_name,
    CAST(price AS DECIMAL(10,2)) AS product_price_usd,
    category AS product_category
FROM {{ source('ecommerce', 'raw_products') }}
