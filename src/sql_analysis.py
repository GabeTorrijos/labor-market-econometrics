#Get packages

import pandas as pd
import sqlite3

#Step #1: Load cleaned dataset. 

print("LABOR MARKET ECONOMETRICS")
print("SQL ANALYSIS")
print("------------------------")

df = pd.read_csv("data/processed/acs_2024_wages_clean.csv")

print(f"Observations loaded: {len(df):,}")
print(f"Variables loaded: {len(df.columns)}")

#Step #2: Create a SQLite database

print("\nCREATING SQLITE DATABASE")
print("------------------------")

connection = sqlite3.connect("data/labor_market.db")

df.to_sql("workers", connection, if_exists="replace", index=False)

print("Database created: data/labor_market.db")
print("Table created: workers")
print(f"Records inserted: {len(df):,}")

connection.close()