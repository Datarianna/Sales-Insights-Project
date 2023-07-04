# Sales Insights Project

# About
AtliQ Hardware is a technology company based in India and was established in 2017. The company sells various types of computer hardware and devices to several companies throughout India and the United States.

### Problem
Atliq has an issue where they are unable to track sales accurately and gather proper insight of their performances. Their data is solely stored in spreadsheets, which can be difficult to properly see their business performance. They rely on managers to give them verbal reports on how the business is doing, which can be problematic because they may tend to make it seem like the company is doing better than it really is.

### Objective
The objective of this project is to gather valuable sales insights on the company's peformance and to create an interactive dashboard that will provide visual insights on the company's performance. This dashboard will help managers and stakeholders make better informed decisions based on data.

### Software Used
- Python (Pandas) for data cleaning and manipulation
- Tableau for visualizations and the dashboard

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
1. Who are the top five customers for AtliQ in 2019 based on total sales revenue??
2. What is the trend of total sales revenue for AtliQ in 2017-2019?
3. From 2017-2020, which three products sold the most units?
4. How does the sales revenue vary across different regions in India throughout the years?
5. What is the total sales revenue and total number of units sold for each customer type in 2019?

# Data Cleaning
Before cleaning, I created the functions missing() and duplicate() which checks if the specified dataframe contains any NA or duplicate values.
```python
def missing(df):
  missing = df.isna().any().any()
  if missing:
    print('Missing values detected')
  else:
    print('No missing values')

def duplicate(df):
  duplicate = df.duplicated().any().any()
  if duplicate:
    print('Duplicate values present')
  else:
    print('No duplicate values')
```
### 💲 Cleaning Transaction Sales Dataset

```python
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
1. I first utilized .dropna() to remove any rows that contained null values. Examining the dataset, I have identified some rows that had a -1 and 0 under the ‘sales_amount’ column, so I removed those rows from the dataset.
2. There are only two currencies presented in the ‘currency’ column: INR and USD. Many of the rows in this column had an ‘\r’ at the end (ex. INR\r instead of INR), so they were replaced with a proper format.
3. Since some transactions were in USD, I created a new column called ‘norm_sales_amount’ which contains USD sales amounts converted to INR.
4. Converted all values under the order_date into a date format to ensure the correct data type.
5. Used duplicated() to check for any row that is a duplicated. No duplicate rows were detected.
6. Checked the dataset for anymore missing values before putting the new cleaned dataset into a new .csv file.
```python
ts = ts.dropna()
ts = ts.drop(ts[(ts['sales_amount']==-1) | (ts['sales_amount']==0)].index)
ts = ts.replace('INR\r','INR').replace('USD\r','USD')
ts['norm_sales_amount'] = ts['sales_amount']
ts.loc[ts['currency'] == 'USD','norm_sales_amount'] = ts.loc[ts['currency'] == 'USD','sales_amount']*82
ts['order_date'] = pd.to_datetime(ts['order_date'], dayfirst=False)

duplicate(ts)
missing(ts)

print(ts.head())
ts.to_csv('clean_transaction_sales.csv', index=False)
```
| product_code | customer_code | market_code | order_date | sales_qty | sales_amount | currency | norm_sales_amount |
|--------------|---------------|-------------|------------|-----------|--------------|----------|-------------------|
|    Prod001   |    Cus001     |	 Mark001   | 2017-10-10 |	   100    |     41241    |	  INR   |       4124        |
|    Prod002   |    Cus003     |	 Mark003   | 2018-04-06 |	   1      |     875      |	  INR   |        875        |
|    Prod002   |    Cus003     |	 Mark003   | 2018-04-11 |	   1      |      583     |	  INR   |        583        |
|    Prod002   |    Cus004     |	 Mark003   | 2018-06-18 |	   6      |      7176    |	  INR   |       7176        |       
|    Prod003   |    Cus005     |	 Mark004   | 2017-11-20 |	   59     |      500     |	  USD   |      41000        |    

### 🌍 Cleaning Markets Dataset
```python
m = pd.read_csv('markets.csv')
print(m.head())
print(m.tail())
```
Top 5 rows
| markets_code | markets_name | zone  |
|--------------|--------------|-------|
|    Mark001   |	  Chennai   |	South |
|    Mark002 	 |    Mumbai    |Central|
|    Mark003 	 |   Ahmedabad  |	North |
|    Mark004	 |   Delhi NCR  |	North |
|    Mark005	 |    Kanpur    |	North |

Bottom 5 rows
| markets_code | markets_name | zone  |
|--------------|--------------|-------|
|    Mark013   |	  Bhopal    |Central|
|    Mark014	 |  Hyderabad 	| South |
|    Mark015   | Bhubaneshwar | South |
|    Mark097   |   New York   |  NaN  |	
|    Mark999   |	  Paris   	|  NaN  |
1. I used .dropna() to remove rows with NA values. The values dropped happened to be the New York and Paris markets.
2. The column name ‘markets_code’ was changed to ‘market_code’ for consistency and to make joins easier to do for analysis.
3. Used duplicated() to check for any row that is a duplicated. No duplicate rows were detected.
4. Checked the dataset for anymore missing values before putting the new cleaned dataset into a new .csv file.
```python
m = m.dropna()
m = m.rename(columns={'markets_code':'market_code'})

