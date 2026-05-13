{{
    config(
        materialized='incremental',
        unique_key=['order_id', 'product_id']
    )
}}

WITH raw_data AS (
    SELECT
        order_id,
        customer_id,
        product_id,
        CAST(quantity AS INTEGER) AS quantity,
        -- Thử parse ngày tháng, nếu lỗi trả về NULL
        TRY_STRPTIME(order_date, '%m/%d/%y %H:%M') AS order_created_at
    FROM {{ source('ecommerce', 'raw_orders') }}
)

SELECT * FROM raw_data

{% if is_incremental() %}
  -- Sử dụng >= để tránh mất dữ liệu, dbt sẽ dùng unique_key để loại bỏ trùng lặp
  WHERE order_created_at >= (SELECT MAX(order_created_at) FROM {{ this }})
{% endif %}
