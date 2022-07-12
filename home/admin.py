from django.contrib import admin
from .models import Admin, Doctor, Patient, Appointment, PatientDischargeDetails, Medicalreceipt

# Register your models here.
# Patient
admin.site.register(Patient)
# Doctor
admin.site.register(Doctor)
# appoitment
admin.site.register(Appointment)
# appoitment
admin.site.register(PatientDischargeDetails)
# appoitment
admin.site.register(Medicalreceipt)
# Patient
admin.site.register(Admin)
