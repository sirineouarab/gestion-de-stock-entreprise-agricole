from django.shortcuts import render,redirect, get_object_or_404
from .models import Produit, Client,Fournisseur, Centre,Employe, Achat,Reglement, Transfert, Vente, PayementCredit
from .forms import ProduitForm,ClientForm, FournisseurForm, CentreForm, EmployeForm,ReglementForm, TransfertForm, PayementCreditForm, VenteForm, AchatForm
from datetime import datetime


from django.http import FileResponse
import io 
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your views here.

def index(request):
    return render(request,'index.html')

def tablesManagement(request):
    produits = Produit.objects.all()
    clients = Client.objects.all()
    fournisseurs = Fournisseur.objects.all()
    centres = Centre.objects.all()
    employes= Employe.objects.all()

    return render(request, 'magasin/tables/tablesmanagement.html', {'produits': produits,'clients': clients,'fournisseurs':fournisseurs,'centres':centres,'employes':employes})

def achat(request):
    achats = Achat.objects.all()
    montantDesAchats = [
        {
            'achat': achat,
            'montant': achat.qteAchat * achat.HTAchat
        }
        for achat in achats
    ]
    montantDesAchats=sum(item['montant'] for item in montantDesAchats)
    return render(request, 'magasin/achat/achat.html',{'achats':achats,'montant':montantDesAchats})

def achatDetails(request, id):
    achat = get_object_or_404(Achat, CodeAchat=id)
    reglements = Reglement.objects.filter(achat=id)
    montantTotal = achat.qteAchat * achat.HTAchat
    resteAPayer = montantTotal - sum(reglement.montantReg for reglement in reglements)

    return render(request, 'magasin/achat/achatDetails.html', {
        'achat': achat,
        'reglements': reglements,
        'montantTotal': montantTotal,
        'resteAPayer': resteAPayer
    })


def venteDetails(request,id):
    vente = get_object_or_404(Vente, CodeV=id)
    payementCredits = PayementCredit.objects.filter(vente=id)
    montantTotal = vente.qteVente * vente.prixUniVente
    resteAPayer = montantTotal - sum(payementCredit.montantPayCredit for payementCredit in payementCredits)
    return render(request, 'magasin/vente/venteDetails.html',{'vente':vente,'payementCredits':payementCredits,'montantTotal':montantTotal, 'resteAPayer':resteAPayer})



def transfert(request):
    transferts = Transfert.objects.all()
    return render(request, 'magasin/transfert/transfert.html',{"transferts": transferts})
def vente(request):
    ventes = Vente.objects.all()
    montantDesVentes = sum(vente.qteVente * vente.prixUniVente for vente in ventes)
    
    return render(request, 'magasin/vente/vente.html', {'ventes': ventes, 'montant': montantDesVentes})

def stock(request):
    produits = Produit.objects.filter(qteStock__gt=0)
    totalAchat = sum(produit.qteStock * produit.HTProd for produit in produits)
    return render(request, 'magasin/stock/stock.html',{'produits':produits,'totalAchat':totalAchat})

