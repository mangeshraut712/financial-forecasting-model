<div align="center">

# 📊 Financial Forecasting Model

Forecasting and visualization workflow built around Excel, Power BI, and Python.

![Python](https://img.shields.io/badge/Python-Analysis-3776ab?style=flat&logo=python&logoColor=white)
![Excel](https://img.shields.io/badge/Excel-Modeling-217346?style=flat&logo=microsoftexcel&logoColor=white)
![Power%20BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=flat&logo=powerbi&logoColor=black)
![Forecasting](https://img.shields.io/badge/Forecasting-Regression%20%26%20ARIMA-4c78a8?style=flat)

</div>

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Stack](#stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Scripts](#scripts)

## Overview

This repository packages a small finance analytics workflow for comparing actuals against budget, generating forecast outputs, and visualizing trends in Python, Excel, or Power BI.

## Features

- Budget-vs-actual analysis with a simple forecast-friendly data model.
- Regression and ARIMA examples for baseline forecasting.
- Plotly-driven visualizations for quick exploration.
- Excel workbook and Power BI template for presentation-ready reporting.

## Stack

- Python for data preparation, forecasting, and charts.
- Excel for workbook-based modeling.
- Power BI for dashboard presentation.
- CSV input data for repeatable analysis.

## Quick Start

1. Run `scripts/scaffold.py` to prepare or refresh the working model files.
2. Use `scripts/regression_predictor.py` for the regression baseline.
3. Use `scripts/advanced_forecast_arima.py` for the ARIMA-style forecast.
4. Generate charts with `scripts/visualizations.py` or open the Excel/Power BI files directly.

## Project Structure

```text
.
├── data/financials_raw.csv
├── models/financial_forecast_model.xlsx
├── powerbi/financial_dashboard_template.pbix
└── scripts/
    ├── scaffold.py
    ├── regression_predictor.py
    ├── advanced_forecast_arima.py
    └── visualizations.py
```

## Scripts

- `scaffold.py` prepares the workbook-style forecast assets.
- `regression_predictor.py` runs the baseline regression forecast.
- `advanced_forecast_arima.py` adds a time-series forecast option.
- `visualizations.py` builds visual summaries from the dataset.
