
from rest_framework import serializers

from goods.serializers import GoodsSerializer
from orders.models import Order, OrderGoods


class OrderViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        ordergoods = instance.ordergoods_set.all()
        order_goods_serializer = OrderGoodsSerializer(ordergoods, many=True)
        data = super().to_representation(instance)
        data['order_goods_info'] = order_goods_serializer.data
        return data


class OrderGoodsSerializer(serializers.ModelSerializer):

    o_goods = GoodsSerializer()

    class Meta:
        model = OrderGoods
        fields = '__all__'



