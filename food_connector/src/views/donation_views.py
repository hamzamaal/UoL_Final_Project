from django.shortcuts import render
from django.http import HttpResponse

def DonationView(request):
    return render(request, 'donations.html')




# # A basic DonationView for demonstration
# def DonationView(request):
#     return HttpResponse("This is the Donation View.")
