<h1>API_connect_mysql</h1>
<h2>Summary</h2>
<p>This is an API written in Python for connecting to a MySQL database and performing CRUD operations based on the corresponding permissions. It uses the pymysql library and applies the Flask framework and some dependent libraries. It mainly uses four Python files: api.py as the main file, route_model.py for replacing the parser and recording request and response data, __init__.py for identifying files of the same layer of Python (which is empty), and member.py for writing the content of the API execution.</p>
<p>The following records only member.py.</p>
<h3>Imported Modules and Libraries</h3>
<ul>
    <li><code>pymysql</code> is used for executing commands for database connection and CRUD operations.</li>
    <li><code>MethodResource</code> is an object that can capture the content of request and response methods.</li>
    <li><code>marshal_with</code>, <code>doc</code>, <code>use_kwargs</code> can help organize and format textual data for presentation.</li>
    <li><code>jsonify</code> is used to convert the response format content to the JSON data format.</li>
    <li><code>create_access_token</code> is used to create a JWT token.</li>
    <li><code>jwt_required</code> can be used to verify and execute the JWT token.</li>
    <li><code>get_jwt_identity</code> can be used to obtain the identity content in the JWT token, and the obtained data is of type dict.</li>
    <li><code>timedelta</code> is a function that represents the interval between two times.</li>
</ul>
<h3>Create a JWT Token</h3>
<p>The <code>get_access_token</code> function receives two parameters, <code>account</code> and <code>role_id</code>, and different permissions are granted according to the role_id. When <code>http_method="GET"</code>, it means that only the <code>request.get</code> method can be used; when <code>http_method="!DELETE"</code>, it means that all methods except <code>request.delete</code> can be used; <code>http_method="*"</code> means that all permissions are allowed. Finally, the <code>http_method</code> is put into the identity to generate a JWT token.</p>
<h3>Verify CRUD Permissions</h3>
<p>The <code>set_http_methods</code> function is used to verify the CRUD permissions. The <code>current_user</code> variable obtains the http_method from the JWT token. Then, the <code>http_method</code> is compared with the current function name, and if there is no permission, the function will return <code>{"message":"沒有權限"}</code>.</p>
<h3>Connect to MySQL and Set Authentication Mode</h3>
<p>The <code>db_init</code> function is used to connect to the MySQL database. The <code>security_params = [{"bearer": []}]</code> is used for the authentication mode later, and its token verification method is "bearer".</p>

<h3>Login Object and POST Request Content:</h3>
<p>Below is the code for the Login object and its corresponding POST request content:</p>
<pre>
<code class="language-python">
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
</code>
</pre>
<p>The <code>post()</code> method uses three decorators that are used to generate Swagger-formatted documentation. The user enters their account and password to log in and returns the user's personal information. The account and role_id portions are used to generate a JWT token. Finally, the method returns a success or failure message.</p>
<h3>GET Request Content for Displaying Data:</h3>
<p>Below is the code for the GET request content used to display data:</p>
<pre>
<code class="language-python">
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
</code>
</pre>
<p>The <code>get()</code> method uses several decorators. The <code>@doc</code>, <code>@use_kwargs</code>, and <code>@marshal_with</code> decorators are used to generate Swagger documentation. The <code>@jwt_required()</code> decorator is used to verify the JWT token, and the <code>@set_http_methods</code> decorator is used to verify the CRUD permissions.</p>
<h3>Request to create data through post content::</h3>
<pre>
<code class="language-python">
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
</code>
</pre>
<h3>Request to display data with ID as index through get content:</h3>
<pre>
<code class="language-python">
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
</code>
</pre>
<h3>Request to modify partial data through patch content:</h3>
<pre>
<code class="language-python">
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
</code>
</pre>
<h3>Request to delete specified user data through delete content:</h3>
<pre>
<code class="language-python">
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
</code>
</pre>
