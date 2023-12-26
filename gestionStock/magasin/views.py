from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from .models import Produit, Client,Fournisseur
from .forms import ProduitForm,ClientForm, FournisseurForm

import io 
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your views here.
def tablesManagement(request):
    produits = Produit.objects.all()
    clients = Client.objects.all()
    fournisseurs = Fournisseur.objects.all()

    return render(request, 'magasin/tablesmanagement.html', {'produits': produits,'clients': clients,'fournisseurs':fournisseurs})

def achat(request):
    return HttpResponse('achat page')

def transfert(request):
    return HttpResponse('transfert page')

def vente(request):
    return HttpResponse('vente page')

def stock(request):
    return HttpResponse('stock page')

def newProduct(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            form = ProduitForm()
        return redirect('tablesManagement')
    else:
        form = ProduitForm() 
    return render(request,"magasin/addProduct.html",{"form":form})

def newClient(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            form = ClientForm()
        return redirect('tablesManagement')
    else:
        form = ClientForm() 
    return render(request,"magasin/addClient.html",{"form":form})

def newFournisseur(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            form = FournisseurForm()
        return redirect('tablesManagement')
    else:
        form = FournisseurForm() 
    return render(request,"magasin/addFournisseur.html",{"form":form})

def deleteProduct(request, id):
    product_delete = get_object_or_404(Produit, CodeP=id)
    if request.method=='POST': 
        product_delete.delete()
        return redirect('tablesManagement')
    else:
        return render(request,"magasin/deleteProduct.html",{'produit': product_delete} )
    

def deleteClient(request, id):
    client_delete = get_object_or_404(Client, CodeC=id)
    if request.method=='POST': 
        client_delete.delete()
        return redirect('tablesManagement')
    else:
        return render(request,"magasin/deleteClient.html",{'client': client_delete} )
    

def deleteFournisseur(request, id):
    fournisseur_delete = get_object_or_404(Fournisseur, CodeF=id)
    if request.method=='POST': 
        fournisseur_delete.delete()
        return redirect('tablesManagement')
    else:
        return render(request,"magasin/deleteFournisseur.html",{'fournisseur_delete':fournisseur_delete} )
    
def editProduct(request, id):
    product_edit = get_object_or_404(Produit, CodeP=id)
    if request.method=='POST':
        product_save= ProduitForm(request.POST,request.FILES,instance=product_edit)
        if product_save.is_valid():
            product_save.save()
            return redirect('tablesManagement')
    else:
        product_save= ProduitForm(instance=product_edit)
    return render(request,"magasin/editProduct.html",{'produit':product_save})


def editClient(request, id):
    client_edit = get_object_or_404(Client, CodeC=id)
    if request.method=='POST':
        client_save= ClientForm(request.POST,request.FILES,instance=client_edit)
        if client_save.is_valid():
            client_save.save()
            return redirect('tablesManagement')
    else:
        client_save= ClientForm(instance=client_edit)
    return render(request,"magasin/editClient.html",{'client':client_save})

def editFournisseur(request, id):
    fournisseur_edit = get_object_or_404(Fournisseur, CodeF=id)
    if request.method=='POST':
        fournisseur_save= FournisseurForm(request.POST,request.FILES,instance=fournisseur_edit)
        if fournisseur_save.is_valid():
            fournisseur_save.save()
            return redirect('tablesManagement')
    else:
        fournisseur_save= FournisseurForm(instance=fournisseur_edit)
    return render(request,"magasin/editFournisseur.html",{'fournisseur':fournisseur_save})

def searchProduct(request):
    if request.method == "GET":
        query=request.GET['search']
        if query:
            produits=Produit.objects.filter(Designation__contains=query)
            return render(request,'magasin/searchProduct.html', {'produits': produits })
    return render(request,'magasin/searchProduct.html')

def searchClient(request):
    if request.method == "GET":
        query=request.GET['search']
        if query:
            clients=Client.objects.filter(nomPrenomC__contains=query)
            return render(request,'magasin/searchClient.html', {'clients': clients })
    return render(request,'magasin/searchClient.html')

def searchFournisseur(request):
    if request.method == "GET":
        query=request.GET['search']
        if query:
            fournisseurs=Fournisseur.objects.filter(nomPrenomF__contains=query)
            return render(request,'magasin/searchFournisseur.html', {'fournisseurs': fournisseurs })
    return render(request,'magasin/searchFournisseur.html')


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
