import pandas as pd
import os

def categorize_products():
    input_path = 'data/raw/products.csv'
    output_path = 'data/raw/products_categorized.csv'
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run 01_generate_data.py first.")
        return
        
    print(f"Reading products from {input_path}...")
    df = pd.read_csv(input_path)
    
    # Rule-based categorization (giả lập AI categorization)
    def assign_category(name):
        name_lower = str(name).lower()
        if any(keyword in name_lower for keyword in ['laptop', 'smartphone', 'monitor', 'keyboard', 'mouse']):
            return 'Electronics'
        elif any(keyword in name_lower for keyword in ['desk', 'chair']):
            return 'Furniture'
        elif any(keyword in name_lower for keyword in ['t-shirt', 'jeans', 'sneakers']):
            return 'Clothing'
        else:
            return 'Other'
            
    print("Applying AI (rule-based) categorization...")
    df['category'] = df['name'].apply(assign_category)
    
    df.to_csv(output_path, index=False)
    print(f"Categorized products saved to {output_path}")

if __name__ == "__main__":
    categorize_products()
