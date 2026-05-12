SELECT
    product_id,
    product_name,
    COALESCE(product_category, 'Unknown') AS product_category,
    product_price_usd
FROM {{ ref('stg_products') }}
