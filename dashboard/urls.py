from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register("WasteBin", WasteBinPickupView, basename="wastebin pickup")
router.register("dashboard", DashViewset, basename="dashboard")
router.register("bin-request", WasteBinRequest, basename="bin-request")
urlpatterns = [
    
]+router.urls