import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.response import Response

from tools.errors import PramException
from user.models import AXFUser


# 这里默认校验整个模型的字段
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AXFUser
        # 序列化所有字段
        fields = '__all__'


class UserRegisterSerializer(serializers.Serializer):

    # 只用于校验字段, 不用于序列化字段
    # 和前端人员沟通好, 需要校验字段的名称
    u_username = serializers.CharField(required=True, max_length=32,
                                       min_length=4,
                                       error_messages={
                                           'required': '注册账号必填',
                                           'max_length': '注册账号不能超过32位',
                                           'min_length': '注册账号不少于4位',
                                       })

    u_password = serializers.CharField(required=True,
                                       max_length=10,
                                       min_length=3,
                                       error_messages={
                                           'required': '密码必填',
                                           'max_length': '密码不能超过10位',
                                           'min_length': '密码不少于3位',
                                       })
    u_password2 = serializers.CharField(required=True,
                                        max_length=10,
                                        min_length=3,
                                        error_messages={
                                           'required': '确认密码必填',
                                           'max_length': '确认密码不能超过10位',
                                           'min_length': '确认密码不少于3位',
                                        })
    u_email = serializers.CharField(required=True,
                                    error_messages={
                                        'required': '邮箱必填'
                                    })

    def validate(self, attrs):
        # 判断用户是否注册
        username = attrs.get('u_username')
        if AXFUser.objects.filter(u_username=username).exists():
            raise PramException({'code': 1001, 'msg': '注册账号已存在,请重新注册'})

        # 判断密码是否一致
        if attrs.get('u_password') != attrs.get('u_password2'):
            raise PramException({'code': 1002, 'msg': '密码不一致'})

        # 判断邮箱是否存在
        if AXFUser.objects.filter(u_email=attrs.get('u_email')).exists():
            raise PramException({'code': 1003, 'msg': '注册邮箱已存在'})

        return attrs

    def register_data(self, validate_data):
        # 实现注册功能
        u_password = make_password(validate_data['u_password'])
        user = AXFUser.objects.create(u_username=validate_data['u_username'],
                                      u_password=u_password,
                                      u_email=validate_data['u_email'],)

        res = {
            'code': 200,
            'msg': '注册成功',
            'user_id': user.id
        }

        return Response(res)


class UserLoginSerializer(serializers.Serializer):

    u_username = serializers.CharField(required=True, max_length=32,
                                       min_length=4,
                                       error_messages={
                                           'required': '注册账号必填',
                                           'max_length': '注册账号不能超过32位',
                                           'min_length': '注册账号不少于4位',
                                       })

    u_password = serializers.CharField(required=True,
                                       max_length=10,
                                       min_length=3,
                                       error_messages={
                                           'required': '密码必填',
                                           'max_length': '密码不能超过10位',
                                           'min_length': '密码不少于3位',
                                       })

    def validate(self, attrs):
        # 判断账号是否存在
        if not AXFUser.objects.filter(u_username=attrs.get('u_username')).exists():
            raise PramException({'code': 1005, 'msg': '账号不存在,请登录'})

        # 账号存在后判断密码是否正确
        user = AXFUser.objects.filter(u_username=attrs.get('u_username')).first()
        if not check_password(attrs.get('u_password'), user.u_password):
            raise PramException({'code': 1006, 'msg': '密码错误,登录失败'})

        # 登录操作

        return attrs

    def login_data(self, validate_data):
        # 登录功能
        token = uuid.uuid4().hex
        user = AXFUser.objects.filter(u_username=validate_data['u_username']).first()
        # cache使用redis进行存储
        # set存储的是字符串类型的值
        cache.set(token, user.id, timeout=60 * 60 * 24)

        res = {
            'token': token
        }
        return res



