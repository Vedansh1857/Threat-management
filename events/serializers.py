from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "source_name",
            "event_type",
            "severity",
            "description",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_source_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Source name cannot be empty.")
        if len(value) > 255:
            raise serializers.ValidationError("Source name is too long.")
        return value

    def validate_description(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Description is required.")
        if len(value) > 5000:
            raise serializers.ValidationError("Description is too long.")
        return value

    def validate(self, attrs):
        severity = attrs.get("severity")
        description = attrs.get("description", "")
        if severity == "Critical" and len(description.strip()) < 10:
            raise serializers.ValidationError(
                "Critical events must include a detailed description (at least 20 characters)."
            )
        return attrs
