import duckdb
import os
import json
import pandas as pd

def load_to_bronze():
    db_path = 'database/ecom.duckdb'
    os.makedirs('database', exist_ok=True)
    
    print(f"Connecting to DuckDB at {db_path}...")
    con = duckdb.connect(db_path)
    
    # 1. Load Customers
    if os.path.exists('data/raw/customers.csv'):
        print("Loading raw_customers...")
        con.execute("CREATE OR REPLACE TABLE raw_customers AS SELECT * FROM read_csv_auto('data/raw/customers.csv');")
    
    # 2. Load Orders
    if os.path.exists('data/raw/orders.csv'):
        print("Loading raw_orders...")
        con.execute("CREATE OR REPLACE TABLE raw_orders AS SELECT * FROM read_csv_auto('data/raw/orders.csv');")
        
    # 3. Load Categorized Products
    prod_path = 'data/raw/products_categorized.csv'
    if not os.path.exists(prod_path):
        prod_path = 'data/raw/products.csv' # Fallback
        
    if os.path.exists(prod_path):
        print("Loading raw_products...")
        con.execute(f"CREATE OR REPLACE TABLE raw_products AS SELECT * FROM read_csv_auto('{prod_path}');")
        
    # 4. Load Exchange Rates (JSON)
    if os.path.exists('data/raw/exchange_rates.json'):
        print("Loading raw_exchange_rates...")
        with open('data/raw/exchange_rates.json', 'r') as f:
            rates_data = json.load(f)
            
        # Convert JSON structure to a flat dataframe for easy loading
        rates_df = pd.DataFrame([
            {'currency': currency, 'rate': rate, 'date': rates_data['date']} 
            for currency, rate in rates_data['rates'].items()
        ])
        
        con.execute("CREATE OR REPLACE TABLE raw_exchange_rates AS SELECT * FROM rates_df;")
        
    print("\n--- DuckDB Tables ---")
    tables = con.execute("SHOW TABLES").fetchall()
    for table in tables:
        count = con.execute(f"SELECT COUNT(*) FROM {table[0]}").fetchone()[0]
        print(f"Table: {table[0]} | Rows: {count}")
        
    con.close()
    print("All raw data loaded to DuckDB (Bronze Layer).")

if __name__ == "__main__":
    load_to_bronze()
