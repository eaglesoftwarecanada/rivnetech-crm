from rest_framework import serializers

from healthcheck.models import HealthDatabase


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


class HealthDatabaseSerializer(serializers.ModelSerializer):
    db_password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    api_pass = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = HealthDatabase
        fields = [
            "id",
            "alias",
            "type",
            "name",
            "host",
            "port",
            "db_user",
            "db_password",
            "api_url",
            "api_login",
            "api_pass",
            "is_enabled",
            "updated_at",
        ]
        read_only_fields = ["id", "updated_at"]

    def create(self, validated_data):
        db_password = validated_data.pop("db_password", None)
        api_pass = validated_data.pop("api_pass", None)

        instance = HealthDatabase.objects.create(**validated_data)

        if db_password:
            instance.db_password = db_password
        if api_pass:
            instance.api_pass = api_pass
        instance.save()

        return instance

    def update(self, instance, validated_data):
        db_password = validated_data.pop("db_password", None)
        api_pass = validated_data.pop("api_pass", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if db_password is not None:
            instance.db_password = db_password
        if api_pass is not None:
            instance.api_pass = api_pass

        instance.save()
        return instance
