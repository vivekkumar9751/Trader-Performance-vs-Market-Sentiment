# Trader Performance vs Market Sentiment

This repository contains an exploratory data analysis project evaluating how cryptocurrency retail and volume traders behave during different market sentiment days (e.g., Fear vs. Greed). 

## Project Highlights
- Part A: Extracted and aligned over 200k+ historical trades against daily Fear & Greed index values.
- Part B: Segmented traders based on their trading frequency and volume to uncover behavioral alpha.
- Part C: Highlighted actionable risk-management strategies based on empirical data from the analysis.
- Bonus: Provided an interactive Streamlit dashboard (`app.py`) & a quick predictive model utilizing Scikit-Learn within the notebook.

## Files Structure
- `historical_data.csv`: Source trading data (2023-2025) across various wallets/accounts.
- `fear_greed_index.csv`: Daily historical crypto Fear & Greed Index from 2018-2025.
- `analysis_exec.ipynb`: The primary executable Jupyter Notebook containing all steps—data cleaning, EDA, feature engineering, and the insights report.
- `app.py`: An interactive Streamlit dashboard visualizing the project findings.
- `explore.py` / `analyze_data.py`: Pre-analysis exploratory scripts used for drafting logic.

## Setup Requirements
To run this project, make sure you have python 3.9+ and the libraries installed:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn streamlit jupyter
```

## How to Run

### 1. Jupyter Notebook Analysis
The full analysis, visualizations, and written conclusions are available in the Jupyter Notebook. To view or run it:
```bash
jupyter notebook analysis_exec.ipynb
```
Follow the cells iteratively to see data preprocessing, visual plots comparing Trade Segments, and the final Random Forest Predictive Model evaluation.

### 2. Streamlit Dashboard (Bonus)
To explore the high-level findings interactively:
```bash
streamlit run app.py
```
This will open up a local server (typically at `http://localhost:8501`) displaying:
- Metrics filtered by sentiment
- Long vs Short biased performance charts
- Trader Segment comparisons
