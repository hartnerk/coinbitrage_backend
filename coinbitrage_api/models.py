from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts', null=True)
    alert_name =  models.CharField(max_length=50)
    coin =  models.CharField(max_length=50)
    threshold =  models.IntegerField(default=0)
    enabled =  models.BooleanField(max_length=50)
    

    def __str__(self):
        return self.alert_name