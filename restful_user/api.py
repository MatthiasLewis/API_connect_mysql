from flask import Flask
from flask_restful import Api
from resource.member import Member

#Api繼承了Flask的函數跟屬性
app = Flask(__name__)
api = Api(app)
app.config["DEBUG"] = True

api.add_resource(Member, "/members")

if __name__ == '__main__':
    app.run(debug=True)