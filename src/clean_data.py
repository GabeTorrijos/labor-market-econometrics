#Labor Market Econometrics
#Data Cleaning and Preperation
#Source 2024 ACS 1-Year Microdata (IPUMS USA)

#Get packages
import pandas as pd

#Load the original dataset
df = pd.read_csv("data/raw/usa_00002.csv")

#Display initial dataset information
print("LABOR MARKET ECONOMETRICS")
print("DATA CLEANING PIPELINE")
print("----------------------")

print(f"\nOriginal observations: {len(df):,}")
print(f"Original variables: {len(df.columns)}")

#Step 1: Restrict sample to adults ages 25-64

working_age = df[
    (df["AGE"] >= 25) &
    (df["AGE"] <= 64)
].copy()

print("\nSAMPLE RESTRICTIONS")
print("-------------------")

print(f"Adults ages 25-64: {len(working_age):,}")

#Step 2: Keep positive, non-special wage values

#Keep observations with positive, valid annual wage income
#IPUMS special codes:
#999998 = Missing
#999999 = Not applicable

research_sample = working_age[
    (working_age["INCWAGE"] > 0) &
    (~working_age["INCWAGE"].isin([999998, 999999]))
].copy()

print(f"Positive-wage earners ages 25-64: {len(research_sample):,}")

#Step 3: Calculate sample retention rate

retention_rate = (len(research_sample) / len(df)) * 100

print(f"Sample retention rate: {retention_rate:.2f}%")

#Step 4: Check missing values in research variables

print("\nMISSING VALUE CHECK")
print("-------------------")

#Define variables relevant to our research
research_variables = [
    "INCWAGE",
    "EDUC",
    "AGE",
    "SEX",
    "RACE",
    "OCC",
    "WKSWORK1",
    "UHRSWORK",
    "PERWT"
]

# Count missing values for each variable
missing_values = research_sample [research_variables].isna().sum()

print(missing_values)

#Count observations containing at least one missing value
incomplete_observations = research_sample[
    research_variables
].isna().any(axis=1).sum()

print(f"\nObservations with missing values: {incomplete_observations:,}")

#Step 5: Investigate potential special values
print("\nSPECIAL VALUE INVESTIGATION")

print("---------------------------")

variables_to_check = [

    "OCC",

    "WKSWORK1",

    "UHRSWORK"

]

for variable in variables_to_check:

    print(f"\nVariable: {variable}")

    print(f"Minimum: {research_sample[variable].min()}")

    print(f"Maximum: {research_sample[variable].max()}")

    zero_count = (research_sample[variable] == 0).sum()

    print(f"Observations equal to zero: {zero_count:,}")

#Step 6: Investigate unusually high working hours
print("\nWORKING HOURS INVESTIGATION")
print("---------------------------")

#Summary statistics for usual weekly hours
print(research_sample["UHRSWORK"].describe())

#Count observations reporting unusually high hours
high_hours = research_sample[
    research_sample["UHRSWORK"] >= 80
]

print(f"\nObservations reporting 80+ hours: {len(high_hours):,}")

#Examine the most frequently reported working hours
print("\nMost common weekly working hours:")

print(
    research_sample["UHRSWORK"]
    .value_counts()
    .head(10)
)

#Step 7: Examine unusually high working-hour values

print("\nHIGH WORKING HOURS DISTRIBUTION")
print("--------------------------------")

high_hours_distribution = (
    research_sample.loc[
        research_sample["UHRSWORK"] >= 80,
        "UHRSWORK"
    ]
    .value_counts()
    .sort_index()
)

print(high_hours_distribution)

#Step 8: Document UHRSWORK top-coding
#
#IPUMS USA documentation:
#UHRSWORK = 00 indicates N/A.
#UHRSWORK = 99 represents top-coded weekly hours.
#
#The research sample contains 49 observations with UHRSWORK = 99.
#
#Retain these observations rather then excluding them since the primary dependent
#variable is annual wage (INCWAGE), not hourly wages.
#
#If hourly earnings are constructed later, the treatment of top-coded hours must be considered.
#
#
#Step 9: Document WKSWORK1 coding
#
#Source: IPUMS USA variable documentation
#
#WKSWORK1 measures weeks worked during the previous
#12 months for ACS respondents.
#
#00 = Not applicable
#01-52 = Number of weeks worked
#
#Paid vacations and other paid absences are included.
#
#Our research sample contains no observations with
#WKSWORK1 = 0.
#
#Decision:
#Retain all observations. No additional filtering
#is required for WKSWORK1.
#
#
#Step 10: Document OCC coding
#
#Source: IPUMS USA, 2018-present occupation codes
#
#OCC identifies a respondent's primary or most recent occupation.
#
#Special codes:
#0000 = Not applicable
#9920 = Unemployed, no recent work experience or never worked
#
#Our research sample contains occupation codes ranging
#from 0010 to 9830.
#
#Decision:
#Retain all observations for now.
#No additional occupation-based exclusions are necessary.
#
#Econometric note:
#OCC is a categorical variable, not a continuous measure.
#It should be represented using occupation categories
#or indicator variables in regression models.

#Step 11: Create education labels

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

#Create a new column containing education descriptions
research_sample["education_label"] = (
    research_sample["EDUC"].map(education_labels)
)

print("\nEDUCATION LABEL VALIDATION")
print("--------------------------")

#Check whether any observations received a missing label
missing_labels = research_sample["education_label"].isna().sum()

print(f"Observations without an education label: {missing_labels:,}")

#Display education categories and their frequencies
print("\nEducation categories:")

print(
    research_sample["education_label"].value_counts()
)

#Step 12: Select variables for the processed dataset

print("\nPROCESSED DATASET PREPARATION")
print("-----------------------------")

selected_variables = [
    "YEAR",
    "STATEFIP",
    "STRATA",
    "CLUSTER",
    "PERWT",
    "AGE",
    "SEX",
    "RACE",
    "EDUC",
    "EDUCD",
    "education_label",
    "EMPSTAT",
    "OCC",
    "WKSWORK1",
    "UHRSWORK",
    "INCWAGE"
]

#Create a separate DataFrame containing selected variables
processed_data = research_sample[selected_variables].copy()

print(f"Processed observations: {len(processed_data):,}")
print(f"Selected variables: {len(processed_data.columns)}")

print("\nSelected columns:")
print(processed_data.columns.tolist())

#Step 13: Export the processed dataset

print("\nEXPORTING PROCESSED DATASET")
print("---------------------------")

output_path = "data/processed/acs_2024_wages_clean.csv"

processed_data.to_csv(output_path, index=False)

print(f"Dataset saved to: {output_path}")
print(f"Final observations: {len(processed_data):,}")
print(f"Final variables: {len(processed_data.columns)}")