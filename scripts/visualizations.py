import pandas as pd
import plotly.express as px

# Load data
df = pd.read_excel("models/financial_forecast_model.xlsx", sheet_name="BudgetVsActual")

# Simple Line Chart: Actual vs Budget Revenue
fig = px.line(df, x="Date", y=["Actual_Revenue", "Budget_Revenue"], 
              title="Actual vs Budget Revenue Over Time",
              labels={"value": "Revenue", "Date": "Month"})
fig.show()

# Bar Chart: Revenue Variance
fig2 = px.bar(df, x="Date", y="Revenue_Variance", 
              title="Revenue Variance Over Time",
              labels={"Revenue_Variance": "Variance"})
fig2.show()
