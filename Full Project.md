# Sales Insights Project

# About
AtliQ Hardware is a technology company based in India that sells various types of hardware for other companies.

### Problem
AtliQ is unable to track sales accurately and gather proper insight of their performances.

### Objective
The objective of this project is to create a dashboard that provides visual insights on the company's performance that will help managers and stakeholders make better informed decisions based on data.

### Software Used
- Python (Pandas)
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

```python
print('- - - - - Transaction Sales - - - - -')
print('\nOriginal Dataset:')
ts = pd.read_csv('transaction_sales.csv')
print(ts.head())
```
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
5. Converted all values under the order_date into a date format.
6. Checked the dataset for anymore missing values before putting the new cleaned dataset into a new .csv file.
```python
ts = ts.dropna()
ts = ts.drop(ts[(ts['sales_amount']==-1) | (ts['sales_amount']==0)].index)
ts = ts.replace('INR\r','INR').replace('USD\r','USD')
ts['norm_sales_amount'] = ts['sales_amount']
ts.loc[ts['currency'] == 'USD','norm_sales_amount'] = ts.loc[ts['currency'] == 'USD','sales_amount']*82
ts['order_date'] = pd.to_datetime(ts['order_date'], dayfirst=False)

print('')
duplicate(ts)
missing(ts)

print('\nCleaned Dataset:')
print(ts.head())
ts.to_csv('clean_transaction_sales.csv', index=False)
```
| product_code | customer_code | market_code | order_date | sales_qty | sales_amount | currency | norm_sales_amount |
|--------------|---------------|-------------|------------|-----------|--------------|----------|-------------------|
|    Prod001   |    Cus001     |	 Mark001   | 2017-10-10 |	   100    |     41241    |	  INR   | 41241 |
|    Prod002   |    Cus003     |	 Mark003   | 2018-04-06 |	   1      |     875      |	  INR   | 875 |
|    Prod002   |    Cus003     |	 Mark003   | 2018-04-11 |	   1      |      583     |	  INR   | 583 |
|    Prod002   |    Cus004     |	 Mark003   | 2018-06-18 |	   6      |      7176    |	  INR   | 7176
|    Prod003   |    Cus005     |	 Mark004   | 2017-11-20 |	   59     |      500     |	  USD   | 41000 |

### 🌍 Cleaning Markets Dataset
```python
print('\n- - - - - Market - - - - -')
print('\nOriginal Dataset:')
m = pd.read_csv('markets.csv')
print('Top 5 rows')
print(m.head())
print('Bottom 5 rows')
print(m.tail())
```

Top 5 rows
| markets_code | markets_name | zone |
|--------------|--------------|------|
|Mark001 |	Chennai |	South |
Mark002	| Mumbai |	Central |
Mark003	| Ahmedabad |	North |
Mark004	| Delhi NCR |	North |
Mark005	| Kanpur |	North |

Bottom 5 rows
| markets_code | markets_name | zone |
|--------------|--------------|------|
| Mark013 |	Bhopal |	Central |
| Mark014	| Hyderabad	| South |
| Mark015 |	Bhubaneshwar | South |
| Mark097 | New York | NaN |	
| Mark999 |	Paris	| NaN |


1. All rows with NA values were dropped, which happened to be the New York and Paris markets.
2. The column name ‘markets_code’ was changed to ‘market_code’ for consistency.
3. Used duplicated() to check for any row that is a duplicated. No duplicate rows were detected.
4. Checked the dataset for anymore missing values before putting the new cleaned dataset into a new .csv file.
```python
m = m.dropna()
m = m.rename(columns={'markets_code':'market_code'})

print('')
duplicate(m)
missing(m)

print('\nCleaned Dataset:')
print('Top 5 rows')
print(m.head())
print('Bottom 5 rows')
print(m.tail())
m.to_csv('clean_markets.csv', index=False)
```
Top 5 rows
| market_code | markets_name | zone |
|--------------|--------------|------|
|Mark001 |	Chennai |	South |
Mark002	| Mumbai |	Central |
Mark003	| Ahmedabad |	North |
Mark004	| Delhi NCR |	North |
Mark005	| Kanpur |	North |

Bottom 5 rows
| market_code | markets_name | zone |
|--------------|--------------|------|
| Mark011	| Nagpur |	Central |
| Mark012	| Surat	| North |
| Mark013	| Bhopal	| Central |
| Mark014	| Hyderabad	| South |
| Mark015	| Bhubaneshwar |	South |


### 🧑 Cleaning Customers Dataset
```python
print('\n- - - - - Customers - - - - -')
print('\nOriginal Dataset:')
c = pd.read_csv('customers.csv')
print(c.head())
```
|customer_code|custmer_name|customer_type|
|-------------|------------|-------------|
|Cus001|	Surge Stores|	Brick & Mortar|
|Cus002	|Nomad Stores	|Brick & Mortar|
|Cus003	|Excel Stores	|Brick & Mortar|
|Cus004	|Surface Stores|	Brick & Mortar|
|Cus005	|Premium Stores	|Brick & Mortar|


