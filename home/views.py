from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth, Group

from . import forms

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
    if request.method == "POST":
        userform = forms.patientuserform(request.POST)
        patientform = forms.patientform(request.POST, request.FILES)
        if userform.is_valid() and patientform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            patient = patientform.save(commit=False)
            patient.user = user
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient = patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request, 'patientsignup.html', context=p_context)


def doctorlogin(request):
    return render(request, 'doctorlogin.html')


def doctorsignup(request):
    userform = forms.doctoruserform()
    doctorform = forms.doctorform()
    p_context = {'userform': userform, 'doctorform': doctorform}
    if request.method == 'POST':
        userform = forms.doctoruserform(request.POST)
        doctorform = forms.doctorform(request.POST, request.FILES)
        if userform.is_valid() and doctorform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorform.save(commit=False)
            doctor.user = user
            doctor = doctor.save()
            doctor_group = Group.objects.get_or_create(name='DOCTOR')
            doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request, 'doctorsignup.html', context=p_context)
