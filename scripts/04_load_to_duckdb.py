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
    
    # 1. Load Customers
    if os.path.exists('data/raw/customers.csv'):
        logging.info("Loading raw_customers incrementally...")
        con.execute("CREATE TABLE IF NOT EXISTS raw_customers AS SELECT * FROM read_csv_auto('data/raw/customers.csv') LIMIT 0;")
        con.execute("INSERT INTO raw_customers SELECT * FROM read_csv_auto('data/raw/customers.csv') WHERE customer_id NOT IN (SELECT customer_id FROM raw_customers);")
    
    # 2. Load Orders
    if os.path.exists('data/raw/orders.csv'):
        logging.info("Loading raw_orders incrementally...")
        con.execute("CREATE TABLE IF NOT EXISTS raw_orders AS SELECT * FROM read_csv_auto('data/raw/orders.csv') LIMIT 0;")
        con.execute("INSERT INTO raw_orders SELECT * FROM read_csv_auto('data/raw/orders.csv') WHERE order_id NOT IN (SELECT order_id FROM raw_orders);")
        
    # 3. Load Categorized Products
    prod_path = 'data/raw/products_categorized.csv'
    if os.path.exists(prod_path):
        logging.info("Loading raw_products (categorized) incrementally...")
        con.execute(f"CREATE TABLE IF NOT EXISTS raw_products AS SELECT * FROM read_csv_auto('{prod_path}') LIMIT 0;")
        con.execute(f"INSERT INTO raw_products SELECT * FROM read_csv_auto('{prod_path}') WHERE product_id NOT IN (SELECT product_id FROM raw_products);")
    elif os.path.exists('data/raw/products.csv'):
        logging.warning("products_categorized.csv not found! Falling back to raw products.csv and adding 'Unknown' category...")
        con.execute("CREATE TABLE IF NOT EXISTS raw_products AS SELECT *, 'Unknown' AS category FROM read_csv_auto('data/raw/products.csv') LIMIT 0;")
        con.execute("INSERT INTO raw_products SELECT *, 'Unknown' AS category FROM read_csv_auto('data/raw/products.csv') WHERE product_id NOT IN (SELECT product_id FROM raw_products);")
    else:
        logging.error("No product data found!")
        
    # 4. Load Exchange Rates (JSON)
    if os.path.exists('data/raw/exchange_rates.json'):
        logging.info("Loading raw_exchange_rates...")
        with open('data/raw/exchange_rates.json', 'r') as f:
            rates_data = json.load(f)
            
        # Convert JSON structure to a flat dataframe for easy loading
        rates_df = pd.DataFrame([
            {'currency': currency, 'rate': rate, 'date': rates_data['date']} 
            for currency, rate in rates_data['rates'].items()
        ])
        
        con.execute("CREATE TABLE IF NOT EXISTS raw_exchange_rates AS SELECT * FROM rates_df LIMIT 0;")
        con.execute("INSERT INTO raw_exchange_rates SELECT * FROM rates_df EXCEPT SELECT * FROM raw_exchange_rates;")
        
    logging.info("--- DuckDB Tables ---")
    tables = con.execute("SHOW TABLES").fetchall()
    for table in tables:
        count = con.execute(f"SELECT COUNT(*) FROM {table[0]}").fetchone()[0]
        logging.info(f"Table: {table[0]} | Rows: {count}")
        
    con.close()
    logging.info("All raw data loaded to DuckDB (Bronze Layer).")

if __name__ == "__main__":
    load_to_bronze()
