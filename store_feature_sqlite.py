import os
import sqlite3
import pandas as pd


def init_db():
    conn = sqlite3.connect("finance_feature.db")
    sql = """
        CREATE TABLE features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id TEXT,
            mean REAL,
            variance REAL,
            skewness REAL, 
            kurt REAL
        );
    """
    conn.execute(sql)
    conn.commit()

    sql = """
            CREATE TABLE classification (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `stock_id` TEXT,
                `group` REAL,
                `sortino_ratio` REAL
            );"""
    conn.execute(sql)
    conn.commit()

    conn.close()


def create_feature(stock_id, mean, variance, skewness, kurt):
    conn = sqlite3.connect("finance_feature.db")
    sql = """
        INSERT INTO features (stock_id, mean, variance, skewness, kurt)
        VALUES (?, ?, ?, ?, ?);
    """
    conn.execute(sql, (stock_id, mean, variance, skewness, kurt))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # create database
    init_db()

    # generate feature from stocks_info
    for (root, dirs, files) in os.walk('./stock_info'):
        for file in files:
            if file.endswith(".csv"):
                df = pd.read_csv(os.path.join('./stock_info', file))
                df = df[~(df['close'] == 0)]
                df = df['close'].pct_change().dropna()
                stock_id = file[:-4]

                mean = df.mean()
                var = df.var()
                skewness = df.skew()
                kurt = df.kurt()
                create_feature(stock_id, mean, var, skewness, kurt)
