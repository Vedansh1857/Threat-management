# alerts/models.py
from django.db import models
from events.models import Event

class Alert(models.Model):
    STATUS_CHOICES = (
        ("Open", "Open"),
        ("Acknowledged", "Acknowledged"),
        ("Resolved", "Resolved"),
    )

    event = models.OneToOneField(Event,on_delete=models.CASCADE,related_name="alert")
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="Open",db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Alert #{self.id} | {self.event.severity} | {self.status}"
