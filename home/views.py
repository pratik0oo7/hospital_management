from datetime import date
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User, auth, Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from . import forms, models
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
import io

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
            patients = models.Patient.objects.get(user_id=user.id)
            doctors = models.Doctor.objects.get(user_id=request.user.id)
            data = {
                'Patient_Fname': user.first_name,
                'Patient_Lname': user.last_name,
                'Patient_mobile': patients.mobile,
                'email': user.email,
                'massage': patients.symptoms,
                'Patient_address': patients.address,
            }

            msg = '''
            Patient Name:\t{}\t{}
            Patient Email:\t{}
            Patient Number:\t{}
            Patient Address:\t{}
            ------------------------------------------------Symptoms Description---------------------------------------------------
            Symptoms:\t{}


            Here, Your New Patient Details please Approv from Your Portal Doctor...
            '''.format(data['Patient_Fname'], data['Patient_Lname'], data['email'], data['Patient_mobile'], data['Patient_address'], data['massage'])
            send_mail('Your New Appoitment', msg, settings.EMAIL_HOST_USER,
                      [doctors.email], fail_silently=False)
            print(data)
            print(doctors.email)
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
        'patientname': patient.get_name,
        'doctorName': doctor.get_name,
        'doctorMobile': doctor.mobile,
        'doctorAddress': doctor.address,
        'symptoms': patient.symptoms,
        'doctorDepartment': doctor.department,
        'admitDate': patient.admitDate,
    }
    return render(request, 'patient_dashboard.html', context=mydict)


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    return render(request, 'patient_appointment.html', {'patient': patient})


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment(request):
    appoitmentform = forms.patientappointmentform()
    patient = models.Patient.objects.get(user_id=request.user.id)
    massage = None
    p_context = {'appointmentform': appoitmentform,
                 'patient': patient, 'massage': massage}
    if request.method == 'POST':
        appoitmentform = forms.patientappointmentform(request.POST)
        if appoitmentform.is_valid():
            doctor = models.Doctor.objects.get(
                user_id=request.POST.get('doctorId'))
            appointment = appoitmentform.save(commit=False)
            appointment.doctorId = request.POST.get('doctorId')
            # ----user can choose any patient but only their info will be stored
            appointment.patientId = request.user.id
            appointment.doctorName = models.User.objects.get(
                id=request.POST.get('doctorId')).first_name
            # ----user can choose any patient but only their info will be stored
            appointment.patientName = request.user.first_name
            appointment.status = False
            data = {
                'Patient_name': patient.get_name,
                'Doctor_name': doctor.get_name,
                'Patient_mobile': patient.mobile,
                'email': request.user.email,
                'massage': request.POST.get('description'),
                'Patient_address': patient.address,
                'Symptoms': patient.symptoms
            }

            msg = '''
            Patient Name:\t{}
            Doctor Name:\t{}
            Patient Email:\t{}
            Patient Number:\t{}
            Patient Address:\t{}
            Before Symptoms:\t{}
            ------------------------------------------------Symptoms Description---------------------------------------------------
            Symptoms:\t{}
            '''.format(data['Patient_name'], data['Doctor_name'], data['email'], data['Patient_mobile'], data['Patient_address'], data['Symptoms'], data['massage'])
            send_mail('Your New Appoitment', msg, settings.EMAIL_HOST_USER,
                      [doctor.email], fail_silently=False)
            print('message from' + settings.EMAIL_HOST_USER + 'to' + doctor.email)
            appointment.save()
        return HttpResponseRedirect('patient_view_appointment')
    return render(request, 'patient_book_appointment.html', context=p_context)


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    appointment = models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request, 'patient_view_appointment.html', {'appointment': appointment, 'patient': patient})


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_doctor(request):
    # for profile picture of patient in sidebar
    patient = models.Patient.objects.get(user_id=request.user.id)
    doctors = models.Doctor.objects.all().order_by('-id')
    doctor = models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict = {
        'patient': patient,
        'doctors': doctors,
        'doctor': doctor,
    }
    return render(request, 'patient_doctor.html', context=mydict)


