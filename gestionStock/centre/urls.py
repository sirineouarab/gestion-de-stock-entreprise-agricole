
# centre1/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('sales/', views.record_sale, name='record_sale'),
    # Ajouter d'autres patterns d'URL au besoin
]