print('')
m = m.dropna()
m = m.rename(columns={'markets_code':'market_code'})

duplicate(m)
missing(m)

print(m.head())
print(m.tail())
m.to_csv('clean_markets.csv', index=False)
```
Top 5 rows
| market_code | markets_name |  zone  |
|--------------|--------------|-------|
|    Mark001   |  	Chennai   |	South |
|    Mark002 	 |    Mumbai    |Central|
|    Mark003	 |   Ahmedabad  |	North |
|    Mark004	 |   Delhi NCR  |	North |
|    Mark005	 |     Kanpur   |	North |

Bottom 5 rows
| market_code | markets_name |  zone  |
|--------------|-------------|--------|
|    Mark011   |    Nagpur   |Central |
|    Mark012 	 |    Surat	   | North  |
|    Mark013	 |    Bhopal	 | Central|
|    Mark014	 |  Hyderabad	 | South  |
|    Mark015   | Bhubaneshwar|	South |


### 🧑 Cleaning Customers Dataset
```python
c = pd.read_csv('customers.csv')
print(c.head())
```
|customer_code| custmer_name | customer_type|
|-------------|--------------|--------------|
|    Cus001   |	Surge Stores |Brick & Mortar|
|    Cus002	  |Nomad Stores	 |Brick & Mortar|
|    Cus003	  | Excel Stores |Brick & Mortar|
|    Cus004  	|Surface Stores|Brick & Mortar|
|    Cus005	  |Premium Stores|Brick & Mortar|


1. I fixed the misspelling of the ‘custmer_name’ column.
2. Dropped any NA values from the dataset.
3. Checked for any duplicates in the dataset and none were detected.
4. I checked dataset for anymore missing values before putting the new cleaned dataset into a new .csv file.
```python
c = c.rename(columns={'custmer_name':'customer_name'})
c = c.dropna()

duplicate(c)
missing(c)

print(c.head())
c.to_csv('clean_customers.csv', index=False)
```
|customer_code|customer_name |customer_type |
|-------------|--------------|--------------|
|    Cus001   |	Surge Stores |Brick & Mortar|
|    Cus002	  |Nomad Stores	 |Brick & Mortar|
|    Cus003	  |Excel Stores	 |Brick & Mortar|
|    Cus004  	|Surface Stores|Brick & Mortar|
|    Cus005	  |Premium Stores|Brick & Mortar|


### 🖱️ Cleaning Products Dataset
```python
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
1. In this dataset, there is formatting issues under the ‘product_type’ column due to extra spacing, similarly to the currencies in the Transaction Sales dataset. I removed ‘\r’ from all rows that had this.
2. Checked for duplicate rows, to which there were none.
3. I checked dataset for anymore missing values before putting the new cleaned dataset into a new .csv file.
```python
p['product_type'] = p['product_type'].str.rstrip("\r")
p = p.dropna()

duplicate(p)
missing(p)

print(p.head())
p.to_csv('clean_products.csv', index=False)
```
|product_code|product_type|
|-------------|-----------|
|   Prod001   | Own Brand |
|   Prod002   | Own Brand |
|   Prod003   | Own Brand |
|   Prod004   | Own Brand |
|   Prod005   | Own Brand |

