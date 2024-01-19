# centre1/urls.py
from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib import admin
from .views import record_sale



urlpatterns = [
    path('sales/', views.record_sale, name='record_sale'),
    
]
