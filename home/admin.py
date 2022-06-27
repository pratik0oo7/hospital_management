from django.contrib import admin
from home.models import Doctor, Patient

# Register your models here.
#Patient
admin.site.register(Patient)
#Doctor
admin.site.register(Doctor)
