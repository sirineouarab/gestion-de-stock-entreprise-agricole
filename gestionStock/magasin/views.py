from django.shortcuts import render,redirect, get_object_or_404
from .models import Produit, Client,Fournisseur, Centre,Employe, Achat,Reglement,ProduitAchat
from .forms import ProduitForm,ClientForm, FournisseurForm, CentreForm, EmployeForm,ReglementForm
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
            'montant': sum(
                produit.qteAchat * produit.HTAchat 
                for produit in ProduitAchat.objects.filter(achat=achat)
            )
        }
        for achat in achats
    ]
    montantDesAchats=sum(item['montant'] for item in montantDesAchats)
    return render(request, 'magasin/achat/achat.html',{'achats':achats,'montant':montantDesAchats})

def achatDetails(request,id):
    achat = get_object_or_404(Achat, CodeAchat=id)
    reglements = Reglement.objects.filter(achat=id)
    produits = ProduitAchat.objects.filter(achat=id)
    montantTotal = sum(produit.HTAchat*produit.qteAchat for produit in produits)
    resteAPayer = montantTotal - sum(reglement.montantReg for reglement in reglements)
    return render(request, 'magasin/achat/achatDetails.html',{'achat':achat,'reglements':reglements,'produits':produits,'montantTotal':montantTotal, 'resteAPayer':resteAPayer})

def transfert(request):
    return render(request, 'magasin/transfert/transfert.html')

def vente(request):
    return render(request, 'magasin/vente/vente.html')

def stock(request):
    return render(request, 'magasin/stock/stock.html')

def newProduct(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            form = ProduitForm()
        return redirect('tablesManagement')
    else:
        form = ProduitForm() 
    return render(request,"magasin//tables/addProduct.html",{"form":form})

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

def deleteProduct(request, id):
    product_delete = get_object_or_404(Produit, CodeP=id)
    if request.method=='POST': 
        product_delete.delete()
        return redirect('tablesManagement')
    else:
        return render(request,"magasin/tables/deleteProduct.html",{'produit': product_delete} )
    

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
   

def deleteAchat(request, id):
    Achat_delete = get_object_or_404(Achat, CodeAchat=id)
    produits_achat = ProduitAchat.objects.filter(achat=Achat_delete)

    if request.method=='POST': 
        for produit_achat in produits_achat:
            produit = produit_achat.produit
            produit.qteStock -= produit_achat.qteAchat
            produit.save()
        Achat_delete.delete()
        return redirect('achat')
    else:
        return render(request,"magasin/achat/deleteAchat.html",{'Achat':Achat_delete} )
   

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

def searchProduct(request):
    if request.method == "GET":
        query=request.GET['search']
        if query:
            produits=Produit.objects.filter(Designation__contains=query)
            return render(request,'magasin/searchProduct.html', {'produits': produits })
    return render(request,'magasin/tables/searchProduct.html')

def searchClient(request):
    if request.method == "GET":
        query=request.GET['search']
        if query:
            clients=Client.objects.filter(nomPrenomC__contains=query)
            return render(request,'magasin/searchClient.html', {'clients': clients })
    return render(request,'magasin/tables/searchClient.html')

def searchFournisseur(request):
    if request.method == "GET":
        query=request.GET['search']
        if query:
            fournisseurs=Fournisseur.objects.filter(nomPrenomF__contains=query)
            return render(request,'magasin/searchFournisseur.html', {'fournisseurs': fournisseurs })
    return render(request,'magasin/tables/searchFournisseur.html')


def searchCentre(request):
    if request.method == "GET":
        query=request.GET['search']
        if query:
            centres=Centre.objects.filter(DesignationCentre__contains=query)
            return render(request,'magasin/searchCentre.html', {'centres': centres })
    return render(request,'magasin/tables/searchCentre.html')

def searchEmploye(request):
    if request.method == "GET":
        query=request.GET['search']
        if query:
            employes=Employe.objects.filter(nomPrenomE__contains=query)
            return render(request,'magasin/searchEmploye.html', {'employes': employes })
    return render(request,'magasin/tables/searchEmploye.html')

def searchAchatParFournisseur(request):
    if request.method == "GET":
        query=request.GET['fournisseur']
        if query:
            achats=Achat.objects.filter(fournisseur__nomPrenomF__contains=query)
            return render(request,'magasin/searchAchatParFournisseur.html', {'achats': achats })
    return render(request,'magasin/achat/searchAchatParFournisseur.html')

def searchAchatParDate(request):
    if request.method == "GET":
        debut=request.GET['dateDeb']
        fin=request.GET['dateFin']
        if debut and fin:            
            debut_date = datetime.strptime(debut, '%Y-%m-%d')
            fin_date = datetime.strptime(fin, '%Y-%m-%d')
            achats = Achat.objects.filter(dateAchat__range=[debut_date, fin_date])            
            return render(request,'magasin/searchAchatParDate.html', {'achats': achats })
    return render(request,'magasin/achat/searchAchatParDate.html')


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


def completerPayement(request,id):
    achat = get_object_or_404(Achat, CodeAchat=id)

    # pour tester s'il a payé completement apr cet reglement
    reglements = Reglement.objects.filter(achat=id)
    produits = ProduitAchat.objects.filter(achat=id)
    montantTotal = sum(produit.HTAchat*produit.qteAchat for produit in produits)
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
            if(resteAPayer<=0): 
                achat.PayeEntierement = True
                achat.save()
            form = ReglementForm()
        return redirect('achat')
    else:
        form = ReglementForm() 
    return render(request,"magasin/achat/completerPayement.html",{"form":form})

    