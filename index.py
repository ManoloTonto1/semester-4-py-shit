import pandas as pd
import pyodbc
# Read the data from access database

dbPath = "./go_sales.accdb"
sales_db = pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + dbPath)

# Read the tables from access database
order_details = pd.read_sql("SELECT * FROM order_details", sales_db)
product = pd.read_sql("SELECT * FROM product", sales_db)
order_header = pd.read_sql("SELECT * FROM order_header", sales_db)
order_method = pd.read_sql("SELECT * FROM order_method", sales_db)

# Merge the tables
order_details = pd.merge(order_details, product, on="PRODUCT_NUMBER")
order_details = pd.merge(order_details, order_header, on="ORDER_NUMBER")
order_details = pd.merge(order_details, order_method, on="ORDER_METHOD_CODE")

# Create a new column
order_details["QUANTITY"] =  order_details["QUANTITY"].astype(float).where(order_details["QUANTITY"].notnull(), 0)
order_details["UNIT_PRICE"] = order_details["UNIT_PRICE"].astype(float).where(order_details["UNIT_PRICE"].notnull(), 0)
order_details["total_revenue"] = order_details["QUANTITY"] * order_details["UNIT_PRICE"]

# total revenue per year per product, per order method, unit price
order_details["ORDER_DATE"] = pd.to_datetime(order_details["ORDER_DATE"])
order_details["YEAR"] = order_details["ORDER_DATE"].dt.year
# Group by the order method type
order_details.groupby(["YEAR", "PRODUCT_NAME", "ORDER_METHOD_EN", "UNIT_PRICE"])["total_revenue"].sum()







