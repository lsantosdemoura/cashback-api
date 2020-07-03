from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api import views

router = DefaultRouter()
router.register('resellers', views.UserViewSet)
router.register('purchases', views.PurchaseViewSet, basename='purchase')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'gathered-cashback/',
        views.GatheredCashbackView.as_view(),
        name='gathered_cashback'
    ),
    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('refresh-token/', TokenRefreshView.as_view(), name="refresh_token"),
]
