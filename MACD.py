import pandas as pd
import os
import matplotlib


#down-MACD cross from down(after crossing is higher then signal)
down = 0
up = 1
buy = 0
sell = 1
pas = 2

def down():
    return down


def up():
    return up


def buy():
    return buy


def sell():
    return sell


def pas():
    return pas


def find_cut(signals: list, macd: list):
    cuts = []
    for idx in range(1, len(signals)):
        if signals[idx-1] is not None and macd[idx-1] is not None:
            if bool(signals[idx-1] > macd[idx-1]) != bool(signals[idx] > macd[idx]):
                cuts.append([idx, bool(signals[idx] > macd[idx])])
    return cuts


def decision(actualDay,nextDay, df):
    if(actualDay[1] is down):
        if df[actualDay[0]]["open"] < df[nextDay[0]]["open"]:
            return buy
        else:
            return pas
    else:
        if df[actualDay[0]]["open"] < df[nextDay[0]]["open"]:
            return sell
        else:
            return pas


# create plot with given x,y,path to save plot and name of ylabel
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
    for idx in range(len(data_file), 26, -1):
        data_file.loc[idx, "MACD"] = generate_EMA((data_file.loc[idx - 12:idx-1, "open"].tolist())[::-1]) - \
                                     generate_EMA((data_file.loc[idx - 26:idx-1, "open"].tolist())[::-1])


def generate_SIGNAL(data_file):
    data_file.insert(len(data_file.columns), "SIGNAL", None)
    for idx in range(len(data_file), 35, -1):
        data_file.loc[idx, "SIGNAL"] = generate_EMA(data_file.loc[idx - 9:idx - 1, "MACD"].tolist()[::-1])


def organiser(path: str):
    data = open_file(path)
    data = data.loc[0:200]
    generate_MACD(data)
    generate_SIGNAL(data)
    draw_plot(data.loc[36:])
    print(find_cut(data.loc[:, "SIGNAL"].tolist(), data.loc[:, "MACD"].tolist()))
    x = data.loc[:, "SIGNAL"].tolist(), data.loc[:, "MACD"].tolist()
    for i in range(len(x)-1):
        print(decision(x[i],x[i+1],data))

def draw_plot(data):
    data.plot(x="date", y=["MACD", "SIGNAL"], title="SIGNAL/MACD")


organiser("data/INTC.csv")