def search_doctor_view(request):
    # for profile picture of patient in sidebar
    patient = models.Patient.objects.get(user_id=request.user.id)
    # whatever user write in search box we get in query
    query = request.GET['query']
    doctors = models.Doctor.objects.all().filter(status=True).filter(
        Q(department__icontains=query) | Q(user__first_name__icontains=query))
    return render(request, 'patient_doctor.html', {'patient': patient, 'doctors': doctors})


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge(request):
    # for profile picture of patient in sidebar
    patient = models.Patient.objects.get(user_id=request.user.id)
    patientdict = {
        'is_discharged': False,
        'patient': patient,
        'patientId': request.user.id,
    }
    return render(request, 'patient_discharge.html', context=patientdict)
# ---------------------------------------------------------------------------------
# ------------------------ DOCTOR RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------


@ login_required(login_url='doctorlogin')
@ user_passes_test(is_doctor)
def doctor_dashboard(request):
    # for both table in admin dashboard
    doctors = models.Doctor.objects.all().order_by('-id')
    patients = models.Patient.objects.all().order_by('-id')

    # for  cards
    patientcount = models.Patient.objects.all().filter(
        status=True, assignedDoctorId=request.user.id).count()
    pendingpatientcount = models.Patient.objects.all().filter(
        status=False, assignedDoctorId=request.user.id).count()

    appointmentcount = models.Appointment.objects.all().filter(
        status=True, doctorId=request.user.id).count()
    pendingappointmentcount = models.Appointment.objects.all().filter(
        status=False, doctorId=request.user.id).count()
    patientdischarged = models.PatientDischargeDetails.objects.all(
    ).distinct().filter(assignedDoctorName=request.user.first_name).count()

    # for  table in doctor dashboard
    appointments = models.Appointment.objects.all().filter(
        status=True, doctorId=request.user.id).order_by('-id')
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(
        status=True, user_id__in=patientid).order_by('-id')
    appointments = zip(appointments, patients)
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    p_context = {
        'doctors': doctors,
        'doctor': doctor,
        'patients': patients,
        'patientcount': patientcount,
        'pendingpatientcount': pendingpatientcount,
        'patientdischarged': patientdischarged,
        'appointmentcount': appointmentcount,
        'appointments': appointments,
        'pendingappointmentcount': pendingappointmentcount,
    }
    return render(request, 'doctor_dashboard.html', context=p_context)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment(request):
    # for profile picture of doctor in sidebar
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    return render(request, 'doctor_appointment.html', {'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment(request):
    # for profile picture of doctor in sidebar
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    appointment = models.Appointment.objects.all()
    appointments = models.Appointment.objects.all().filter(
        status=True, doctorId=request.user.id)
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(
        status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(request, 'doctor_view_appointment.html', {'appointments': appointments, 'doctor': doctor, 'appointment': appointment})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_book_appointment(request):
    # for profile picture of doctor in sidebar
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    appointmentForm = forms.appointmentform()
    mydict = {'appointmentForm': appointmentForm, 'doctor': doctor}
    if request.method == 'POST':
        appointmentForm = forms.appointmentform(request.POST)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get('doctorId')
            appointment.patientId = request.POST.get('patientId')
            appointment.doctorName = models.User.objects.get(
                id=request.POST.get('doctorId')).first_name
            appointment.patientName = models.User.objects.get(
                id=request.POST.get('patientId')).first_name
            appointment.status = True
            appointment.save()
            data = {
                'Doctor_name': doctor.get_name,
                'Doctor_mobile': doctor.mobile,
                'email': request.user.email,
                'Patient_name': models.User.objects.get(
                    id=request.POST.get('patientId')).first_name,
                'massage': request.POST.get('description'),
                'Doctor_address': doctor.address,
                'Department': doctor.department
            }

            msg = '''
            Doctor Name:\t{}
            Patient Name:\t{}
            Doctor Email:\t{}
            Doctor Number:\t{}
            Doctor Address:\t{}
            Department:\t{}
            ------------------------------------------------Symptoms Description---------------------------------------------------
            Symptoms:\t{}
            '''.format(data['Doctor_name'], data['Patient_name'], data['email'], data['Doctor_mobile'], data['Doctor_address'], data['Department'], data['massage'])
            send_mail('Your New Appoitment', msg, settings.EMAIL_HOST_USER,
                      [doctor.email], fail_silently=False)
            print('message from' + settings.EMAIL_HOST_USER + 'to' + doctor.email)
        return HttpResponseRedirect('doctor_view_appointment')
    return render(request, 'doctor_book_appointment.html', context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_approve_appointment(request):
    # for profile picture of doctor in sidebar
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    appointments = models.Appointment.objects.all().filter(
        status=False, doctorId=request.user.id)
    return render(request, 'doctor_approve_appointment.html', {'appointments': appointments, 'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def approve_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.status = True
    appointment.save()
    return redirect(reverse('doctor_approve_appointment'))


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def reject_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('doctor_approve_appointment')


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment(request):
    # for profile picture of doctor in sidebar
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    appointments = models.Appointment.objects.all().filter(
        status=True, doctorId=request.user.id)
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(
        status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(request, 'doctor_delete_appointment.html', {'appointments': appointments, 'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('doctor_delete_appointment')


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient(request):
    # for  cards
    patientcount = models.Patient.objects.all().filter(
        status=True, assignedDoctorId=request.user.id).count()
    pendingpatientcount = models.Patient.objects.all().filter(
        status=False, assignedDoctorId=request.user.id).count()
    patientdischarged = models.PatientDischargeDetails.objects.all(
    ).distinct().filter(assignedDoctorName=request.user.first_name).count()
    mydict = {
        # 'patients': patients,
        'patientcount': patientcount,
        'pendingpatientcount': pendingpatientcount,
        'patientdischarged': patientdischarged,
        # for profile picture of doctor in sidebar
        'doctor': models.Doctor.objects.get(user_id=request.user.id),
    }
    return render(request, 'doctor_patient.html', context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_add_patient(request):
    userform = forms.patientuserform()
    patientform = forms.patientform()
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    p_context = {'userform': userform, 'patientform': patientform,
                 'doctor': doctor}
    if request.method == "POST":
        userform = forms.patientuserform(request.POST)
        patientform = forms.patientform(request.POST, request.FILES)
        if userform.is_valid() and patientform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            patient = patientform.save(commit=False)
            patient.user = user
            patient.status = True
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient = patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
            data = {
                'Doctor_name': doctor.get_name,
                'Doctor_mobile': doctor.mobile,
                'email': request.user.email,
                'Patient_name': user.first_name,
                'Patient_username': user.username,
                'Patient_password': user.password,
                'Doctor_address': doctor.address,
                'Department': doctor.department
            }

            msg = '''
                                                            Your Doctor

            Doctor Name:\t{}
            Patient Name:\t{}
            Doctor Email:\t{}
            Doctor Number:\t{}
            Doctor Address:\t{}
            Department:\t{}
                ------------------------------------------------Symptoms Description---------------------------------------------------
            Hello Patient,

            In starting you doctor details is described, and you need your Patient portal so here your Id and Password:\n usrname:\t{}\n Password:\t{}\n
            '''.format(data['Doctor_name'], data['Patient_name'], data['email'], data['Doctor_mobile'], data['Doctor_address'], data['Department'], data['Patient_username'], data['Patient_password'])
            send_mail('Your Doctor', msg, settings.EMAIL_HOST_USER,
                      [user.email], fail_silently=False)
            print(data)
            print(user.email)
        return HttpResponseRedirect('doctor_view_patient')
    return render(request, 'doctor_add_patient.html', context=p_context)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient(request):
    patients = models.Patient.objects.all().filter(
        status=True, assignedDoctorId=request.user.id)
    # for profile picture of doctor in sidebar
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    return render(request, 'doctor_view_patient.html', {'patients': patients, 'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_patient_from_hospital(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('doctor_view_patient')


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_approve_patient(request):
    patients = models.Patient.objects.all().filter(
        status=False, assignedDoctorId=request.user.id)
    # for profile picture of doctor in sidebar
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    return render(request, 'doctor_approve_patient.html', {'patients': patients, 'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def approve_patient(request, pk):
    patient = models.Patient.objects.get(id=pk)
    patient.status = True
    patient.save()
    return redirect(reverse('doctor_approve_patient'))


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def reject_patient(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('doctor_approve_patient')


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_discharge_patient(request):
    # for profile picture of patient in sidebar
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    patients = models.Patient.objects.all().filter(
        status=True, assignedDoctorId=request.user.id)
    return render(request, 'doctor_discharge_patient.html', {'doctor': doctor, 'patients': patients})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def discharge_patient(request, pk):
    patient = models.Patient.objects.get(id=pk)
    # for profile picture of patient in sidebar
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    days = (date.today()-patient.admitDate)  # 2 days, 0:00:00
    assignedDoctor = models.User.objects.all().filter(id=patient.assignedDoctorId)
    d = days.days  # only how many day that is 2
    patientDict = {
        'patientId': pk,
        'doctor': doctor,
        'name': patient.get_name,
        'mobile': patient.mobile,
        'address': patient.address,
        'symptoms': patient.symptoms,
        'admitDate': patient.admitDate,
        'todayDate': date.today(),
        'day': d,
        'assignedDoctorName': assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        feeDict = {
            'roomCharge': int(request.POST['roomCharge'])*int(d),
            'doctorFee': request.POST['doctorFee'],
            'medicineCost': request.POST['medicineCost'],
            'OtherCharge': request.POST['OtherCharge'],
            'total': (int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        # for updating to database patientDischargeDetails (pDD)
        pDD = models.PatientDischargeDetails()
        pDD.patientId = pk
        pDD.patientName = patient.get_name
        pDD.assignedDoctorName = assignedDoctor[0].first_name
        pDD.address = patient.address
        pDD.mobile = patient.mobile
        pDD.symptoms = patient.symptoms
        pDD.admitDate = patient.admitDate
        pDD.releaseDate = date.today()
        pDD.daySpent = int(d)
        pDD.medicineCost = int(request.POST['medicineCost'])
        pDD.roomCharge = int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee = int(request.POST['doctorFee'])
        pDD.OtherCharge = int(request.POST['OtherCharge'])
        pDD.total = (int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(
            request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request, 'patient_final_bill.html', context=patientDict)
    return render(request, 'discharge_generate_bill.html', context=patientDict)


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return


def download_pdf_view(request, pk):
    dischargeDetails = models.PatientDischargeDetails.objects.all().filter(
        patientId=pk).order_by('-id')[:1]
    dict = {
        'patientName': dischargeDetails[0].patientName,
        'assignedDoctorName': dischargeDetails[0].assignedDoctorName,
        'address': dischargeDetails[0].address,
        'mobile': dischargeDetails[0].mobile,
        'symptoms': dischargeDetails[0].symptoms,
        'admitDate': dischargeDetails[0].admitDate,
        'releaseDate': dischargeDetails[0].releaseDate,
        'daySpent': dischargeDetails[0].daySpent,
        'medicineCost': dischargeDetails[0].medicineCost,
        'roomCharge': dischargeDetails[0].roomCharge,
        'doctorFee': dischargeDetails[0].doctorFee,
        'OtherCharge': dischargeDetails[0].OtherCharge,
        'total': dischargeDetails[0].total,
    }
    return render_to_pdf('download_bill.html', dict)
