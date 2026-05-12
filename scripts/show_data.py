import duckdb
import pandas as pd

# Định dạng số trong Pandas để không bị hiển thị dạng khoa học (e+10) và có dấu phẩy ngăn cách hàng nghìn
pd.options.display.float_format = '{:,.2f}'.format

def show_gold_data():
    db_path = 'database/ecom.duckdb'
    print(f"\n🚀 --- TRUY VẤN LỚP GOLD (DATA MARTS) TỪ {db_path} --- 🚀")
    
    try:
        con = duckdb.connect(db_path)
        
        # Các bảng quan trọng nhất trong hệ thống
        queries = {
            "1. TỶ GIÁ NGOẠI TỆ HIỆN TẠI (STG)": "SELECT * FROM stg_exchange_rates LIMIT 5",
            "2. DOANH THU THEO DANH MỤC (MART)": "SELECT * FROM mart_sales_by_category ORDER BY total_revenue_vnd DESC LIMIT 5",
            "3. DOANH THU THEO NGÀY (MART)": "SELECT * FROM mart_sales_daily ORDER BY sale_date DESC LIMIT 5",
            "4. CHI TIẾT ĐƠN HÀNG (FACT)": "SELECT order_id, quantity, total_revenue_usd, total_revenue_vnd FROM fct_orders LIMIT 5"
        }
        
        for title, query in queries.items():
            print(f"\n{'='*60}")
            print(f" {title}")
            print(f"{'='*60}")
            
            try:
                df = con.execute(query).df()
                # Format hiển thị cho đẹp
                if not df.empty:
                    print(df.to_string(index=False))
                else:
                    print("(Không có dữ liệu)")
            except duckdb.Error as e:
                print(f"(Bảng chưa được tạo hoặc có lỗi: {e})")
            
        con.close()
        print(f"\n✅ --- HOÀN TẤT TRUY VẤN --- ✅\n")
    except Exception as e:
        print(f"Lỗi kết nối database: {e}")

if __name__ == "__main__":
    show_gold_data()
