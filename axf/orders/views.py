

from rest_framework import viewsets, mixins
from rest_framework.response import Response

from cart.models import Cart
from goods.models import Goods
from orders.filters import OrderFilter
from orders.models import Order, OrderGoods
from orders.serializers import OrderViewSerializer, OrderGoodsSerializer
from tools.errors import PramException
from user.UserAuthentication import UserTokenAuthentication


class OrderView(viewsets.GenericViewSet,
                mixins.CreateModelMixin,
                mixins.ListModelMixin,):

    queryset = Order.objects.all()
    serializer_class = OrderViewSerializer
    authentication_classes = (UserTokenAuthentication,)
    filter_class = OrderFilter

    def get_queryset(self):
        return self.queryset.filter(o_user=self.request.user).all()

    def create(self, request, *args, **kwargs):

        # 获取当前用户购物车中已下单的商品信息
        # 创建订单
        # 创建订单详情表信息
        # 删除购物车中已下单的信息
        user = request.user
        carts = Cart.objects.filter(c_user=user, c_is_select=True).all()
        if carts:
            # 计算总价
            total = 0
            for cart in carts:
                total += cart.c_goods_num * cart.c_goods.price
            # 创建订单
            order = Order.objects.create(o_user=user, o_price=total)
            # 创建详情
            for cart in carts:
                OrderGoods.objects.create(o_order=order,
                                          o_goods=cart.c_goods,
                                          o_goods_num=cart.c_goods_num)
                # 删除购物车中的信息
                cart.delete()
            res = {
                'order_id': order.id
            }
            return Response(res)
        else:
            raise PramException({'code': 1010, 'msg': '购物车中没有下单的商品'})

    # def list(self, request, *args, **kwargs):
    #
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = OrderViewSerializer(queryset, many=True)
    #     for instance_data in serializer.data:
    #         order_id = instance_data['id']
    #         ordergoods = OrderGoods.objects.filter(o_order_id=order_id).all()
    #         o_g_ser = OrderGoodsSerializer(ordergoods, many=True)
    #         instance_data['order_goods_info'] = o_g_ser.data
    #
    #     return Response(serializer.data)





















