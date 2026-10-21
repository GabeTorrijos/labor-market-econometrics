#Get Packages

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

print("LABOR MARKET ECONOMETRICS")
print("REGRESSION ANALYSIS")
print("------------------------")

#Load cleaned dataset
df = pd.read_csv("data/processed/acs_2024_wages_clean.csv")

print(f"Observations loaded: {len(df):,}")

#Create the natual logarithm of annual wage income
df["log_wage"] = np.log(df["INCWAGE"])

print("\nLOG WAGE VARIABLE")
print("------------------------")
print(df["log_wage"].describe())

#Model 1: Education and annual wage income
model_1 = smf.ols(
    formula='log_wage ~ C(education_label, Treatment(reference="Grade 12"))',
    data=df
).fit(cov_type="HC3")

print("\nMODEL 1: ECUCATION AND LOG WAGES")
print("--------------------------------")
print(model_1.summary())

#Model 2: Education and wages with additional controls

print("\nMODEL 2: EDUCATION WITH WORKER CONTROLS")
print("---------------------------------------")

model_2 = smf.ols(
    formula=(
        'log_wage ~ '
        'C(education_label, Treatment(reference="Grade 12")) '
        '+ C(SEX)'
        '+ UHRSWORK '
        '+ WKSWORK1 '
        '+ C(STATEFIP)'
    ),
    data=df
).fit(cov_type="HC3")

print(model_2.summary())

#Compare Model 1 and Model 2

# Compare Model 1 and Model 2

print("\nREGRESSION MODEL COMPARISON")
print("---------------------------")

comparison = pd.DataFrame({
    "Model 1": model_1.params,
    "Model 2": model_2.params
})

education_comparison = comparison.loc[
    comparison.index.str.contains("college")
].copy()

education_comparison.index = [
    "1 year of college",
    "2 years of college",
    "4 years of college",
    "5+ years of college"
]

print(education_comparison.round(4))

print("\nMODEL PERFORMANCE")
print("-----------------")
print(f"Model 1 R-squared: {model_1.rsquared:.4f}")
print(f"Model 2 R-squared: {model_2.rsquared:.4f}")

#Export regression comparison table
education_comparison.to_csv(
    "reports/regression_comparison.csv",
    index_label="Education Level"
)

print("\nRegression comparison exported successfully!")