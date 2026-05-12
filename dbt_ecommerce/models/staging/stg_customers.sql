SELECT
    customer_id,
    name AS customer_name,
    email AS customer_email,
    country AS customer_country
FROM {{ source('ecommerce', 'raw_customers') }}
