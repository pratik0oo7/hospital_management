from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth

from home import forms

# Create your views here.

# home pages views start here


def home(request):
    return render(request, "home.html")


def adminclick(request):
    return render(request, "adminclick.html")


def doctorclick(request):
    return render(request, "doctorclick.html")


def patientclick(request):
    return render(request, "patientclick.html")

# home pages views end here

# registration view start


def registration(request):
    return render(request, "registration.html")


def patientlogin(request):
    return render(request, 'patientlogin.html')


def patientsignup(request):
    userform = forms.patientuserform()
    patientform = forms.patientform()
    p_context = {'userform': userform, 'patientform': patientform}
    return render(request, 'patientsignup.html', context=p_context)

def doctorlogin(request):
    return render(request, 'doctorlogin.html')

def doctorsignup(request):
    return render(request, 'doctorsignup.html')
