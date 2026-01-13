from django.db import models
from django.db import models
from users.models import CustomUser

class UserActivation(models.Model):
    id = models.CharField(primary_key=True,max_length=50)
    date_of_activation = models.DateField(null=True, blank=True)
    activation_time = models.TimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False,null=True, blank=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    class Meta:
        db_table = 'active_bot_users'  # 👈 this sets the actual DB table name

