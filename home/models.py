from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# patient model


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pic/PatientProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    symptoms = models.CharField(max_length=100, null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
    # this is property which use to save data in database which specific type

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"


# doctor model
departments = [('Cardiologist', 'Cardiologist'),
               ('Dermatologists', 'Dermatologists'),
               ('Emergency Medicine Specialists',
                'Emergency Medicine Specialists'),
               ('Allergists/Immunologists', 'Allergists/Immunologists'),
               ('Anesthesiologists', 'Anesthesiologists'),
               ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons')
               ]


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pic/DoctorProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    department = models.CharField(
        max_length=50, choices=departments, default='Cardiologist')
    status = models.BooleanField(default=False)
    exprience = models.IntegerField(null=True)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
# is is used to derived name and department name save formate in database

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return "{} ({})".format(self.user.first_name, self.department)
