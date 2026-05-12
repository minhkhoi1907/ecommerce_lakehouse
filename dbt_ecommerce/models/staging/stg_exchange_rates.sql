SELECT
    currency,
    CAST(rate AS DECIMAL(18,4)) AS exchange_rate_to_usd,
    CAST(date AS TIMESTAMP) AS rate_updated_at
FROM {{ source('ecommerce', 'raw_exchange_rates') }}
