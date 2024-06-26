from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    send_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="send_user")
    receive_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receive_user")
    message = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.send_user_id.first_name
