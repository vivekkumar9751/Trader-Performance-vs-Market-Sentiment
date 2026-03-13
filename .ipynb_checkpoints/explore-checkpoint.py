import pandas as pd

# Load files
hist_df = pd.read_csv("historical_data.csv")
fg_df = pd.read_csv("fear_greed_index.csv")

# Info
print("==== historical_data.csv ====")
print(hist_df.info())
print(hist_df.head())
print("\nMissing values:\n", hist_df.isnull().sum())
print("Duplicates: ", hist_df.duplicated().sum())

print("\n==== fear_greed_index.csv ====")
print(fg_df.info())
print(fg_df.head())
print("\nMissing values:\n", fg_df.isnull().sum())
print("Duplicates: ", fg_df.duplicated().sum())
