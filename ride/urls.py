from django.urls import path
from ride.views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewset)
router.register('rides', RidesViewset)

urlpatterns = [
    
] + router.urls

