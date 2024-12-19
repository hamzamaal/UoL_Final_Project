from django.shortcuts import render
from django.http import HttpResponseRedirect
# from .models import Donor  # Ensure this matches your model file
from src.models.donations import Donor

def register_donor(request):
    if request.method == "POST":
        # Collect form data
        full_name = request.POST.get('fullName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        street_number = request.POST.get('street_number')
        street_name = request.POST.get('street_name')
        town = request.POST.get('town')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        province = request.POST.get('province')
        organization_name = request.POST.get('organization')

        # Save to database
        Donor.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            street_number=street_number,
            street_name=street_name,
            town=town,
            city=city,
            postal_code=postal_code,
            province=province,
            organization_name=organization_name,
        )

        return HttpResponseRedirect('/')  # Redirect to a success page

    return render(request, 'donor_register.html')  # Render the registration form
