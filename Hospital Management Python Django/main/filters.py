# import django.contrib.admin.filters
import django_filters
from .models import *

# ModelnameFilter
class PatientFilter(django_filters.FilterSet):
    class Meta:
        model = Patient
        #fields = ['name', 'bed_num', 'doctor', 'status']
        fields = '__all__'
        exclude = ['user', 'phone_num', 'address', 'prior_ailments', 'dob', 'patient_relative_name', 'patient_relative_contact', 'symptoms', 'doctors_visiting_time', 'doctors_notes']
        
