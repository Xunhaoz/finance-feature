import password
from FinMind.data import DataLoader
from tqdm import tqdm
import stock_crawer

import globals

if __name__ == "__main__":
    api = DataLoader()
    api.login_by_token(api_token=password.findmind_api_token)
    df = api.taiwan_stock_info()
    for stock_id in tqdm(df["stock_id"][:101]):
        globals.STOCK_CODE = stock_id
        globals.STOCK_PATH = f"./{stock_id}.csv"
        stock_crawer.download()
