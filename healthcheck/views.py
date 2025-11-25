from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .models import HealthDatabase
from .serializers import HealthCheckListSerializer, HealthDatabaseSerializer
from .services import cache_key_for_alias, iter_health_db_aliases


class HealthDatabaseViewSet(ModelViewSet):
    queryset = HealthDatabase.objects.all().order_by("alias")
    serializer_class = HealthDatabaseSerializer
    permission_classes = [IsAdminUser]


@extend_schema(
    tags=["Healthcheck"],
    summary="Get healthcheck status for all DB mirrors",
    responses=HealthCheckListSerializer,
)
@api_view(["GET"])
@permission_classes([AllowAny])
def healthcheck_status(request):
    aliases = iter_health_db_aliases()
    items = []

    for alias in aliases:
        data = cache.get(cache_key_for_alias(alias))
        if not data:
            data = {
                "alias": alias,
                "ok": False,
                "status": "no_data",
                "checked_at": None,
                "message": "No recent healthcheck data",
                "api_timestamp": None,
                "mirror_timestamp": None,
            }
        items.append(data)

    serializer = HealthCheckListSerializer({"results": items})
    return Response(serializer.data)
