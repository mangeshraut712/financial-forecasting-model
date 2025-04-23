import pandas as pd
import numpy as np
from pathlib import Path

# Load and preprocess data
csv_path = Path("data/financials_raw.csv")
df = pd.read_csv(csv_path)

# Normalize column names
df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("-", "_")

# Ensure Sales and COGS columns are numeric
df["Sales"] = pd.to_numeric(df["Sales"].astype(str).str.replace(",", "").str.replace("$", ""), errors='coerce')
df["COGS"] = pd.to_numeric(df["COGS"].astype(str).str.replace(",", "").str.replace("$", ""), errors='coerce')

# Create Budget & Actual columns
df["Budget_Revenue"] = df["Sales"] * 1.10
df["Actual_Revenue"] = df["Sales"]

df["Budget_Cost"] = df["COGS"] * 1.05
df["Actual_Cost"] = df["COGS"]

# Compute Variances
df["Revenue_Variance"] = df["Actual_Revenue"] - df["Budget_Revenue"]
df["Cost_Variance"] = df["Actual_Cost"] - df["Budget_Cost"]

# Save to Excel
excel_path = Path("models/financial_forecast_model.xlsx")
excel_path.parent.mkdir(parents=True, exist_ok=True)

with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="RawData", index=False)
    df.to_excel(writer, sheet_name="BudgetVsActual", index=False)

print("✅ Excel model generated successfully at:", excel_path)

# Generate Regression Script Dynamically
regression_code = f'''\
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Load data
df = pd.read_csv(r"{csv_path}")
df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("-", "_")
df["Sales"] = pd.to_numeric(df["Sales"].astype(str).str.replace(",", "").str.replace("$", ""), errors='coerce')

# Create Month Index
df["Month_Index"] = np.arange(len(df))

# Fit Linear Regression Model
model = LinearRegression().fit(df[["Month_Index"]], df["Sales"])
future_idx = np.arange(len(df), len(df)+3).reshape(-1,1)
preds = model.predict(future_idx).round(2)

# Forecast Output
forecast = pd.DataFrame({{
    "Forecast_Month_Index": future_idx.flatten(),
    "Forecasted_Revenue": preds
}})
print("Next Quarter Revenue Forecast:")
print(forecast.to_string(index=False))
'''

script_path = Path("scripts/regression_predictor.py")
script_path.parent.mkdir(parents=True, exist_ok=True)
script_path.write_text(regression_code)

print("✅ Regression script created at:", script_path)
