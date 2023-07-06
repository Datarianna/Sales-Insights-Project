# Creating the Database
```sql
CREATE DATABASE atliq;
```

# Adding the Tables
### Customers
```sql
CREATE TABLE customers (
  customer_code VARCHAR(200),
  customer_name VARCHAR(200),
  customer_type VARCHAR(200)
  );

INSERT INTO customers 
VALUES ('Cus001','Surge Stores','Brick & Mortar'),
('Cus002','Nomad Stores','Brick & Mortar'),
('Cus003','Excel Stores','Brick & Mortar'),
('Cus004','Surface Stores','Brick & Mortar'),
('Cus005','Premium Stores','Brick & Mortar')
;
/* And continued... there are 38 rows in total in the table */
```

### Markets
```sql
CREATE TABLE markets (
  market_code VARCHAR(50),
  markets_name VARCHAR(250),
  zone VARCHAR(250)
);

INSERT INTO markets VALUES
('Mark001','Chennai','South'),
('Mark002','Mumbai','Central'),
('Mark003','Ahmedabad','North'),
('Mark004','Delhi NCR','North'),
('Mark005','Kanpur','North')
;
/* Continued... 15 rows in total */
```

###  Products
```sql
CREATE TABLE products (
  product_code VARCHAR(50),
  product_type VARCHAR(250)
);

INSERT INTO products 
VALUES ('Prod001','Own Brand'),
('Prod002','Own Brand'),
('Prod003','Own Brand'),
('Prod004','Own Brand'),
('Prod005','Own Brand')
;
/* continued... there are 279 products in total */
```

### Transaction Sales
```sql
CREATE TABLE transaction_sales (
  product_code VARCHAR(50),
  customer_code VARCHAR(50),
  market_code VARCHAR(50),
  order_date DATE,
  sales_qty INT,
  sales_amount INT,
  currency VARCHAR(3),
  norm_sales_amount INT
);

INSERT INTO transaction_sales VALUES
('Prod001','Cus001','Mark001','2017-10-10',100,41241,'INR',41241),
('Prod002','Cus003','Mark003','2018-04-06',1,875,'INR',875),
('Prod002','Cus003','Mark003','2018-04-11',1,583,'INR',583),
('Prod002','Cus004','Mark003','2018-06-18',6,7176,'INR',7176),
('Prod003','Cus005','Mark004','2017-11-20',59,500,'USD',41000)
;
/* continued... 991 records in total */
```

### Sales Years
```sql
CREATE TABLE sales_years (
  order_date DATE,
  year INT,
  month_name VARCHAR(50)
);

INSERT INTO sales_year VALUES
('2017-06-01',2017,'June'),
('2017-06-02',2017,'June'),
('2017-06-03',2017,'June'),
('2017-06-04',2017,'June'),
('2017-06-05',2017,'June');
/* continued... 1000 rows in total */
```
