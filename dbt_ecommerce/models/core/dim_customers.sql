SELECT
    customer_id,
    customer_name,
    customer_email,
    customer_country
FROM {{ ref('stg_customers') }}
