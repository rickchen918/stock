import requests as r
import pandas as pd
from pprint import pprint
import time,json,csv,os,configparser

TWSE_URL = "https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date="
MIS_URL = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?'

# 抓取notify token id
cfgpath = os.path.join('/root/aviatrix/python/stock/twse/','token.ini')
conf = configparser.ConfigParser()
conf.read(cfgpath,encoding='utf-8')
token = conf['token']['id']

begin = "09:00" # 開盤時間
close = "13:30" # 收盤時間

t = time.localtime()
tfmt = time.strftime("%Y%m%d",t) # 當日時間

# 大盤指數抓取
def twse():
    url = (TWSE_URL+tfmt+"&type=IND")
    #url = "https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=20210628&type=IND"
    try:
        resp = json.loads(r.get(url).text)['data1']
        for x in resp:
            if "發行量加權股價指數" in x:
                index = x[1]
                point = x[3]
                ratio = x[4]
        else:
            pass
        line_token = token
        headers = {
            "Authorization": "Bearer " + line_token,
            "Content-Type": "application/x-www-form-urlencoded"
            }
        
        params = {"message":"\n"
         +"日期: "+str(tfmt)+"\n"
         +"台股收盤指數: "+str(index)+"\n"
         +"指數漲跌: "+str(point)+"\n"
         +"漲跌幅度: "+str(ratio) +"\n"
         }
        stock = r.post("https://notify-api.line.me/api/notify",headers=headers, params=params)
        
        # writing the result data into csv file
        try:
            f = open('./taiwan_stock_index.csv','r')
            x = f.readlines()
            for y in x:
                z = y.split(",")
                if tfmt in z:
                    writing = "false"
                    break
                else:
                    pass

            if writing != "false":
                with open('./taiwan_stock_index.csv','a',newline='') as f:   
                    writer = csv.writer(f)
                    writer.writerow((tfmt,index,point,ratio)) 
        except FileNotFoundError:
            with open('./taiwan_stock_index.csv','w',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(('date','close_index',"up_down_index","up_down_precentage"))
                writer.writerow((tfmt,index,point,ratio))
    
    except KeyError:
        pass

# 個股信息抓取
def track(stockid,lprice,hprice):
    url = (MIS_URL+'ex_ch=tse_%s.tw_'+tfmt+'&json=1&delay=0')%stockid
    resp = json.loads(r.get(url).text)
    apicall = resp.get('msgArray')
    for msg in apicall:
        day = msg.get('d')
        name = msg.get('n')
        code = msg.get('c')
        yclose = msg.get('y') # 前一天收盤價
        dopen = msg.get('o') # 開盤價
        dhigh = msg.get('h') # 一天的高價
        dlow = msg.get('l')  # 一天的低價
        dprice = max(msg.get('a').split('_'))
        tamount = msg.get('f')
        #print(dprice)

    line_token = token
    headers = {
       "Authorization": "Bearer " + line_token,
       "Content-Type": "application/x-www-form-urlencoded"
     }
    params = {"message":"\n" 
            +"觸發原因: 成交價不再設定區域內 %s - %s"%(lprice,hprice)+"\n"
     +"股票代號:"+stockid+"\n"
     +"股票名稱:"+str(name)+"\n"
     +"日期 "+str(day) +"\n"
     +"昨日收盤價"+str(yclose) +"\n"
     +"開盤價"+str(dopen) +"\n"
     +"今日最高價"+str(dhigh) +"\n"
     +"今日最低價"+str(dlow) +"\n"
     +"當下成交價"+str(dprice) +"\n"
     +"當下成交量"+str(tamount) +"\n"
     }
    if lprice > dlow or hprice < dhigh:
        stock = r.post("https://notify-api.line.me/api/notify",headers=headers, params=params)
        #print ("match")
    else:
        pass


now = time.ctime().split(" ")[4]
#大盤回報
while now > close:
    twse()
    break

# # # 開盤時間每5分鐘檢查一次
while begin < now < close:
    track ("2912","250","275") # 統一超
    time.sleep(300)









