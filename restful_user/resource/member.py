import pymysql
from flask_restful import Resource,reqparse
from flask import jsonify
import os
#�w�qmysql.connect���禡�A�æ^��db��cursor
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

#�w�q�@���~�ӤFResource��class�A�ó]get��post��ب禡
class Member(Resource):
    def get(self):   #�Hrequest.get�覡���ouser.member�o��table�����e�A�åHjson�榡�e�{
        db, cursor = db_init()
        #�Y�S���Hget�覡�n�D�^�ǫ��w��name�A�h�^�Ǿ��member table���e
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
    def post(self):#�Hrequest.post�覡�s�Wuser.member�o��table�����e�A�åHjson�榡�e�{
        db, cursor = db_init()
        parser = reqparse.RequestParser() #���opost��payload��
        parser.add_argument('id', type=int, required=True, location="form")
        parser.add_argument('name', type=str, required=True, location="form")
        parser.add_argument('gender', type=str, required=True, location="form")
        parser.add_argument('birth', type=str, required=True, location="form")
        parser.add_argument('note', type=str, location="form")
        args = parser.parse_args()
        #�N���o��payload�ȩ�Jdict
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
        #�^�Ǥ@��json{"message": message}�A�p�Gresult��True�A�h��success�A�Ϥ���failure
        return jsonify({"message": message})


#DELETE
sql = f'DELETE FROM `user`.`member` WHERE id = {id};'