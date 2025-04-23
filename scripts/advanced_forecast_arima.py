import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Load and prepare data
df = pd.read_excel("models/financial_forecast_model.xlsx", sheet_name="BudgetVsActual")
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')
df.set_index('Date', inplace=True)

# Fit ARIMA model
model = ARIMA(df['Actual_Revenue'], order=(1, 1, 1))  # You can tweak order=(p,d,q)
model_fit = model.fit()

# Forecast next 3 months
forecast = model_fit.forecast(steps=3)
print("Next 3-Month Forecast:")
print(forecast)

# Plot forecast
df['Actual_Revenue'].plot(label='Actual', legend=True)
forecast.plot(label='Forecast', legend=True, style='--', color='red')
plt.title("ARIMA Forecast of Revenue")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.show()
