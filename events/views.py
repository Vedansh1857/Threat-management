from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from .models import Event
from .serializers import EventSerializer
from .permissions import IsAdminOnly
from alerts.models import Alert

class EventThrottle(UserRateThrottle):
    rate = "20/minute"

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    throttle_classes = [EventThrottle]
    permission_classes = [IsAuthenticated, IsAdminOnly]

    def perform_create(self, serializer):
        event = serializer.save()

        # Auto create alert
        if event.severity in ["High", "Critical"]:
            Alert.objects.create(event=event)
