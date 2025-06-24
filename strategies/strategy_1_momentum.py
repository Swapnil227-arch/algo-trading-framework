import pandas as pd

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
#print(df.info())


trade = []
xbuying = 1#sl kitna niche hoga actual candle low se
xselling = 1

ybuying = [1,3,1] # maxprofitcalc se jo values nikal ke aarhi hai unhe yaha put karna hai.
yselling = [1,3,1]
# ydowntrendbuying = [4,1,4]
# ydowntrendselling = [4,1,4]
ivariable = 100# yaha per maximun SL for that particular instrument 
partitions = 10
steplen = ivariable/partitions
pointa = 4# maxprofitcalc mein jo aarhe hai pehle 2 numbers vo ye dono hai
pointb = 5


multiplier = 1
takeprofit = 0
stoploss = 0
buying = False
selling = False

for i in range(1, len(df) - 1):
    # Buying conditions
    if (
        df["green"].iloc[i]
        and df["green"].iloc[i - 1]
        and not selling  # Only buy if not selling
        and not buying  # Ensure that buying is not already ongoing
    ):
        buying = True
        selling = False  # Explicitly set selling to False
        lst = list(df.iloc[i + 1])
        lst.append("Buying started")
        stoploss = df["low"].iloc[i] - xbuying
        stoplosslen = df["open"].iloc[i+1] - stoploss 
        # Set take profit depending on trend
       
        if stoplosslen <pointa*steplen:
            takeprofit = df["open"].iloc[i+1] + (df["open"].iloc[i+1] - stoploss) * ybuying[0]
            multiplier = ybuying[0]

        if stoplosslen <pointb*steplen and stoplosslen> pointa*steplen:
            takeprofit = df["open"].iloc[i+1] + (df["open"].iloc[i+1] - stoploss) * ybuying[1]
            multiplier = ybuying[1]
                
        if stoplosslen >pointb*steplen:
            takeprofit = df["open"].iloc[i+1] + (df["open"].iloc[i+1] - stoploss) * ybuying[2]
            multiplier = ybuying[2]


        # elif not pd.isna(df["Down Trend"].iloc[i]):
        #     if stoplosslen <pointa*steplen:
        #         takeprofit = df["open"].iloc[i+1] + (df["open"].iloc[i+1] - stoploss) * ydowntrendbuying[0]
        #         multiplier = yuptrendbuying[0]

        #     if stoplosslen <pointb*steplen and stoplosslen> pointa*steplen:
        #         takeprofit = df["open"].iloc[i+1] + (df["open"].iloc[i+1] - stoploss) * ydowntrendbuying[1]
        #         multiplier = yuptrendbuying[1]
                
        #     if stoplosslen >pointb*steplen:
        #         takeprofit = df["open"].iloc[i+1] + (df["open"].iloc[i+1] - stoploss) * ydowntrendbuying[2]
        #         multiplier = yuptrendbuying[2]


        lst.append(0) # the y multiplier column will be set to 0 once the trade starts
        lst.append(df["open"].iloc[i+1]-stoploss); # adding stoploss to the lst
        lst.append(0) # adding pips
        trade.append(lst)
    # If currently buying, check if we need to finish buying
    if buying:
        if df["high"].iloc[i] >= takeprofit:  # Hit take profit
            lst = list(df.iloc[i])
            lst.append("Buying finished at Take profit")
            lst.append(multiplier)
            lst.append(0) # stop loss is set to zero when the trade ends
            lst.append(trade[-1][-2]*multiplier) # adding pips
            trade.append(lst)
            buying = False  # Finish buying
        elif df["low"].iloc[i] <= stoploss:  # Hit stop loss
            lst = list(df.iloc[i])
            
            lst.append("Buying finished at Stop loss")
            lst.append(-1)
            lst.append(0) # sl set to zero

            lst.append(trade[-1][-2]*-1) #  adding pips
            trade.append(lst)
            buying = False  # Finish buying

    # Selling conditions
    if (
        df["red"].iloc[i]
        and df["red"].iloc[i - 1]
        and not buying  # Only sell if not buying
        and not selling  # Ensure that selling is not already ongoing
    ):
        selling = True
        buying = False  # Explicitly set buying to False
        lst = list(df.iloc[i + 1])
        lst.append("Selling started")
        stoploss = df["high"].iloc[i] + xselling
        stoplosslen = stoploss - df["open"].iloc[i+1]
        # Set take profit depending on trend
        if stoplosslen <pointa*steplen:
            takeprofit = df["open"].iloc[i+1] + (df["open"].iloc[i+1] - stoploss) * yselling[0]
            multiplier = yselling[0]
        if stoplosslen <pointb*steplen and stoplosslen> pointa*steplen:
            takeprofit = df["open"].iloc[i+1] + (df["open"].iloc[i+1] - stoploss) * yselling[1]
            multiplier = yselling[1]
            
        if stoplosslen >pointb*steplen:
            takeprofit = df["open"].iloc[i+1] + (df["open"].iloc[i+1] - stoploss) * yselling[2]
            multiplier = yselling[2]
            
        # elif not pd.isna(df["Down Trend"].iloc[i]):
        #     if stoplosslen <pointa*steplen:
        #         takeprofit = df["open"].iloc[i+1] + (df["open"].iloc[i+1] - stoploss) * ydowntrendselling[0]
        #         multiplier = ydowntrendselling[0]

        #     if stoplosslen <pointb*steplen and stoplosslen> pointa*steplen:
        #         takeprofit = df["open"].iloc[i+1] + (df["open"].iloc[i+1] - stoploss) * ydowntrendselling[1]
        #         multiplier = ydowntrendselling[1]
                
        #     if stoplosslen >pointb*steplen:
        #         takeprofit = df["open"].iloc[i+1] + (df["open"].iloc[i+1] - stoploss) * ydowntrendselling[2]
        #         multiplier = ydowntrendselling[2]

        lst.append(0) # y multiplier is set to zero when the trade starts
        lst.append(stoploss -df["open"].iloc[i+1]); # addings stop loss to the list
        lst.append(0) # adding pips to the list
        trade.append(lst)
    # If currently selling, check if we need to finish selling
    if selling:
        if df["low"].iloc[i] <= takeprofit:  # Hit take profit
            lst = list(df.iloc[i])
            lst.append("Selling finished at Take profit")
            lst.append(multiplier)
            lst.append(0) #sl set to zero when the trade ends
            lst.append(trade[-1][-2]*multiplier) # addings pips
            trade.append(lst)
            selling = False  # Finish selling
        elif df["high"].iloc[i] >= stoploss:  # Hit stop loss
            lst = list(df.iloc[i])
            lst.append("Selling finished at Stop loss")
            lst.append(-1)
            lst.append(0) # sl set to zero when the trade ends
            lst.append(trade[-1][-2]*-1) # adding pips
            trade.append(lst)
            selling = False  # Finish selling

