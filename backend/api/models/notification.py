from django.contrib.auth.models import User
from django.db import models


class Notification(models.Model):
    link = models.TextField()
    read = models.BooleanField(default=False)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.TextField()  # Type field maintains the internal notification type, used to send updates via ws
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Notification #{self.id} for {self.user.username}'

    class Meta:
        ordering = ['-timestamp']
