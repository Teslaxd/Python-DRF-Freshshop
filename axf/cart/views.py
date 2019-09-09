from django.core.cache import cache
from rest_framework import viewsets, mixins
from rest_framework.decorators import list_route
from rest_framework.response import Response

from cart.models import Cart
from cart.serializers import CartViewSerializer

from user.UserAuthentication import UserTokenAuthentication


class CartView(viewsets.GenericViewSet, mixins.ListModelMixin,
               mixins.UpdateModelMixin):

    queryset = Cart.objects.all()
    serializer_class = CartViewSerializer
    authentication_classes = (UserTokenAuthentication,)

    def list(self, request, *args, **kwargs):
        # 1 获取user, 通过token
        # token = request.query_params.get('token')
        # user_id = cache.get(token)
        # 2 获取购物车数据
        cart = Cart.objects.filter(c_user_id=request.user.id).all()
        serializer = self.get_serializer(cart, many=True)
        res = {
            'carts': serializer.data,
            'total_price': self.total_price(request),
        }
        return Response(res)

    def total_price(self, request):
        carts = Cart.objects.filter(c_user_id=request.user.id,
                                    c_is_select=True)
        total = 0
        for cart in carts:
            total = cart.c_goods.price * cart.c_goods_num
        return round(total, 1)

    @list_route(methods=['POST'])
    def add_cart(self, request):
        # 添加购物车
        # 前端传递: token, goodsid
        # 1 获取User, 通过token
        # token = self.request.data.get('token')
        # user_id = cache.get(token)
        # if user_id:
        # user = AXFUser.objects.get(pk=user_id)
        user = request.user
        # 2 获取购物车数据
        goodsid = self.request.data.get('goodsid')
        cart = Cart.objects.filter(c_user=user,
                                   c_goods_id=goodsid).first()
        # 判断购物车数据是否存在, 并做对应的处理
        c_goods_num = 1
        if cart:
            cart.c_goods_num += 1
            cart.save()
            c_goods_num = cart.c_goods_num
        else:
            Cart.objects.create(
                c_user=user,
                c_goods_id=goodsid
            )
        res = {
            'c_goods_num': c_goods_num
        }

        return Response(res)

        # raise PramException({'code': 1008, 'msg': '无法添加商品, 请先登录'})

    @list_route(methods=['POST'])
    def sub_cart(self, request):
        # 减少购物车中的商品数量

        # 1. 获取购物车中该商品信息
        goodsid = request.data.get('goodsid')
        user = request.user
        cart = Cart.objects.filter(c_user=user,
                                   c_goods_id=goodsid).first()
        c_goods_num = 0
        if cart:
            if cart.c_goods_num > 1:
                # 商品数量大于1 ,则自检
                cart.c_goods_num -= 1
                cart.save()
                c_goods_num = cart.c_goods_num
            else:
                # 表示商品的数量为1, 则删除
                cart.delete()
        res = {
            'c_goods_num': c_goods_num
        }
        return Response(res)

    def update(self, request, *args, **kwargs):
        # /api/cart/cart/1/ PATCH
        # 参数: token, goodsid
        instance = self.get_object()
        instance.c_is_select = not instance.c_is_select
        instance.save()
        return Response({'code': '200', 'msg': '修改商品信息成功'})

    @list_route(methods=['PATCH'])
    def all_update(self, request):
        # api/cart/cart/all_update  PATCH
        # 传参token
        user = request.user
        carts = Cart.objects.first(c_user=user).all()

        for cart in carts:
            cart.c_is_select = True
            cart.save()
        return Response({'code': 200, 'msg': '批量修改商品选择状态成功'})

















