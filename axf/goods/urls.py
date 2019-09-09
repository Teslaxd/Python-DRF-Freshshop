from django.urls import path
from rest_framework.routers import SimpleRouter
from goods.views import *

router = SimpleRouter()
router.register('foodtype', FoodTypeView)
router.register('market', MarketView)

urlpatterns = [
    path('home/', home)
]

urlpatterns += router.urls



