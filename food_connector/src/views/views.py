from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def training(request):
    return render(request, 'training.html')

def donors(request):
    return render(request, 'donors.html')

def recipients(request):
    return render(request, 'recipients.html')

def get_started(request):
    return render(request, 'get-started.html')

def liabilities(request):
    return render(request, 'liabilities.html')

def tax_benefits(request):
    return render(request, 'tax-benefits.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')
