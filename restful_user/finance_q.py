from datetime import datetime
import requests
import os
API_KEY=os.getenv("X_API_KEY")
def get_symbols_info(symbols):
    url = "https://yfapi.net/v8/finance/spark"
    querystring = {
        "symbols": symbols,
        "interval": "1d",
        "range": "1mo"
    }

    headers = {
        'x-api-key': API_KEY
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    results = response.json()
#亦可用zip()將可迭代物件打包成用tuple組成的list，當有2組或以上list要分組時好用。
#用法zip(a,b)-->[(a1, b1), (a2, b2), (a3, b3)]
    results2={}
    results3={}
    for i in results: #取出的i會是symbols裡的值
        for k,v in enumerate(results[i]["timestamp"]): #list會取出index及value
            dt = datetime.fromtimestamp(v).strftime("%Y/%m/%d")
            results3[dt]=results[i]["close"][k]   
            #resulte3=dict(zip(a,b)) zip()用法
        results2[i]=results3
    return results2
#測試行/執行行(__name__ 代表檔案名 '__main__'代表執行時的檔名)
if __name__ == '__main__':
    print(get_symbols_info("AAPL,MSFT"))  

# results4={}
#["AAPL"]["timestamp"]
# for i in results["AAPL"]["timestamp"]:
#   dt = datetime.fromtimestamp(i)
#   dt = dt.strftime("%Y/%m/%d")
#   results2[dt]=results["AAPL"]["chartPreviousClose"]
# for i in results["TSLA"]["timestamp"]:
#   dt = datetime.fromtimestamp(i)
#   dt = dt.strftime("%Y/%m/%d")
#   results3[dt]=results["TSLA"]["chartPreviousClose"]
# #
# results4["AAPL"]=results2
# results4["TSLA"]=results3
# print(results4)
'''
透過"https://yfapi.net/v8/finance/spark"這隻API
取得AAPL, TSLA為期一個月且間格為一天的股價, 並整理成下方資料格式
{
    "AAPL": {
        "2021/12/21": "216.5",
        "2021/12/21": "216.5",
        "2021/12/21": "216.5",
        "2021/12/21": "216.5"
    },
    "TSLA": {
        "2021/12/21": "216.5",
        "2021/12/21": "216.5",
        "2021/12/21": "216.5",
        "2021/12/21": "216.5"
    }
}
'''
'''
Steps:
1. 將timestamp轉換成datetime(2021/12/21)
2. 將轉換過的timestamp_list 與close的price list合成上放的dict
3. 將股票代號設為key, value為整理過後的dict並return.
'''

