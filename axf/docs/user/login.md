
### 用户登录接口

请求地址: /api/user/auth/login/

请求方式: POST

请求参数:

        u_username  用户名  string 必填  长度4-10
        password    密码    string 必填  长度4-32
     
响应:

    成功响应
    {
    'code': 200,
    'msg': '请求成功'
     "data": {
        "token": "428cf1c08d4541ab85ddb0f91066a277"
        }
    }

    
    失败响应
    {
    'code': 1005
    'msg':  '账号不存在, 请登录'
    'data': {}
    }
    
    {
    'code': 1006
    'msg':  '密码错误登录失败'
    'data': {}
    }
    
    {
    'code': 1007
    'msg':  '参数有误'
    'data': {}
    }

响应参数:

    code 响应状态码提示  int
    msg  响应提示        string
    data 响应结果      
    "token": "428cf1c08d4541ab85ddb0f91066a277"   响应结果内容  string  

