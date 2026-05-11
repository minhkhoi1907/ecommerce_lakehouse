import requests
import json
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

os.makedirs("data/raw", exist_ok=True)

def fetch_exchange_rates():
    load_dotenv() # Đọc file .env
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    
    if api_key:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
        logging.info("Using ExchangeRate-API with API Key...")
    else:
        url = "https://open.er-api.com/v6/latest/USD"
        logging.info("No API Key found, using free fallback endpoint...")
    
    logging.info(f"Fetching exchange rates from {url}...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # API có key hoặc free API có thể trả về 'conversion_rates' hoặc 'rates'
        rates_dict = data.get('conversion_rates') or data.get('rates', {})
        
        rates = {
            'base_code': data.get('base_code', 'USD'),
            'date': data.get('time_last_update_utc', ''),
            'rates': {
                'VND': rates_dict.get('VND', 25000),
                'EUR': rates_dict.get('EUR', 0.9),
                'GBP': rates_dict.get('GBP', 0.8),
                'JPY': rates_dict.get('JPY', 150)
            }
        }
    except Exception as e:
        logging.warning(f"Failed to fetch from API ({e}). Using mock data.")
        rates = {
            'base_code': 'USD',
            'date': 'Mock Date',
            'rates': {
                'VND': 25400,
                'EUR': 0.92,
                'GBP': 0.79,
                'JPY': 151.2
            }
        }
        
    output_path = 'data/raw/exchange_rates.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(rates, f, indent=4)
        
    logging.info(f"Exchange rates saved to {output_path}")

if __name__ == "__main__":
    fetch_exchange_rates()
