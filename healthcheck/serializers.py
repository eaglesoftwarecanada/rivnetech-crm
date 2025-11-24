from rest_framework import serializers


class HealthCheckResultSerializer(serializers.Serializer):
    alias = serializers.CharField()
    ok = serializers.BooleanField()
    status = serializers.CharField()
    checked_at = serializers.DateTimeField(allow_null=True)
    message = serializers.CharField(allow_blank=True)
    api_timestamp = serializers.CharField(allow_null=True)
    mirror_timestamp = serializers.CharField(allow_null=True)


class HealthCheckListSerializer(serializers.Serializer):
    results = HealthCheckResultSerializer(many=True)
