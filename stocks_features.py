import argparse
import logging
import math
import os
import stock_info.stock_crawer
import globals
import pandas as pd


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


def cal_apr():
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
    niu = dr.sum() / len(dr)  # niu表示平均值,即期望.
    niu2 = (dr ** 2).sum() / len(dr)  # niu2表示平方平均值
    niu3 = (dr ** 3).sum() / len(dr)  # niu3表示三方平均值
    sigma = math.sqrt(niu2 - niu * niu)
    niu4 = ((dr - niu) ** 4).sum()  # 峰度公式分子
    skewness = (niu3 - 3 * niu * sigma ** 2 - niu - -3) / (sigma ** 3)  # 偏度公式
    kurt = niu4 / (sigma ** 4)
    logging.info(f"skewness: {skewness}, kurt: {kurt}")
    print(f"skewness: {skewness}, kurt: {kurt}")
    return skewness, kurt


def cal_sortino_ratio():
    df = pd.read_csv(globals.STOCK_PATH)['close']
    dr = df.pct_change().dropna()

    # downside deviation:
    dr = dr.apply(lambda x: x if x < 0 else 0)
    temp_expectation = dr.mean()
    downside_dev = float(temp_expectation) ** 0.5

    # Sortino ratio:
    sortino_ratio = dr.mean() / downside_dev
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
        cal_apr()
    elif FEATURE == 2:
        # 年化波動度
        cal_volatility()
    elif FEATURE == 3:
        # 偏斜性
        cal_skewness()
    elif FEATURE == 4:
        cal_sortino_ratio()
