import pymysql
from flask_restful import Resource,reqparse
from flask import jsonify
import os
#定義mysql.connect的函式，並回傳db及cursor
def db_init():
    KEY =os.getenv("SQL_PD")
    db = pymysql.connect(
        host='localhost',
        user='admin1',
        password=KEY,
        port=3306,
        db='user'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor

#定義一個繼承了Resource的class，並設get及post兩種函式
class Member(Resource):
    def get(self):   #以request.get方式取得user.member這個table的內容，並以json格式呈現
        db, cursor = db_init()
        #若沒有以get方式要求回傳指定的name，則回傳整個member table內容
        parser = reqparse.RequestParser()  
        parser.add_argument('name', type=str, location="args")
        args = parser.parse_args()
        
        filter_name = args.get("name")
        if filter_name is None:
            sql = 'SELECT * FROM user.member;'
        else:
            sql = f"SELECT * FROM user.member WHERE name LIKE '%{filter_name}%';"

        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()
        return jsonify(users)
    
    # Create User
    def post(self):#以request.post方式新增user.member這個table的內容，並以json格式呈現
        db, cursor = db_init()
        parser = reqparse.RequestParser() #取得post的payload值
        parser.add_argument('id', type=int, required=True, location="form")
        parser.add_argument('name', type=str, required=True, location="form")
        parser.add_argument('gender', type=str, required=True, location="form")
        parser.add_argument('birth', type=str, required=True, location="form")
        parser.add_argument('note', type=str, location="form")
        args = parser.parse_args()
        #將取得的payload值放入dict
        user = {
            'id': args['id'],
            'name': args['name'],
            'gender': args['gender'],
            'birth': args.get('birth') or '1900-01-01',
            'note': args.get('note')
        }
        sql = """

        INSERT INTO `user`.`member` (`id`,`name`,`gender`,`birth`,`note`)
        VALUES ('{}','{}','{}','{}','{}');

        """.format(user['id'],user['name'], user['gender'], user['birth'], user['note'])
        result = cursor.execute(sql)
        message = "success" if result == 1 else "failure"
        db.commit()
        db.close()
        #回傳一個json{"message": message}，如果result為True，則為success，反之為failure
        return jsonify({"message": message})


#DELETE
sql = f'DELETE FROM `user`.`member` WHERE id = {id};'