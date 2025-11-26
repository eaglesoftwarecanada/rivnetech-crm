from healthcheck.consumers import HealthCheckConsumer
from django.urls import path

websocket_urlpatterns = [
    path('ws/health-check/', HealthCheckConsumer.as_asgi()),
]
