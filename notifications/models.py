from django.db import models
from users.models import CustomUser

class Notification(models.Model): 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications") 
    message = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True) 
    is_read = models.BooleanField(default=False) 

    class Meta:
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self): 
        return f"Notification for {self.user.username}: {self.message[:20]}..."