# Output the results
netpips = 0.0
netmultiplier = 0
for i in range(len(trade)):
    netpips += trade[i][-1]
    netmultiplier += trade[i][11]
    trade[i].append(netpips)
    trade[i].append(netmultiplier)
        
startdate = 0 
finaldate = 0 
maxloss = 0
for i in range(len(trade)):
    for j in range(i+1,len(trade)):
        if(trade[j][-2]-trade[i][-2]<maxloss):
            maxloss = trade[j][-2] - trade[i][-2]
            startdate = i
            finaldate = j 

startmulti = 0 
finalmulti = 0 
minmulti = 0
for i in range(len(trade)):
    for j in range(i+1,len(trade)):
        if(trade[j][-1]-trade[i][-1]<minmulti):
            minmulti = trade[j][-1] - trade[i][-1]
            startmulti = i
            finalmulti = j 


output = pd.DataFrame(trade, columns=["time", "open", "high", "low", "close", "volume", "green", "red", "action","y multiplier","stop loss","pips","Net Pips","Net multiplier"])
#pd.set_option('display.max_rows', None)  # Show all rows
print("Minimum value of Net Pips is ",maxloss," between the dates ",trade[startdate][0]," and ",trade[finaldate][0])
print("pips sum is ",output["pips"].sum())
#print("Minimum value of Net Multipliers is ",minmulti, "between the dates ",trade[startmulti][0], " and ", trade[finalmulti][0])
#print("Sum of multipliers is ",output["y multiplier"].sum())
#print(output)
# print(df)
