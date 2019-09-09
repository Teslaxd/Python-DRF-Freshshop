from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication

from tools.errors import PramException
from user.models import AXFUser


class UserTokenAuthentication(BaseAuthentication):
    # 认证功能

    def authenticate(self, request):
        try:
            token = request.query_params.get('token') \
                if request.query_params.get('token') \
                else request.data.get('token')

            user_id = cache.get(token)
            user = AXFUser.objects.get(pk=user_id)
            # 返回user ===> request.user
            # 返回token ===> request.auth
            return user, token
        except:
            raise PramException({'code': 1009, 'msg': '用户没有登录, 没有权限操作'})




























