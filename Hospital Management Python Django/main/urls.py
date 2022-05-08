from django.urls import path
from . import views
from .views import autosuggest
urlpatterns = [
    #path("", views.index, name="index"),
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login, name="login"),
    path("signup/", views.patient_signup, name="signup"),
    path("DocSignup/", views.signupdr, name="signupdr"),
    path('logout/', views.logout, name='logout'),
    path("add_patient/", views.add_patient, name="add_patient"),
    path("patient_list/", views.patient_list, name="patient_list"),
    path("patient/<str:pk>", views.patient, name="patient"),
    path("patientDelete/<int:id>", views.patientDelete, name="patientDelete"),
    path("patientAppointmentDelete/<int:id>", views.patientAppointmentDelete, name="patientAppointmentDelete"),    
    path("autosuggest/", views.autosuggest, name="autosuggest"),
    path("autodoctor/", views.autodoctor, name="autodoctor"),
    #path("info/", views.info, name="info"),
    path("appointments/", views.request_appointment, name="appointments"),    
    path("doctor-appointments/", views.approve_appointment, name="doctor-appointments"),
    path("appointmentDelete/<int:id>", views.appointmentDelete, name="appointmentDelete"),
    path("appointmentUpdate/<int:pk>", views.AppointmentUpdateView.as_view(), name="appointmentUpdate"),
    path("patientInfo/", views.patientInfo, name="patientInfo"),
    path('change/password/', views.ChangePassword.as_view(), name='update_password'),


    path('chat/', views.chat, name='chat'),
    path('<str:room>/', views.room, name='room'),
    path('chat/checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
]
