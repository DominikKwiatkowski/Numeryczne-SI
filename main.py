import pandas as pd
import os
import matplotlib.pyplot as plt


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

plt.style.use('classic')

def decision(actualDay, nextDay, crossingType, df):
    if(crossingType is down):
        if df[actualDay] < df[nextDay]:
            return buy
        else:
            return pas
    else:
        if df[actualDay] < df[nextDay]:
            return sell
        else:
            return pas

# create plot with given x,y,path to save plot and name of ylabel
def plotCreate(y1, y2, y3, lbl1, lbl2, lbl3, name,rang):
    fig, ax = plt.subplots()
    x = list(range(26, rang))
    ax.plot(x, y1, '-b', label=lbl1)
    x = list(range(35, rang))
    ax.plot(x, y2, '-r', label=lbl2)
    #x = list(range(1000))
    #ax.plot(x, y3, '-g', label=lbl3)
    ax.legend()
    ax.set_title(name)


# counting value of ema, if data are wrong return 0

def ema(N: int, p, actualDay):
    if (actualDay - N < 0):
        return 0
    if (len(p) <= actualDay):
        return 0
    alpha = 1 - (2 / (N + 1))
    counter = 0
    denominator = 0
    factor = 1
    for i in range(actualDay, actualDay - N, -1):
        counter += factor * p[i]
        denominator += factor
        factor *= alpha
    return counter / denominator


# create a plot with stock prize, macd and signal
def create(CSVPath):
    rang=200
    df = pd.read_csv(CSVPath)
    df = df["open"]
    MACDList = []
    signalList = []
    for i in range(26, rang):
        MACDList.append(ema(12, df, i) - ema(26, df, i))
    for i in range(9, len(MACDList)):
        signalList.append(ema(9, MACDList, i))
    PriceList = []
    min = df.min()
    for i in range(rang):
        PriceList.append(df[i] - min)
    plotCreate(MACDList, signalList, PriceList, 'MACD', 'signal', 'stock prize', CSVPath,rang)


path = 'data/'
files = []
# files is list of all csv in data folder
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            files.append(os.path.join(r, file))
for f in files:
    create(f)
plt.show()
