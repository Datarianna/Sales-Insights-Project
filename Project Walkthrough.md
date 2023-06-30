# Sales Insights Project

# About
AtliQ Hardware is a technology company based in India that sells various types of hardware for other companies.

### Problem
AtliQ is unable to track sales accurately and gather proper insight of their performances.

### Objective
The objective of this project is to create a dashboard that provides visual insights on the company's performance that will help managers and stakeholders make better informed decisions based on data.

### Software Used
- Python (Pandas)
- SQL
- Tableau

## Datasets and Data Description
**💲 Transaction Sales Dataset**
- **product_code** *(text)*: Unique identifier for each product.
- **customer_code** *(text)*: Unique identifier for each customer.
- **market_code** *(text)*: Unique identifier for each market.
- **order_date** *(date)*: Date of the transaction order in (YYYY-MM-DD) format.
- **sales_qty** *(num)*: number of the item purchased in the transaction.
- **sales_amount** *(num)*: total sales of the transaction.
- **currency** *(text)*: currency used for the transaction.

**🌍 Markets Dataset**
- **markets_code** *(text)*: Unique identifier for each market.
- **markets_name** *(text)*: Region name of the market.
- **zone** *(text)*: location of the region (North, South, Central)

**🧑 Customers Dataset**
- **customer_code** *(text)*: Unique identifier for each customer.
- **custmer_name** *(text)*: Name of the customer.
- **customer_type** *(text)*: Indicates whether the customer is a Brick & Mortar or E-Commerce store.

**🖱️ Products Dataset**
- **product_code** *(text)*: Unique identifier for each product.
- **product_type** *(text)*: Indicates whether the product in the store is an AtliQ Brand or distributed by another company.

**🗓️ Sales Years Dataset**
- **date** *(date)*: Date of the transaction.
- **cy_date** *(date)*: The date of the transaction, set to the first day of the month of transaction.
- **year** *(date)*: The year the transaction was made.
- **month_name** *(date)*: The month the transaction was made.
- **date_yy_mmm** *(text)*: The day and month of the transaction.

## Research Questions
1. Who are the top five customers for AtliQ each year based on total sales revenue?
2. What is the trend of sales revenue for AtliQ over the past three years?
3. Within the last year, which top three products sold the most in terms of the quantity of sales?
4. How does the sales revenue vary across different regions in India throughout the years?
5. What are the top three products in terms of sales quantity for Brick & Mortar and E-Commerce customers?

# Data Cleaning
### 💲 Cleaning Transaction Sales Dataset

```
ts = pd.read_csv('transaction_sales.csv')
print(ts.head())
```




