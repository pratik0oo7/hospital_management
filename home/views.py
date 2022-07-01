from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth, Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test

from . import forms, models

# Create your views here.

# home pages views start here


def home(request):
    return render(request, "home.html")


def adminclick(request):
    return render(request, "adminclick.html")


def doctorclick(request):
    doctors = models.Doctor.objects.all().order_by('-id')
    p_context = {
        'doctors': doctors
    }
    return render(request, "doctorclick.html", context=p_context)


def patientclick(request):
    patients = models.Patient.objects.all().order_by('-id')
    p_context = {
        'patients': patients,
    }
    return render(request, "patientclick.html", context=p_context)

# home pages views end here

# registration view start


def registration(request):
    return render(request, "registration.html")


def patientlogin(request):
    form = forms.loginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if is_patient(request.user):
                    accountapproval = models.Patient.objects.all().filter(
                        user_id=request.user.id, status=True)
                    if accountapproval:
                        return redirect('patient_dashboard')
                    else:
                        return render(request, 'approval.html')
                else:
                    msg = 'anathorized credentials '
            else:
                msg = 'invalid credentials '
        else:
            msg = 'error validating form'
    return render(request, 'patientlogin.html', {'form': form, 'msg': msg})


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
    form = forms.loginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if is_doctor(request.user):
                    accountapproval = models.Doctor.objects.all().filter(
                        user_id=request.user.id, status=True)
                    if accountapproval:
                        return redirect('doctor_dashboard')
                    else:
                        return render(request, 'approval.html')
                else:
                    msg = 'anathorized credentials '
            else:
                msg = 'invalid credentials '
        else:
            msg = 'error validating form'

    return render(request, 'doctorlogin.html', {'form': form, 'msg': msg})


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
# -----------for checking user is doctor , patient


def is_doctor(user):
    return user.groups.filter(name="DOCTOR").exists()


def is_patient(user):
    return user.groups.filter(name="PATIENT").exists()

# ---------------------------------------------------------------------------------
# ------------------------ PATIENT RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    doctor = models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict = {
        'patient': patient,
        'doctorName': doctor.get_name,
        'doctorMobile': doctor.mobile,
        'doctorAddress': doctor.address,
        'symptoms': patient.symptoms,
        'doctorDepartment': doctor.department,
        'admitDate': patient.admitDate,
    }
    return render(request, 'patient_dashboard.html', context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    return render(request, 'patient_dashboard.html')
