from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'onlive', OnLiveViewSet)
router.register(r'vtuber', VtuberViewSet)
router.register(r'req', RequestViewSet)