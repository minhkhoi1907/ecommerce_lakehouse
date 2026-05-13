import duckdb
import os
import json
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def load_to_bronze():
    db_path = 'database/ecom.duckdb'
    os.makedirs('database', exist_ok=True)
    
    logging.info(f"Connecting to DuckDB at {db_path}...")
    con = duckdb.connect(db_path)
    
    # --- 1. Load Customers (Parquet) ---
    cust_path = 'data/raw/customers.parquet'
    if os.path.exists(cust_path):
        logging.info("Upserting raw_customers from Parquet...")
        con.execute("""
            CREATE TABLE IF NOT EXISTS raw_customers (
                customer_id VARCHAR PRIMARY KEY,
                name VARCHAR,
                email VARCHAR,
                country VARCHAR
            );
        """)
        # DuckDB can read parquet directly in the SQL
        con.execute(f"INSERT OR REPLACE INTO raw_customers SELECT * FROM read_parquet('{cust_path}');")
    
    # --- 2. Load Products (Parquet) ---
    prod_path = 'data/raw/products_categorized.parquet'
    if os.path.exists(prod_path):
        logging.info("Upserting raw_products from Parquet...")
        con.execute("""
            CREATE TABLE IF NOT EXISTS raw_products (
                product_id VARCHAR PRIMARY KEY,
                name VARCHAR,
                price DOUBLE,
                category VARCHAR
            );
        """)
        con.execute(f"INSERT OR REPLACE INTO raw_products SELECT * FROM read_parquet('{prod_path}');")

    # --- 3. Load Orders (Parquet with Deduplication) ---
    order_path = 'data/raw/orders.parquet'
    if os.path.exists(order_path):
        logging.info("Loading raw_orders from Parquet with deduplication...")
        con.execute("""
            CREATE TABLE IF NOT EXISTS raw_orders (
                order_id VARCHAR,
                customer_id VARCHAR,
                product_id VARCHAR,
                quantity INTEGER,
                order_date VARCHAR,
                UNIQUE(order_id, product_id)
            );
        """)
        # Using INSERT OR IGNORE to handle duplicates based on UNIQUE constraint
        con.execute(f"""
            INSERT OR IGNORE INTO raw_orders 
            SELECT * FROM read_parquet('{order_path}');
        """)
        
    # --- 4. Load Exchange Rates (History Pattern) ---
    if os.path.exists('data/raw/exchange_rates.json'):
        logging.info("Loading raw_exchange_rates (History)...")
        with open('data/raw/exchange_rates.json', 'r') as f:
            rates_data = json.load(f)
            
        rates_df = pd.DataFrame([
            {'currency': currency, 'rate': rate, 'date': rates_data['date']} 
            for currency, rate in rates_data['rates'].items()
        ])
        
        con.execute("""
            CREATE TABLE IF NOT EXISTS raw_exchange_rates (
                currency VARCHAR,
                rate DOUBLE,
                rate_date TIMESTAMP
            );
        """)
        
        con.execute("""
            INSERT INTO raw_exchange_rates 
            SELECT currency, rate, CAST(date AS TIMESTAMP) 
            FROM rates_df s
            WHERE NOT EXISTS (
                SELECT 1 FROM raw_exchange_rates t 
                WHERE s.currency = t.currency 
                AND date_trunc('day', CAST(s.date AS TIMESTAMP)) = date_trunc('day', t.rate_date)
            );
        """)
        
    logging.info("--- DuckDB Tables Summary ---")
    tables = con.execute("SHOW TABLES").fetchall()
    for table in tables:
        count = con.execute(f"SELECT COUNT(*) FROM {table[0]}").fetchone()[0]
        logging.info(f"Table: {table[0]} | Rows: {count}")
        
    con.close()
    logging.info("Parquet-based load process complete.")

if __name__ == "__main__":
    load_to_bronze()
