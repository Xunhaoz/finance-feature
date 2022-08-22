import argparse
import logging
import math
import os
import stock_info.stock_crawer
import globals
import pandas as pd
import finance_calculator as fc


def is_file_exist(file_name):
    file_path = os.path.join('stock_info', file_name + '.csv')
    if os.path.exists(file_path):
        return True
    return False


def cal_max_drawdown():
    df = pd.read_csv(globals.STOCK_PATH)
    max_price = df['close'].max(axis=0, skipna=True)
    min_price = df['close'].min(axis=0, skipna=True)
    max_drawdown = (min_price - max_price) / max_price
    logging.info(f"max_price: {max_price}, min_price: {min_price}, max_drawdown: {max_drawdown}")
    print(f"max_price: {max_price}, min_price: {min_price}, max_drawdown: {max_drawdown}")
    return max_price, min_price, max_drawdown


def cal_irr():
    df = pd.read_csv(globals.STOCK_PATH)['close']
    dr = df / df.shift(1)  # 取得損益百分比
    dr = dr.dropna()
    pr = dr.prod() ** (1 / len(dr))  # 幾何平均數
    apr = pr ** 252
    logging.info(f"apr: {apr}")
    print(f"apr: {apr}")
    return apr


def cal_volatility():
    df = pd.read_csv(globals.STOCK_PATH)['close']
    dr = df.pct_change().dropna()
    volatility = dr.std() * (252 ** 0.5)  # 年畫波動度
    logging.info(f"volatility: {volatility}")
    print(f"volatility: {volatility}")
    return volatility


def cal_skewness():
    df = pd.read_csv(globals.STOCK_PATH)['close']
    dr = df.pct_change().dropna()
    skewness = dr.skew()
    kurt = dr.kurt()
    print(f"skewness: {skewness}, kurt: {kurt}")
    logging.info(f"skewness: {skewness}, kurt: {kurt}")
    return skewness, kurt


def cal_sortino_ratio():
    df = pd.read_csv(globals.STOCK_PATH)['close']
    dr = df.pct_change().dropna()
    mean = dr.mean() * 252
    std_neg = dr[dr < 0].std() * (252 ** 0.5)
    sortino_ratio = mean / std_neg
    print(f"sortino_ratio: {sortino_ratio}")
    logging.info(f"sortino_ratio: {sortino_ratio}")
    return sortino_ratio


if __name__ == "__main__":
    # logging config
    logging.basicConfig(filename='stocks_features.log', level=logging.INFO)

    # args config
    parser = argparse.ArgumentParser()
    parser.add_argument("--stock_code", "-code", type=str, help="Entering stock code", required=True)
    parser.add_argument("--feature", "-f", type=int, help="choose feature ypu want", required=True)
    args = parser.parse_args()

    # global argument
    globals.STOCK_CODE = args.stock_code
    globals.STOCK_PATH = f'./stock_info/{globals.STOCK_CODE}.csv'
    FEATURE = args.feature

    # download files or not
    logging.info(is_file_exist(globals.STOCK_CODE))
    if not is_file_exist(globals.STOCK_CODE):
        stock_info.stock_crawer.download()

    if FEATURE == 0:
        # max drawdown
        cal_max_drawdown()
    elif FEATURE == 1:
        # 年化報酬率
        cal_irr()
    elif FEATURE == 2:
        # 年化波動度
        cal_volatility()
    elif FEATURE == 3:
        # 偏斜性
        cal_skewness()
    elif FEATURE == 4:

        cal_sortino_ratio()
# skewness: 849441.9169631663, kurt: 13436.992232774108
