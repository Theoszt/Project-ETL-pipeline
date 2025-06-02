import psycopg2
from psycopg2.extras import execute_batch
import pandas as pd
import numpy as np

def clean_dataframe_for_postgres(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "IsWeekend" in df.columns:
        df["IsWeekend"] = df["IsWeekend"].apply(lambda x: bool(x) if pd.notnull(x) else None)

    for col in df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns:
        df[col] = df[col].apply(lambda x: x if pd.notnull(x) else None)
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x if pd.notnull(x) else None)

    return df

def save_to_postgres(df: pd.DataFrame):
    """
    Simpan DataFrame ke PostgreSQL dengan menangani nilai null secara eksplisit.
    """
    conn_params = {
        'host': 'localhost',
        'port': '5432',
        'database': 'Cafe sales',
        'user': 'postgres',
        'password': 'admin123'
    }

    table_name = 'result_cafe'
    df_clean = clean_dataframe_for_postgres(df)
    try:
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()
        cols = [f'"{col}"' for col in df_clean.columns]
        placeholders = ', '.join(['%s'] * len(cols))
        query = f'INSERT INTO {table_name} ({", ".join(cols)}) VALUES ({placeholders})'
        
        # Coba satu per satu agar tahu baris mana yang error
        for i, row in enumerate(df_clean.to_numpy()):
            try:
                cur.execute(query, tuple(row))
            except Exception as row_error:
                print(f"❌ Gagal pada baris ke-{i}: {row_error}")
                print("👉 Nilai kolom:")
                for col_name, val in zip(df_clean.columns, row):
                    print(f"   - {col_name}: {val} ({type(val)})")
                raise row_error  # opsional: hentikan langsung
        conn.commit()
        print(f"✅ Data berhasil disimpan ke tabel {table_name}")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error saat menyimpan data ke PostgreSQL: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
