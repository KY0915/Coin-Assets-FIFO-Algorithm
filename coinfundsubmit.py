import csv
import queue
import sys
class Crypto:
    def __init__(self, time, name, buyorsell,price,quantity):
        self.time=time
        self.name=name
        self.buyorsell=buyorsell
        self.price=price
        self.quantity=quantity
        

    def getname(self):
        print(self.name)


class trade:
    def __init__(self, buytime, selltime, name, quantity, pl, signforbuy, signforsell, buyprice, sellprice,):
        self.buytime = buytime
        self.selltime = selltime
        self.name = name
        self.quantity = quantity
        self.pl = pl
        self.signforbuy = signforbuy
        self.signforsell = signforsell
        self.buyprice = buyprice
        self.sellprice = sellprice



def calculate(input_csv):        
    with open(input_csv) as csv_file: 
        next(csv_file)
        readCSV = csv.reader(csv_file, delimiter=',')        
        trade_done = [] 
        d={}        
        pl=0
        namelst=[]
        rows=[]
        totalcoin=0
        msgs=[]
        for row in readCSV:
            if row[1] not in namelst:
                namelst.append(row[1])
            
            rows.append(row)
         
        for name in namelst:
            lst = [] #reset the list
            pl = 0 #reset the profit/loss
            for row in rows: #for all rows perform action
                if row[1]==name:
                    if int(row[3])<0:
                        buysellsign='sell'
                        totalcoin+=int(row[3])
                    else:
                        buysellsign='buy'
                        totalcoin+=int(row[3])
                    time,name,buyorsell,price,quantity=row[0],row[1],buysellsign,int(row[2]),int(row[3])
                    
                    if lst==[]:#this is going to work like a queue
                        lst.append(Crypto(time,name,buyorsell,price,quantity)) 
                        
                    if lst[0].name ==name and lst[0].buyorsell!=buyorsell:
                                        
                        if lst[0].quantity>=quantity:
                            
                            pl+=abs(price*quantity - lst[0].price*quantity)
                            d[name]=pl
                            lst[0].quantity+=quantity
                            trade_done.append(trade(lst[0].time, time, name, quantity, abs(price*quantity - lst[0].price*quantity), lst[0].buyorsell, buyorsell, lst[0].price, price))
                            
                            if lst[0].quantity==0:#if quantity==0 reset lst
                                del lst[0]


                        elif lst[0].quantity<quantity:
                            pl+=abs(lst[0].price*lst[0].quantity-price*lst[0].quantity)
                            quantity += lst[0].quantity
                            d[name]=pl
                            trade_done.append(trade(lst[0].time, time, name, lst[0].quantity, abs(lst[0].price*lst[0].quantity - price*lst[0].quantity), lst[0].buyorsell, buyorsell, lst[0].price, price))
                            del lst[0]

                            for open_trade in lst:
                                if open_trade.name==name:
                                    if quantity <= open_trade.quantity:
                                        pl += abs(price*quantity - open_trade.price*quantity)
                                        open_trade.quantity -= quantity
                                        
                                        trade_done.append(trade(open_trade.time, time, name, quantity, abs(price*quantity - open_trade.price*quantity), open_trade.buyorsell, buyorsell, open_trade.price, price))
                                        if open_trade.quantity == 0: 
                                            lst.remove(open_trade)
                                            break
                                    else:
                                        pl += abs(open_trade.price*open_trade.quantity - price*open_trade.quantity)
                                        quantity -= open_trade.quantity
                                        lst.remove(open_trade)
                                        continue                             
                                else:
                                    continue
                            if quantity >0:
                                lst.append(Crypto(time,name,buyorsell,price,quantity))

          
     
            if totalcoin < 0:
                return False
            msgs.append([name,totalcoin,totalcoin*price])
            totalcoin=0
            
    return d,msgs

try:
    input_csv = sys.argv[1] 
    d={}
    total=0
    totalpfv=0
    d,msgs=calculate(input_csv)
    print("Portfolio ( "+ str(len(d)) + " assets )")
    for msg in msgs:
        print(msg[0] + " : " + str(msg[1]) + " $" + str(msg[2]))
        totalpfv+=msg[2]
    print("Total portfolio value: $" + str(totalpfv))
    print("Portfolio P&L (" +str(len(d))+" assets) :") 

    for key,value in d.items():
        print(key+": $"+ str(value))
        total+=value
    print("Total P&L: $" + str(total))
except:
    print("Error: detected sale before purchase (short selling is not supported)")
