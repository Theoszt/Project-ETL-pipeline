import numpy as np
import logging
import pandas as pd

def feature_engineer(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Mulai proses feature engineering.")
    
    # Debug tipe data awal
    print("Tipe data awal:")
    print(df.dtypes)
    print("\nContoh data awal:")
    print(df.head(3))
    
    # Konversi kolom tanggal dan numerik
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], errors='coerce', unit='ms')
    df['Total Spent'] = pd.to_numeric(df['Total Spent'], errors='coerce')
    
    # Debug tipe data setelah konversi
    print("\nTipe data setelah konversi 'Transaction Date' dan 'Total Spent':")
    print(df[['Transaction Date', 'Total Spent']].dtypes)
    print(df[['Transaction Date', 'Total Spent']].head(3))
    
    # Tambah fitur baru
    df['DayOfWeek'] = df['Transaction Date'].dt.dayofweek
    df['Month'] = df['Transaction Date'].dt.month
    df['IsWeekend'] = df['DayOfWeek'].isin([5,6]).astype(int)
    
    # Debug tipe data setelah fitur waktu
    print("\nTipe data setelah menambahkan fitur waktu:")
    print(df[['DayOfWeek', 'Month', 'IsWeekend']].dtypes)
    print(df[['DayOfWeek', 'Month', 'IsWeekend']].head(3))
    
    # Rata-rata pengeluaran per lokasi
    avg_spent_per_location = df.groupby('Location')['Total Spent'].transform('mean')
    df['AvgSpentPerLocation'] = avg_spent_per_location
    df['SpentRatioToLocationAvg'] = df['Total Spent'] / df['AvgSpentPerLocation']
    
    # Debug tipe data setelah fitur pengeluaran
    print("\nTipe data setelah menambahkan fitur pengeluaran:")
    print(df[['AvgSpentPerLocation', 'SpentRatioToLocationAvg']].dtypes)
    print(df[['AvgSpentPerLocation', 'SpentRatioToLocationAvg']].head(3))
    
 
    payment_counts = df.groupby('Payment Method')['Transaction Date'].transform('count')
    df['PaymentMethodCount'] = payment_counts
    
    # Debug tipe data setelah fitur metode p    embayaran
    print("\nTipe data setelah menambahkan fitur metode pembayaran:")
    print(df['PaymentMethodCount'].dtype)
    print(df['PaymentMethodCount'].head(3))
    
    
    # Klasifikasi musim penjualan
    def get_sales_season(month):
        if month in [11, 12, 1]: 
            return 'High Season'
        elif month in [6, 7, 8]:  
            return 'Mid Season'
        else:
            return 'Low Season'

    df['Sales Season'] = df['Month'].apply(get_sales_season)
    
    # Klasifikasi kategori harga
    def categorize_price(price):
        if price <= 2.0:
            return 'Murah'
        elif price <= 3.5:
            return 'Sedang'
        else:
            return 'Mahal'

    df['Price Category'] = df['Price Per Unit'].apply(categorize_price)
    
    # Debug tipe data akhir
    print("\nTipe data akhir setelah semua feature engineering:")
    print(df.dtypes)
    print(df.head(3))
    
    logging.info("Proses feature engineering selesai.")
    return df
