from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from .filters import PatientFilter
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

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



def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            print(request.POST)
            username = request.POST['username']
            password = request.POST['password']
            confirm_password = request.POST['Confirm-Password']
            if password ==  confirm_password:
                user = User.objects.get_or_create(username =username, password=make_password(password),is_active = True,) 
                print(user)

                auth.login(request, user[0])
                return redirect('/')
            else:
                messages.error(request, 'confirm password is not the same, reenter your password')
                return redirect('signup')
    return render(request, 'main/signup.html')

def signupdr(request):
    if request.user.is_staff:
        return redirect('/')
    else:
        if request.method == 'POST':
            print(request.POST)
            username = request.POST['username']
            password = request.POST['password']
            confirm_password = request.POST['Confirm-Password']
            if password ==  confirm_password:
                user = User.objects.get_or_create(username =username, password=make_password(password),is_active = True, is_staff=True) #doctor view
                print(user)

                auth.login(request, user[0])
                return redirect('/')
            else:
                messages.error(request, 'confirm password is not the same, reenter your password')
                return redirect('signup')
    return render(request, 'main/signupdr.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')




def dashboard(request):
    patients = Patient.objects.all()
    beds = Bed.objects.all()
    beds_available = Bed.objects.filter(occupied=False).count()
    context = {
        
        'beds_available': beds_available,
        
        'beds':beds
    }
    
    return render(request, 'main/dashboard.html', context)

def add_patient(request):
    beds = Bed.objects.filter(occupied=False)
    doctors = Doctor.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        phone_num = request.POST['phone_num']
        patient_relative_name = request.POST['patient_relative_name']
        patient_relative_contact = request.POST['patient_relative_contact']
        address = request.POST['address']
        symptoms = request.POST['symptoms']
        prior_ailments = request.POST['prior_ailments']
        bed_num_sent = request.POST['bed_num']
        bed_num = Bed.objects.get(bed_number=bed_num_sent)
        dob = request.POST['dob']
        status = request.POST['status']
        doctor = request.POST['doctor']
        doctor = Doctor.objects.get(name=doctor)
        print(request.POST)
        patient = Patient.objects.create(
            name = name,
        phone_num = phone_num,
        patient_relative_name = patient_relative_name,
        patient_relative_contact = patient_relative_contact, 
        address = address, 
        symptoms = symptoms, 
        prior_ailments = prior_ailments, 
        bed_num = bed_num,
        dob = dob, 
        doctor=doctor,
        status = status
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

def patient(request, pk):
    patient = Patient.objects.get(id=pk)
    if request.method == "POST":
        doctor = request.POST['doctor']
        doctor_time = request.POST['doctor_time']
        doctor_notes = request.POST['doctor_notes']
        mobile = request.POST['mobile']
        mobile2 = request.POST['mobile2']
        relativeName = request.POST['relativeName']
        address  = request.POST['location']
        print(doctor_time)
        print(doctor_notes)
        status = request.POST['status']
        doctor = Doctor.objects.get(name=doctor)
        print(doctor)
        patient.phone_num = mobile
        patient.patient_relative_contact = mobile2
        patient.patient_relative_name = relativeName
        patient.address = address
        patient.doctor = doctor
        patient.doctors_visiting_time = doctor_time
        patient.doctors_notes = doctor_notes
        print(patient.doctors_visiting_time)
        print(patient.doctors_notes)
        patient.status = status
        patient.save()
    context = {
        'patient': patient
    }
    return render(request, 'main/patient.html', context)


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

def index(request):
     return render(request, "main/index.html")