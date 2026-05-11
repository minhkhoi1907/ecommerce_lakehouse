import pandas as pd
import random
from datetime import datetime, timedelta
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

def generate_customers(n=100):
    countries = ['US', 'VN', 'UK', 'JP', 'CA']
    customers = []
    for i in range(1, n + 1):
        customers.append({
            'customer_id': f'C{i:03}',
            'name': f'Customer {i}',
            'email': f'customer{i}@example.com',
            'country': random.choice(countries)
        })
    df = pd.DataFrame(customers)
    df.to_csv('data/raw/customers.csv', index=False)
    logging.info(f"Generated {n} customers.")

def generate_products(n=50):
    products = []
    names = ['Laptop', 'Smartphone', 'Desk', 'Chair', 'Monitor', 'Keyboard', 'Mouse', 'T-Shirt', 'Jeans', 'Sneakers']
    for i in range(1, n + 1):
        products.append({
            'product_id': f'P{i:03}',
            'name': f'{random.choice(names)} {i}',
            'price': round(random.uniform(10.0, 1500.0), 2)
        })
    df = pd.DataFrame(products)
    df.to_csv('data/raw/products.csv', index=False)
    logging.info(f"Generated {n} products.")

def generate_orders(n=500, num_customers=100, num_products=50):
    orders = []
    start_date = datetime.now() - timedelta(days=30)
    for i in range(1, n + 1):
        orders.append({
            'order_id': f'O{i:04}',
            'customer_id': f'C{random.randint(1, num_customers):03}',
            'product_id': f'P{random.randint(1, num_products):03}',
            'quantity': random.randint(1, 5),
            'order_date': (start_date + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))).strftime('%Y-%m-%d %H:%M:%S')
        })
    df = pd.DataFrame(orders)
    df.to_csv('data/raw/orders.csv', index=False)
    logging.info(f"Generated {n} orders.")

if __name__ == "__main__":
    logging.info("Starting data generation...")
    generate_customers()
    generate_products()
    generate_orders()
    logging.info("Data generation complete. Saved to data/raw/")
