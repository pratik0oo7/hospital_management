"""hospital_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from re import template
from django import views
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # click urls
    path('doctorclick', views.doctorclick, name='doctorclick'),
    path('adminclick', views.adminclick, name='adminclick'),
    path('patientclick', views.patientclick, name='patientclick'),

    #regitration and login
    path('registration', views.registration, name='registration'),
    # patient
    path('patientlogin', views.patientlogin, name='patientlogin'),
    path('patientsignup', views.patientsignup, name='patientsignup'),
    # Doctor
    path('doctorlogin', views.doctorlogin, name='doctorlogin'),
    path('doctorsignup', views.doctorsignup, name='doctorsignup'),

    # logout
    path('logout', LoginView.as_view(template_name="home.html"), name="logout"),

]
# doctor-related pattaren
urlpatterns += [
    path('doctor_dashboard', views.doctor_dashboard, name="doctor_dashboard"),
    path('doctor_appointment', views.doctor_appointment, name="doctor_appointment"),
    path('doctor_view_appointment', views.doctor_view_appointment,
         name='doctor_view_appointment'),
    path('doctor_book_appointment', views.doctor_book_appointment,
         name='doctor_book_appointment'),
    path('doctor_approve_appointment', views.doctor_approve_appointment,
         name='doctor_approve_appointment'),
    path('approve-appointment/<int:pk>',
         views.approve_appointment_view, name='approve-appointment'),
    path('reject-appointment/<int:pk>',
         views.reject_appointment_view, name='reject-appointment'),
    path('doctor_delete_appointment', views.doctor_delete_appointment,
         name='doctor_delete_appointment'),
    path('delete_appointment/<int:pk>',
         views.delete_appointment, name='delete_appointment'),
    path('doctor_patient', views.doctor_patient, name="doctor_patient"),
    path('doctor_patient_discharge', views.doctor_patient_discharge,
         name='doctor_patient_discharge'),
]
# patient-related pattaren
urlpatterns += [
    path('patient_dashboard', views.patient_dashboard, name="patient_dashboard"),
    path('patient_appointment', views.patient_appointment,
         name="patient_appointment"),
    path('patient_view_appointment', views.patient_view_appointment,
         name="patient_view_appointment"),
    path('patient_book_appointment', views.patient_book_appointment,
         name="patient_book_appointment"),

    path('patient_doctor', views.patient_doctor, name="patient_doctor"),
    path('patient_discharge', views.patient_discharge, name='patient_discharge'),
    path('searchdoctor', views.search_doctor_view, name='searchdoctor'),
]
