#Get packages

import pandas as pd
import sqlite3

#Step 1: Load cleaned dataset. 

print("LABOR MARKET ECONOMETRICS")
print("SQL ANALYSIS")
print("------------------------")

df = pd.read_csv("data/processed/acs_2024_wages_clean.csv")

print(f"Observations loaded: {len(df):,}")
print(f"Variables loaded: {len(df.columns)}")

#Step 2: Create a SQLite database

print("\nCREATING SQLITE DATABASE")
print("------------------------")

connection = sqlite3.connect("data/labor_market.db")

df.to_sql("workers", connection, if_exists="replace", index=False)

print("Database created: data/labor_market.db")
print("Table created: workers")
print(f"Records inserted: {len(df):,}")

#Step 3: Execute education wage SQL query 

print("\nWAGES BY EDUCATION LEVEL")

print("------------------------")

with open("sql/wage_by_education.sql", "r") as file:

    query = file.read()

results = pd.read_sql_query(query, connection)

print(results.to_string(index=False))

#Step 4: Execute survey-weighted wage analysis

print("\nSURVEY-WEIGHTED WAGES BY EDUCATION")
print("----------------------------------")

with open("sql/weighted_wage_by_education.sql", "r") as file:
    weighted_query = file.read()

weighted_results = pd.read_sql_query(weighted_query, connection)

print(weighted_results.to_string(index=False))

connection.close()