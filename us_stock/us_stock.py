import yfinance as yf
import time,os,csv,re
from pprint import pprint

t = time.localtime()
tfmt = time.strftime("%Y%m%d",t) 

chklist = ["symbol","regularMarketPreviousClose","regularMarketOpen","regularMarketPrice","regularMarketDayHigh","regularMarketDayLow"]

def get_stock(stockid,buy,num):
      try:
        stk_basic_data = yf.Ticker(stockid).info
        close = stk_basic_data.get('regularMarketPrice')
        earning = round(float(close)-float(buy),2)*(int(num))
        result = (str(tfmt) +" "+ stockid + " total earning is "+ str(earning))  
        print (result)
        try:
          f = open('./%s.csv'%stockid,'r')
          x = f.readlines()
          for y in x:
                z = y.split(",")
                if tfmt in z[0]:
                      writing = "false"
                      break
                else:
                     pass
          
          if writing != "false":
                with open('./%s.csv'%stockid,'a',newline='') as f:
                  writer = csv.writer(f)
                  writer.writerow((tfmt,stockid,close,earning))  
        
        except FileNotFoundError:
          with open('./%s.csv'%stockid,'w',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(("date","stockid","close priice","total earning"))
            writer.writerow((tfmt,stockid,close,earning))
      except KeyError:
        pass  


get_stock('snow',"247.03","100")
