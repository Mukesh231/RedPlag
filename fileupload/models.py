from django.db import models
from django.conf import settings

class FILE(models.Model):
    file=models.FileField(blank=False, null=False)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    timestamp=models.DateTimeField(null=True)
    name=models.CharField(null=True, max_length=50)
    def __str__(self):
        return self.file.name
