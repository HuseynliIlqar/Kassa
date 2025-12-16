📘 Kassa Sistemi – API Dokumentasiyası
Giriş
Bu sistem pərakəndə satış və stok idarəetməsi üçün hazırlanmışdır. API-lər aşağıdakı əsas funksionallıqları təmin edir:
    • İstifadəçi (mərkəz, market, kassir və s.) idarəsi
    • Məhsul, tədarükçü və kateqoriya idarəsi
    • Satış və qaytarma əməliyyatları
    • Stok hərəkətləri və sessiyalar
    • Qiymət dəyişiklikləri və barkod əsaslı çap

🔐 Auth – Token Sistemi
1.1 Token əldə et
POST /api/token/
Request:
{
  "username": "kassir",
  "password": "parol"
}
Response:
{
  "access": "JWT_ACCESS_TOKEN",
  "refresh": "JWT_REFRESH_TOKEN"
}
1.2 Token yenilə
POST /api/token/refresh/
Request:
{
  "refresh": "JWT_REFRESH_TOKEN"
}
Response:
{
  "access": "NEW_ACCESS_TOKEN"
}

👤 İstifadəçi Yarat (Mərkəz istifadəçisi)
POST /
Authorization: Bearer <access_token>
Body:
{
  "username": "kassir1",
  "password": "secret",
  "is_stock_accses": true,
  "is_cash_desk_accses": true,
  "is_panel_accses": false,
  "is_price_accses": true
}
Response:
{
  "id": 3,
  "username": "kassir1",
  "is_market": true,
  "is_stock_accses": true,
  ...
}

🛒 Satış Əməliyyatları (Cash Desk)
2.1 Satış yaradılma (Səbət yaradılır)
POST /cashdesk/sale/
Body:
{
  "items": [
    {"product": 1, "quantity": 2}
  ]
}
2.2 Checkout – səbəti satışa çevirmək
POST /cashdesk/sale/checkout/
Response:
{
  "detail": "Səbət satışa çevrildi.",
  "sale_id": 15
}
2.3 Kassir X-Rapor
GET /cashdesk/sale/day-summary/
Response:
Kassirin bu günkü satışlarının cəmi və detallı siyahısı.
2.4 Kassir Z-Rapor (Hesabat + sıfırlama)
POST /cashdesk/sale/reset-sales/
Response:
Satışlar is_counted=true edilir.
2.5 Məhsul Qaytarma
POST /cashdesk/sale/return-item/
Body:
{
  "sale_id": 5,
  "sale_item_id": 11,
  "return_quantity": 1
}

📦 Stok Hərəkətləri
3.1 Bütün məhsulları (market məhsulları) gətir
GET /markets/list/
3.2 Tək-tək stok hərəkəti əlavə et
POST /markets/stock/
Body:
{
  "market_product_id": 2,
  "movement_type": "in",
  "quantity": 10
}
3.3 Toplu stok hərəkəti (StockBulk)
POST /markets/stock-bulk/
Body:
{
  "movement_type": "out",
  "comment": "Təmizlik səbəbi ilə",
  "items": [
    {"product_barcode": "123456", "quantity": 5}
  ]
}
3.4 Stock Session siyahısı
GET /markets/stock-sessions/
3.5 Session-a aid qaimə (HTML)
GET /markets/stock-session/<id>/receipt/

📦 Məhsullar
4.1 Məhsul əlavə et
POST /products/products/
Authorization: Bearer <center_access_token>
Body:
{
  "barcode": "999001",
  "name": "Yeni Məhsul",
  "category": "Şirniyyat",
  "unit": "ədəd",
  "supplier": "Test",
  "price": 3.5
}
4.2 Qiyməti dəyiş (update=True olur)
PATCH /products/products/<id>/
Body-də price dəyişdirilir.

📋 Qiymət Dəyişiklikləri və Çap
5.1 Dəyişmiş qiymət siyahısını al
GET /products/products/price-change-list/
5.2 Dəyişmiş qiymətləri HTML olaraq çap et
POST /products/products/price-change-list/
Response: HTML
5.3 Seçilmiş barkodlara əsasən qiymətləri çap et
POST /products/products/get-prices-by-barcodes-html/
Body:
{
  "barcodes": ["1234567890", "9876543210"]
}


🔖 Kateqoriya və Tədarükçü
6.1 Kateqoriya əlavə et
POST /products/categories/
{ "name": "Süd məhsulları" }
6.2 Tədarükçü əlavə et
POST /products/suppliers/
{
  "name": "Məhsullar MMC",
  "phone": "0501234567",
  "address": "Bakı, Yasamal"
}

