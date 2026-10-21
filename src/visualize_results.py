#Get packages

import pandas as pd
import matplotlib.pyplot as plt

print("LABOR MARKET ECONOMETRICS")
print("DATA VISUALIZATION")
print("------------------------")

#Load regression comparison results
df = pd.read_csv("reports/regression_comparison.csv")

print("\nREGRESSION RESULTS")
print("------------------------")
print(df)

#Create a grouped bar chart comparing regression coefficients
fig, ax = plt.subplots(figsize=(10, 6))

x = range(len(df))
bar_width = 0.35

ax.bar(
    [i - bar_width / 2 for i in x],
    df["Model 1"],
    width=bar_width,
    label="Model 1: Education Only"
)

ax.bar(
    [i + bar_width / 2 for i in x],
    df["Model 2"],
    label="Model 2: With Controls"
)

ax.set_xticks(list(x))
ax.set_xticklabels(df["Education Level"])

ax.set_title("Education and Annual Wage Income: Regression Comparison")
ax.set_ylabel("Log-Wage Coefficient")
ax.set_xlabel("Educational Attainment")

ax.legend()

#Add methodological context
fig.text(
    0.5,
    0.01,
    "Reference: Grade 12 | N = 37,294 | Source: 2024 ACS (IPUMS USA)",
    ha="center",
    fontsize=9,
    color="dimgray"
)

fig.tight_layout(rect=[0, 0.04, 1, 1])

#Export a high-resolution figure for research report
fig.savefig(
    "reports/education_regression_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

print("\nVisualization saved successfully!")

plt.show()