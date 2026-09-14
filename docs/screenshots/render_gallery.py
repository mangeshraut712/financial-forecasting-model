#!/usr/bin/env python3
"""Render README gallery PNGs from the Excel budget-vs-actual workbook."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA

REPO = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
WORKBOOK = REPO / "models" / "financial_forecast_model.xlsx"

plt.rcParams.update(
    {
        "figure.facecolor": "#f6f4ef",
        "axes.facecolor": "#fbfaf7",
        "axes.edgecolor": "#2c3e50",
        "axes.labelcolor": "#1f2a37",
        "xtick.color": "#1f2a37",
        "ytick.color": "#1f2a37",
        "text.color": "#1f2a37",
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.grid": True,
        "grid.alpha": 0.25,
    }
)


def monthly_budget_vs_actual() -> pd.DataFrame:
    df = pd.read_excel(WORKBOOK, sheet_name="BudgetVsActual")
    # Source dates are day-first (01/06/2014 = June 2014); Year/Month_Number are authoritative.
    monthly = (
        df.groupby(["Year", "Month_Number"], as_index=False)
        .agg(
            Actual_Revenue=("Actual_Revenue", "sum"),
            Budget_Revenue=("Budget_Revenue", "sum"),
            Revenue_Variance=("Revenue_Variance", "sum"),
        )
        .sort_values(["Year", "Month_Number"])
    )
    monthly["Date"] = pd.to_datetime(
        dict(year=monthly["Year"], month=monthly["Month_Number"], day=1)
    )
    return monthly.set_index("Date")


def money(value: float) -> str:
    return f"${value:,.0f}"


def format_revenue_axis(ax) -> None:
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _p: f"${v/1e6:.1f}M"))


def render_actual_vs_budget(monthly: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(11.2, 5.0))
    ax.plot(
        monthly.index,
        monthly["Actual_Revenue"],
        marker="o",
        color="#1f4e5f",
        linewidth=2.0,
        label="Actual revenue",
    )
    ax.plot(
        monthly.index,
        monthly["Budget_Revenue"],
        marker="s",
        color="#c45c26",
        linewidth=1.8,
        linestyle="--",
        label="Budget revenue (+10% buffer)",
    )
    ax.set_title("Budget vs actual revenue (monthly, from Excel model)")
    ax.set_ylabel("Revenue")
    format_revenue_axis(ax)
    ax.legend(frameon=False)
    fig.autofmt_xdate()
    fig.tight_layout()
    dest = OUT / "01-budget-vs-actual.png"
    fig.savefig(dest, dpi=140)
    plt.close(fig)
    print(f"wrote {dest}")


def render_arima(monthly: pd.DataFrame) -> None:
    series = monthly["Actual_Revenue"].asfreq("MS")
    model_fit = ARIMA(series, order=(1, 1, 1)).fit()
    forecast = model_fit.forecast(steps=3)

    fig, ax = plt.subplots(figsize=(11.2, 5.0))
    ax.plot(series.index, series.values, color="#1f4e5f", linewidth=2.0, label="Actual")
    ax.plot(
        forecast.index,
        forecast.values,
        color="#c45c26",
        linewidth=2.0,
        linestyle="--",
        marker="o",
        label="ARIMA(1,1,1) next 3 months",
    )
    ax.axvline(series.index[-1], color="#8a8a8a", linestyle=":", linewidth=1)
    ax.set_title("ARIMA revenue forecast from monthly actuals")
    ax.set_ylabel("Revenue")
    format_revenue_axis(ax)
    ax.legend(frameon=False)
    fig.autofmt_xdate()
    fig.tight_layout()
    dest = OUT / "02-arima-forecast.png"
    fig.savefig(dest, dpi=140)
    plt.close(fig)
    print(f"wrote {dest}")


def render_excel_and_regression(monthly: pd.DataFrame) -> None:
    idx = np.arange(len(monthly)).reshape(-1, 1)
    model = LinearRegression().fit(idx, monthly["Actual_Revenue"].values)
    future_idx = np.arange(len(monthly), len(monthly) + 3).reshape(-1, 1)
    preds = model.predict(future_idx)

    display = monthly.tail(8).copy()
    display["Month"] = display.index.strftime("%b %Y")
    cell_text = [
        [
            row["Month"],
            money(row["Actual_Revenue"]),
            money(row["Budget_Revenue"]),
            money(row["Revenue_Variance"]),
        ]
        for _, row in display.iterrows()
    ]

    fig, axes = plt.subplots(
        1, 2, figsize=(11.2, 5.0), gridspec_kw={"width_ratios": [1.35, 1.0]}
    )
    axes[0].axis("off")
    axes[0].set_title("Excel-style BudgetVsActual (latest months)")
    table = axes[0].table(
        cellText=cell_text,
        colLabels=["Month", "Actual", "Budget", "Variance"],
        loc="center",
        cellLoc="right",
        colLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.15, 1.55)
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor("#1f4e5f")
            cell.set_text_props(color="white", weight="bold")
        elif row % 2 == 0:
            cell.set_facecolor("#e8efe9")

    axes[1].plot(
        monthly.index,
        monthly["Actual_Revenue"],
        color="#1f4e5f",
        linewidth=2.0,
        label="Actual",
    )
    last = monthly.index[-1]
    future_dates = pd.date_range(last + pd.offsets.MonthBegin(1), periods=3, freq="MS")
    axes[1].plot(
        future_dates,
        preds,
        color="#6b4c9a",
        marker="o",
        linewidth=2.0,
        label="Linear regression (+3 mo)",
    )
    axes[1].set_title(
        "Next-quarter regression\n"
        + " · ".join(money(p) for p in preds)
    )
    axes[1].set_ylabel("Revenue")
    format_revenue_axis(axes[1])
    axes[1].legend(frameon=False)
    fig.autofmt_xdate()
    fig.tight_layout()
    dest = OUT / "03-excel-regression.png"
    fig.savefig(dest, dpi=140)
    plt.close(fig)
    print(f"wrote {dest}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if not WORKBOOK.exists():
        raise SystemExit(f"missing workbook: {WORKBOOK}")
    monthly = monthly_budget_vs_actual()
    if len(monthly) < 6:
        raise SystemExit(
            f"expected a multi-month series, got {len(monthly)} rows "
            "(check Year/Month_Number grouping)"
        )
    render_actual_vs_budget(monthly)
    render_arima(monthly)
    render_excel_and_regression(monthly)


if __name__ == "__main__":
    main()
