from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Alert
from .serializers import AlertSerializer
from .permissions import AdminOrAnalystReadOnly

class AlertViewSet(viewsets.ModelViewSet):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated, AdminOrAnalystReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "event__severity"]

    def get_queryset(self):
        return Alert.objects.select_related("event").all().order_by("-created_at")
