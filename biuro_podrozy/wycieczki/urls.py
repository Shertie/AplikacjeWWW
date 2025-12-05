from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'kraje', views.KrajViewSet)
router.register(r'linie-lotnicze', views.LiniaLotniczaViewSet)
router.register(r'loty', views.LotViewSet)
router.register(r'hotele', views.HotelViewSet)
router.register(r'wycieczki', views.WycieczkaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
