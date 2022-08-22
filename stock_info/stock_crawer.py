import password
import requests
from FinMind.data import DataLoader
import logging
from datetime import date
from dateutil.relativedelta import relativedelta
import globals


def download():
    logging.info('stock_crawer.py function execution')
    # logging config
    logging.basicConfig(filename='stock_crawer.log', level=logging.INFO)

    # login
    api = DataLoader()
    api.login_by_token(api_token=password.findmind_api_token)

    # get user limitation
    url = "https://api.web.finmindtrade.com/v2/user_info"
    parload = {"token": password.findmind_api_token}
    resp = requests.get(url, params=parload)
    user_count = resp.json()["user_count"]  # 使用次數
    api_request_limit = resp.json()["api_request_limit"]  # api 使用上限
    time_wait = 0
    while user_count >= api_request_limit - 1:
        logging.warning(f'wait until api is available, we have already waited: {time_wait}s')

    # 設定時間序 十年
    end_date = date.today()
    start_date = end_date - relativedelta(years=10)
    logging.info(f"end_date: {end_date}, start_date:{start_date}")

    # 取得台股資料
    df = api.taiwan_stock_daily(
        stock_id=globals.STOCK_CODE,
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d")
    )

    # save and change index
    df.set_index('date', drop=True).to_csv(globals.STOCK_PATH)
    logging.info(f"successful save {globals.STOCK_CODE}")


if __name__ == "__main__":
    logging.info('stock_crawer.py direct execution')
    download()
