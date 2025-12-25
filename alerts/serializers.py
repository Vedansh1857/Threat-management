from rest_framework import serializers
from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    event_severity = serializers.CharField(source="event.severity", read_only=True)
    event_type = serializers.CharField(source="event.event_type", read_only=True)
    source_name = serializers.CharField(source="event.source_name", read_only=True)

    class Meta:
        model = Alert
        fields = [
            "id",
            "status",
            "created_at",
            "event_severity",
            "event_type",
            "source_name",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_status(self, value):
        if value not in ["Open", "Acknowledged", "Resolved"]:
            raise serializers.ValidationError("Invalid status value.")
        return value

    def validate(self, attrs):
        # Preventing reopening of a Resolved alert
        instance = getattr(self, "instance", None)
        new_status = attrs.get("status")

        if instance and instance.status == "Resolved" and new_status != "Resolved":
            raise serializers.ValidationError("Resolved alerts cannot be reopened. Create a new alert instead.")
        return attrs
