from rest_framework.routers import DefaultRouter
from django.urls import path, include

from healthcheck.views import HealthDatabaseViewSet, healthcheck_status


app_name = 'stages'

router = DefaultRouter()
router.register(r"health-databases", HealthDatabaseViewSet, basename="healthdatabase")

urlpatterns = [
    path("healthcheck/", healthcheck_status, name="healthcheck_status"),
    path('', include(router.urls)),
]
