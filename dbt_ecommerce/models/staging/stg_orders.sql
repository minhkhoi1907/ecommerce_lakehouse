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
        -- Sử dụng strptime để xử lý định dạng ngày tháng thực tế của Online Retail (MM/DD/YY HH:MM)
        strptime(order_date, '%m/%d/%y %H:%M') AS order_created_at
    FROM {{ source('ecommerce', 'raw_orders') }}
)

SELECT * FROM raw_data

{% if is_incremental() %}
  -- Chỉ lấy các dòng dữ liệu mới hơn thời điểm lớn nhất hiện tại
  WHERE order_created_at > (SELECT MAX(order_created_at) FROM {{ this }})
{% endif %}
