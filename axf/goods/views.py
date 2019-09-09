
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_redis import get_redis_connection
from rest_framework.utils import json
from rest_framework import viewsets, mixins

from goods.filters import GoodsFilter
from goods.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods
from goods.serializers import MainWheelSerializer, MainNavSerializer, MainMustBuySerializer, MainShopSerializer, \
    MainShowSerializer, FoodTypeSerializer, GoodsSerializer


@api_view(['GET'])
def home(request):

    # 如何优化查询, 如何设置存储的格式(默认为bytes), json
    # main_wheels
    conn = get_redis_connection()
    redis_main_wheels = conn.hget('goods', 'main_wheels')
    if not redis_main_wheels:
        main_wheels = MainWheel.objects.all()
        new_main_wheels = MainWheelSerializer(main_wheels, many=True).data
        # 存储结果为json格式数据 (字符串),  json.dumps
        value_wheels = json.dumps(new_main_wheels)
        conn.hset('goods', 'main_wheels', value_wheels)
        redis_main_wheels = conn.hget('goods', 'main_wheels')

    main_wheels = json.loads(redis_main_wheels)

    # main_navs
    conn1 = get_redis_connection()
    redis_main_navs = conn1.hget('goods', 'main_navs')
    if not redis_main_navs:
        old_main_navs = MainNav.objects.all()
        new_main_navs = MainNavSerializer(old_main_navs, many=True).data
        value_navs = json.dumps(new_main_navs)
        conn1.hset('goods', 'main_navs', value_navs)
        redis_main_navs = conn1.hget('goods', 'main_navs')

    main_navs = json.loads(redis_main_navs)


    # main_mustbuys
    conn2 = get_redis_connection()
    redis_main_mustbuys = conn2.hget('goods', 'main_mustbuys')

    if not redis_main_mustbuys:
        main_mustbuys = MainMustBuy.objects.all()
        new_main_mustbuys = MainMustBuySerializer(main_mustbuys, many=True).data
        value_mustbuys = json.dumps(new_main_mustbuys)
        conn2.hset('goods', 'main_mustbuys', value_mustbuys)
        redis_main_mustbuys = conn2.hget('goods', 'main_mustbuys')

    main_mustbuys = json.loads(redis_main_mustbuys)


    main_shops = MainShop.objects.all()
    main_shows = MainShow.objects.all()

    res = {
        'main_wheels': main_wheels,
        'main_navs': main_navs,
        'main_mustbuys': main_mustbuys,
        'main_shops': MainShopSerializer(main_shops, many=True).data,
        'main_shows': MainShowSerializer(main_shows, many=True).data,
    }
    return Response(res)


class FoodTypeView(viewsets.GenericViewSet,
                   mixins.ListModelMixin):

    queryset = FoodType.objects.all()
    serializer_class = FoodTypeSerializer


class MarketView(viewsets.GenericViewSet,
                 mixins.ListModelMixin):

    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    filter_class = GoodsFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        #  分类
        typeid = self.request.query_params.get('typeid')
        foodtype = FoodType.objects.filter(typeid=typeid).first()
        res_list = foodtype.childtypenames.split('#')
        # 推导式写法
        foodtypelist = [{'child_name': i.split(':')[0], 'child_value': i.split(':')[1]}for i in res_list]

        # 定义排序规则
        rule_list = [
            {'order_name': '综合排序', 'order_value': 0},
            {'order_name': '价格排序', 'order_value': 1},
            {'order_name': '价格降序', 'order_value': 2},
            {'order_name': '销量升序', 'order_value': 3},
            {'order_name': '销量降序', 'order_value': 4},

        ]
        res = {
            'goods_list': serializer.data,
            'foodtype_childname_list': foodtypelist,  # 需要child_name和child_value
            'order_rule_list': rule_list,
        }
        return Response(res)