def newProduct(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            form = ProduitForm()
        return redirect('tablesManagement')
    else:
        form = ProduitForm() 
    return render(request,"magasin/tables/addProduct.html",{"form":form})


def newProductStock(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            form = ProduitForm()
        return redirect('stock')
    else:
        form = ProduitForm() 
    return render(request,"magasin/stock/addProduct.html",{"form":form})

def newClient(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            form = ClientForm()
        return redirect('tablesManagement')
    else:
        form = ClientForm() 
    return render(request,"magasin/tables/addClient.html",{"form":form})

def newFournisseur(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            form = FournisseurForm()
        return redirect('tablesManagement')
    else:
        form = FournisseurForm() 
    return render(request,"magasin/tables/addFournisseur.html",{"form":form})

def newCentre(request):
    if request.method == 'POST':
        form = CentreForm(request.POST)
        if form.is_valid():
            form.save()
            form = CentreForm()
        return redirect('tablesManagement')
    else:
        form = CentreForm() 
    return render(request,"magasin/tables/addCentre.html",{"form":form})


def newEmploye(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()
            form = EmployeForm()
        return redirect('tablesManagement')
    else:
        form = EmployeForm() 
    return render(request,"magasin/tables/addEmploye.html",{"form":form})


def newAchat(request):
    if request.method == 'POST':
        form = AchatForm(request.POST)
        if form.is_valid():
            achat = form.save()

            product = achat.produit
            product.qteStock += achat.qteAchat
            product.save()

            if not achat.PayeEntierement:
                remaining_amount = achat.qteAchat * achat.HTAchat
                fournisseur = achat.fournisseur
                fournisseur.solde += remaining_amount
                fournisseur.save()

            form = AchatForm()
            return redirect('achat')
    else:
        form = AchatForm()

    return render(request, "magasin/achat/addAchat.html", {'form': form})



def newTransfert(request):
    cost = 0

    if request.method == 'POST':
        form = TransfertForm(request.POST)

        if form.is_valid():
            transfert = form.save(commit=False)
            quantity = form.cleaned_data['qteTransfert']
            product = form.cleaned_data['produit']
            product_price = product.HTProd

            if product.qteStock >= quantity:
                cost = product_price * quantity
                transfert.cost = cost
                transfert.save()

                product.qteStock -= quantity
                product.save()

                return redirect('transfert')
            else:
                form.add_error('qteTransfert', 'quantité inssufisante en stock.')

    else:
        form = TransfertForm()

    return render(request, "magasin/transfert/addTransfert.html", {"form": form, 'cout': cost})

def newVente(request):
    if request.method == 'POST':
        form = VenteForm(request.POST)
        if form.is_valid():
            vente = form.save()

            product = vente.produit
            product.qteStock -= vente.qteVente
            product.save()

            if not vente.PayeEnt:
                remaining_amount = vente.qteVente * vente.prixUniVente
                client = vente.client
                client.credit += remaining_amount
                client.save()

            form = VenteForm()
            return redirect('vente')
    else:
        form = VenteForm() 

    return render(request,"magasin/vente/addVente.html",{'form':form})

def deleteProduct(request, id):
    product_delete = get_object_or_404(Produit, CodeP=id)
    if request.method=='POST': 
        product_delete.delete()
        return redirect('tablesManagement')
    else:
        return render(request,"magasin/tables/deleteProduct.html",{'produit': product_delete} )
    
def deleteProductStock(request, id):
    product_delete = get_object_or_404(Produit, CodeP=id)
    if request.method=='POST': 
        product_delete.delete()
        return redirect('stock')
    else:
        return render(request,"magasin/stock/deleteProduct.html",{'produit': product_delete} )
    

def deleteClient(request, id):
    client_delete = get_object_or_404(Client, CodeC=id)
    if request.method=='POST': 
        client_delete.delete()
        return redirect('tablesManagement')
    else:
        return render(request,"magasin/tables/deleteClient.html",{'client': client_delete} )
    

def deleteFournisseur(request, id):
    fournisseur_delete = get_object_or_404(Fournisseur, CodeF=id)
    if request.method=='POST': 
        fournisseur_delete.delete()
        return redirect('tablesManagement')
    else:
        return render(request,"magasin/tables/deleteFournisseur.html",{'fournisseur':fournisseur_delete} )
    


def deleteCentre(request, id):
    centre_delete = get_object_or_404(Centre, CodeCentre=id)
    if request.method=='POST': 
        centre_delete.delete()
        return redirect('tablesManagement')
    else:
        return render(request,"magasin/tables/deleteCentre.html",{'centre':centre_delete} )
    
def deleteEmploye(request, id):
    employe_delete = get_object_or_404(Employe, CodeE=id)
    if request.method=='POST': 
        employe_delete.delete()
        return redirect('tablesManagement')
    else:
        return render(request,"magasin/tables/deleteEmploye.html",{'Employe':employe_delete} )
   
def deleteTransfert(request, id):
    transfert = get_object_or_404(Transfert, CodeTransfert=id)

    if request.method == 'POST':
        product = transfert.produit
        quantity = transfert.qteTransfert
        product.qteStock += quantity 
        product.save()

        transfert.delete()

        return redirect('transfert')
    else:
        return render(request,"magasin/transfert/deleteTransfert.html",{'transfert':transfert} )
   

def deleteAchat(request, id):
    Achat_delete = get_object_or_404(Achat, CodeAchat=id)

    if request.method == 'POST':
        produit = Achat_delete.produit
        produit.qteStock += Achat_delete.qteAchat
        produit.save()
        
        Achat_delete.delete()
        return redirect('achat')
    else:
        return render(request,"magasin/achat/deleteAchat.html",{'Achat':Achat_delete} )
    

def deleteVente(request, id):
    vente_delete = get_object_or_404(Vente, CodeV=id)

    if request.method == 'POST':
        produit = vente_delete.produit
        produit.qteStock += vente_delete.qteVente
        produit.save()

        if not vente_delete.PayeEnt:
            client = vente_delete.client
            client.credit -= (vente_delete.qteVente * vente_delete.prixUniVente)
            client.save()

        vente_delete.delete()
        return redirect('vente')
    else:
        return render(request, "magasin/vente/deleteVente.html", {'vente': vente_delete})


def editProduct(request, id):
    product_edit = get_object_or_404(Produit, CodeP=id)
    if request.method=='POST':
        product_save= ProduitForm(request.POST,request.FILES,instance=product_edit)
        if product_save.is_valid():
            product_save.save()
            return redirect('tablesManagement')
    else:
        product_save= ProduitForm(instance=product_edit)
    return render(request,"magasin/tables/editProduct.html",{'produit':product_save})



def editProductStock(request, id):
    product_edit = get_object_or_404(Produit, CodeP=id)
    if request.method=='POST':
        product_save= ProduitForm(request.POST,request.FILES,instance=product_edit)
        if product_save.is_valid():
            product_save.save()
            return redirect('stock')
    else:
        product_save= ProduitForm(instance=product_edit)
    return render(request,"magasin/stock/editProduct.html",{'produit':product_save})


def editClient(request, id):
    client_edit = get_object_or_404(Client, CodeC=id)
    if request.method=='POST':
        client_save= ClientForm(request.POST,request.FILES,instance=client_edit)
        if client_save.is_valid():
            client_save.save()
            return redirect('tablesManagement')
    else:
        client_save= ClientForm(instance=client_edit)
    return render(request,"magasin/tables/editClient.html",{'client':client_save})

def editFournisseur(request, id):
    fournisseur_edit = get_object_or_404(Fournisseur, CodeF=id)
    if request.method=='POST':
        fournisseur_save= FournisseurForm(request.POST,request.FILES,instance=fournisseur_edit)
        if fournisseur_save.is_valid():
            fournisseur_save.save()
            return redirect('tablesManagement')
    else:
        fournisseur_save= FournisseurForm(instance=fournisseur_edit)
    return render(request,"magasin/tables/editFournisseur.html",{'fournisseur':fournisseur_save})

def editCentre(request, id):
    centre_edit = get_object_or_404(Centre, CodeCentre=id)
    if request.method=='POST':
        centre_save= CentreForm(request.POST,request.FILES,instance=centre_edit)
        if centre_save.is_valid():
            centre_save.save()
            return redirect('tablesManagement')
    else:
        centre_save= CentreForm(instance=centre_edit)
    return render(request,"magasin/tables/editCentre.html",{'centre':centre_save})


def editEmploye(request, id):
    employe_edit = get_object_or_404(Employe, CodeE=id)
    if request.method=='POST':
        employe_save= EmployeForm(request.POST,request.FILES,instance=employe_edit)
        if employe_save.is_valid():
            employe_save.save()
            return redirect('tablesManagement')
    else:
        employe_save= EmployeForm(instance=employe_edit)
    return render(request,"magasin/tables/editEmploye.html",{'employe':employe_save})

def editVente(request, id):
    vente = get_object_or_404(Vente, CodeV=id)

    if request.method == 'POST':
        form = VenteForm(request.POST, instance=vente)
        if form.is_valid():
            form.save()
            return redirect('vente')
    else:
        form = VenteForm(instance=vente)

    return render(request, "magasin/vente/editVente.html", {'form': form, 'vente': vente})

def editAchat(request, id):
    achat = get_object_or_404(Achat, CodeAchat=id)

    if request.method == 'POST':
        form = AchatForm(request.POST, instance=achat)
        if form.is_valid():
            form.save()
            return redirect('achat')
    else:
        form = AchatForm(instance=achat)

    return render(request, "magasin/achat/editAchat.html", {'form': form, 'achat': achat})


def searchProduct(request):
    if request.method == "GET":
        query=request.GET['search']
        if query:
            produits=Produit.objects.filter(Designation__contains=query)
            return render(request,'magasin/tables/searchProduct.html', {'produits': produits })
    return render(request,'magasin/tables/searchProduct.html')

def searchClient(request):
    if request.method == "GET":
        query=request.GET['search']
        if query:
            clients=Client.objects.filter(nomPrenomC__contains=query)
            return render(request,'magasin/tables/searchClient.html', {'clients': clients })
    return render(request,'magasin/tables/searchClient.html')

def searchFournisseur(request):
    if request.method == "GET":
        query=request.GET['search']
        if query:
            fournisseurs=Fournisseur.objects.filter(nomPrenomF__contains=query)
            return render(request,'magasin/tables/searchFournisseur.html', {'fournisseurs': fournisseurs })
    return render(request,'magasin/tables/searchFournisseur.html')


def searchCentre(request):
    if request.method == "GET":
        query=request.GET['search']
        if query:
            centres=Centre.objects.filter(DesignationCentre__contains=query)
            return render(request,'magasin/tables/searchCentre.html', {'centres': centres })
    return render(request,'magasin/tables/searchCentre.html')

def searchEmploye(request):
    if request.method == "GET":
        query=request.GET['search']
        if query:
            employes=Employe.objects.filter(nomPrenomE__contains=query)
            return render(request,'magasin/tables/searchEmploye.html', {'employes': employes })
    return render(request,'magasin/tables/searchEmploye.html')

def searchAchatParFournisseur(request):
    if request.method == "GET":
        query=request.GET['fournisseur']
        if query:
            achats=Achat.objects.filter(fournisseur__nomPrenomF__contains=query)
            return render(request,'magasin/achat/searchAchatParFournisseur.html', {'achats': achats })
    return render(request,'magasin/achat/searchAchatParFournisseur.html')

def searchVenteParClient(request):
    montant_total = 0
    
    if request.method == "GET":
        query = request.GET.get('client', '')
        if query:
            ventes = Vente.objects.filter(client__nomPrenomC__contains=query)
            
            montant_total = sum(vente.qteVente * vente.prixUniVente for vente in ventes)

            return render(request, 'magasin/vente/searchVenteParClient.html', {'ventes': ventes, 'montant_total': montant_total})

    return render(request, 'magasin/vente/searchVenteParClient.html', {'montant_total': montant_total})


def searchAchatParDate(request):
    if request.method == "GET":
        debut=request.GET['dateDeb']
        fin=request.GET['dateFin']
        if debut and fin:            
            debut_date = datetime.strptime(debut, '%Y-%m-%d')
            fin_date = datetime.strptime(fin, '%Y-%m-%d')
            achats = Achat.objects.filter(dateAchat__range=[debut_date, fin_date])            
            return render(request,'magasin/achat/searchAchatParDate.html', {'achats': achats })
    return render(request,'magasin/achat/searchAchatParDate.html')


def searchVenteParDate(request):
    montant_total = 0
    
    if request.method == "GET":
        debut = request.GET.get('dateDeb', '')
        fin = request.GET.get('dateFin', '')
        
        if debut and fin:
            debut_date = datetime.strptime(debut, '%Y-%m-%d')
            fin_date = datetime.strptime(fin, '%Y-%m-%d')
            
            ventes = Vente.objects.filter(dateVente__range=[debut_date, fin_date])
            
            montant_total = sum(vente.qteVente * vente.prixUniVente for vente in ventes)

            return render(request, 'magasin/vente/searchVenteParDate.html', {'ventes': ventes, 'montant_total': montant_total})

    return render(request, 'magasin/vente/searchVenteParDate.html', {'montant_total': montant_total})

def searchProduitParNom(request):
    if request.method == "GET":
        query=request.GET['nom']
        if query:
            produits = Produit.objects.filter(Designation__contains=query)
            totalAchat = sum(produit.qteStock * produit.HTProd for produit in produits)
            return render(request,'magasin/stock/searchStockParNomProduit.html', {'produits': produits ,'totalAchat':totalAchat,'query':query})
    return render(request,'magasin/stock/searchStockParNomProduit.html')

def searchProduitParFournisseur(request):
    if request.method == "GET":
        query=request.GET['fournisseur']
        if query:
            produits = Produit.objects.filter(achat__fournisseur__nomPrenomF__contains=query)
            totalAchat = sum(produit.qteStock * produit.HTProd for produit in produits)
            return render(request,'magasin/stock/searchStockParFournisseur.html', {'produits': produits,'totalAchat':totalAchat,'query':query })
    return render(request,'magasin/stock/searchStockParFournisseur.html')

def searchProduitParDate(request):
    debut_date= None
    fin_date= None
    if request.method == "GET":
        debut=request.GET['dateDeb']
        fin=request.GET['dateFin']
        if debut and fin:            
            debut_date = datetime.strptime(debut, '%Y-%m-%d')
            fin_date = datetime.strptime(fin, '%Y-%m-%d')
            produits = Produit.objects.filter(achat__dateAchat__range=(debut_date, fin_date))
            totalAchat = sum(produit.qteStock * produit.HTProd for produit in produits)
            return render(request,'magasin/stock/searchStockParDate.html', {'produits': produits ,'totalAchat':totalAchat,'debut_date': debut_date, 'fin_date': fin_date})
    return render(request,'magasin/stock/searchStockParDate.html')


def searchTransfert(request):
    if request.method == "GET":
        query=request.GET['search']
        if query:
            transferts=Transfert.objects.filter(produit__Designation__contains=query)
            return render(request,'magasin/transfert/searchTransfert.html', {'transferts': transferts })
    return render(request,'magasin/transfert/searchTransfert.html')

def printProducts(request):
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=letter,bottomup=0)
    textob = p.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica",14)

    produits = Produit.objects.all()
    lines = []

    for produit in produits:
        lines.append("code produit : "+str(produit.CodeP))
        lines.append("designation produit : "+str(produit.Designation))
        lines.append("quantité en stock : "+str(produit.qteStock))
        lines.append("HT produit : "+str(produit.HTProd))
        lines.append("==============================")
 
    
    for line in lines:
        textob.textLine(line)
    
    p.drawText(textob)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="produits.pdf")


def printProductsStock(request):
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=letter,bottomup=0)
    textob = p.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica",14)

    produits = Produit.objects.filter(qteStock__gt=0)

    lines = []

    for produit in produits:
        lines.append("code produit : "+str(produit.CodeP))
        lines.append("designation produit : "+str(produit.Designation))
        lines.append("quantité en stock : "+str(produit.qteStock))
        lines.append("HT produit : "+str(produit.HTProd))
        lines.append("==============================")
 
    
    for line in lines:
        textob.textLine(line)
    
    p.drawText(textob)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="produitsEnStock.pdf")



def printProductsStockDate(request,debut_date,fin_date):
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=letter,bottomup=0)
    textob = p.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica",14)

    produits = Produit.objects.filter(produitachat__achat__dateAchat__range=(debut_date, fin_date))

    lines = []

    for produit in produits:
        lines.append("code produit : "+str(produit.CodeP))
        lines.append("designation produit : "+str(produit.Designation))
        lines.append("quantité en stock : "+str(produit.qteStock))
        lines.append("HT produit : "+str(produit.HTProd))
        lines.append("==============================")
 
    
    for line in lines:
        textob.textLine(line)
    
    p.drawText(textob)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="produitsEnStock.pdf")

