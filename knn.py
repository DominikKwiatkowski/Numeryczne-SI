import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


def open_file(path: str) -> pd.DataFrame:
    return pd.DataFrame(pd.read_csv(path))


def generate_EMA(data_file: list) -> float:
    val = 0
    period = len(data_file)
    alpha = 1 - 2 / (period + 1)
    for day in range(0, period):
        val += (alpha ** day) * data_file[day]
    return val / ((1 - alpha ** period) / (1 - alpha))


def generate_MACD(data_file):
    data_file.insert(len(data_file.columns), "MACD", None)
    for idx in range(len(data_file) - 1, 26, -1):
        data_file.loc[idx, "MACD"] = generate_EMA((data_file.loc[idx - 12:idx - 1, "open"].tolist())[::-1]) - \
                                     generate_EMA((data_file.loc[idx - 26:idx - 1, "open"].tolist())[::-1])


def generate_SIGNAL(data_file):
    data_file.insert(len(data_file.columns), "SIGNAL", None)
    for idx in range(len(data_file) - 1, 35, -1):
        data_file.loc[idx, "SIGNAL"] = generate_EMA(data_file.loc[idx - 9:idx - 1, "MACD"].tolist()[::-1])


def draw_plot(data):
    data.plot(x="date", y=["MACD", "SIGNAL"], title="SIGNAL/MACD")


def find_cut(signals: list, macd: list):
    cuts = []
    for idx in range(1, len(signals)):
        if signals[idx - 1] is not None and macd[idx - 1] is not None:
            if bool(signals[idx - 1] > macd[idx - 1]) != bool(signals[idx] > macd[idx]):
                cuts.append([idx, bool(signals[idx] > macd[idx])])
    return cuts[:-1]


def insert_decisions(data_file, decisions):
    data_file.insert(len(data_file.columns), "DECISION", None)
    for decision in decisions:
        data_file.loc[decision[0], "DECISION"] = int(decision[1])


def remove_non_decisional(data_file):
    for i in range(0, len(data_file)):
        if data_file.loc[i, "DECISION"] is None:
            data_file.drop(i, inplace=True)
    data_file.reset_index()


def buyer_seller(starting_price, X_test, y_pred,y_test):
    stocks_amount = 0
    money = 1000
    max_stocks = 0
    max_money=1000
    for i in range(len(X_test)):
        if(y_pred[i]==0):
            stockBuy = int(money / X_test[i][0])
            money -= stockBuy * X_test[i][0]
            stocks_amount+=stockBuy
        elif y_test[i]==1:
            money += stocks_amount * X_test[i][0]
            stocks_amount = 0
    return stocks_amount * starting_price[1] + money - 1000

def decision(actualDay, nextDay, df):
    if (actualDay[1] is False):
        if df.loc[actualDay[0]]["open"] > df.loc[nextDay[0]]["open"]:
            actualDay[1] = 2
    # else:
    #    if df.loc[actualDay[0]]["open"] < df.loc[nextDay[0]]["open"]:
    #       actualDay[1]=2


def predict_knn(df):
    y = df.iloc[:, 5].values
    X = df.iloc[:, [1,3,4]].values
    y = y.astype('int')
    knn = KNeighborsClassifier(n_neighbors=3, metric='euclidean')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20,shuffle=False)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    return y_pred,X_test,y_test

def organiser(path: str):
    data = open_file(path)
    #data = data.loc[0:200]
    generate_MACD(data)
    generate_SIGNAL(data)
    # draw_plot(data.loc[36:])
    cuts = find_cut(data.loc[:, "SIGNAL"].tolist(), data.loc[:, "MACD"].tolist())
    for i in range(len(cuts) - 1):
        decision(cuts[i], cuts[i + 1], data)
    insert_decisions(data, cuts)
    starting_price = [data.loc[0, "open"], data.loc[len(data) - 1, "open"]]
    remove_non_decisional(data)
    #print(data)
    y_pred,X_test, y_test = predict_knn(data)
    print(buyer_seller(starting_price, X_test,y_pred,y_test))


organiser("data/AMD.csv")
