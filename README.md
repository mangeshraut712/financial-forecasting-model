# Financial Forecasting Model 📊

[![Python](https://img.shields.io/badge/Python-Analysis-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Excel](https://img.shields.io/badge/Excel-Modeling-217346?logo=microsoftexcel&logoColor=white)](https://www.microsoft.com/microsoft-365/excel)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-Regression-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![statsmodels](https://img.shields.io/badge/statsmodels-ARIMA-4c78a8)](https://www.statsmodels.org/)

Budget vs actual tracking and illustrative revenue forecasts in Excel, Power BI, and Python (linear regression and ARIMA).

**Homepage:** this README (no separate live demo).

## Gallery

Charts below are generated from `models/financial_forecast_model.xlsx` (the `BudgetVsActual` sheet).

![Monthly budget vs actual revenue](docs/screenshots/01-budget-vs-actual.png)

![ARIMA three-month revenue forecast](docs/screenshots/02-arima-forecast.png)

![Excel-style monthly table and regression forecast](docs/screenshots/03-excel-regression.png)

Refresh the PNGs after changing the workbook:

```bash
pip install -r requirements.txt
python docs/screenshots/render_gallery.py
```

## Features

- Budget vs actual tracking
- Visualizations in Excel and Plotly
- Regression and ARIMA forecasting

## Project structure

- `/data` — raw financial CSV
- `/models` — Excel forecasting workbook
- `/scripts` — Python analysis and visualization
- `/powerbi` — Power BI template (placeholder)
- `/docs/screenshots` — README gallery outputs

## How to use

1. `pip install -r requirements.txt`
2. Run `scripts/scaffold.py` to prepare Excel models.
3. Use `scripts/regression_predictor.py` for basic regression.
4. Use `scripts/advanced_forecast_arima.py` for the ARIMA example.
5. Visualize with `scripts/visualizations.py` or Excel/Power BI.

## Financial assumptions

- Budgeted revenue includes a 10% buffer over actuals.
- Budgeted costs are 5% over actual COGS.
- Forecasting models are illustrative (linear regression, ARIMA).

## Future work

- More interactive dashboards
- Deeper ML-based forecasting

---

<!-- codex:project-diagram:start -->

## Project diagram

```mermaid
flowchart LR
    A["Raw Data"] --> B["Preprocessing"]
    B --> C["Model Training"]
    C --> D["Predictions / Reports"]
```

_Core machine-learning workflow from source data to final artifacts._

<!-- codex:project-diagram:end -->
