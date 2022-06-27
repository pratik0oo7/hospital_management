from django import forms
from django.contrib.auth.models import User
from . import models


class patientuserform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class patientform(forms.ModelForm):
    class Meta:
        model = models.Patient
        fields = ['address', 'symptoms', 'profile_pic', 'mobile', 'status']


class doctoruserform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class doctorform(forms.ModelForm):
    class Meta:
        model = models.Doctor
        fields = ['address', 'mobile', 'department',
                  'status', 'profile_pic', 'exprience']
