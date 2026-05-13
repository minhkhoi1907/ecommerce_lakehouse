Write-Host "Bắt đầu chạy E-commerce Data Lakehouse Pipeline..." -ForegroundColor Green

Write-Host "1. Tải dữ liệu thực tế (Online Retail)..." -ForegroundColor Cyan
python scripts/01_fetch_real_data.py
if ($LASTEXITCODE -ne 0) { Write-Host "Lỗi ở bước 1" -ForegroundColor Red; exit $LASTEXITCODE }

Write-Host "2. Lấy dữ liệu tỷ giá từ API..." -ForegroundColor Cyan
python scripts/02_fetch_api.py
if ($LASTEXITCODE -ne 0) { Write-Host "Lỗi ở bước 2" -ForegroundColor Red; exit $LASTEXITCODE }

Write-Host "3. Phân loại sản phẩm bằng AI/Logic..." -ForegroundColor Cyan
python scripts/03_ai_categorize.py
if ($LASTEXITCODE -ne 0) { Write-Host "Lỗi ở bước 3" -ForegroundColor Red; exit $LASTEXITCODE }

Write-Host "4. Nạp dữ liệu vào DuckDB (Bronze Layer)..." -ForegroundColor Cyan
python scripts/04_load_to_duckdb.py
if ($LASTEXITCODE -ne 0) { Write-Host "Lỗi ở bước 4" -ForegroundColor Red; exit $LASTEXITCODE }

Write-Host "5. Chạy dbt để Transform dữ liệu (Silver & Gold Layers)..." -ForegroundColor Cyan
cd dbt_ecommerce
dbt run
if ($LASTEXITCODE -ne 0) { cd ..; Write-Host "Lỗi ở bước 5 (dbt run)" -ForegroundColor Red; exit $LASTEXITCODE }

Write-Host "6. Chạy dbt test để kiểm tra Data Quality..." -ForegroundColor Cyan
dbt test
if ($LASTEXITCODE -ne 0) { cd ..; Write-Host "Lỗi ở bước 6 (dbt test) - Dữ liệu không đạt chuẩn!" -ForegroundColor Red; exit $LASTEXITCODE }
cd ..

Write-Host "Pipeline hoàn tất thành công!" -ForegroundColor Green
