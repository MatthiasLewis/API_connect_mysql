import pymysql
from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required,get_jwt_identity
from . import route_model
from datetime import timedelta
import os

def db_init():
    db = pymysql.connect(
        host='localhost',
        user='admin1',
        password=os.getenv("SQL_PD"),
        port=3306,
        db='user'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor

security_params = [{"bearer": []}]

class Login(MethodResource):
    @doc(description="login API", tags=['Login'])
    @use_kwargs(route_model.LoginSchema, location="form")
    @marshal_with(route_model.LoginResponse)
    def post(self, **kwargs):
        db, cursor = db_init()
        account, password = kwargs["account"], kwargs["password"]
        sql = f"SELECT * FROM user.member WHERE account = '{account}' AND password = '{password}';"
        cursor.execute(sql)
        user = cursor.fetchall()
        db.close()

        if user != ():
            token = get_access_token(account,user[0]["role_id"])
            data = {
                "message": f"Welcome back {user[0]['name']}",
                "token": token}
            return data, 200
        
        return jsonify({"message":"Account or password is wrong"})
#從JWT中取"user_claims"，若沒有權限會直接403
def set_http_methods(func):
    def wrap(*args,**kwrags):
        current_user = get_jwt_identity()
        http_method = current_user["user_claims"]
        if http_method=="GET" and func.__name__ != "get":
            return jsonify({"message":"沒有權限"})
        elif http_method=="!DELETE" and func.__name__ =="delete":
                return jsonify({"message":"沒有權限"})
        return func(*args,**kwrags)
    return wrap
#建立JWTtoken       
def get_access_token(account,role_id):
    http_method=None
    if role_id==1:
        http_method="GET"
    elif role_id==2:
        http_method="!DELETE"
    elif role_id==3:
        http_method="*"
    token = create_access_token(
        identity={"account": account,"user_claims":http_method},
        expires_delta=timedelta(days=1)
    )
    return token

class Member(MethodResource):
    @doc(description="Get members", tags=['User'], security=security_params)
    @use_kwargs(route_model.MemberGetSchema, location="query")
    @marshal_with(route_model.MemberGetRes)
    @jwt_required()
    @set_http_methods
    def get(self, name=None, limit=None , offset=0):
        db, cursor = db_init()
        sql = "SELECT * FROM user.member "
        if name :
            sql += f"where name LIKE '%{name}%' "
        if limit :
            sql += f"limit {limit} "    
            sql += f"offset {offset}"

        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()
        return {"data":users}, 200
    #,{"data": users}
    @doc(description="create members", tags=['User'], security=security_params)
    @use_kwargs(route_model.MemberPostSchema, location="form")
    @marshal_with(route_model.MemberPostRes)
    @jwt_required()
    @set_http_methods
    def post(self, **kwargs):
        db, cursor = db_init()
        
        user = {
            'id':kwargs['id'],
            'name': kwargs['name'],
            'gender': kwargs['gender'],
            'birth': kwargs.get('birth') or '1900-01-01',
            'note': kwargs.get('note'),
            'account': kwargs['account'],
            'password': kwargs['password'],
            'role_id':kwargs['role_id']
        }
        sql = """

        INSERT INTO `user`.`member` (`id`,`name`,`gender`,`birth`,`note`,`account`,`password`,`role_id`)
        VALUES ('{}','{}','{}','{}','{}','{}','{}','{}');

        """.format(user['id'],user['name'], user['gender'], user['birth'], user['note'], user['account'], user['password'],user['role_id'])
        result = cursor.execute(sql)
        message = "success" if result == 1 else "failure"
        
        db.commit()
        db.close()      
        return jsonify({"message": message})

class SingleMember(MethodResource):
    #Get single by id
    @doc(description="get single members", tags=['User'], security=security_params)
    @marshal_with(route_model.SingleMemberGetRes)
    @jwt_required()
    @set_http_methods
    def get(self, id):
        db, cursor = db_init()
        sql = f"SELECT * FROM user.member WHERE id = '{id}';"
        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()
        return {"data": users}, 200

    @doc(description="update single members", tags=['User'], security=security_params)
    @use_kwargs(route_model.SingleMemberPatchRes, location="form")
    @marshal_with(route_model.SingleMemberPatcRes)
    @jwt_required()
    @set_http_methods
    def patch(self, id, **kwargs):
        db, cursor = db_init()
        
        user = {
            'name': kwargs.get('name'),
            'gender': kwargs.get('gender'),
            'birth': kwargs.get('birth'),
            'note': kwargs.get('note'),
            'account': kwargs.get('account'),
            'password': kwargs.get('password'),
        }

        query = []
        for key, value in user.items():
            if value is not None:
                query.append(f"{key} = '{value}'")
        query = ",".join(query)
        '''
        UPDATE table_name
        SET column1=value1, column2=value2, column3=value3···
        WHERE some_column=some_value;

        '''
        sql = """
            UPDATE user.member
            SET {}
            WHERE id = {};
        """.format(query, id)

        result = cursor.execute(sql)
        message = "success" if result == 1 else "failure"
        db.commit()
        db.close()
        
        return jsonify({"message": message})

    @doc(description="Delete single members", tags=['User'], security=security_params)
    @marshal_with(route_model.SingleMemberDeleteRes, code=200)
    @jwt_required()
    @set_http_methods
    def delete(self, id):
        db, cursor = db_init()
        sql = f'DELETE FROM `user`.`member` WHERE id = {id};'
        result = cursor.execute(sql)
        message = "success" if result == 1 else "failure"
        db.commit()
        db.close()

        return jsonify({"message": message})



