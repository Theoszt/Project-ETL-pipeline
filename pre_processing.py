import pandas as pd
import numpy as np
from datetime import datetime
import logging
import warnings
from io import StringIO

def clean_numeric_column(df, col_name):
    """Bersihkan kolom numerik dari karakter non-digit dan konversi ke float."""
    original_non_numeric = df[col_name].astype(str).str.contains(r'[^\d.]').sum()
    df[col_name] = df[col_name].astype(str).str.replace(r'[^\d.]', '', regex=True)
    df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
    logging.info(f"Kolom '{col_name}': {original_non_numeric} nilai non-numerik dibersihkan dan dikonversi.")
    return df
def clean_date_column(df, col_name):
    df[col_name] = df[col_name].replace(['UNKNOWN', 'ERROR', '', None], pd.NA)
    date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%B %d, %Y']
    def try_parsing_date(text):
        for fmt in date_formats:
            try:
                return pd.to_datetime(text, format=fmt)
            except (ValueError, TypeError):
                continue
        return pd.NaT
    df[col_name] = df[col_name].apply(try_parsing_date)

    missing_count = df[col_name].isna().sum()

    if missing_count > 0:
        date_range = pd.date_range(start='2023-01-01', end='2023-12-31')
        random_dates = np.random.choice(date_range, size=missing_count)
        df.loc[df[col_name].isna(), col_name] = random_dates

    print(f"Jumlah nilai tanggal yang diimputasi: {missing_count}")
    return df
def standardize_categorical(df, col_name, mapping=None):
    df[col_name] = df[col_name].apply(lambda x: np.nan if x == 'Nan' else x)
    df.loc[:, col_name] = df[col_name].astype('object').fillna('').astype(str).str.strip().str.title()

    
    if mapping:
        df.loc[:, col_name] = df[col_name].replace(mapping)
    
    df.loc[:, col_name] = df[col_name].replace({
        'Unknown': pd.NA, 'Error': pd.NA, 'Nan': pd.NA, 'Na': pd.NA,
        'NaN': pd.NA, 'None': pd.NA, '': pd.NA
    })
    return df
def reconcile_total_spent(df):
    mask = df['Quantity'].notna() & df['Price Per Unit'].notna() & df['Total Spent'].notna()
    diff = (df.loc[mask, 'Quantity'] * df.loc[mask, 'Price Per Unit']) - df.loc[mask, 'Total Spent']
    inconsistent = (diff.abs() > 0.01).sum()
    logging.info(f"Rekonsiliasi Total Spent: {inconsistent} baris tidak konsisten ditemukan.")
    df.loc[mask & (diff.abs() > 0.01), 'Total Spent'] = df.loc[mask & (diff.abs() > 0.01), 'Quantity'] * df.loc[mask & (diff.abs() > 0.01), 'Price Per Unit']
    return df
def impute_numeric(df):
    missing_total_spent = df['Total Spent'].isna().sum()
    df.loc[df['Total Spent'].isna() & df['Quantity'].notna() & df['Price Per Unit'].notna(), 'Total Spent'] = \
        df['Quantity'] * df['Price Per Unit']
    logging.info(f"Imputasi Total Spent: {missing_total_spent} nilai diisi berdasarkan Quantity * Price Per Unit.")

    missing_quantity = df['Quantity'].isna().sum()
    df.loc[df['Quantity'].isna() & df['Total Spent'].notna() & df['Price Per Unit'].notna() & (df['Price Per Unit'] != 0), 'Quantity'] = \
        df['Total Spent'] / df['Price Per Unit']
    logging.info(f"Imputasi Quantity: {missing_quantity} nilai diisi berdasarkan Total Spent / Price Per Unit.")

    missing_price = df['Price Per Unit'].isna().sum()
    df.loc[df['Price Per Unit'].isna() & df['Total Spent'].notna() & df['Quantity'].notna() & (df['Quantity'] != 0), 'Price Per Unit'] = \
        df['Total Spent'] / df['Quantity']
    logging.info(f"Imputasi Price Per Unit: {missing_price} nilai diisi berdasarkan Total Spent / Quantity.")

    return df
def impute_categorical(df):
    df = df.copy()
    
    for col in ['Location', 'Payment Method', 'Item']:
        if df[col].isna().sum() > 0:
            mode_val = df[col].mode()
            if not mode_val.empty:
                df[col] = df[col].fillna(mode_val[0])

    logging.info("Imputasi nilai kategorikal dengan modus global selesai.")
    return df

def preprocess_data(data_input):
    logging.info("Mulai proses pre-processing data.")

    if isinstance(data_input, pd.DataFrame):
        df = data_input
    elif isinstance(data_input, str):
        if data_input.endswith('.csv'):
            df = pd.read_csv(data_input)
        else:
            df = pd.read_json(StringIO(data_input), orient='split')
    else:
        raise ValueError("Input harus berupa DataFrame, path file CSV, atau JSON string.")
    df = clean_numeric_column(df, 'Quantity')
    df = clean_numeric_column(df, 'Price Per Unit')
    df = clean_numeric_column(df, 'Total Spent')

    df = clean_date_column(df, 'Transaction Date')
    df = standardize_categorical(df, 'Item')
    df = standardize_categorical(df, 'Payment Method')
    df = standardize_categorical(df, 'Location')
    df = reconcile_total_spent(df)
    df = impute_numeric(df)

    df = impute_categorical(df)

    logging.info("Proses pre-processing data selesai.")
    df=df.to_json(orient='split')
    return df
