import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import pandas as pd
import sklearn
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import stocks_features
import globals


def read_feature():
    conn = sqlite3.connect("finance_feature.db")
    sql = """
        SELECT * from features
    """
    result = conn.execute(sql)

    data = {
        "stock_id": [],
        "mean": [],
        "variance": [],
        "skewness": [],
        "kurt": []
    }

    for stock_feature in result:
        data["stock_id"].append(stock_feature[1])
        data["mean"].append(stock_feature[2])
        data["variance"].append(stock_feature[3])
        data["skewness"].append(stock_feature[4])
        data["kurt"].append(stock_feature[5])

    df = pd.DataFrame(data=data)
    conn.close()
    return df


def processing_standard_scaler(df):
    stock_id = df.loc[:, 'stock_id']
    df = df.drop(['stock_id'], axis=1)

    scaler = preprocessing.StandardScaler()
    z_score = scaler.fit_transform(df)
    z_score = pd.DataFrame(z_score)

    z_score['stock_id'] = stock_id

    return z_score


def reduce_dimension(df):
    stock_id = df.loc[:, 'stock_id']
    df = df.drop(['stock_id'], axis=1)

    reduce = PCA(2)
    reduce.fit(df)
    df = reduce.transform(df)

    # df['stock_id'] = stock_id
    return df


def classify_by_KMeas(two_dime):
    kmeans = KMeans(n_clusters=6)
    kmeans.fit(two_dime)
    y_kmeans = kmeans.predict(two_dime)
    return y_kmeans


def plot_graph(data, pred):
    plt.scatter(data[:, 0], data[:, 1], c=pred, s=5, cmap='viridis')
    plt.show()


def store_result(df):
    conn = sqlite3.connect("finance_feature.db")
    for data in df.iterrows():
        sql = """
                INSERT INTO classification (`stock_id`, `group`, `sortino_ratio`)
                VALUES (?, ?, ?);
            """
        globals.STOCK_PATH = f'./stock_info/{data[1]["stock_id"]}.csv'
        conn.execute(sql, (data[1]["stock_id"], data[1]["kMeans"], stocks_features.cal_sortino_ratio()))
        conn.commit()
    conn.close()


if __name__ == "__main__":
    features = read_feature()

    # 標準化
    features_std_normal = processing_standard_scaler(features)

    # 降維
    feature_two_dime = reduce_dimension(features_std_normal)

    # 結果
    features['kMeans'] = classify_by_KMeas(feature_two_dime)

    # 畫圖
    plot_graph(feature_two_dime, features['kMeans'])

    print(features)
    store_result(features)
