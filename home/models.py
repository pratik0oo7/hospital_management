from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile-pic/PatientProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=50)
    mobile = models.CharField(max_length=20, null=False)
    symptoms = models.CharField(max_length=100, null=False)
    assignedDoctorid = models.PositiveIntegerField(null=False)
    admitDate = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