### 🗓️ Cleaning Sales Years Dataset
```python
sy = pd.read_csv('sales_years.csv')
print(sy.head())
```
|   date   | cy_date  |year|month_name|date_yy_mmm|
|----------|----------|----|----------|-----------|
|2017-06-01|2017-06-01|2017|   June   |  17-Jun\r |
|2017-06-02|2017-06-01|2017|   June   |  17-Jun\r |
|2017-06-03|2017-06-01|2017|   June   |  17-Jun\r |
|2017-06-04|2017-06-01|2017|   June   |  17-Jun\r |
|2017-06-05|2017-06-01|2017|   June   |  17-Jun\r |
1. Dropped the ‘date_yy_mmm’ and ‘cy_date’ column since I felt that they were redundant.
2. Renamed the 'date' column to 'order_date' to make joins easier, as well as converted the ‘order_date’ column into date format to ensure proper formatting.
4. Extracted the year portion of the ‘date’ column and used it to replace the values in the 'year.' Then, I extracted the month portion from the ‘order_date’ column and did the same. This was to ensure that the columns are in the proper format.
5. Checked for duplicate rows, to which there were none.
6. I checked dataset for anymore missing values before putting the new cleaned dataset into a new .csv file.
```python
sy.drop("date_yy_mmm", axis=1, inplace=True)
sy.drop("cy_date", axis=1, inplace=True)
sy = sy.rename(columns={'date':'order_date'})
sy['order_date'] = pd.to_datetime(sy['order_date'], dayfirst=False)
sy['year'] = sy['order_date'].dt.year
sy['month_name'] = sy['order_date'].dt.month_name()

duplicate(sy)
missing(sy)

print(sy.head())
sy.to_csv('clean_sales_years.csv', index=False)
```
|order_date|year |month_name|
|----------|-----|----------|
|2017-06-01|2017 |   June   |
|2017-06-02|2017 |   June   |
|2017-06-03|2017 |   June   |
|2017-06-04|2017 |   June   |
|2017-06-05|2017 |   June   |