def printProductsStockFournisseur(request,query):
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=letter,bottomup=0)
    textob = p.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica",14)

    produits = Produit.objects.filter(produitachat__achat__fournisseur__nomPrenomF__contains=query)

    lines = []

    for produit in produits:
        lines.append("code produit : "+str(produit.CodeP))
        lines.append("designation produit : "+str(produit.Designation))
        lines.append("quantité en stock : "+str(produit.qteStock))
        lines.append("HT produit : "+str(produit.HTProd))
        lines.append("==============================")
 
    
    for line in lines:
        textob.textLine(line)
    
    p.drawText(textob)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="produitsEnStock.pdf")

def printProductsStockNom(request,query):
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=letter,bottomup=0)
    textob = p.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica",14)

    produits = Produit.objects.filter(Designation__contains=query)

    lines = []

    for produit in produits:
        lines.append("code produit : "+str(produit.CodeP))
        lines.append("designation produit : "+str(produit.Designation))
        lines.append("quantité en stock : "+str(produit.qteStock))
        lines.append("HT produit : "+str(produit.HTProd))
        lines.append("==============================")
 
    
    for line in lines:
        textob.textLine(line)
    
    p.drawText(textob)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="produitsEnStock.pdf")



def printClients(request):
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=letter,bottomup=0)
    textob = p.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica",14)

    clients = Client.objects.all()
    lines = []

    for client in clients:
        lines.append("code client : "+str(client.CodeC))
        lines.append("nom prenom client : "+str(client.nomPrenomC))
        lines.append("adresse client : "+str(client.adresseC))
        lines.append("telephone client : "+str(client.telephoneC))
        lines.append("credit : "+str(client.credit))
        lines.append("==============================")
 
    
    for line in lines:
        textob.textLine(line)
    
    p.drawText(textob)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="clients.pdf")

