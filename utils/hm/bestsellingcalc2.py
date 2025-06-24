import csv

# defining the range of RSI (selected candles will have RSI less than the RSI value from the range)
rsilow = 20
rsihigh = 40
rsistep = 1
# defining the range of targetdecrement
tdecrementlow = 0.001
tdecrementhigh = 0.01
tdecrementstep = 0.0005
# defining the range of loss decrement
lincrementlow = 0.0005
lincrementhigh = 0.008
lincrementstep = 0.0005

# for lot calculation
lotcal = False# Set True if you want to calculate the Lot Size
lot = 1 # Default Lot size if it's not being calculated
lotlimit = 1# If lot is greater than this limit it's value will be reduced down to the limit


fivelow = 0.0
fivehigh = 0.001
#five = 0.0005 # must be positive agar value isse kam hogi then trail nhi karna hai
# note this variable must be integer
fivestep = 0.0001


margin = 71787.714
startinglosslength = 0.0005 # must be positive


# with open("datasheet badi vali.csv", mode="r") as csvfile:
#     file = csv.reader(csvfile)
#     data = []
#     for lines in file:
#         data.append(lines)
#
#     del data[0]  
#
with open("OANDA_AUDCAD, 240.csv", mode="r") as csvfile:
    file = csv.reader(csvfile)
    data = []
    for lines in file:      
        a0 = lines[0] #time 
        a1 = lines[1] #open
        a2 = lines[2] #high
        a3 = lines[3] #low
        a4 = lines[4] #close
        a5 = lines[5] #exit arows
        a6 = lines[6] #parabolicsar
        a7 = lines[7] #ema
        a8 = lines[8] #basis
        a9 = lines[9] #upper
        a10 = lines[10] #lower
        a11 = lines[11] #ema
        a12 = lines[12] #vwap
        a13 = lines[13] #volume
        a14 = lines[14] #rsi
        a15 = lines[15] #centre line
        a16 = lines[16] #volume strength
        a17 = lines[17] #price strength
        a18 = lines[18] #ATR
        line = [a0,a1,a2,a3,a4,a13,a8,a9,a10,a12,a14,a15,a16,a17]      
        data.append(line)

    del data[0]  



def netprofit(opening, loss, target, data, lot, net, lincrement,tdecrement,five):
    extra = 0

    for counter in range(opening, len(data)):
        extra += 1
        line = data[counter]
        high = float(line[2])
        op = float(line[1])
        low = float(line[3])
        clos = float(line[4])
        
        if high>=loss:
            lost = (float(data[opening][1])-loss)*lot*margin
            net += lost
            return extra,net
        elif low <= target:
            profit = (lot*tdecrement*margin)
            net+= profit
            
            return extra,net
        if op - clos >= five:
            loss = op + lincrement
            # loss =op +2
        elif op -clos <=-five:
            loss = clos+lincrement
            # loss = clos +2
    return extra,net

bestrsi = rsilow
bestticrement = tdecrementlow
bestlincrement = lincrementlow
bestfive = fivelow
maxprofit = 0.0
five = fivelow
rsi = rsilow
tdecrement = tdecrementlow
lincrement = lincrementlow
while five <=fivehigh:
    rsi = rsilow
    while rsi <= rsihigh:
        tdecrement = tdecrementlow
        while tdecrement<= tdecrementhigh:
            lincrement = lincrementlow
            while lincrement <= lincrementhigh:
                counter = 0 
                net = 0
                while(counter<len(data)-1):
                    line = data[counter]
                    if float(line[12])>float(line[13]) and float(line[4]) < float(line[6]) and float(line[4]) <float(line[9]) and float(line[10])<rsi:
                        start = counter
                        op =0.0
                        loss = startinglosslength
                        for cand in range(start,-1,-1):
                            candle = data[cand]
                            op = float(candle[1])
                            clos = float(candle[4])
                            # if op-clos >= 5 and op+lincrement-float(data[counter+1][1])>5: # difference of loss with the opening of trade should be greater than 5
                            if op - clos >= five and op - float(data[counter+1][1])>five: # difference of open of eligible candle with the opening of trade should be greater than 5
                                loss = op + lincrement
                                # loss = op +2
                                break
                        if loss==startinglosslength:
                            loss+= float(data[counter+1][1])
                        target = float(data[counter+1][1]) -tdecrement

                        if lotcal:
                            lot = 4/(loss-float(data[counter+1][1]))
                            if lot>lotlimit:
                                lot = lotlimit

                        ext,netnew = netprofit(counter+1,loss,target,data,lot,net,lincrement,tdecrement,five)
                        counter+= ext
                        net = netnew
                    else:
                        counter+=1

                if net>maxprofit:
                    maxprofit = net
                    bestrsi = rsi
                    bestticrement = tdecrement
                    bestlincrement = lincrement
                    bestfive = five
        
                lincrement += lincrementstep
                
            tdecrement += tdecrementstep
            
        rsi += rsistep
    five+= fivestep
        
print(f"Maximum Achievable Profit is {maxprofit} and that is possible")
print(f"when Target Increment is {bestticrement}\nLoss Decrement is {bestlincrement}\nRSI is {bestrsi}\nBest value of five is {bestfive}")
