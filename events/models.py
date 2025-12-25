# events/models.py
from django.db import models

class Event(models.Model):
    SEVERITY_CHOICES = (
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Critical", "Critical"),
    )

    source_name = models.CharField(max_length=255)
    event_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=10,choices=SEVERITY_CHOICES,db_index=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.source_name} | {self.event_type} | {self.severity}"
