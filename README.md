
---

# 📘 Kassa Sistemi – API Documentation

## 📌 Overview

Bu layihə **pərakəndə satış (POS)** və **stok idarəetməsi** üçün hazırlanmış RESTful API sistemidir. Sistem bir neçə rol və modul üzərində qurulub və aşağıdakı əsas biznes proseslərini əhatə edir:

* İstifadəçi və rol idarəetməsi (mərkəz, market, kassir)
* Məhsul, kateqoriya və tədarükçü idarəsi
* Satış, checkout və qaytarma əməliyyatları
* Stok hərəkətləri və stok sessiyaları
* Qiymət dəyişiklikləri və barkod əsaslı çap funksiyaları

API JWT token əsaslı autentifikasiya ilə qorunur.

---

## 🔐 Authentication (JWT)

### Token əldə etmək

**POST** `/api/token/`

```json
{
  "username": "kassir",
  "password": "parol"
}
```

**Response**

```json
{
  "access": "JWT_ACCESS_TOKEN",
  "refresh": "JWT_REFRESH_TOKEN"
}
```

---

### Token yeniləmək

**POST** `/api/token/refresh/`

```json
{
  "refresh": "JWT_REFRESH_TOKEN"
}
```

**Response**

```json
{
  "access": "NEW_ACCESS_TOKEN"
}
```

---

## 👤 User Management

### İstifadəçi yaratmaq (Mərkəz səviyyəsi)

**POST** `/`

**Headers**

```
Authorization: Bearer <access_token>
```

**Body**

```json
{
  "username": "kassir1",
  "password": "secret",
  "is_stock_accses": true,
  "is_cash_desk_accses": true,
  "is_panel_accses": false,
  "is_price_accses": true
}
```

**Response**

```json
{
  "id": 3,
  "username": "kassir1",
  "is_market": true,
  "is_stock_accses": true
}
```

---

## 🛒 Cash Desk – Satış Əməliyyatları

### Satış yaratmaq (Səbət)

**POST** `/cashdesk/sale/`

```json
{
  "items": [
    { "product": 1, "quantity": 2 }
  ]
}
```

---

### Checkout (səbəti satışa çevirmək)

**POST** `/cashdesk/sale/checkout/`

**Response**

```json
{
  "detail": "Səbət satışa çevrildi.",
  "sale_id": 15
}
```

---

### Kassir X-Rapor (Günlük icmal)

**GET** `/cashdesk/sale/day-summary/`

> Kassirin gün ərzində etdiyi satışların ümumi məbləği və detallı siyahısı.

---

### Kassir Z-Rapor (Hesabat + sıfırlama)

**POST** `/cashdesk/sale/reset-sales/`

> Satışlar `is_counted=true` olaraq işarələnir.

---

### Məhsul qaytarma

**POST** `/cashdesk/sale/return-item/`

```json
{
  "sale_id": 5,
  "sale_item_id": 11,
  "return_quantity": 1
}
```

---

## 📦 Stock Management

### Market məhsullarını siyahıla

**GET** `/markets/list/`

---

### Tək stok hərəkəti

**POST** `/markets/stock/`

```json
{
  "market_product_id": 2,
  "movement_type": "in",
  "quantity": 10
}
```

---

### Toplu stok əməliyyatı

**POST** `/markets/stock-bulk/`

```json
{
  "movement_type": "out",
  "comment": "Təmizlik səbəbi ilə",
  "items": [
    { "product_barcode": "123456", "quantity": 5 }
  ]
}
```

---

### Stok sessiyaları

**GET** `/markets/stock-sessions/`

---

### Sessiyaya aid qaimə (HTML)

**GET** `/markets/stock-session/<id>/receipt/`

---

## 📦 Products

### Məhsul əlavə etmək

**POST** `/products/products/`

**Headers**

```
Authorization: Bearer <center_access_token>
```

```json
{
  "barcode": "999001",
  "name": "Yeni Məhsul",
  "category": "Şirniyyat",
  "unit": "ədəd",
  "supplier": "Test",
  "price": 3.5
}
```

---

### Qiymət yeniləmək

**PATCH** `/products/products/<id>/`

> `price` dəyişdirildikdə məhsul avtomatik olaraq `update=True` vəziyyətinə keçir.

---

## 📋 Price Change & Printing

### Qiyməti dəyişmiş məhsullar

**GET** `/products/products/price-change-list/`

---

### Qiymətləri HTML formatında çap et

**POST** `/products/products/price-change-list/`

**Response**: HTML

---

### Barkodlara görə qiymət çapı

**POST** `/products/products/get-prices-by-barcodes-html/`

```json
{
  "barcodes": ["1234567890", "9876543210"]
}
```

---

## 🔖 Categories & Suppliers

### Kateqoriya əlavə et

**POST** `/products/categories/`

```json
{
  "name": "Süd məhsulları"
}
```

---

### Tədarükçü əlavə et

**POST** `/products/suppliers/`

```json
{
  "name": "Məhsullar MMC",
  "phone": "0501234567",
  "address": "Bakı, Yasamal"
}
```

---

## 🧩 Notes

* API JWT authentication tələb edir
* HTML response-lar printer və ya POS ekranları üçün nəzərdə tutulub
* Rollara əsaslanan access control tətbiq olunur

---
