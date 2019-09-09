from django.core.cache import cache
from rest_framework import viewsets, mixins
from rest_framework.decorators import list_route
from rest_framework.response import Response

from tools.errors import PramException
from user.UserAuthentication import UserTokenAuthentication
from user.models import AXFUser
from user.serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer


class UserView(viewsets.GenericViewSet,
               mixins.ListModelMixin,
               mixins.RetrieveModelMixin,):

    # 1 获取用户相关的数据
    queryset = AXFUser.objects.all()
    # 2 定义序列化类
    serializer_class = UserSerializer
    # 3 定义校验通过
    authentication_classes = (UserTokenAuthentication,)

    def list(self, request, *args, **kwargs):
        # token = request.query_params.get('token')
        # # 从redis中获取数据
        # user_id = cache.get(token)
        user = AXFUser.objects.filter(id=request.user.id).first()
        # if not user:
        #     raise PramException({'code': 1008, 'msg': '你还没有登录,请登录'})
        # 序列化,调用UserSerializer进行序列化user对象
        serializer = self.get_serializer(user)
        res = {
            'user_info': serializer.data
        }
        return Response(res)

    # 指定register的请求方式, 指定register的序列化的类, 同时register的字段校验也经过 UserRegisterSerializer 类
    @list_route(methods=['POST'], serializer_class=UserRegisterSerializer)
    def register(self, request):
        # /api/user/auth/register/  POST   -  url地址

        # 校验参数
        serializers = self.get_serializer(data=request.data)
        res = serializers.is_valid(raise_exception=False)
        if not res:
            raise PramException({'code': 1004, 'msg': '注册参数有误'})

        # 实现注册功能
        data = serializers.register_data(serializers.data)
        return data

    @list_route(methods=['POST'], serializer_class=UserLoginSerializer)
    def login(self, request):
        serializers = self.get_serializer(data=request.data)
        res = serializers.is_valid(raise_exception=False)
        if not res:
            raise PramException({'code': 1007, 'msg': '参数有误'})

        # 登录功能
        result = serializers.login_data(serializers.data)
        return Response(result)












