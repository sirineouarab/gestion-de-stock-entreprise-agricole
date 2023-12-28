from django.urls import path
from . import views

urlpatterns = [
    path('venteDash/',views.vente,name='venteDash'),
    path('achatDash/',views.achat,name='achatDash'),
   


]