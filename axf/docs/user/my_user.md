
###  获取用户信息接口api

url:  /api/user/auth/list/

请求方式: GET

请求参数: 

        token   登录校验值   uuid值  uuid4.hex  必填
        

响应:

        正常响应
        {
            'code': 200
            'msg': 请求成功
            'data': {
                user_info: {
                    "id": 1,
                    "u_username": "MKpossible",
                    "u_password": "pbkdf2_sha256$120000$Qm2rZNQieY7e$A7uEbk/nbYD5IEAW5QSh/GT/ZBcqRRpTP9/lKTam4Ws=",
                    "u_email": "desire@qq.com",
                    "is_active": false,
                    "is_delete": false
                }
            }        
        }   
            
        失败响应
        {           
            "code": 1008,
            "msg": "你还没有登录,请登录",
            "data": {}        
        }


响应参数:
    
    code 响应状态码提示  int
    msg  响应提示        string
    data 响应结果 
    