# ERD Diagram: Datasets represents a star schema
![image](https://github.com/Datarianna/Sales-Insights-Project/assets/138058039/10222a20-f42a-4ff8-a1a4-8c0ac69d3e3e)

# Querying Results and Analysis
### Question 1: Who are the top five customers for AtliQ in 2019 based on total sales revenue?
I first created a left join between the Transaction Sales (left) and Customer (right) Datasets.
```python
join_ts_c = pd.merge(ts, c, on='customer_code', how='left')
print(join_ts_c.head())
```
|product_code |customer_code| market_code| order_date|  sales_qty | sales_amount |currency|norm_sales_amount|customer_name|customer_type|
|-------------|-------------|------------|-----------|------------|--------------|--------|-----------------|-------------|-------------|
| Prod001     | Cus001      |Mark001     | 2017-10-10|     100    |     41241   |   INR      |        41241  |  Surge Stores | Brick & Mortar
|   Prod002   |    Cus003   |Mark003     | 2018-04-06 |    1      |   875     | INR        |        875  |  Excel Stores | Brick & Mortar
|  Prod002    |   Cus003    |Mark003     | 2018-04-11 |      1    |   583    |  INR        |        583  |  Excel Stores | Brick & Mortar
|   Prod002   |   Cus004    |Mark003     | 2018-06-18|     6      | 7176   |   INR        |       7176 | Surface Stores | Brick & Mortar
|  Prod003    |  Cus005     |Mark004     |2017-11-20  |   59      | 500    |  USD          |    41000 | Premium Stores | Brick & Mortar

1. Created a filter that will only contain rows with an order date within the year 2019.
2. Grouped the filtered dataset by customers and summed up the total normalized sales amount for each customer.
3. Sorted the dataframe in descending order and ensured to only include the top five customers and their total sales.
```python
year_filter = join_ts_c[(join_ts_c['order_date']>='2019-01-01') & (join_ts_c['order_date']<='2019-12-31')]
top_five_customers = year_filter.groupby('customer_name')['norm_sales_amount'].sum().sort_values(ascending=False).head(5)
print(top_five_customers)
```
|customer_name         | |
|----------------------|-|
|Electricalsara Stores |917920
|Electricalslytical    |629237
|Logic Stores          |525379
|Path                  |454822
|Info Stores           |347682

Name: norm_sales_amount, dtype: int64

**Tableau Graph**:

![image](https://github.com/Datarianna/Sales-Insights-Project/assets/138058039/fd061071-7035-46b2-a0a6-a657005f8c22)

**Answer**: In 2019, Electricalsara Stores spent the most money on AtliQ hardware products totaling ₹917,920 ($11,199). The second highest spending company is Electricalslytical with a spending amount of ₹629,237 ($7,677). The third highest spender in 2019 was Logic Stores with a total of ₹525,379 ($6,410). The fourth highest spender is Path, with a spending amount of ₹454822 ($5,549). The fifth and last highest spender is Info Stores, totaling ₹347,682 ($4,242)

### Question 2: What is the trend of total sales revenue for AtliQ in 2017-2019?
1. Created a filter that filters in rows that are within the years 2017-2019.
2. Grouped the filtered dataset by the order date year, then summed up the total normalized sales amount for each year.
```python
year_filter = ts[(ts['order_date']>='2017-01-01') & (ts['order_date']<='2019-12-31')]
total_rev_years = year_filter.groupby(year_filter['order_date'].dt.year)['norm_sales_amount'].sum()
print(total_rev_years)
```
|order_date| |
|----------|-|
|2017  |  1895109
|2018  |  7687469
|2019  |  3296370

Name: norm_sales_amount, dtype: int64

**Tableau Graph**:

![image](https://github.com/Datarianna/Sales-Insights-Project/assets/138058039/e0f6db0c-e87d-4848-a4e8-41ee0d35d166)

**Answer**: In 2017 during the early stages of AtliQ, they made ₹1,895,109 ($23,122) as their first, initial revenue. Then, in 2018, AtliQ experience a huge 305.648% increase in revenue, totaling a revenue of ₹7,687,469 ($93,794). This may be due to the fact that they have established strong business strategies that have allowed their revenue to grow tremendously. However, the frequency of sales decreased dramatically and the total revenue in 2019 plummeted by 57.1202% with a revenue of ₹3,296,370 ($40219). There are several possibilities whyy this could be the case such as that the strategies used in 2018 may no longer working due to increased competitors and their ability to mimic their strategies. It could also be due to economic factors out of the company's control, customer buying power changing, problems in business operations, etc.

### Question 3: From 2017-2020, which three products sold the most units?
1. Created a filter that filters in rows thar are within 2017-2020.
2. Created a for loop that goes through every unique year from the 'order_date' column. Each row is filtered by the 'year_data' so that only the year is represented.
3. The 'year_data' variable is grouped according to 'product_code.' I calculated the sum of sales quantity each product and presented only the products with the three highest sales quantities.
4. The for loop repeats the process for each year.
```python
year_filter = ts[(ts['order_date'] >= '2017-01-01') & (ts['order_date'] <= '2020-12-31')]
for year in year_filter['order_date'].dt.year.unique():
  year_data = year_filter[year_filter['order_date'].dt.year == year]
  top_three = year_data.groupby('product_code')['sales_qty'].sum().nlargest(3)
  print(f"\nTop 3 products sold in {year}:")
  print(top_three)
```
**2017**
product_code| |
------------|-|
Prod003  |  1512
Prod013   |  582
Prod001   |  200

Name: sales_qty, dtype: int64

**2018**
product_code| |
------------|-|
Prod018  |  2075
Prod016  |  1032
Prod013   |  495

Name: sales_qty, dtype: int64

**2019**
product_code| |
------------|-|
Prod005  |  946
Prod016   | 872
Prod018   | 727

Name: sales_qty, dtype: int64

**2020**
product_code| |
------------|-|
Prod005  |  34
Prod011   |  4

Name: sales_qty, dtype: int64

**Tableau Graph**:

![image](https://github.com/Datarianna/Sales-Insights-Project/assets/138058039/7468ed78-5da7-49e7-a544-ef28f64b9ecd)


**Answer**: In 2017, the most popular products sold from AtliQ were Prod003, Prod013, and Prod001. In 2018, the most popular products were Prod005, Prod018, Prod016, and Prod013. 2019 had Prod005, Prod016, and Prod018 as the highest sold products. Lastly, 2020 had Prod005 and Prod011 as their highest selling products. Seen in the table and the graph, Prod013, Prod018, and Prod018 remain as AtliQ's most popular products since they were consistently the most popular products sold for more than a year. There is a noticeable shift in top products from 2018-2020 as less customers purchased less Prod016 and Prod018 in 2019 than they did in 2018, while Prod005 outsold both of them in 2019. This would suggest some shift in the market demand for products.

### Question 4: How does the sales revenue vary across different regions in India throughout the years?
I first left joined the Transaction Sales and Market Datasets, then created a 'year' column that has all years of the transactions extracted from the 'oter_date' column. This is important for grouping the data by year later on.
```python
join_ts_m = pd.merge(ts, m, on='market_code', how='left')
join_ts_m['year'] = pd.to_datetime(join_ts_m['order_date']).dt.year
print(join_ts_m.head())
```
|product_code| customer_code| market_code| order_date | sales_qty | sales_amount | currency | norm_sales_amount | markets_name | zone | year|
|-|-|-|-|-|-|-|-|-|-|-|
|   Prod001  |   Cus001     |  Mark001   | 2017-10-10 |    100    |     41241    |  INR     |         41241     | Chennai      | South |2017
|      Prod002|Cus003  |   Mark003| 2018-04-06   |       1|875   |   INR     |           875  |  Ahmedabad | North|2018
|      Prod002    |    Cus003   |  Mark003 |2018-04-11     |     1      |     583    |  INR          |      583|Ahmedabad|  North|2018
|      Prod002    |    Cus004  |   Mark003 |2018-06-18     |     6     |     7176   |   INR      |         7176 |   Ahmedabad|North|2018
|      Prod003    |    Cus005  |   Mark004 |2017-11-20    |     59     |      500   |   USD    |          41000 |   Delhi NCR | North|2017

Once left joined, I grouped the dataframe by zone and the name of the market, the summed up the total sales amount for each market.
```python
sales_regions = join_ts_m.groupby(['year','zone','markets_name'])['norm_sales_amount'].sum()
print(sales_regions.to_string())
```
|year | zone  |   markets_name |
|-|-|-|
2017 | Central | Mumbai      |     430502|
     | North   | Delhi NCR   |    1092377|
     |         | Kanpur      |       2628|
     | South   | Chennai     |     369602|
2018 | Central | Bhopal      |      88388|
     |         | Mumbai      |    4492658|
     | North   | Ahmedabad   |     896700|
     |         | Delhi NCR   |    1842988|
     |         | Kanpur      |     145921|
     |         | Lucknow     |     105333|
     | South   | Chennai     |     115481|
2019 | Central | Mumbai      |    1613340|
     | North   | Ahmedabad   |     130788|
     |         | Delhi NCR   |    1265908|
     |         | Kanpur      |     286334|
2020 | Central | Mumbai      |       3084|
     | North   | Delhi NCR   |      18944|

**Tableau Graph**:

![image](https://github.com/Datarianna/Sales-Insights-Project/assets/138058039/138f2ca5-eecf-468e-a7e0-80d0dfa31609) ![image](https://github.com/Datarianna/Sales-Insights-Project/assets/138058039/1b07b7e7-cb4b-4745-b142-6fb2b6043a4a)

**Answer**:

### Question 5: What is the total sales revenue and total number of units sold for each customer type in 2019?
A left join of the Transaction Sales and Customer Datasets is needed, but since a variable has already been made for this join (in Question 1), it will be reused for this question.
```python
print(join_ts_c.head())
```
|product_code |customer_code| market_code| order_date|  sales_qty | sales_amount |currency|norm_sales_amount|customer_name|customer_type|
|-------------|-------------|------------|-----------|------------|--------------|--------|-----------------|-------------|-------------|
| Prod001     | Cus001      |Mark001     | 2017-10-10|     100    |     41241   |   INR      |        41241  |  Surge Stores | Brick & Mortar
|   Prod002   |    Cus003   |Mark003     | 2018-04-06 |    1      |   875     | INR        |        875  |  Excel Stores | Brick & Mortar
|  Prod002    |   Cus003    |Mark003     | 2018-04-11 |      1    |   583    |  INR        |        583  |  Excel Stores | Brick & Mortar
|   Prod002   |   Cus004    |Mark003     | 2018-06-18|     6      | 7176   |   INR        |       7176 | Surface Stores | Brick & Mortar
|  Prod003    |  Cus005     |Mark004     |2017-11-20  |   59      | 500    |  USD          |    41000 | Premium Stores | Brick & Mortar

1. Created a year filter that only includes rows that have an order date within 2019.
2. Grouped the filtered dataframe by customer_type, then summed the sales quantity and sales amount.
```python
year_filter = join_ts_c[(join_ts_c['order_date'] >= '2019-01-01') & (join_ts_c['order_date'] <= '2019-12-31')]
customer_type = year_filter.groupby('customer_type')[['sales_qty','norm_sales_amount']].sum()
print(customer_type)
```
|    customer_type    |sales_qty|norm_sales_amount|
|---------------------|---------|-----------------|
|Brick & Mortar       |1895     |       1922075  |
|E-Commerce           |828      |      1374295   |

**Tableau Graph**:

![image](https://github.com/Datarianna/Sales-Insights-Project/assets/138058039/5a775260-08f9-4dad-9ca4-4123740e6288) 
![image](https://github.com/Datarianna/Sales-Insights-Project/assets/138058039/3acd9d53-dfa3-4125-ab31-fe4c13c4adc8)


**Answer**:



# Tableau Dashboard
Link: https://public.tableau.com/app/profile/arianna.jara/viz/SalesInsightsAnalytics/Dashboard1?publish=yes
![image](https://github.com/Datarianna/Sales-Insights-Project/assets/138058039/83ec6a65-3a83-47d6-81f9-e2d561f7cd45)

