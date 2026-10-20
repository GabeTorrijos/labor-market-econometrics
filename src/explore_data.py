#Get packages
import pandas as pd

#Load our 2024 ACS dataset
df = pd.read_csv("data/raw/usa_00002.csv")

#Display basic information
print("LABOR MARKET ECONOMETRICS")
print("------------------------")

print("\nDataset dimensions:")
print(df.shape)

print("\nFirst 5 observations:")
print(df.head())

print("\nAvailable variables:")
print(df.columns.tolist())

print("\nDataset information:")
df.info()

#Examine important economic variables
print ("\nWAGE DISTRIBUTION")
print("-----------------")
print(df["INCWAGE"].describe())

print("\nEDUCATION CATEGORIES")
print("-----------------")
print(df["EDUC"].value_counts().sort_index())

print("\nEMPLOYMENT STATUS")
print("-----------------")
print(df["EMPSTAT"].value_counts().sort_index())

#Clean and filter out invalid values

print("\nWAGE DATA QUALITY CHECK")
print("-----------------------")

#Count observations with specific wage values
print("Zero wages:", (df["INCWAGE"] == 0).sum())

print("999999 wages:", (df["INCWAGE"] == 999999).sum())

print("Positive wages below 999999:",
      ((df["INCWAGE"] > 0) & (df["INCWAGE"] < 999999)).sum())

# Compare the original mean with a preliminary filtered mean
valid_wages = df[
    (df["INCWAGE"] > 0) &
    (df["INCWAGE"] < 999999)
]

print("\nOriginal mean wage:")
print(round(df["INCWAGE"].mean(), 2))

print("\nPreliminary mean wage (positive wages below 999999):")
print(round(valid_wages["INCWAGE"].mean(), 2))

print("\nObservations remaining:")
print(len(valid_wages))

#Introduce Cross-Tabulation

print("\nEMPLOYMENT STATUS VS WAGE CODES")
print("-------------------------------")

#Create categories for wage observations
df["wage_category"] = "Positive wage"

df.loc[df["INCWAGE"] == 0, "wage_category"] = "Zero wage"

df.loc[
    df["INCWAGE"] == 999999,
    "wage_category"
] = "Special code (999999)"

#Cross-tabulate employment status and wage categories
wage_table = pd.crosstab(
    df["EMPSTAT"],
    df["wage_category"]
)

print(wage_table)

#Define the preliminary research sample

print("\nPRELIMINARY RESEARCH SAMPLE")
print("---------------------------")

#Start with full dataset
print("Original observations:", len(df))

#Restrict to adults with ages 25 through 64 years
working_age = df[
    (df["AGE"] >= 25) &
    (df["AGE"] <= 64)
]

print("Working-age adults (25-64):", len(working_age))

#Keep observations with positive, non-special wage values
research_sample = working_age[
    (working_age["INCWAGE"] > 0) &
    (working_age["INCWAGE"] < 999999)
].copy()

print("Positive-wage earners ages 25-64:", len(research_sample))

print("\nPreliminary wage statistics:")
print(research_sample["INCWAGE"].describe())

#Introduce Survey Weights

#Get packages
import numpy as np

print("\nWEIGHTED VS UNWEIGHTED WAGES")
print("----------------------------")

#Calculate the ordinary sample mean
unweighted_mean = research_sample["INCWAGE"].mean()

#Calculate the survey-weighted mean
weighted_mean = np.average(
    research_sample["INCWAGE"],
    weights=research_sample["PERWT"]
)

print(f"Unweighted mean wage: ${unweighted_mean:,.2f}")
print(f"Weighted mean wage:   ${weighted_mean:,.2f}")

print("\nSurvey weight statistics:")
print(research_sample["PERWT"].describe())

#Investigate Education and Wages

print("\nWAGES BY EDUCATION LEVEL")
print("------------------------")

#Group observations by educational attainment
education_wages = research_sample.groupby("EDUC").agg(
    observations=("INCWAGE", "count"),
    mean_wage=("INCWAGE", "mean"),
    median_wage=("INCWAGE", "median")
)

#Round values for data visualization
education_wages = education_wages.round(2)

print(education_wages)

#Create Readable Education Labels

print("\nEDUCATION LEVELS WITH LABELS")
print("----------------------------")

#Preliminary education labels
education_labels = {
    0: "N/A or no schooling",
    1: "Nursery to grade 4",
    2: "Grades 5-8",
    3: "Grade 9",
    4: "Grade 10",
    5: "Grade 11",
    6: "Grade 12",
    7: "1 year of college",
    8: "2 years of college",
    10: "4 years of college",
    11: "5+ years of college"
}

#Translate numerical codes into readable categories
research_sample["education_label"] = research_sample["EDUC"].map(
    education_labels
)

#Calculate mean wages by education category
labeled_wages = research_sample.groupby(
    ["EDUC", "education_label"]
)["INCWAGE"].mean()

print(labeled_wages.round(2))