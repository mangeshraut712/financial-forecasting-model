import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Load data
df = pd.read_csv(r"data/financials_raw.csv")
df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("-", "_")
df["Sales"] = pd.to_numeric(df["Sales"].astype(str).str.replace(",", "").str.replace("$", ""), errors='coerce')

# Create Month Index
df["Month_Index"] = np.arange(len(df))

# Fit Linear Regression Model
model = LinearRegression().fit(df[["Month_Index"]], df["Sales"])
future_idx = np.arange(len(df), len(df)+3).reshape(-1,1)
preds = model.predict(future_idx).round(2)

# Forecast Output
forecast = pd.DataFrame({
    "Forecast_Month_Index": future_idx.flatten(),
    "Forecasted_Revenue": preds
})
print("Next Quarter Revenue Forecast:")
print(forecast.to_string(index=False))