1. I fixed the misspelling of the ‘custmer_name’ column.
2. Dropped any NA values from the dataset.
3. Checked for any duplicates in the dataset and none were detected.
4. I checked dataset for anymore missing values before putting the new cleaned dataset into a new .csv file.
```python
c = c.rename(columns={'custmer_name':'customer_name'})
c = c.dropna()
print('')
duplicate(c)
missing(c)

print('\nCleaned Dataset:')
print(c.head())
c.to_csv('clean_customers.csv', index=False)
```
|customer_code|customer_name|customer_type|
|-------------|------------|-------------|
|Cus001|	Surge Stores|	Brick & Mortar|
|Cus002	|Nomad Stores	|Brick & Mortar|
|Cus003	|Excel Stores	|Brick & Mortar|
|Cus004	|Surface Stores|	Brick & Mortar|
|Cus005	|Premium Stores	|Brick & Mortar|


### 🖱️ Cleaning Products Dataset
```python
print('\n- - - - - Products - - - - -')
print('Original Dataset:')
p = pd.read_csv('products.csv')
print(p.head())
```
|product_code |product_type|
|-------------|------------|
|Prod001 | Own Brand\r |
|   Prod002 | Own Brand\r|
|  Prod003  |Own Brand\r|
|  Prod004  |Own Brand\r|
|  Prod005  |Own Brand\r|
1. In this dataset, there is formatting issues under the ‘product_type’ column due to extra spacing, similarly to the currencies in the Transaction Sales dataset. I removed ‘\r’ from all rows.
2. Checked for duplicate rows, to which there were none.
3. I checked dataset for anymore missing values before putting the new cleaned dataset into a new .csv file.
```python
p['product_type'] = p['product_type'].str.rstrip("\r")
p = p.dropna()
print('')
duplicate(p)
missing(p)

print('\nCleaned Dataset:')
print(p.head())
p.to_csv('clean_products.csv', index=False)
```
|product_code |product_type|
|-------------|------------|
|Prod001 | Own Brand |
|   Prod002 | Own Brand|
|  Prod003  |Own Brand|
|  Prod004  |Own Brand|
|  Prod005  |Own Brand|

### 🗓️ Cleaning Sales Years Dataset
```python
print('\n- - - - - Sales Years - - - - -')
sy = pd.read_csv('sales_years.csv')
print('Original Dataset:')
print(sy.head())
```
|date|cy_date|year|month_name|date_yy_mmm|
|-------------|------------|-------------|-------------|-------------|
|2017-06-01|  2017-06-01 | 2017 |      June  |  17-Jun\r|
|2017-06-02 | 2017-06-01  |2017  |     June   | 17-Jun\r|
|  2017-06-03|  2017-06-01 | 2017 |      June  |  17-Jun\r|
|  2017-06-04 | 2017-06-01 | 2017  |     June  |  17-Jun\r|
|  2017-06-05 | 2017-06-01 | 2017   |    June  |  17-Jun\r|
1. Dropped the ‘date_yy_mmm’ and ‘cy_date’ column since I felt that they were redundant.
2. Converted the ‘date’ column into date format to ensure proper formatting.
3. Dropped the ‘year’ and ‘month_name’ columns from the dataset and created new versions of them. This time, I extracted the year portion of the ‘date’ column and put it into a new ‘year’ column. Then, I extracted the month portion from the ‘date’ column and put it into a new ‘month_name’ column while also making sure that it is written in the month name and not the month number. I did this to really make sure that they are in date format.
4. Checked for duplicate rows, to which there were none.
5. I checked dataset for anymore missing values before putting the new cleaned dataset into a new .csv file.
```python
sy.drop("date_yy_mmm", axis=1, inplace=True)
sy.drop("cy_date", axis=1, inplace=True)
sy['date'] = pd.to_datetime(sy['date'], dayfirst=False)
sy['year'] = sy['date'].dt.year
sy['month_name'] = sy['date'].dt.month_name()
print('')
duplicate(sy)
missing(sy)

print('\nCleaned Dataset:')
print(sy.head())
sy.to_csv('clean_sales_years.csv', index=False)
```
|date|year|month_name|
|---|-----|-----|
|2017-06-01|2017      |June
| 2017-06-02|  2017    |   June
| 2017-06-03 | 2017     |  June
| 2017-06-04  |2017      | June
| 2017-06-05  |2017       |June

# ERD Diagram: Datasets represents a star schema
![image](https://github.com/Datarianna/Sales-Insights-Project/assets/138058039/10222a20-f42a-4ff8-a1a4-8c0ac69d3e3e)

# Querying Results and Analysis
### Question 1: Who are the top five customers for AtliQ each year based on total sales revenue?
```python

```
### Question 2: What is the trend of sales revenue for AtliQ over the past three years?
```python

```
### Question 3: Within the last year, which top three products sold the most in terms of the quantity of sales?
```python

```
### Question 4: How does the sales revenue vary across different regions in India throughout the years?
```python

```
### Question 5: What are the top three products in terms of sales quantity for Brick & Mortar and E-Commerce customers?
```python

```

# Tableau Dashboard


