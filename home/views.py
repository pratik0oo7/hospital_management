from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

#home pages views start here
def home(request):
    return HttpResponse("index page")


def adminclick(request):
    return HttpResponse("admin click")


def doctorclick(request):
    return HttpResponse("doctor click")


def patientclick(request):
    return HttpResponse("patient click")

#home pages views end here