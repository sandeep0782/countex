from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Authetication_Service(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE,  null=True, blank=True)
    sampling_add = models.BooleanField(default=False)
    view_sampling =  models.BooleanField(default=False)
    update_sampling = models.BooleanField(default=False)
    delete_sampling =  models.BooleanField(default=False)
    daily_approval_sampling = models.BooleanField(default=False)
    daily_dispatch_sampling =  models.BooleanField(default=False)
    dashboard = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username