from marshmallow import Schema, fields

## Login
class LoginSchema(Schema):
    account = fields.Str(doc="account", example="string", required=True)
    password = fields.Str(doc="password", example="string", required=True)

class LoginResponse(Schema):
    # message = fields.Str(example="Welcome back john")
    token = fields.Str(example="jcjjojjoeknkna")
    
## Member
class MemberGetSchema(Schema):
    name = fields.Str(doc="name", example="john")
    limit = fields.Str(doc="limit", example="john")
    offset = fields.Str(doc="offset", example="john")


class MemberGetRes(Schema):
    data = fields.List(fields.Dict(example={"name": "john"}))

class MemberPostSchema(Schema):
    id = fields.Str(example="string",required=True)
    name = fields.Str(example="string",required=True)
    gender = fields.Str(example="string",required=True) 
    birth = fields.Str(example="string",required=True) 
    account = fields.Str(example="string",required=True)
    password = fields.Str(example="string",required=True) 
    note = fields.Str(example="string")
    role_id = fields.Str(example="string",required=True)

class MemberPostRes(Schema):
    message = fields.Str(example="string")

## Single Member
class SingleMemberGetRes(Schema):
    data = fields.List(fields.Dict(example={"name": "john"}))

class SingleMemberPatchRes(Schema):
    name = fields.Str(example="string")
    gender = fields.Str(example="string") 
    birth = fields.Str(example="string") 
    note = fields.Str(example="string")
    account = fields.Str(example="string")
    password = fields.Str(example="string") 

class SingleMemberPatcRes(Schema):
    message = fields.Str(example="string")

class SingleMemberDeleteRes(Schema):
    message = fields.Str(example="string")






# pm.test("JWT Token 檢查", function () {
#     pm.environment.set("token", pm.response.json().token) 
# });