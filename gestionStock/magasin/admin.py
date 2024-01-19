from django.contrib import admin
from .models import Centre
from .models import Produit
from .models import Client
from .models import Fournisseur
from .models import Employe
from .models import Vente
from .models import Achat
from .models import PayementCredit
from .models import Reglement
from .models import Transfert



# Register your models here.
admin.site.register(Centre)
admin.site.register(Produit)
admin.site.register(Client)
admin.site.register(Fournisseur)
admin.site.register(Employe)
admin.site.register(Vente)
admin.site.register(Achat)
admin.site.register(PayementCredit)
admin.site.register(Reglement)
admin.site.register(Transfert)