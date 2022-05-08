from datetime import datetime
from sqlite3 import Time
from time import time
from xmlrpc.client import _datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView

from main.forms import AppointmentForm, PasswordChangeForm
from .models import *
from .filters import PatientFilter
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
# PatientFilter = OrderFilter


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            print(user)
            if user is not None:
                auth.login(request, user)
                print(auth.login(request, user))
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
        else:
            return render(request, 'main/login.html')


'''
def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            print(request.POST)
            username = request.POST['username']
            password = request.POST['password']
            confirm_password = request.POST['Confirm-Password']
            if password == confirm_password:
                user = User.objects.get_or_create(username=username, password=make_password(password), is_active=True, )
                print(user)

                auth.login(request, user[0])
                return redirect('/')
            else:
                messages.error(request, 'confirm password is not the same, reenter your password')
                return redirect('signup')
    return render(request, 'main/signup.html')
'''


def signupdr(request):
    if request.user.is_staff:
        return redirect('/')
    else:
        if request.method == 'POST':
            print(request.POST)
            username = request.POST['username']
            password = request.POST['password']
            confirm_password = request.POST['Confirm-Password']
            if password == confirm_password:
                user = User.objects.get_or_create(username=username, password=make_password(password), is_active=True,
                                                  is_staff=True)  # doctor view
                print(user)

                auth.login(request, user[0])
                return redirect('/')
            else:
                messages.error(
                    request, 'confirm password is not the same, reenter your password')
                return redirect('signup')
    return render(request, 'main/signupdr.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')

def dashboard(request):
    beds = Bed.objects.all()
    beds_available = Bed.objects.filter(occupied=False).count()
    patients = Patient.objects.all()
    patient_count = patients.count()
    appointments = Appointment.objects.all()
    appointments_approved = Appointment.objects.filter(approved = True).count
    appointments_pending = Appointment.objects.filter(approved = False).count


    context = {
        'appointments_approved': appointments_approved,
        'appointments_pending': appointments_pending,
        'beds_available': beds_available,
        'patient_count': patient_count,
        'beds': beds
    }

    return render(request, 'main/dashboard.html', context)

@login_required(login_url='login')
def add_patient(request):
    beds = Bed.objects.filter(occupied=False)
    doctors = Doctor.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        phone_num = request.POST['phone_num']
        patient_relative_name = request.POST['patient_relative_name']
        patient_relative_contact = request.POST['patient_relative_contact']
        address = request.POST['address']
        prior_ailments = request.POST['prior_ailments']
        bed_num_sent = request.POST['bed_num']
        bed_num = Bed.objects.get(bed_number=bed_num_sent)
        dob = request.POST['dob']
        status = request.POST['status']
        doctor = request.POST['doctor']
        doctor = Doctor.objects.get(name=doctor)
        print(request.POST)
        patient = Patient.objects.create(
            name=name,
            phone_num=phone_num,
            patient_relative_name=patient_relative_name,
            patient_relative_contact=patient_relative_contact,
            address=address,
            prior_ailments=prior_ailments,
            bed_num=bed_num,
            dob=dob,
            doctor=doctor,
            status=status
        )
        patient.save()

        bed = Bed.objects.get(bed_number=bed_num_sent)
        bed.occupied = True
        bed.save()
        id = patient.id
        return redirect(f"/patient/{id}")

    context = {
        'beds': beds,
        'doctors': doctors
    }
    return render(request, 'main/add_patient.html', context)


def patient_signup(request):
    if request.method == "POST":
        name = request.POST['name']
        username = request.POST['username']
        confirm_password = request.POST['Confirm-Password']
        password = request.POST['password']
        phone_num = request.POST['phone_num']
        patient_relative_name = request.POST['patient_relative_name']
        patient_relative_contact = request.POST['patient_relative_contact']
        address = request.POST['address']
        #dob = ""
        #doctor = ""
        #doctor = ""
        print(request.POST)
        if password == confirm_password:
            user = User.objects.get_or_create(
                username=username, password=make_password(password), is_active=True, )

        patient = Patient.objects.create(
            user=user[0],
            name=name,
            phone_num=phone_num,
            patient_relative_name=patient_relative_name,
            patient_relative_contact=patient_relative_contact,
            address=address,
        )
        patient.save()
        id = patient.id
        auth.login(request, user[0])
        return redirect("/")

    context = {
        'beds': [],
        'doctors': []
    }
    return render(request, 'main/signup.html', context)

@login_required(login_url='login')
def patient(request, pk):

    patient = Patient.objects.get(id=pk)
    if request.method == "POST":
        if patient.bed_num:
            bedOccupied = Bed.objects.get(bed_number=patient.bed_num)
            bedOccupied.occupied = False
            bedOccupied.save()
        doctor = request.POST['doctor']
        bed_num = request.POST['bed_num']
        doctor_time = request.POST['doctor_time']
        doctor_notes = request.POST['doctor_notes']
        mobile = request.POST['mobile']
        mobile2 = request.POST['mobile2']
        relativeName = request.POST['relativeName']
        address = request.POST['location']
        status = request.POST['status']
        if not doctor == 'None':
            doctor = Doctor.objects.get(name=doctor)
            patient.doctor = doctor
        bed = Bed.objects.get(bed_number=bed_num)
        patient.phone_num = mobile
        patient.patient_relative_contact = mobile2
        patient.patient_relative_name = relativeName
        patient.address = address

        patient.bed_num = bed
        patient.doctors_visiting_time = doctor_time
        patient.doctors_notes = doctor_notes
        patient.status = status
        patient.save()
        bed = Bed.objects.get(bed_number=bed_num)
        bed.occupied = True
        bed.save()
    beds = Bed.objects.filter(occupied=False)
    context = {
        'beds': beds,
        'patient': patient
    }
    return render(request, 'main/patient.html', context)

