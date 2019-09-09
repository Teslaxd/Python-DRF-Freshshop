
###  用户注册接口api

注册功能url: /api/user/auth/register/

请求方式: POST

返回格式: Json

请求参数:

    u_username  用户名             string  必填   长度 4-10
    
    u_password  用户注册密码       string  必填    长度 4-32
    
    u_password2 用户注册确认密码   string 必填     长度 4-32
    
    u_email     用户邮箱           string 必填
    

响应:

    正常响应
    {
        'code': 200,
        'msg' : 注册成功
        'data': {
            user_id:1     
        }
    } 

    失败响应
    {
        'code': 1001,
        'msg': '注册账号不存在, 请重新注册'
        'data': {}           
    }
    
    {
        'code': 1002,
        'msg': '密码不一致'
        'data': {}
    }
    
    {
        'code': 1003,
        'msg': '注册邮箱已存在'
        'data': {}
    }    
    
    {
        'code': 1004,
        'msg': '注册参数错误'
        'data': {}
    }   

响应参数:

    code 响应状态码提示  int
    msg  响应提示        string
    data 响应结果      
    user.id  用户的id值  int