def printFournisseurs(request):
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=letter,bottomup=0)
    textob = p.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica",14)

    fournisseurs = Client.objects.all()
    lines = []

    for fournisseur in fournisseurs:
        lines.append("code fournisseur : "+str(fournisseur.CodeC))
        lines.append("nom prenom fournisseur : "+str(fournisseur.nomPrenomC))
        lines.append("adresse fournisseur : "+str(fournisseur.adresseC))
        lines.append("telephone fournisseur : "+str(fournisseur.telephoneC))
        lines.append("solde : "+str(fournisseur.credit))
        lines.append("==============================")
 
    
    for line in lines:
        textob.textLine(line)
    
    p.drawText(textob)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="fournisseurs.pdf")


def printCentres(request):
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=letter,bottomup=0)
    textob = p.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica",14)

    centres = Centre.objects.all()
    lines = []

    for centre in centres:
        lines.append("code centre : "+str(centre.CodeCentre))
        lines.append("designation centre : "+str(centre.DesignationCentre))
        lines.append("==============================")
 
    
    for line in lines:
        textob.textLine(line)
    
    p.drawText(textob)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="centres.pdf")


def printEmployes(request):
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=letter,bottomup=0)
    textob = p.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica",14)

    employes = Employe.objects.all()
    lines = []

    for employe in employes:
        lines.append("code employe : "+str(employe.CodeE))
        lines.append("nom prenom employe : "+str(employe.nomPrenomE))
        lines.append("adresse employe : "+str(employe.adresseE))
        lines.append("telephone employe : "+str(employe.telephoneE))
        lines.append("salaire jour : "+str(employe.salaireJour))
        lines.append("centre : "+str(employe.centre))
        lines.append("==============================")

 
    
    for line in lines:
        textob.textLine(line)
    
    p.drawText(textob)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="employes.pdf")


