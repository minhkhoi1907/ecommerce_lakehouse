import pandas as pd
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def categorize_products():
    input_path = 'data/raw/products.parquet'
    output_path = 'data/raw/products_categorized.parquet'
    
    if not os.path.exists(input_path):
        logging.error(f"Error: {input_path} not found. Run 01_fetch_real_data.py first.")
        return
        
    logging.info(f"Reading products from {input_path} (Parquet)...")
    df = pd.read_parquet(input_path)
    
    # Rule-based categorization
    def assign_category(name):
        name_lower = str(name).lower()
        if any(keyword in name_lower for keyword in ['bag', 'pouch', 'case', 'handbag']):
            return 'Bags & Accessories'
        elif any(keyword in name_lower for keyword in ['candle', 'holder', 'light', 'lamp', 'lantern']):
            return 'Home Decor (Lighting)'
        elif any(keyword in name_lower for keyword in ['heart', 'decoration', 'ornament', 'frame', 'wall']):
            return 'Home Decor (Ornaments)'
        elif any(keyword in name_lower for keyword in ['mug', 'cup', 'plate', 'bowl', 'kitchen', 'tea', 'coffee', 'bottle']):
            return 'Kitchen & Dining'
        elif any(keyword in name_lower for keyword in ['toy', 'game', 'doll', 'puzzle', 'gift']):
            return 'Toys & Gifts'
        elif any(keyword in name_lower for keyword in ['t-shirt', 'jeans', 'sneakers', 'socks', 'garment']):
            return 'Clothing'
        elif any(keyword in name_lower for keyword in ['laptop', 'smartphone', 'monitor', 'keyboard', 'mouse']):
            return 'Electronics'
        else:
            return 'General Merchandise'
            
    logging.info("Applying AI (rule-based) categorization...")
    df['category'] = df['name'].apply(assign_category)
    
    df.to_parquet(output_path, index=False)
    logging.info(f"Categorized products saved to {output_path} (Parquet)")

if __name__ == "__main__":
    categorize_products()
