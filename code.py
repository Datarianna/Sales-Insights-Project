import pandas as pd
###### DATA CLEANING PROCESS ######
print('- - - - - CLEANING THE DATA - - - - -')
# this function will check for missing values
def missing(df):
  missing = df.isna().any().any()
  if missing:
    print('Missing values detected')
  else:
    print('No missing values')

# this function will check for duplicate values
def duplicate(df):
  duplicate = df.duplicated().any().any()
  if duplicate:
    print('Duplicate values present')
  else:
    print('No duplicate values')
  

##### TRANSACTION SALES CLEANING #####
print('\n- - - - - Transaction Sales - - - - -')
print('Original Dataset:')
ts = pd.read_csv('transaction_sales.csv')
print(ts.head())

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

##### MARKETS CLEANING #####
print('\n- - - - - Market - - - - -')
print('Original Dataset:')
m = pd.read_csv('markets.csv')
print('Top 5 rows')
print(m.head())
print('Bottom 5 rows')
print(m.tail())

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

##### CUSTOMERS CLEANING #####
print('\n- - - - - Customers - - - - -')
print('Original Dataset:')
c = pd.read_csv('customers.csv')
print(c.head())

c = c.rename(columns={'custmer_name':'customer_name'})
c = c.dropna()
print('')
duplicate(c)
missing(c)

print('\nCleaned Dataset:')
print(c.head())
c.to_csv('clean_customers.csv', index=False)

##### PRODUCTS CLEANING #####
print('\n- - - - - Products - - - - -')
print('Original Dataset:')
p = pd.read_csv('products.csv')
print(p.head())

p['product_type'] = p['product_type'].str.rstrip("\r")
p = p.dropna()
print('')
duplicate(p)
missing(p)

print('\nCleaned Dataset:')
print(p.head())
p.to_csv('clean_products.csv', index=False)

##### SALES YEARS CLEANING #####
print('\n- - - - - Sales Years - - - - -')
sy = pd.read_csv('sales_years.csv')
print('Original Dataset:')
print(sy.head())

sy.drop("date_yy_mmm", axis=1, inplace=True)
sy.drop("cy_date", axis=1, inplace=True)
sy = sy.rename(columns={'date':'order_date'})
sy['order_date'] = pd.to_datetime(sy['order_date'], dayfirst=False)
sy['year'] = sy['order_date'].dt.year
sy['month_name'] = sy['order_date'].dt.month_name()
print('')
duplicate(sy)
missing(sy)

print('\nCleaned Dataset:')
print(sy.head())
sy.to_csv('clean_sales_years.csv', index=False)

print('__________________________________________________________________')
print('\n- - - - - DATA ANALYSIS AND RESULTS - - - - -')

### QUESTION 1 ####
print('\n[Q1] Who are the top five customers for AtliQ in 2019 based on total sales revenue?')
print('\nLeft Joining Transaction Sales and Customer Datasets:')
join_ts_c = pd.merge(ts, c, on='customer_code', how='left')
print(join_ts_c.head())

print('\nTop Five Customers:')
year_filter = join_ts_c[(join_ts_c['order_date']>='2019-01-01') & (join_ts_c['order_date']<='2019-12-31')]
top_five_customers = year_filter.groupby('customer_name')['norm_sales_amount'].sum().sort_values(ascending=False).head(5)
print(top_five_customers)

### QUESTION 2 ###
print('\n[Q2] What is the trend of total sales revenue for AtliQ in 2017-2020?')
print('\nSales Trends 2017-2019')
year_filter = ts[(ts['order_date']>='2017-01-01') & (ts['order_date']<='2019-12-31')]
total_rev_years = year_filter.groupby(year_filter['order_date'].dt.year)['norm_sales_amount'].sum()
print(total_rev_years)

### QUESTION 3 ###
print('\n[Q3] From 2017-2020, which three products sold the most units?')
year_filter = ts[(ts['order_date'] >= '2017-01-01') & (ts['order_date'] <= '2020-12-31')]
for year in year_filter['order_date'].dt.year.unique():
  year_data = year_filter[year_filter['order_date'].dt.year == year]
  top_three = year_data.groupby('product_code')['sales_qty'].sum().nlargest(3)
  print(f"\nTop 3 products sold in {year}:")
  print(top_three)

### QUESTION 4 ###
print('\n[Q4] How does the sales revenue vary across different regions in India throughout the years?')
join_ts_m = pd.merge(ts, m, on='market_code', how='left')
print(join_ts_m.head())

print('')
sales_regions = join_ts_m.groupby(['zone','markets_name'])['norm_sales_amount'].sum()
print(sales_regions.to_string())

### QUESTION 5 ###
print('\n[Q5]What is the total sales revenue and total number of units sold for each customer type in 2019?')
print(join_ts_c.head())

print('')
year_filter = join_ts_c[(join_ts_c['order_date'] >= '2019-01-01') & (join_ts_c['order_date'] <= '2019-12-31')]
customer_type = year_filter.groupby('customer_type')[['sales_qty','norm_sales_amount']].sum()
print(customer_type)