def completerPayement(request, id):
    achat = get_object_or_404(Achat, CodeAchat=id)
    reglements = Reglement.objects.filter(achat=id)
    montantTotal = achat.qteAchat * achat.HTAchat
    resteAPayer = montantTotal - sum(reglement.montantReg for reglement in reglements)
    
    fournisseur = achat.fournisseur

    if request.method == 'POST':
        form = ReglementForm(request.POST)
        if form.is_valid():
            reglement = form.save(commit=False)
            reglement.achat = achat
            reglement.save()
            
            fournisseur.solde -= reglement.montantReg
            fournisseur.save()

            reglements = Reglement.objects.filter(achat=id)
            resteAPayer = montantTotal - sum(reglement.montantReg for reglement in reglements)

            if resteAPayer <= 0:
                achat.PayeEntierement = True
                achat.save()

            form = ReglementForm()
            return redirect('achat') 
    else:
        form = ReglementForm()

    return render(request, "magasin/achat/completerPayement.html", {"form": form, "resteAPayer": resteAPayer})


def PayementCreditSection(request, id):
    vente = get_object_or_404(Vente, CodeV=id)
    payementCredits = PayementCredit.objects.filter(vente=id)
    montantTotal = vente.qteVente * vente.prixUniVente
    resteAPayer = montantTotal - sum(payementCredit.montantPayCredit for payementCredit in payementCredits)
    
    client = vente.client

    if request.method == 'POST':
        form = PayementCreditForm(request.POST)
        if form.is_valid():
            payementCredit = form.save(commit=False)
            payementCredit.vente = vente
            payementCredit.save()
            
            # Update the client's credit
            client.credit -= payementCredit.montantPayCredit
            client.save()

            # Recalculate the remaining amount to be paid
            payementCredits = PayementCredit.objects.filter(vente=id)
            resteAPayer = montantTotal - sum(payementCredit.montantPayCredit for payementCredit in payementCredits)

            # Update PayeEnt field of the vente
            if resteAPayer <= 0:
                vente.PayeEnt = True
                vente.save()

            form = PayementCreditForm()
        return redirect('vente')
    else:
        form = PayementCreditForm()

    return render(request, "magasin/vente/completerPayement.html", {"form": form, "resteAPayer": resteAPayer})
