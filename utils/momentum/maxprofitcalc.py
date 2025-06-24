import pandas as pd

slvalue = 100 # maximum length of stop loss
sldivisions = 10
xbuying = 1 # buy order mein sl actual value se kitna niche hoga
xselling = 1 # same for sell side
steplen = slvalue / sldivisions
ratios = [1, 2, 3, 4] # kya ratios per check karna hai, like kam stop loss hoga toh kam profit lo and jyada hoga toh jyada ka profit rakho
possibilities = []
for a in range(sldivisions):
    for b in range(a, sldivisions):
        for c in ratios:
            for d in ratios:
                for e in ratios:
                    possibilities.append([a, b, c, d, e])


df = pd.read_csv("OANDA_XAUUSD, 240.csv")
df["green"] = df["close"] > df["open"]
df["red"] = df["close"] < df["open"]
df = df.drop("Exit Arrows",axis =1)
df = df.drop("ParabolicSAR",axis =1)
df = df.drop("EMA",axis =1)
df = df.drop("Basis",axis =1)
df = df.drop("Upper",axis =1)
df = df.drop("Lower",axis =1)
df = df.drop("EMA.1",axis =1)
df = df.drop("VWAP",axis =1)
df = df.drop("RSI",axis =1)
df = df.drop("Centre line",axis =1)
df = df.drop("Volume strength",axis =1)
df = df.drop("Price strength",axis =1)
df = df.drop("ATR",axis =1)

print(df)
multiplier = 0
best = []
trade = []
# format of trade [time,open,high,low,close,up trend,down trend,volume,green,red,action,stoploss,take profit multiplier,pips]

maxpips = 0.0
print(len(possibilities))
for j in possibilities:
    a, b, c, d, e = j
    # a is the first seperator, b second sep, c is the multiplier for take profit in the 0-a region
    # d is the multiplier for take profit in the a-b region

    # e is the multiplier for take profit in the b-end region
    asl = a * steplen
    bsl = b * steplen
    buying = False
    selling = False
    stoploss = 0
    takeprofit = 0
    netpips = 0.0
    for i in range(1, len(df) - 1):
        # condition for starting trade
        if (
            df["green"].iloc[i] == True
            and df["green"].iloc[i - 1] == True
            and buying == False
            and selling == False
        ):
            # print("buying started")
            buying = True
            selling = False
            lst = list(df.iloc[i + 1])
            lst.append("Buying started")
            stoploss = df["low"].iloc[i] - xbuying
            lst.append(df["open"].iloc[i + 1] - stoploss)
            if (
                df["open"].iloc[i + 1] - stoploss <= asl
            ):  # adding multiplier for take profit
                takeprofit = (
                    df["open"].iloc[i + 1] + (df["open"].iloc[i + 1] - stoploss) * c
                )
                multiplier = c

            if (
                df["open"].iloc[i + 1] - stoploss < bsl
                and df["open"].iloc[i + 1] - stoploss > asl
            ):
                takeprofit = (
                    df["open"].iloc[i + 1] + (df["open"].iloc[i + 1] - stoploss) * d
                )
                multiplier = d
            if df["open"].iloc[i + 1] - stoploss >= bsl:
                takeprofit = (
                    df["open"].iloc[i + 1] + (df["open"].iloc[i + 1] - stoploss) * e
                )
                multiplier = e
            lst.append(0)  # multiplier is set to 0 when the trade starts
            lst.append(0)  # adding pips it should be equal to multiplier * stoploss
            trade.append(lst)

        if buying:
            if df["high"].iloc[i] >= takeprofit:  # Hit take profit
                # print("Buying ended at take profit")
                lst = list(df.iloc[i])
                lst.append("Buying finished at Take profit")
                lst.append(multiplier)  # multiplier
                lst.append(0)  # stop loss is set to zero when the trade ends
                lst.append(trade[-1][-3] * multiplier)  # adding pips
                netpips += trade[-1][-3] * multiplier
                # print(netpips)
                trade.append(lst)
                buying = False  # Finish buying
            elif df["low"].iloc[i] <= stoploss:  # Hit stop loss
                lst = list(df.iloc[i])
                # print("buying ended at stop loss")
                lst.append("Buying finished at Stop loss")
                lst.append(-1)  # multiplier
                lst.append(0)  # sl set to zero

                lst.append(trade[-1][-3] * -1)  #  adding pips

                netpips += trade[-1][-3] * -1
                # print(netpips)
                trade.append(lst)
                buying = False  # Finish buying

        # condition for starting trade selling

        if (
            df["red"].iloc[i] == True
            and df["red"].iloc[i - 1] == True
            and buying == False
            and selling == False
        ):
            # print("selling started")
            buying = False
            selling = True
            lst = list(df.iloc[i + 1])
            lst.append("Selling started")
            stoploss = df["high"].iloc[i] + xselling
            lst.append(stoploss - df["open"].iloc[i + 1])
            if (
                stoploss - df["open"].iloc[i + 1] <= asl
            ):  # adding multiplier for take profit

                takeprofit = (
                    df["open"].iloc[i + 1] - (stoploss - df["open"].iloc[i + 1]) * c
                )
                multiplier = c

            if (
                stoploss - df["open"].iloc[i + 1] < bsl
                and stoploss - df["open"].iloc[i + 1] > asl
            ):

                takeprofit = (
                    df["open"].iloc[i + 1] - (stoploss - df["open"].iloc[i + 1]) * d
                )

                multiplier = d
            if stoploss - df["open"].iloc[i + 1] >= bsl:

                takeprofit = (
                    df["open"].iloc[i + 1] - (stoploss - df["open"].iloc[i + 1]) * e
                )
                multiplier = e
            lst.append(0)  # multiplier is set to 0 when the trade starts
            lst.append(0)  # adding pips it should be equal to multiplier * stoploss
            trade.append(lst)

        if selling:

            if df["low"].iloc[i] <= takeprofit:  # Hit take profit
                # print("selling ended")
                lst = list(df.iloc[i])
                lst.append("Selling finished at Take profit")
                lst.append(multiplier)  # multiplier
                lst.append(0)  # stop loss is set to zero when the trade ends
                lst.append(trade[-1][-3] * multiplier)  # adding pips
                netpips += trade[-1][-3] * multiplier
                # print(netpips)
                trade.append(lst)
                selling = False  # Finish selling
            elif df["high"].iloc[i] >= stoploss:  # Hit stop loss
                lst = list(df.iloc[i])

                lst.append("Selling finished at Stop loss")
                lst.append(-1)  # multiplier
                lst.append(0)  # sl set to zero

                lst.append(trade[-1][-3] * -1)  #  adding pips

                netpips += trade[-1][-3] * -1
                # print(netpips)
                trade.append(lst)
                selling = False  # Finish buying

    # print(netpips,"Net pips made when value of a,b,c,d,e were",[a,b,c,d,e],"\n")
    if netpips > maxpips:
        maxpips = netpips
        best.clear()
        best.append(a)

        best.append(b)
        best.append(c)
        best.append(d)
        best.append(e)

# output = pd.DataFrame(trade, columns=["time", "open", "high", "low","close","volume","green", "red","action","stoploss","multiplier","pips"] )
#
# # format of trade [time,open,high,low,close,up trend,down trend,volume,green,red,action,stoploss,take profit multiplier,pips]
# pd.set_option('display.max_rows', None)
# print(output)
print(best)
print(maxpips)
print("hello")
