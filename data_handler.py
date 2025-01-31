
# data_handler.py
import pandas as pd
import streamlit as st

def load_excel(file):
    return pd.ExcelFile(file).parse(sheet_name=None, skiprows=2)

def clean_column_names(df):
    df.columns = df.columns.str.strip().str.replace("\n", " ").str.upper()
    return df.loc[:, ~df.columns.duplicated()]

def get_filtered_view(df, view_type):
    required_columns = ["CUSTOMER NAME"]
    columns_mapping = {
        "Whole Sheet": [col for col in df.columns if not col.startswith("UNNAMED")],
        "Action Items": required_columns + ["NEXT STEPS", "ACTION OWNER"],
        "Knowledge": required_columns + ["STATUS", "MARKET INFO", "CONTACT #1"],
        "Communication and Awareness": required_columns + ["GOALS"],
        "Annual Goals": required_columns + [col for col in df.columns if col not in required_columns]
    }
    return df[columns_mapping.get(view_type, [])]
