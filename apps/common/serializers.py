from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    """Base serializer"""

    class Meta:
        fields = ["id", "created_at", "updated_at"]
