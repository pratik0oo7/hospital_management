from django.http import HttpResponse
from django.shortcuts import render

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
