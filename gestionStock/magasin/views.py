from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from .models import Produit
from .forms import ProduitForm

import io 
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your views here.
def tablesManagement(request):
    produits = Produit.objects.all()
    return render(request, 'magasin/tablesmanagement.html', {'produits': produits})

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

def deleteProduct(request, id):
    product_delete = get_object_or_404(Produit, CodeP=id)
    if request.method=='POST': 
        product_delete.delete()
        return redirect('tablesManagement')
    else:
        return render(request,"magasin/deleteProduct.html",{'produit': product_delete} )
    
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

def searchProduct(request):
    if request.method == "GET":
        query=request.GET['search']
        if query:
            produits=Produit.objects.filter(Designation__contains=query)
            return render(request,'magasin/searchProduct.html', {'produits': produits })
    return render(request,'magasin/searchProduct.html')


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
