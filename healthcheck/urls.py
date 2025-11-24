from rest_framework.routers import DefaultRouter
from django.urls import path, include

from healthcheck.views import healthcheck_status

router = DefaultRouter()

app_name = 'stages'

urlpatterns = [
    path("healthcheck/", healthcheck_status, name="healthcheck_status"),
    path('', include(router.urls)),
]
