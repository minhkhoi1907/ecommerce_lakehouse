import pandas as pd
import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Create data/raw if it doesn't exist
os.makedirs("data/raw", exist_ok=True)

URL = "https://raw.githubusercontent.com/guipsamora/pandas_exercises/master/07_Visualization/Online_Retail/Online_Retail.csv"

def fetch_and_process_data():
    logging.info("Downloading Online Retail Dataset...")
    try:
        df = pd.read_csv(URL, encoding='ISO-8859-1')
        logging.info(f"Downloaded {len(df)} rows.")
    except Exception as e:
        logging.error(f"Error downloading dataset: {e}")
        return

    # Clean data
    # Drop rows without CustomerID
    df = df.dropna(subset=['CustomerID'])
    # Remove cancelled orders (Quantity <= 0)
    df = df[df['Quantity'] > 0]
    
    # 1. Process Customers
    customers_df = df[['CustomerID', 'Country']].drop_duplicates(subset=['CustomerID']).copy()
    customers_df['customer_id'] = 'C' + customers_df['CustomerID'].astype(int).astype(str).str.zfill(5)
    customers_df['name'] = 'Customer ' + customers_df['CustomerID'].astype(int).astype(str)
    customers_df['email'] = 'customer' + customers_df['CustomerID'].astype(int).astype(str) + '@example.com'
    customers_df.rename(columns={'Country': 'country'}, inplace=True)
    customers_df = customers_df[['customer_id', 'name', 'email', 'country']]
    customers_df.to_parquet('data/raw/customers.parquet', index=False)
    logging.info(f"Generated {len(customers_df)} customers (Parquet).")

    # 2. Process Products
    products_df = df[['StockCode', 'Description', 'UnitPrice']].drop_duplicates(subset=['StockCode']).copy()
    # If Description is NaN, fill it
    products_df['Description'] = products_df['Description'].fillna("Unknown Product")
    products_df.rename(columns={
        'StockCode': 'product_id',
        'Description': 'name',
        'UnitPrice': 'price'
    }, inplace=True)
    products_df.to_parquet('data/raw/products.parquet', index=False)
    logging.info(f"Generated {len(products_df)} products (Parquet).")

    # 3. Process Orders
    orders_df = df[['InvoiceNo', 'CustomerID', 'StockCode', 'Quantity', 'InvoiceDate']].copy()
    orders_df.rename(columns={
        'InvoiceNo': 'order_id',
        'StockCode': 'product_id',
        'Quantity': 'quantity',
        'InvoiceDate': 'order_date'
    }, inplace=True)
    orders_df['customer_id'] = 'C' + orders_df['CustomerID'].astype(int).astype(str).str.zfill(5)
    orders_df.drop(columns=['CustomerID'], inplace=True)
    
    # Reorder columns to match previous output
    orders_df = orders_df[['order_id', 'customer_id', 'product_id', 'quantity', 'order_date']]
    orders_df.to_parquet('data/raw/orders.parquet', index=False)
    logging.info(f"Generated {len(orders_df)} orders (Parquet).")

if __name__ == "__main__":
    logging.info("Starting real data fetch process...")
    fetch_and_process_data()
    logging.info("Data fetch complete. Saved to data/raw/")
