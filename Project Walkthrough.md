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
1000 rows x 7 columns
| product_code | customer_code | market_code | order_date | sales_qty | sales_amount | currency |
|--------------|---------------|-------------|------------|-----------|--------------|----------|
|    Prod001   |    Cus001     |	 Mark001   | 2017-10-10 |	   100    |     41241    |	  INR   |
|    Prod001   |    Cus002     |	 Mark002   | 2018-05-08 |	   3      |      -1      |	  INR   |
|    Prod002   |    Cus003     |	 Mark003   | 2018-04-06 |	   1      |      875     |	  INR   |
|    Prod002   |    Cus003     |	 Mark003   | 2018-04-11 |	   1      |      583     |	  INR   |
|    Prod002   |    Cus004     |	 Mark003   | 2018-06-18 |	   6      |      7176    |	  INR   |


1. I first utilized .dropna() to remove any rows that contained null values. Examining the dataset
2. I have identified some rows that had a -1 and 0 under the ‘sales_amount’ column, so I removed those rows from the dataset.
3. Examining the data, there are only two currencies presented in the ‘currency’ column: INR and USD. Many of the rows in this column had an ‘\r’ at the end (ex. INR\r instead of INR), so they were removed.
4. Since some transactions were in USD, I created a new column called ‘norm_sales_amount’ which converts any sales amount in USD to INR.
5. I converted all values under the order_date into a date format.
6. I checked dataset for anymore missing values before putting the new cleaned dataset into a new .csv file.
```
ts = ts.dropna()
ts = ts.drop(ts[(ts['sales_amount']==-1) | (ts['sales_amount']==0)].index)

ts['currency'].str.rstrip("\r")
ts['norm_sales_amount'] = None
ts.loc[ts['currency'] == 'INR', 'norm_sales_amount'] = ts.loc[ts['currency'] == 'INR', 'sales_amount']
ts.loc[ts['currency'] == 'USD','norm_sales_amount'] = ts.loc[ts['currency'] == 'USD','sales_amount']*82
ts['order_date'] = pd.to_datetime(ts['order_date'], dayfirst=False)

missing(ts)
ts.to_csv('clean_transaction_sales.csv', index=False)
```
991 rows x columns
| product_code | customer_code | market_code | order_date | sales_qty | sales_amount | currency | norm_sales_amount |
|--------------|---------------|-------------|------------|-----------|--------------|----------|-------------------|
|    Prod001   |    Cus001     |	 Mark001   | 2017-10-10 |	   100    |     41241    |	  INR   | 41241 |
|    Prod002   |    Cus003     |	 Mark003   | 2018-04-06 |	   1      |     875      |	  INR   | 875 |
|    Prod002   |    Cus003     |	 Mark003   | 2018-04-11 |	   1      |      583     |	  INR   | 583 |
|    Prod002   |    Cus004     |	 Mark003   | 2018-06-18 |	   6      |      7176    |	  INR   | 7176
|    Prod003   |    Cus005     |	 Mark004   | 2017-11-20 |	   59     |      500     |	  USD   | 41000 |

### 🌍 Cleaning Markets Dataset
```
m = pd.read_csv('markets.csv')

print(m.head())
```
| markets_code | markets_name | zone |
|--------------|--------------|------|
|Mark001 |	Chennai |	South |
Mark002	| Mumbai |	Central |
Mark003	| Ahmedabad |	North |
Mark004	| Delhi NCR |	North |
Mark005	| Kanpur |	North |
