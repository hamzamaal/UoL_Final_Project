from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def training(request):
    return render(request, 'training.html')

def donors(request):
    return render(request, 'donors.html')

def begin_donate(request):
    return render(request, 'begin-donate.html')

def recipients(request):
    return render(request, 'recipients.html')

def recipient_register(request):
    return render(request, 'recipient-register.html')

def recipient_register_submit(request):
    if request.method == 'POST':
        # Process the form data
        # Save data to the database or perform actions
        # Redirect to a success page or handle errors
        return redirect('home')  # Redirect to a relevant page after submission
    else:
        # If the form is accessed incorrectly, redirect back
        return redirect('recipient-register')

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
