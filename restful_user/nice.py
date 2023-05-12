import requests
import os
#練習API連接
url = "https://yfapi.net/v6/finance/quote"
API_KEY=os.getenv("X_API_KEY")

querystring = {"symbols":"AAPL,BTC-USD,EURUSD=X"}

headers = {
    'x-api-key': API_KEY
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
            