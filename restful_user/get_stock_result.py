from flask import Flask
import finance_q
#設app為本檔案之flask
app = Flask(__name__)

@app.route("/",methods=["GET"])
def get_stock():
    return finance_q.get_symbols_info("AAPL,MSFT")

#測試行/執行行(__name__ 代表檔案名 '__main__'代表執行時的檔名)
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=10001, debug=True, use_reloader=True)