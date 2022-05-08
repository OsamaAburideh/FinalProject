from django.test import TestCase

from django.test import TestCase
from django.contrib.auth.models import User
from core.restaurant.forms import DeliveriesCreateForm
from django.urls import reverse, resolve
from core.restaurant import views
from core.views import home
from core.restaurant.views import profilepage
from finalproject.urls import driver_urlpatterns


# testing if a user is created


