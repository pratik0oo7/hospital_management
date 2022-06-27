from dataclasses import field, fields
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
