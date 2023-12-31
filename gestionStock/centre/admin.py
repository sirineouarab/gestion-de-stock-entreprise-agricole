from django.contrib import admin

# Register your models here.
from .models import Produit
from .models import Centre
from .models import Client
from .models import Employe
from .models import Vente
from .models import CreditPayment
from .models import Reglement


admin.site.register(Produit)
admin.site.register(Centre)
admin.site.register(Client)
admin.site.register(Employe)
admin.site.register(Vente)
admin.site.register(Reglement)
admin.site.register(CreditPayment)
