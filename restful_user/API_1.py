from flask import Flask
#設app為本檔案之flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
#測試行/執行行(__name__ 代表檔案名 '__main__'代表執行時的檔名)
if __name__ == '__main__':  #debug=True代表會在terminal顯示debug資訊 
    app.run(host="0.0.0.0", port=10001, debug=True, use_reloader=True)
#debug+use_reloader代表檔案不用重啟即可更新每次更動