@login_required(login_url='login')
def patient_list(request):
    patients = Patient.objects.all()

    # filtering
    myFilter = PatientFilter(request.GET, queryset=patients)

    patients = myFilter.qs
    context = {
        'patients': patients,
        'myFilter': myFilter
    }

    return render(request, 'main/patient_list.html', context)


'''
def autocomplete(request):
    if patient in request.GET:
        name = Patient.objects.filter(name__icontains=request.GET.get(patient))
        name = ['js', 'python']
        
        names = list()
        names.append('Shyren')
        print(names)
        for patient_name in name:
            names.append(patient_name.name)
        return JsonResponse(names, safe=False)
    return render (request, 'main/patient_list.html')
'''


def autosuggest(request):
    query_original = request.GET.get('term')
    queryset = Patient.objects.filter(name__icontains=query_original)
    mylist = []
    mylist += [x.name for x in queryset]
    return JsonResponse(mylist, safe=False)


def autodoctor(request):
    query_original = request.GET.get('term')
    queryset = Doctor.objects.filter(name__icontains=query_original)
    mylist = []
    mylist += [x.name for x in queryset]
    return JsonResponse(mylist, safe=False)


def info(request):
    return render(request, "main/info.html")

@login_required(login_url='login')
def request_appointment(request):
    appointments = Appointment.objects.filter(
        patient__user__username=request.user.username)
    doctors = Doctor.objects.all()
    if request.method == "POST":
        description = request.POST['description']
        print(request.POST)
        doctor = Doctor.objects.get(id=request.POST['doctor'])
        appointment = Appointment.objects.create(description=description, doctor=doctor,
                                                 patient=Patient.objects.filter(user=request.user)[0])
        return redirect('/appointments')
    context = {
        'appointments': appointments,
        'doctors': doctors,
    }

    return render(request, 'main/appointment.html', context)

def approve_appointment(request):
    appointments = Appointment.objects.all()
    if request.method == "POST":
        date = request.POST['date']
        time = request.POST['time']
        appointment = Appointment.objects.get(id=request.POST['id'])
        appointment.appointment_date = date
        appointment.appointment_time = time
        appointment.approved = True
        appointment.save()
        return redirect('/doctor-appointments')
    context = {
        'appointments': appointments,
    }

    return render(request, 'main/doctor-appointment.html', context)


def appointmentDelete(request, id):
    obj = get_object_or_404(Appointment, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Appointment Deleted Successfully !")
        return HttpResponseRedirect("/doctor-appointments")
    

    return render(request, "main/doctor-appointment.html")

class AppointmentUpdateView(UpdateView):
    form_class = AppointmentForm
    template_name = 'main/appointmentUpdate.html'
    model = Appointment
    success_url = "/doctor-appointments"


def patientAppointmentDelete(request, id):
    obj = get_object_or_404(Appointment, id=id)
    if request.method == "POST":
        obj.delete()
        return HttpResponseRedirect("/appointments")

    return render(request, "main/appointment.html")


def patientDelete(request, id):
    obj = get_object_or_404(Patient, id=id)
    if request.method == "POST":
        obj.user.delete()        
        messages.success(request, "Patient Deleted Successfully !")
        return HttpResponseRedirect("/patient_list")

    return render(request, "main/patient_list.html")

@login_required(login_url='login')
def patientInfo(request):
    patient = Patient.objects.get(user=request.user.id)
    if request.method == "POST":

        name = request.POST['name']
        mobile = request.POST['mobile']
        relativeContact = request.POST['relativeContact']
        relativeName = request.POST['relativeName']
        address = request.POST['address']
        patient.name = name
        patient.user.save()
        patient.phone_num = mobile
        patient.address = address
        patient.patient_relative_contact = relativeContact
        patient.patient_relative_name = relativeName
        patient.save()

    context = {
        'patient': patient
    }
    return render(request, 'main/patientInfo.html', context)


class ChangePassword(TemplateView):
    template_name = 'main/password_change.html'

    def get_context_data(self, **kwargs):
        kwargs.setdefault('view', self)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        kwargs['form'] = PasswordChangeForm(self.request.user)
        kwargs['is_settings_active'] = True
        kwargs['is_password_active'] = True
        return kwargs

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            login(self.request)
            return redirect(reverse('dashboard'))
        context['form'] = form
        return render(self.request, self.template_name, context)

@login_required(login_url='login')
def chat(request):
    return render(request, 'main/chat.html')

@login_required(login_url='login')
def room(request, room):
    username = request.GET.get('username')
    #patient.user = request.GET.get('username')
    #Doctor.user  = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'main/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })
@login_required(login_url='login')
@csrf_exempt
def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})