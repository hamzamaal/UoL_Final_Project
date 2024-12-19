from django.shortcuts import render, redirect
from django.contrib import messages
from src.models import Donor  # Ensure the correct path to the Donor model
from django.http import HttpResponse
from django.db import IntegrityError

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def training(request):
    return render(request, 'training.html')

def donors(request):
    return render(request, 'donors.html')

# def begin_donate(request):
#     return render(request, 'begin-donate.html')

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

def register_donor(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        street_number = request.POST.get('street_number')
        street_name = request.POST.get('street_name')
        town = request.POST.get('town')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        province = request.POST.get('province')
        country = 'South Africa'
        organization_name = request.POST.get('organization_name')

        # Check for missing fields
        if not all([full_name, email, phone, street_number, street_name, town, city, postal_code, province]):
            return HttpResponse("Missing required fields. Please fill in all fields.", status=400)

        try:
            # Create and save the donor object
            donor = Donor(
                full_name=full_name,
                email=email,
                phone=phone,
                street_number=street_number,
                street_name=street_name,
                town=town,
                city=city,
                postal_code=postal_code,
                province=province,
                country=country,
                organization_name=organization_name,
            )
            donor.save()
            return redirect('donor-success')  # Redirect to the success page

        except IntegrityError as e:
            return HttpResponse(f"Error: {str(e)} - A record with this email already exists.", status=400)
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

    return render(request, 'donor_register.html')

def donor_success(request):
    return render(request, 'donor_success.html', {'message': 'Thank you for registering as a donor!'})
